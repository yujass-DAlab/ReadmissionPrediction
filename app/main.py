# ============================================================
# READMISSION RISK API - FINAL VERSION
# Model: Stacking Ensemble (XGB + LGB + RF) with Corrected ICD-9
# Threshold: 0.25 (86% Recall on <30 days)
# ============================================================
import re
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict

#0 Secret Key
API_KEY = "your-api-key"   

# 1. Initialize FastAPI
app = FastAPI(
    title="Readmission Risk Predictor (Final Model)",
    description="Predicts 30-day readmission risk from clinical text. Optimized for 86% recall on <30 days.",
    version="2.0.0"
)

# 2. Load Model and Threshold
# Make sure the .pkl file is in the same directory as this script
MODEL_PATH = "readmission_stack_ensemble_final.pkl"
THRESHOLD = 0.25

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please ensure it is in the correct path.")

# 3. Define Request/Response Schemas
class PatientContext(BaseModel):
    patient_id: str
    clinical_text: str  # The full messy text string

class PredictionResponse(BaseModel):
    patient_id: str
    risk_class: str  # "NO", ">30 days", or "<30 days"
    probabilities: Dict[str, float]  # e.g., {"NO": 0.1, ">30 days": 0.2, "<30 days": 0.7}
    risk_alert: bool  # True if <30 days probability > THRESHOLD

# 4. Feature Extraction Helpers (Regex + Logic)
def extract_number(pattern, text, default=0.0):
    match = re.search(pattern, text)
    if match:
        try:
            return float(match.group(1))
        except (ValueError, IndexError):
            return default
    return default

def extract_category(pattern, text, default="Unknown"):
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return default

def map_icd9_correct(icd):
    """
    Corrected ICD-9-CM Chapter Ranges.
    Fixed: Diabetes (250) now maps to Endocrine, not Neoplasms.
    """
    try:
        code = int(str(icd).split('.')[0])
    except (ValueError, TypeError):
        return 17  # Unknown

    if 1 <= code <= 139: return 0   # Infectious
    elif 140 <= code <= 239: return 1   # Neoplasms
    elif 240 <= code <= 279: return 2   # Endocrine (DIABETES FIXED!)
    elif 280 <= code <= 289: return 3   # Blood
    elif 290 <= code <= 319: return 4   # Mental
    elif 320 <= code <= 389: return 5   # Nervous
    elif 390 <= code <= 459: return 6   # Circulatory
    elif 460 <= code <= 519: return 7   # Respiratory
    elif 520 <= code <= 579: return 8   # Digestive
    elif 580 <= code <= 629: return 9   # Genitourinary
    elif 630 <= code <= 679: return 10  # Pregnancy
    elif 680 <= code <= 709: return 11  # Skin
    elif 710 <= code <= 739: return 12  # Musculoskeletal
    elif 740 <= code <= 759: return 13  # Congenital
    elif 760 <= code <= 779: return 14  # Perinatal
    elif 780 <= code <= 799: return 15  # Symptoms
    elif 800 <= code <= 999: return 16  # Injury
    else: return 17  # Other

