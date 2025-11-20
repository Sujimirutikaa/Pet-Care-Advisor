from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Pet:
    """Represents a pet with basic information."""
    name: str
    species: str  # dog, cat, bird, rabbit, etc.
    breed: Optional[str]
    age: float  # in years
    weight: Optional[float]  # in kg
    gender: str
    medical_history: List[str]
    current_medications: List[str]
    allergies: List[str]
    last_vet_visit: Optional[str]
    
    def get_age_category(self) -> str:
        """Categorize pet by age."""
        if self.species.lower() == "dog":
            if self.age < 0.5:
                return "puppy"
            elif self.age < 7:
                return "adult"
            else:
                return "senior"
        elif self.species.lower() == "cat":
            if self.age < 0.5:
                return "kitten"
            elif self.age < 10:
                return "adult"
            else:
                return "senior"
        else:
            return "unknown"
    
    def is_senior(self) -> bool:
        """Check if pet is considered senior."""
        return self.get_age_category() == "senior"

@dataclass
class DiagnosisSession:
    """Represents a diagnosis session."""
    pet: Pet
    reported_symptoms: List[str]
    symptom_details: dict
    timestamp: datetime
    session_id: str
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now()
