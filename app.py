#!/usr/bin/env python3
"""
Pet Care Advisor - Knowledge-Based AI Agent
Main application entry point
"""

import os
from app import create_app
from config import config

# Get configuration from environment
config_name = os.environ.get('FLASK_CONFIG', 'development')
app = create_app(config[config_name])

@app.cli.command()
def test():
    """Run unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def init_kb():
    """Initialize knowledge base with sample data."""
    print("Knowledge base initialized with sample data.")
    print(f"Symptoms loaded: {len(app.knowledge_base.symptoms)}")
    print(f"Conditions loaded: {len(app.knowledge_base.conditions)}")
    print(f"Treatments loaded: {len(app.knowledge_base.treatments)}")

@app.shell_context_processor
def make_shell_context():
    """Shell context for Flask shell."""
    return {
        'app': app,
        'kb': app.knowledge_base
    }

if __name__ == '__main__':
    # Development server
    app.run(
        host=os.environ.get('FLASK_HOST', '127.0.0.1'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=app.config['DEBUG']
    )
