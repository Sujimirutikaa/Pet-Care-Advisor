from typing import Dict, List, Tuple, Any
import json
from datetime import datetime

from app.models.knowledge_base import KnowledgeBase, Condition
from app.models.pet import Pet, DiagnosisSession
from app.utils.rule_processor import RuleProcessor

class InferenceEngine:
    """Main inference engine for pet diagnosis."""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.rule_processor = RuleProcessor(knowledge_base)
    
    def diagnose(self, session: DiagnosisSession) -> Dict[str, Any]:
        """Perform complete diagnosis based on symptoms and pet information."""
        
        # Step 1: Check for emergency conditions first
        is_emergency, emergency_alerts = self.rule_processor.check_emergency_conditions(
            session.reported_symptoms, session.pet
        )
        
        if is_emergency:
            return {
                'emergency': True,
                'alerts': emergency_alerts,
                'recommendation': 'SEEK IMMEDIATE VETERINARY ATTENTION',
                'confidence': 1.0,
                'conditions': []
            }
        
        # Step 2: Get potential conditions
        potential_conditions = self.kb.get_conditions_for_symptoms(session.reported_symptoms)
        
        # Step 3: Apply pet-specific rules
        pet_modifications = self.rule_processor.apply_pet_specific_rules(
            session.pet, session.reported_symptoms
        )
        
        # Step 4: Apply exclusion rules
        filtered_conditions = self.rule_processor.apply_exclusion_rules(
            potential_conditions, session.reported_symptoms, session.pet
        )
        
        # Step 5: Calculate confidence scores
        condition_scores = []
        for condition in filtered_conditions:
            base_confidence = self.kb.calculate_confidence(condition, session.reported_symptoms)
            
            # Apply pet-specific multipliers
            multiplier = pet_modifications['risk_multipliers'].get(condition.id, 1.0)
            adjusted_confidence = min(base_confidence * multiplier, 1.0)
            
            condition_scores.append({
                'condition': condition,
                'confidence': adjusted_confidence,
                'base_confidence': base_confidence,
                'risk_multiplier': multiplier
            })
        
        # Step 6: Sort by confidence and filter by threshold
        condition_scores.sort(key=lambda x: x['confidence'], reverse=True)
        probable_conditions = [
            score for score in condition_scores 
            if score['confidence'] >= score['condition'].confidence_threshold
        ]
        
        # Step 7: Generate recommendations
        recommendations = self._generate_recommendations(probable_conditions, session.pet)
        
        return {
            'emergency': False,
            'conditions': probable_conditions[:3],  # Top 3 most likely
            'recommendations': recommendations,
            'pet_specific_notes': self._generate_pet_specific_notes(session.pet, session.reported_symptoms),
            'follow_up_questions': self._generate_follow_up_questions(probable_conditions),
            'session_id': session.session_id,
            'timestamp': session.timestamp.isoformat()
        }
    
    def _generate_recommendations(self, conditions: List[Dict], pet: Pet) -> Dict[str, Any]:
        """Generate treatment recommendations based on diagnosis."""
        if not conditions:
            return {
                'primary_action': 'Monitor symptoms and consult veterinarian if they persist',
                'home_care': ['Ensure pet is comfortable', 'Monitor for changes'],
                'vet_consultation': 'Recommended if symptoms worsen or persist beyond 24-48 hours'
            }
        
        top_condition = conditions[0]
        condition_id = top_condition['condition'].id
        
        # Get treatment recommendations
        treatments = [t for t in self.kb.treatments.values() 
                     if t.condition_id == condition_id]
        
        recommendations = {
            'primary_diagnosis': top_condition['condition'].name,
            'confidence': top_condition['confidence'],
            'severity': top_condition['condition'].severity
        }
        
        if treatments:
            treatment = treatments[0]  # Get primary treatment
            recommendations.update({
                'treatment_type': treatment.treatment_type,
                'description': treatment.description,
                'instructions': treatment.instructions,
                'duration': treatment.duration,
                'precautions': treatment.precautions,
                'seek_help_if': treatment.when_to_seek_help
            })
        
        return recommendations
    
    def _generate_pet_specific_notes(self, pet: Pet, symptoms: List[str]) -> List[str]:
        """Generate notes specific to the pet's characteristics."""
        notes = []
        
        if pet.is_senior():
            notes.append("Senior pets may require more frequent monitoring and veterinary care.")
        
        if pet.age < 1:
            notes.append("Young pets can deteriorate quickly - monitor closely for changes.")
        
        if pet.medical_history:
            notes.append("Consider pet's medical history when evaluating symptoms.")
        
        if pet.current_medications:
            notes.append("Current medications may affect symptoms or treatment options.")
        
        return notes
    
    def _generate_follow_up_questions(self, conditions: List[Dict]) -> List[str]:
        """Generate follow-up questions to improve diagnosis accuracy."""
        questions = []
        
        if not conditions:
            questions.extend([
                "How long have the symptoms been present?",
                "Have you noticed any changes in eating or drinking habits?",
                "Has your pet been exposed to any new environments or animals?"
            ])
        else:
            # Generate condition-specific questions
            top_condition = conditions[0]['condition']
            
            questions.extend([
                f"Have you noticed any other symptoms related to {top_condition.category}?",
                "When did you first notice these symptoms?",
                "Have the symptoms been getting better, worse, or staying the same?"
            ])
        
        return questions
    
    def explain_reasoning(self, diagnosis_result: Dict[str, Any]) -> str:
        """Provide explanation of the diagnostic reasoning."""
        if diagnosis_result.get('emergency'):
            return "Emergency condition detected based on critical symptoms requiring immediate attention."
        
        conditions = diagnosis_result.get('conditions', [])
        if not conditions:
            return "No specific conditions identified. Symptoms may be minor or require additional information."
        
        explanations = []
        for condition_data in conditions[:2]:  # Explain top 2 conditions
            condition = condition_data['condition']
            confidence = condition_data['confidence']
            
            explanation = f"**{condition.name}** (Confidence: {confidence:.1%}): "
            explanation += f"Matches {len([s for s in condition.required_symptoms])} required symptoms"
            
            if condition_data.get('risk_multiplier', 1.0) != 1.0:
                explanation += f" with {condition_data['risk_multiplier']:.1f}x risk adjustment for your pet"
            
            explanations.append(explanation)
        
        return " | ".join(explanations)
