from typing import Dict, List, Any, Tuple
from app.models.knowledge_base import KnowledgeBase, Condition, Symptom
from app.models.pet import Pet, DiagnosisSession

class RuleProcessor:
    """Processes rules and applies inference logic."""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
    
    def apply_pet_specific_rules(self, pet: Pet, symptoms: List[str]) -> Dict[str, Any]:
        """Apply species and age-specific rules."""
        rules = self.kb.pet_specific_rules
        
        # Get species-specific symptom modifications
        species_rules = rules.get('species', {}).get(pet.species.lower(), {})
        age_rules = rules.get('age_categories', {}).get(pet.get_age_category(), {})
        
        modified_assessment = {
            'risk_multipliers': {},
            'additional_symptoms': [],
            'exclusions': [],
            'urgency_modifiers': {}
        }
        
        # Apply species-specific risk modifications
        if 'risk_factors' in species_rules:
            for condition_id, multiplier in species_rules['risk_factors'].items():
                modified_assessment['risk_multipliers'][condition_id] = multiplier
        
        # Apply age-specific modifications
        if 'risk_factors' in age_rules:
            for condition_id, multiplier in age_rules['risk_factors'].items():
                if condition_id in modified_assessment['risk_multipliers']:
                    modified_assessment['risk_multipliers'][condition_id] *= multiplier
                else:
                    modified_assessment['risk_multipliers'][condition_id] = multiplier
        
        return modified_assessment
    
    def check_emergency_conditions(self, symptoms: List[str], pet: Pet) -> Tuple[bool, List[str]]:
        """Check for emergency conditions that require immediate attention."""
        emergency_symptoms = {
            'difficulty_breathing': 'critical',
            'severe_bleeding': 'critical',
            'unconscious': 'critical',
            'seizures': 'critical',
            'severe_trauma': 'critical',
            'bloated_abdomen': 'high',
            'persistent_vomiting': 'high',
            'inability_to_urinate': 'high'
        }
        
        emergency_alerts = []
        max_urgency = 'low'
        
        for symptom in symptoms:
            if symptom in emergency_symptoms:
                urgency = emergency_symptoms[symptom]
                emergency_alerts.append(f"URGENT: {symptom.replace('_', ' ').title()} requires immediate veterinary attention")
                
                if urgency == 'critical':
                    max_urgency = 'critical'
                elif urgency == 'high' and max_urgency != 'critical':
                    max_urgency = 'high'
        
        return max_urgency in ['high', 'critical'], emergency_alerts
    
    def apply_exclusion_rules(self, conditions: List[Condition], 
                            symptoms: List[str], pet: Pet) -> List[Condition]:
        """Apply exclusion rules to filter out incompatible conditions."""
        filtered_conditions = []
        
        for condition in conditions:
            # Check mutual exclusions
            exclude = False
            
            # Age-based exclusions
            if pet.age < 1 and 'adult_only' in condition.id:
                exclude = True
            elif pet.age > 10 and 'young_only' in condition.id:
                exclude = True
            
            # Species-based exclusions
            species_exclusions = {
                'feline_only': ['dog', 'bird', 'rabbit'],
                'canine_only': ['cat', 'bird', 'rabbit']
            }
            
            for exclusion_type, excluded_species in species_exclusions.items():
                if exclusion_type in condition.id and pet.species.lower() in excluded_species:
                    exclude = True
                    break
            
            if not exclude:
                filtered_conditions.append(condition)
        
        return filtered_conditions
