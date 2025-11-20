from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
import uuid

from app.models.pet import Pet, DiagnosisSession
from app.utils.inference_engine import InferenceEngine

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Main page with pet information form."""
    return render_template('index.html')

@bp.route('/symptoms')
def symptoms_page():
    """Symptoms selection page."""
    pet_data = request.args.to_dict()
    
    # Get symptoms from knowledge base
    kb = current_app.knowledge_base
    symptoms_by_category = {}
    
    for symptom in kb.symptoms.values():
        category = symptom.category
        if category not in symptoms_by_category:
            symptoms_by_category[category] = []
        symptoms_by_category[category].append(symptom)
    
    return render_template('symptoms.html', 
                         symptoms=symptoms_by_category, 
                         pet_data=pet_data)

@bp.route('/diagnose', methods=['POST'])
def diagnose():
    """Perform diagnosis based on pet information and symptoms."""
    try:
        data = request.get_json()
        
        # Create pet object
        pet = Pet(
            name=data.get('name', 'Unknown'),
            species=data.get('species', 'dog').lower(),
            breed=data.get('breed'),
            age=float(data.get('age', 5)),
            weight=float(data.get('weight', 0)) if data.get('weight') else None,
            gender=data.get('gender', 'unknown'),
            medical_history=data.get('medical_history', []),
            current_medications=data.get('current_medications', []),
            allergies=data.get('allergies', []),
            last_vet_visit=data.get('last_vet_visit')
        )
        
        # Create diagnosis session
        session = DiagnosisSession(
            pet=pet,
            reported_symptoms=data.get('symptoms', []),
            symptom_details=data.get('symptom_details', {}),
            timestamp=datetime.now(),
            session_id=str(uuid.uuid4())
        )
        
        # Perform diagnosis
        kb = current_app.knowledge_base
        inference_engine = InferenceEngine(kb)
        diagnosis_result = inference_engine.diagnose(session)
        
        # Add explanation
        diagnosis_result['explanation'] = inference_engine.explain_reasoning(diagnosis_result)
        
        return jsonify(diagnosis_result)
    
    except Exception as e:
        return jsonify({'error': f'Diagnosis error: {str(e)}'}), 500

@bp.route('/results')
def results():
    """Display diagnosis results."""
    return render_template('results.html')

@bp.route('/api/symptoms')
def api_symptoms():
    """API endpoint to get available symptoms."""
    kb = current_app.knowledge_base
    symptoms_data = []
    
    for symptom in kb.symptoms.values():
        symptoms_data.append({
            'id': symptom.id,
            'name': symptom.name,
            'category': symptom.category,
            'description': symptom.description,
            'severity_levels': symptom.severity_levels
        })
    
    return jsonify({'symptoms': symptoms_data})

@bp.route('/api/conditions')
def api_conditions():
    """API endpoint to get available conditions."""
    kb = current_app.knowledge_base
    conditions_data = []
    
    for condition in kb.conditions.values():
        conditions_data.append({
            'id': condition.id,
            'name': condition.name,
            'category': condition.category,
            'description': condition.description,
            'severity': condition.severity
        })
    
    return jsonify({'conditions': conditions_data})
