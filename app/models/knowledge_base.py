import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class Symptom:
    """Represents a pet symptom with severity levels."""
    id: str
    name: str
    category: str
    severity_levels: List[str]
    description: str
    common_pets: List[str]  # dogs, cats, birds, etc.

@dataclass
class Condition:
    """Represents a health condition or disease."""
    id: str
    name: str
    category: str
    severity: str
    required_symptoms: List[str]
    optional_symptoms: List[str]
    exclusion_symptoms: List[str]
    confidence_threshold: float
    description: str
    emergency_level: str  # low, medium, high, critical

@dataclass
class Treatment:
    """Represents treatment recommendations."""
    id: str
    condition_id: str
    treatment_type: str  # home_care, vet_visit, emergency
    description: str
    instructions: List[str]
    duration: str
    precautions: List[str]
    when_to_seek_help: List[str]

class KnowledgeBase:
    """Central knowledge repository for pet care information."""
    
    def __init__(self, data_dir: str = "app/data"):
        self.data_dir = data_dir
        self.symptoms: Dict[str, Symptom] = {}
        self.conditions: Dict[str, Condition] = {}
        self.treatments: Dict[str, Treatment] = {}
        self.pet_specific_rules: Dict[str, Dict] = {}
        self.load_knowledge()
    
    def load_knowledge(self):
        """Load all knowledge from JSON files."""
        try:
            self._load_symptoms()
            self._load_conditions()
            self._load_treatments()
            self._load_pet_rules()
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
    
    def _load_symptoms(self):
        """Load symptoms from JSON file."""
        symptoms_path = os.path.join(self.data_dir, "symptoms.json")
        if os.path.exists(symptoms_path):
            with open(symptoms_path, 'r') as f:
                data = json.load(f)
                for symptom_data in data['symptoms']:
                    symptom = Symptom(**symptom_data)
                    self.symptoms[symptom.id] = symptom
    
    def _load_conditions(self):
        """Load conditions from JSON file."""
        conditions_path = os.path.join(self.data_dir, "conditions.json")
        if os.path.exists(conditions_path):
            with open(conditions_path, 'r') as f:
                data = json.load(f)
                for condition_data in data['conditions']:
                    condition = Condition(**condition_data)
                    self.conditions[condition.id] = condition
    
    def _load_treatments(self):
        """Load treatments from JSON file."""
        treatments_path = os.path.join(self.data_dir, "treatments.json")
        if os.path.exists(treatments_path):
            with open(treatments_path, 'r') as f:
                data = json.load(f)
                for treatment_data in data['treatments']:
                    treatment = Treatment(**treatment_data)
                    self.treatments[treatment.id] = treatment
    
    def _load_pet_rules(self):
        """Load pet-specific rules."""
        rules_path = os.path.join(self.data_dir, "rules.json")
        if os.path.exists(rules_path):
            with open(rules_path, 'r') as f:
                self.pet_specific_rules = json.load(f)
    
    def get_symptoms_by_category(self, category: str) -> List[Symptom]:
        """Get all symptoms in a specific category."""
        return [symptom for symptom in self.symptoms.values() 
                if symptom.category == category]
    
    def get_conditions_for_symptoms(self, symptom_ids: List[str]) -> List[Condition]:
        """Get potential conditions based on symptoms."""
        matching_conditions = []
        
        for condition in self.conditions.values():
            # Check if required symptoms are present
            required_match = all(req_symptom in symptom_ids 
                               for req_symptom in condition.required_symptoms)
            
            # Check if exclusion symptoms are NOT present
            exclusion_conflict = any(excl_symptom in symptom_ids 
                                   for excl_symptom in condition.exclusion_symptoms)
            
            if required_match and not exclusion_conflict:
                matching_conditions.append(condition)
        
        return matching_conditions
    
    def calculate_confidence(self, condition: Condition, 
                           present_symptoms: List[str]) -> float:
        """Calculate confidence score for a condition."""
        total_possible = len(condition.required_symptoms) + len(condition.optional_symptoms)
        if total_possible == 0:
            return 0.0
        
        # Required symptoms weight more heavily
        required_score = sum(2 for symptom in condition.required_symptoms 
                           if symptom in present_symptoms)
        optional_score = sum(1 for symptom in condition.optional_symptoms 
                           if symptom in present_symptoms)
        
        max_possible_score = len(condition.required_symptoms) * 2 + len(condition.optional_symptoms)
        confidence = (required_score + optional_score) / max_possible_score
        
        return min(confidence, 1.0)