def extract_features(text: str) -> np.ndarray:
    """
    Extracts the exact 21 features used in training.
    Order must match the training data exactly.
    """
    # --- 1. Raw Numeric Extractions ---
    age = extract_number(r'Age:\s*\[(\d+)', text, default=0)
    num_meds = extract_number(r'Number of medications administered during the encounter:\s*(\d+)', text)
    num_labs = extract_number(r'Number of lab tests performed during the encounter:\s*(\d+)', text)
    num_diag = extract_number(r'Number of diagnosis:\s*(\d+)', text)
    out_vis = extract_number(r'Number of outpatient visits of the patient in the year preceding the encounter:\s*(\d+)', text)
    em_vis = extract_number(r'Number of emergency visits of the patient in the year preceding the encounter:\s*(\d+)', text)
    in_vis = extract_number(r'Number of inpatient visits of the patient in the year preceding the encounter:\s*(\d+)', text)
    num_proc = extract_number(r'Number of procedures \(other than lab tests\) performed during the encounter:\s*(\d+)', text)
    days = extract_number(r'Number of days between admission and discharge:\s*(\d+)', text)

    # --- 2. Categorical Flags (0 or 1) ---
    insulin = extract_category(r'insulin dosage change:\s*(\w+)', text, default="No")
    insulin_change = 1 if insulin in ["Up", "Down"] else 0
    
    diabetic_med = extract_category(r'Change in diabetic medication dosage:\s*(\w+)', text, default="No")
    diabetic_med_change = 1 if diabetic_med == "Ch" else 0
    
    any_med = extract_category(r'Any diabetic medicine prescribed:\s*(\w+)', text, default="No")
    any_diabetic_med = 1 if any_med == "Yes" else 0

    # --- 3. Raw Categoricals (will map to integers) ---
    admission_type_raw = extract_category(r'admission type:\s*(\w+)', text, default="Unknown")
    gender_raw = extract_category(r'Gender:\s*(\w+)', text, default="Unknown")
    race_raw = extract_category(r'Race:\s*([^.]+)', text, default="Unknown").strip()
    icd9_raw = extract_category(r'primary diagnosis \(coded as first three digits of ICD9\):\s*(\d+)', text, default="999")

    # --- 4. Engineered Features ---
    total_visits = out_vis + em_vis + in_vis
    med_per_day = num_meds / (days + 1)
    high_utilization = 1 if total_visits > 5 else 0
    age_med_interaction = age * num_meds
    emergency_ratio = em_vis / (total_visits + 1)
    icd9_group = map_icd9_correct(icd9_raw)

    # --- 5. Map Categoricals to Integers (Must match training LabelEncoder exactly) ---
    # Alphabetical order used by LabelEncoder during training
    admission_map = {'Elective': 0, 'Emergency': 1, 'Newborn': 2, 'Unknown': 3, 'Urgent': 4}
    gender_map = {'Female': 0, 'Male': 1, 'Unknown': 2}
    race_map = {'AfricanAmerican': 0, 'Asian': 1, 'Caucasian': 2, 'Hispanic': 3, 'Unknown': 4}

    admission_type = admission_map.get(admission_type_raw, 3)  # default to Unknown
    gender = gender_map.get(gender_raw, 2)
    race = race_map.get(race_raw, 4)

    # --- 6. Assemble the Array in EXACT Training Order (21 Features) ---
    features = [
        age,                    # 1
        num_meds,               # 2
        num_labs,               # 3
        num_diag,               # 4
        out_vis,                # 5
        em_vis,                 # 6
        in_vis,                 # 7
        num_proc,               # 8
        days,                   # 9
        insulin_change,         # 10
        diabetic_med_change,    # 11
        any_diabetic_med,       # 12
        admission_type,         # 13
        gender,                 # 14
        race,                   # 15
        total_visits,           # 16
        med_per_day,            # 17
        high_utilization,       # 18
        age_med_interaction,    # 19
        emergency_ratio,        # 20
        icd9_group              # 21
    ]

    return np.array([features], dtype=np.float32)

# 6. Prediction Endpoint
@app.post("/predict")
async def predict(patient: PatientContext, x_api_key: str = Header(...)):
    # --- API Key Validation (INSERT THIS RIGHT AT THE TOP) ---
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    try:
        # Extract the 21 features
        features = extract_features(patient.clinical_text)
        
        # Get probabilities for all 3 classes: [NO, >30 days, <30 days]
        probs = model.predict_proba(features)[0]
        
        # Apply the custom threshold for <30 days (Class 2)
        pred_idx = np.argmax(probs)
        #if probs[2] > THRESHOLD:
            #pred_idx = 2
        
        class_map = {0: "NO", 1: ">30 days", 2: "<30 days"}
        risk_class = class_map[pred_idx]
        
        return PredictionResponse(
            patient_id=patient.patient_id,
            risk_class=risk_class,
            probabilities={
                "NO": round(float(probs[0]), 4),
                ">30 days": round(float(probs[1]), 4),
                "<30 days": round(float(probs[2]), 4)
            },
            risk_alert=probs[2] > THRESHOLD
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

# 7. Health Check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "Stacking Ensemble (XGB + LGB + RF)",
        "threshold": THRESHOLD,
        "features": 21
    }

# 8. Root Endpoint (Optional)
@app.get("/")
async def root():
    return {
        "message": "Readmission Risk API is running.",
        "docs": "/docs",
        "health": "/health"
    }
