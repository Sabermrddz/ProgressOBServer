"""
Storage module for managing grades in JSON format
إدارة التخزين حفظ الدرجات في JSON
"""
import json
import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime


logger = logging.getLogger(__name__)


class GradeStorage:
    """Manages grade storage in JSON format"""
    
    def __init__(self, filepath: str = "grades.json"):
        """
        Initialize grade storage
        
        Args:
            filepath: Path to the grades.json file
        """
        self.filepath = filepath
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create the JSON file if it doesn't exist"""
        if not os.path.exists(self.filepath):
            self._save_data({
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "exam_grades": {},
                "continuous_grades": {},
                "metadata": {
                    "total_new_grades": 0,
                    "last_sync": None,
                    "initialized": False
                }
            })
            logger.info(f"Created new storage file: {self.filepath}")
    
    def _load_data(self) -> Dict:
        """Load data from JSON file"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Corrupted JSON file {self.filepath}, creating new one")
            self._ensure_file_exists()
            return self._load_data()
        except Exception as e:
            logger.error(f"Error loading grades: {e}")
            return {
                "version": "1.0",
                "exam_grades": {},
                "continuous_grades": {},
                "metadata": {"total_new_grades": 0}
            }
    
    def _save_data(self, data: Dict) -> None:
        """Save data to JSON file"""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving grades: {e}")
    
    def get_all_grades(self) -> Tuple[Dict, Dict]:
        """
        Get all stored grades
        
        Returns:
            Tuple of (exam_grades, continuous_grades)
        """
        data = self._load_data()
        return data.get("exam_grades", {}), data.get("continuous_grades", {})
    
    def get_exam_grades(self) -> Dict:
        """Get all exam grades"""
        data = self._load_data()
        return data.get("exam_grades", {})
    
    def get_continuous_grades(self) -> Dict:
        """Get all continuous assessment grades"""
        data = self._load_data()
        return data.get("continuous_grades", {})
    
    def save_exam_grades(self, grades: List[Dict]) -> Tuple[List[Dict], int]:
        """
        Save exam grades and detect changes
        
        Args:
            grades: List of exam grade dictionaries
            
        Returns:
            Tuple of (new_grades, count_of_new)
        """
        new_grades = []
        data = self._load_data()
        old_grades = data.get("exam_grades", {})
        
        for grade in grades:
            grade_id = str(grade.get("id", ""))
            if not grade_id:
                continue
            
            grade_entry = {
                "id": grade_id,
                "mcLibelleAr": grade.get("mcLibelleAr", ""),
                "mcLibelleFr": grade.get("mcLibelleFr", ""),
                "noteExamen": grade.get("noteExamen"),
                "planningSessionIntitule": grade.get("planningSessionIntitule", ""),
                "rattachementMcCoefficient": grade.get("rattachementMcCoefficient", 1),
                "absent": grade.get("absent", False),
                "timestamp": datetime.now().isoformat()
            }
            
            # Check if this is a new grade or updated
            if grade_id not in old_grades:
                new_grades.append(grade_entry)
                logger.info(f"New exam grade detected: {grade_id}")
            else:
                # Check if grade value changed
                old_value = old_grades[grade_id].get("noteExamen")
                new_value = grade_entry.get("noteExamen")
                if old_value != new_value:
                    new_grades.append(grade_entry)
                    logger.info(f"Exam grade updated: {grade_id} ({old_value} → {new_value})")
            
            old_grades[grade_id] = grade_entry
        
        data["exam_grades"] = old_grades
        data["last_updated"] = datetime.now().isoformat()
        data["metadata"]["last_sync"] = datetime.now().isoformat()
        self._save_data(data)
        
        return new_grades, len(new_grades)
    
    def save_continuous_grades(self, grades: List[Dict]) -> Tuple[List[Dict], int]:
        """
        Save continuous assessment grades and detect changes
        
        Args:
            grades: List of continuous grade dictionaries
            
        Returns:
            Tuple of (new_grades, count_of_new)
        """
        new_grades = []
        data = self._load_data()
        old_grades = data.get("continuous_grades", {})
        
        for grade in grades:
            grade_id = str(grade.get("id", ""))
            if not grade_id:
                continue
            
            grade_entry = {
                "id": grade_id,
                "mcLibelleAr": grade.get("mcLibelleAr", ""),
                "mcLibelleFr": grade.get("mcLibelleFr", ""),
                "noteExamen": grade.get("noteExamen"),
                "planningSessionIntitule": grade.get("planningSessionIntitule", ""),
                "rattachementMcCoefficient": grade.get("rattachementMcCoefficient", 1),
                "absent": grade.get("absent", False),
                "timestamp": datetime.now().isoformat()
            }
            
            # Check if this is a new grade or updated
            if grade_id not in old_grades:
                new_grades.append(grade_entry)
                logger.info(f"New continuous grade detected: {grade_id}")
            else:
                # Check if grade value changed
                old_value = old_grades[grade_id].get("noteExamen")
                new_value = grade_entry.get("noteExamen")
                if old_value != new_value:
                    new_grades.append(grade_entry)
                    logger.info(f"Continuous grade updated: {grade_id} ({old_value} → {new_value})")
            
            old_grades[grade_id] = grade_entry
        
        data["continuous_grades"] = old_grades
        data["last_updated"] = datetime.now().isoformat()
        data["metadata"]["last_sync"] = datetime.now().isoformat()
        self._save_data(data)
        
        return new_grades, len(new_grades)
    
    def clear_storage(self) -> None:
        """Clear all stored grades"""
        self._ensure_file_exists()
        logger.warning("Storage cleared")
    
    def get_stats(self) -> Dict:
        """Get storage statistics"""
        data = self._load_data()
        return {
            "total_exam_grades": len(data.get("exam_grades", {})),
            "total_continuous_grades": len(data.get("continuous_grades", {})),
            "last_updated": data.get("last_updated"),
            "last_sync": data.get("metadata", {}).get("last_sync"),
            "initialized": data.get("metadata", {}).get("initialized", False)
        }

    def is_initialized(self) -> bool:
        """Check if storage has been initialized with baseline grades"""
        data = self._load_data()
        return data.get("metadata", {}).get("initialized", False)

    def mark_initialized(self) -> None:
        """Mark storage as initialized after baseline sync"""
        data = self._load_data()
        data.setdefault("metadata", {})["initialized"] = True
        data["metadata"]["last_sync"] = datetime.now().isoformat()
        self._save_data(data)


class TokenStorage:
    """Manages JWT token storage"""
    
    def __init__(self, filepath: str = "token.json"):
        """
        Initialize token storage
        
        Args:
            filepath: Path to the token.json file
        """
        self.filepath = filepath
    
    def save_token(self, token: str, expires_in: int) -> None:
        """
        Save JWT token with expiration time
        
        Args:
            token: JWT token string
            expires_in: Expiration time in seconds
        """
        try:
            data = {
                "token": token,
                "expires_in": expires_in,
                "created_at": datetime.now().isoformat()
            }
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.debug("Token saved successfully")
        except Exception as e:
            logger.error(f"Error saving token: {e}")
    
    def load_token(self) -> Optional[str]:
        """
        Load stored JWT token if still valid
        
        Returns:
            Token string or None if expired/not found
        """
        try:
            if not os.path.exists(self.filepath):
                return None
            
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data.get("token")
        except Exception as e:
            logger.debug(f"Error loading token: {e}")
            return None
    
    def clear_token(self) -> None:
        """Clear stored token"""
        try:
            if os.path.exists(self.filepath):
                os.remove(self.filepath)
            logger.debug("Token cleared")
        except Exception as e:
            logger.error(f"Error clearing token: {e}")
