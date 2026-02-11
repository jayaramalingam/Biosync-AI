from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import PIL.Image
import json
import os
from datetime import datetime

#/dash ->dashboard patient
#se -> side effects
#dd -> drug discovery

app = Flask(__name__)

# Sample patient data stored in JSON format
SAMPLE_PATIENTS = [
    {
        "id": 1,
        "name": "John Smith",
        "age": 65,
        "gender": "Male",
        "condition": "Hypertension & Type 2 Diabetes",
        "medications": ["Metformin", "Lisinopril", "Atorvastatin", "Aspirin"],
        "last_updated": "2024-02-15"
    },
    {
        "id": 2,
        "name": "Maria Garcia",
        "age": 72,
        "gender": "Female",
        "condition": "Arthritis & Osteoporosis",
        "medications": ["Ibuprofen", "Calcium Carbonate", "Vitamin D", "Alendronate"],
        "last_updated": "2024-02-10"
    },
    {
        "id": 3,
        "name": "Robert Johnson",
        "age": 58,
        "gender": "Male",
        "condition": "Asthma & High Cholesterol",
        "medications": ["Albuterol", "Fluticasone", "Simvastatin", "Montelukast"],
        "last_updated": "2024-02-12"
    },
    {
        "id": 4,
        "name": "Sarah Williams",
        "age": 45,
        "gender": "Female",
        "condition": "Migraine & Anxiety",
        "medications": ["Sumatriptan", "Propranolol", "Sertraline", "Clonazepam"],
        "last_updated": "2024-02-08"
    },
    {
        "id": 5,
        "name": "David Chen",
        "age": 81,
        "gender": "Male",
        "condition": "Heart Disease & COPD",
        "medications": ["Warfarin", "Furosemide", "Spiriva", "Metoprolol"],
        "last_updated": "2024-02-14"
    }
]

# File-based patient data storage
PATIENT_DATA_FILE = "patients.json"

