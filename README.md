# **Pet Care Advisor AI**

## **Project Overview**

Pet Care Advisor is a knowledge-based AI web application built with Python and Flask. It helps pet owners diagnose common pet health issues, offers care recommendations, and advises when professional veterinary help is needed. The system uses a structured knowledge base and inference rules to deliver accurate, explainable expert guidance.

---

## **Features**

* Diagnoses common pet health problems from user symptoms
* Provides care and treatment recommendations
* Suggests when veterinary consultation is necessary
* Simple and user-friendly web interface
* Knowledge-based AI reasoning for accurate advice

---

## **Technology Stack**

* Python
* Flask
* Knowledge-based AI agent architecture
* HTML, CSS, JavaScript

---

## **Installation**

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory**

   ```bash
   cd pet-care-advisor
   ```

3. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   ```

   **Windows:**

   ```bash
   venv\Scripts\activate
   ```

   **Mac/Linux:**

   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask app**

   ```bash
   flask run
   ```

6. Open browser → **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## **Usage**

* Enter pet symptoms or health-related questions
* System interprets input using the knowledge base
* Provides diagnosis-like suggestions and care tips instantly

---

## **Testing Suggestions**

Try inputs like:

* "My dog has seizures and won't wake up"
* "Cat is vomiting and not eating"
* "When should I take my pet to the vet?"

---

## **Project Structure**

```
pet-care-advisor/
├── app.py                 # Main Flask application
├── knowledge_base.json    # Knowledge base for inference
├── templates/             # HTML templates
├── static/                # CSS and JS files
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

---

