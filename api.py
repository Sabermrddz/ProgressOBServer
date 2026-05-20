"""
WebEtu API client module
واجهة برمجة التطبيقات للاتصال بنظام ويب إيتو
"""
import requests
import logging
from typing import Dict, List, Optional, Tuple
from config import Config
from storage import TokenStorage
import gzip
import io


logger = logging.getLogger(__name__)


class WebEtuAPI:
    """WebEtu API client with authentication and error handling"""
    
    def __init__(self):
        """Initialize API client"""
        self.base_url = Config.WEBETU_BASE_URL
        self.username = Config.WEBETU_USERNAME
        self.password = Config.WEBETU_PASSWORD
        self.dia_id = Config.DIA_ID
        self.ind_id = Config.IND_ID
        self.token_storage = TokenStorage(Config.TOKEN_FILE)
        self.current_token: Optional[str] = None
        
        # Create session with persistent cookies
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": Config.USER_AGENT,
        })
        
        self.consecutive_failures = 0
    
    def _get_headers(self, token: Optional[str] = None) -> Dict:
        """
        Build request headers
        
        Args:
            token: JWT token (if None, uses current token)
            
        Returns:
            Dictionary of headers
        """
        if token is None:
            token = self.current_token
        
        headers = {
            "User-Agent": Config.USER_AGENT,
            "accept": Config.ACCEPT,
            "Accept-Encoding": Config.ACCEPT_ENCODING,
            "x-dia-id": self.dia_id,
            "x-ind-id": self.ind_id,
        }
        
        if token:
            # WebEtu mobile app sends raw JWT without "Bearer" prefix
            headers["authorization"] = token
        
        return headers
    
    def _handle_gzip_response(self, response: requests.Response) -> Dict:
        """
        Handle gzip-encoded responses from API
        
        Args:
            response: Response object
            
        Returns:
            Parsed JSON data
        """
        try:
            if response.headers.get('Content-Encoding') == 'gzip':
                # Manually decompress gzip content
                content = gzip.GzipFile(fileobj=io.BytesIO(response.content)).read()
                return content.decode('utf-8')
            else:
                return response.text
        except Exception as e:
            logger.error(f"Error decompressing gzip response: {e}")
            return response.text
    
    def authenticate(self) -> bool:
        """
        Authenticate with WebEtu API and obtain JWT token
        تسجيل الدخول إلى نظام ويب إيتو والحصول على رمز JWT
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            url = f"{self.base_url}/api/authentication/v1/"
            payload = {
                "username": self.username,
                "password": self.password
            }
            headers = {
                "User-Agent": Config.USER_AGENT,
                "accept": Config.ACCEPT,
                "Accept-Encoding": Config.ACCEPT_ENCODING,
                "Content-Type": Config.CONTENT_TYPE
            }
            
            logger.info("Attempting to authenticate with WebEtu API...")
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=Config.REQUEST_TIMEOUT_SECONDS
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"API Response: {data}")
                # API returns 'token', not 'access_token'
                self.current_token = data.get("token") or data.get("access_token")
                
                if self.current_token:
                    expires_in = data.get("expires_in", 3600)
                    self.token_storage.save_token(self.current_token, expires_in)
                    logger.info("✅ Authentication successful")
                    self.consecutive_failures = 0
                    return True
                else:
                    logger.error("❌ No token in response")
                    logger.error(f"Full response: {data}")
                    return False
            else:
                logger.error(f"❌ Authentication failed: {response.status_code}")
                logger.error(f"Response: {response.text[:500]}")
                return False
                
        except requests.exceptions.Timeout:
            logger.error("❌ Authentication timeout")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("❌ Connection error during authentication")
            return False
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Tuple[bool, Optional[Dict]]:
        """
        Make HTTP request with error handling and retries
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Tuple of (success, response_data)
        """
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(1, Config.MAX_RETRIES + 1):
            try:
                headers = self._get_headers()
                logger.debug(f"Request attempt {attempt}: {method.upper()} {endpoint}")
                logger.debug(f"Full URL: {url}")
                logger.debug(f"Token starts with: {self.current_token[:50] if self.current_token else 'NONE'}...")
                logger.debug(f"DIA_ID: {self.dia_id}, IND_ID: {self.ind_id}")
                
                if method.upper() == "GET":
                    response = self.session.get(
                        url,
                        headers=headers,
                        timeout=Config.REQUEST_TIMEOUT_SECONDS,
                        verify=True,
                        **kwargs
                    )
                else:
                    response = self.session.request(
                        method,
                        url,
                        headers=headers,
                        timeout=Config.REQUEST_TIMEOUT_SECONDS,
                        verify=True,
                        **kwargs
                    )
                
                # Handle 401 Unauthorized - token expired
                if response.status_code == 401:
                    logger.warning("💤 Token expired, re-authenticating...")
                    logger.debug(f"401 Response: {response.text[:500]}")
                    self.token_storage.clear_token()
                    self.current_token = None
                    if self.authenticate():
                        # Retry the request with new token
                        headers = self._get_headers()
                        logger.debug(f"Retry headers: {headers}")
                        if method.upper() == "GET":
                            response = self.session.get(
                                url,
                                headers=headers,
                                timeout=Config.REQUEST_TIMEOUT_SECONDS,
                                **kwargs
                            )
                        else:
                            response = self.session.request(
                                method,
                                url,
                                headers=headers,
                                timeout=Config.REQUEST_TIMEOUT_SECONDS,
                                **kwargs
                            )
                        logger.debug(f"Retry response status: {response.status_code}")
                    else:
                        return False, None
                
                if response.status_code == 200:
                    data = response.json()
                    self.consecutive_failures = 0
                    return True, data
                else:
                    logger.warning(f"⚠️ Request failed: {response.status_code}")
                    logger.debug(f"Response body: {response.text[:500]}")
                    if attempt < Config.MAX_RETRIES:
                        import time
                        time.sleep(Config.RETRY_DELAY_SECONDS)
                        continue
                    else:
                        logger.error(f"❌ Request failed after {Config.MAX_RETRIES} attempts")
                        self.consecutive_failures += 1
                        return False, None
                        
            except requests.exceptions.Timeout:
                logger.warning(f"⏱️ Request timeout (attempt {attempt}/{Config.MAX_RETRIES})")
                if attempt < Config.MAX_RETRIES:
                    import time
                    time.sleep(Config.RETRY_DELAY_SECONDS)
                    continue
                else:
                    self.consecutive_failures += 1
                    return False, None
                    
            except requests.exceptions.ConnectionError:
                logger.warning(f"🔗 Connection error (attempt {attempt}/{Config.MAX_RETRIES})")
                if attempt < Config.MAX_RETRIES:
                    import time
                    time.sleep(Config.RETRY_DELAY_SECONDS)
                    continue
                else:
                    self.consecutive_failures += 1
                    return False, None
                    
            except Exception as e:
                logger.error(f"❌ Request error: {e}")
                self.consecutive_failures += 1
                return False, None
        
        return False, None
    
    def get_exam_grades(self) -> Tuple[bool, List[Dict]]:
        """
        Fetch exam grades from API
        احصل على درجات الامتحانات من الواجهة
        
        Returns:
            Tuple of (success, grades_list)
        """
        endpoint = f"/api/infos/planningSession/dia/{self.dia_id}/noteExamens"
        success, data = self._make_request("GET", endpoint)
        
        if success and data:
            grades = data.get("body", []) if isinstance(data, dict) else data
            if isinstance(grades, list):
                logger.info(f"✅ Fetched {len(grades)} exam grades")
                return True, grades
        
        logger.warning("❌ Failed to fetch exam grades")
        return False, []
    
    def get_continuous_grades(self) -> Tuple[bool, List[Dict]]:
        """
        Fetch continuous assessment grades from API
        احصل على درجات التقييم المستمر من الواجهة
        
        Returns:
            Tuple of (success, grades_list)
        """
        endpoint = f"/api/infos/controleContinue/dia/{self.dia_id}/notesCC"
        success, data = self._make_request("GET", endpoint)
        
        if success and data:
            grades = data.get("body", []) if isinstance(data, dict) else data
            if isinstance(grades, list):
                logger.info(f"✅ Fetched {len(grades)} continuous grades")
                return True, grades
        
        logger.warning("❌ Failed to fetch continuous grades")
        return False, []
    
    def test_token_with_info(self) -> Tuple[bool, Optional[Dict]]:
        """
        Test if token works by fetching student info with and without custom headers
        
        Returns:
            Tuple of (success, info_data)
        """
        if not self.ensure_authenticated():
            return False, None
        
        logger.info("🧪 Testing token with student info endpoint...")
        
        # Test 1: Try without custom headers
        logger.debug("Test 1: Trying without x-dia-id and x-ind-id headers...")
        headers_no_custom = {
            "User-Agent": Config.USER_AGENT,
            "accept": Config.ACCEPT,
            "Accept-Encoding": Config.ACCEPT_ENCODING,
            "authorization": f"Bearer {self.current_token}"
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/infos/etudiant",
                headers=headers_no_custom,
                timeout=Config.REQUEST_TIMEOUT_SECONDS
            )
            logger.debug(f"Response status (no custom headers): {response.status_code}")
            if response.status_code == 200:
                logger.info("✅ Token works WITHOUT custom headers!")
                return True, response.json()
        except Exception as e:
            logger.debug(f"Error: {e}")
        
        # Test 2: Try with Authorization only
        logger.debug("Test 2: Trying with ONLY Authorization header...")
        headers_auth_only = {
            "authorization": f"Bearer {self.current_token}"
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/infos/etudiant",
                headers=headers_auth_only,
                timeout=Config.REQUEST_TIMEOUT_SECONDS
            )
            logger.debug(f"Response status (auth only): {response.status_code}")
            if response.status_code == 200:
                logger.info("✅ Token works with AUTH ONLY!")
                return True, response.json()
        except Exception as e:
            logger.debug(f"Error: {e}")
        
        logger.warning("⚠️ Token test failed - API may require specific access or account setup")
        return False, None
    
    def ensure_authenticated(self) -> bool:
        """
        Ensure we have a valid token, try to use stored one or re-authenticate
        
        Returns:
            True if authenticated, False otherwise
        """
        if self.current_token:
            return True
        
        # Try to load stored token
        stored_token = self.token_storage.load_token()
        if stored_token:
            self.current_token = stored_token
            logger.info("Used stored token")
            return True
        
        # Re-authenticate
        if self.authenticate():
            return True
        
        return False