def init_patient_data():
    """Initialize patient data file with sample data if it doesn't exist"""
    if not os.path.exists(PATIENT_DATA_FILE):
        with open(PATIENT_DATA_FILE, 'w') as f:
            json.dump(SAMPLE_PATIENTS, f, indent=4)
        return SAMPLE_PATIENTS
    else:
        try:
            with open(PATIENT_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return SAMPLE_PATIENTS

# Initialize patient data
patients_data = init_patient_data()

# Gemini API Configuration
genai.configure(api_key="AIzaSyAW4P-8xzwwPNiEd9KGjju3BN2GRxO07Ac")
# Using Gemini Flash model
gemini_model = genai.GenerativeModel("gemini-3-flash-preview")



@app.route('/')
def home():
    return render_template('base.html')

@app.route('/se')
def side_effects_page():
    return render_template('sideeffects.html')

@app.route('/dd')
def drugdisc():
    return render_template('drugdisc.html')

@app.route('/get_drug_info', methods=['POST'])
def get_drug_info():
    try:
        data = request.get_json()
        medicine_name = data.get("medicine_name", "")

        if not medicine_name:
            return jsonify({"error": "Medicine name is required!"})

        query = f"""Explain the medicine {medicine_name}.
        Return response in clean HTML using <p>, <ul>, <li>, <h3>.
        Do NOT use markdown symbols like ** or ###.
        """

        response = gemini_model.generate_content(query)

        side_prompt = f"List common side effects of {medicine_name} in clean HTML format."
        side_response = gemini_model.generate_content(side_prompt)

        return jsonify({
            "medicine_name": medicine_name,
            "description": response.text,
            "side_effects": side_response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/extract_medicine_names', methods=['POST'])
def extract_medicine_names():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded!"})

        image = request.files['image']
        image_path = "uploaded_image.jpg"
        image.save(image_path)

        image_pil = PIL.Image.open(image_path)

        # Step 1: Extract medicine names
        prompt = "Extract only medicine names as comma-separated list."
        response = gemini_model.generate_content([prompt, image_pil])
        medicine_names = response.text.strip()

        if not medicine_names:
            return jsonify({"error": "No medicines detected!"})

        # Step 2: Generate explanation
        explain_prompt = f"""
        For each of these medicines: {medicine_names},
        provide:
        - What it is used for
        - Why it is prescribed
        - Common side effects
        Return clean HTML using <h3>, <p>, <ul>, <li>.
        Do NOT use markdown symbols.
        """

        explanation = gemini_model.generate_content(explain_prompt)

        return jsonify({
            "medicine_names": medicine_names,
            "side_effects": explanation.text
        })

    except Exception as e:
        return jsonify({"error": str(e)})


def get_medicine_side_effects(medicine_list):
    prompt = f"""
    For each of these medicines: {', '.join(medicine_list)}, provide:
    1. **What is the use of the medicine?**
    2. **Why and where is it used?**
    Format the response in structured HTML <div> with proper <h3>, <p>, and <ul> elements for each medicine.
    """
    response = gemini_model.generate_content(prompt)
    return response.text

@app.route('/dash')
def dash():
    return render_template('dashboard.html')

# JSON-based patient routes
@app.route('/get_patients', methods=['GET'])
def get_patients():
    """Get list of all patient names - This matches your JavaScript call"""
    try:
        patient_names = [patient["name"] for patient in patients_data]
        return jsonify({"patients": patient_names})
    except Exception as e:
        print(f"Error loading patients: {e}")
        return jsonify({"patients": ["John Smith", "Maria Garcia", "Robert Johnson", "Sarah Williams", "David Chen"]})

@app.route('/get_patient_data', methods=['POST'])
def get_patient_data():
    """Get detailed patient data including medications - This matches your JavaScript call"""
    data = request.json
    patient_name = data.get("name")
    
    if not patient_name:
        return jsonify({"error": "Patient name is required!"})
    
    # Find patient by name
    patient = None
    for p in patients_data:
        if p["name"].lower() == patient_name.lower():
            patient = p
            break
    
    if not patient:
        return jsonify({"error": "Patient not found!"})
    
    # Return only medications as your JavaScript expects
    return jsonify({
        "medications": patient.get("medications", [])
    })

@app.route('/analyze_risk', methods=['POST'])
def analyze_risk():
    """Analyze medication risks - This matches your JavaScript call"""
    data = request.json
    medications = data.get("medications", [])

    if not medications:
        return jsonify({"error": "No medications provided!"})

    # Generate Risk Assessment using Gemini
    risk_prompt = f"""Analyze the risk levels of these medications: {', '.join(medications)}. 
    Format the response in structured HTML <div> with proper <h3>, <p>, and <ul> elements for each medicine name with an well presenting format in a html website,give a short and clear description"""
    
    risk_response = gemini_model.generate_content(risk_prompt).text

    # Generate Alternative Medications using Gemini
    alternative_prompt = f"""Suggest safer alternative medicines for: {', '.join(medications)}. 
    Format the response in structured HTML <div> with proper <h3>, <p>, and <ul> elements for each medicine name with an well presenting format in a html website,give a short and clear description"""
    
    alternative_response = gemini_model.generate_content(alternative_prompt).text

    return jsonify({
        "risk_assessment": risk_response,
        "alternatives": alternative_response
    })

# Optional endpoints for future enhancements (not required for current UI)
@app.route('/add_patient', methods=['POST'])
def add_patient():
    """Add a new patient (optional endpoint)"""
    data = request.json
    
    new_patient = {
        "id": len(patients_data) + 1,
        "name": data.get("name"),
        "age": data.get("age", ""),
        "gender": data.get("gender", ""),
        "condition": data.get("condition", ""),
        "medications": data.get("medications", []),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    patients_data.append(new_patient)
    save_patient_data(patients_data)
    
    return jsonify({"success": True, "message": "Patient added successfully"})

@app.route('/update_patient_medications', methods=['POST'])
def update_patient_medications():
    """Update patient medications (optional endpoint)"""
    data = request.json
    patient_name = data.get("name")
    medications = data.get("medications", [])
    
    # Find and update patient
    for patient in patients_data:
        if patient["name"].lower() == patient_name.lower():
            patient["medications"] = medications
            patient["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            save_patient_data(patients_data)
            return jsonify({"success": True, "message": "Medications updated"})
    
    return jsonify({"error": "Patient not found!"})

def save_patient_data(patients):
    """Save patient data to JSON file"""
    with open(PATIENT_DATA_FILE, 'w') as f:
        json.dump(patients, f, indent=4)

if __name__ == '__main__':
    print("=" * 60)
    print("Patient Dashboard Backend Starting...")
    print("=" * 60)
    print(f"✓ Loaded {len(patients_data)} sample patients")
    print("\n📋 Available Patients:")
    print("-" * 40)
    for patient in patients_data:
        meds = ', '.join(patient['medications'])
        print(f"  • {patient['name']} ({patient['age']} years)")
        print(f"    Condition: {patient['condition']}")
        print(f"    Medications: {meds}")
        print()
    print("=" * 60)
    print("🌐 Dashboard available at: http://localhost:5000/dash")
    print("=" * 60)
    app.run(debug=True, port=5000)
