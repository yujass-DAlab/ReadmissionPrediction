# check_setup.py
import os
import sys
import ast
import joblib

print("🔍 Checking your FastAPI setup...")

# --- 1. Check if files exist ---
print("\n📁 Checking files...")
if not os.path.exists("main.py"):
    print("❌ ERROR: main.py not found in the current folder.")
    sys.exit(1)
else:
    print("✅ main.py found.")

if not os.path.exists("readmission_stack_ensemble_final.pkl"):
    print("❌ ERROR: readmission_stack_ensemble_final.pkl not found.")
    print("   Make sure it is in the exact same folder as this script.")
    sys.exit(1)
else:
    # Check file size (should be > 1 MB for an ensemble)
    size_mb = os.path.getsize("readmission_stack_ensemble_final.pkl") / (1024 * 1024)
    print(f"✅ Model file found (Size: {size_mb:.2f} MB).")

# --- 2. Check Python syntax of main.py ---
print("\n🐍 Checking main.py syntax...")
try:
    with open("main.py", "r") as f:
        code = f.read()
    ast.parse(code)  # This compiles the code without executing it
    print("✅ main.py has valid Python syntax.")
except SyntaxError as e:
    print(f"❌ main.py has a SYNTAX ERROR at line {e.lineno}:")
    print(f"   {e.text}")
    sys.exit(1)

# --- 3. Try to load the model (the most critical test) ---
print("\n📦 Attempting to load the model with joblib...")
try:
    model = joblib.load("readmission_stack_ensemble_final.pkl")
    print("✅ Model loaded successfully!")
    print(f"   Model type: {type(model).__name__}")
    
    # Extra check: Is it a StackingClassifier?
    if "StackingClassifier" in str(type(model)):
        print("   ✅ Correct model architecture (Stacking Ensemble) detected.")
    else:
        print("   ⚠️ Model is not a StackingClassifier, but it loaded successfully.")
        
except ModuleNotFoundError as e:
    print(f"❌ Missing Python library: {e.name}")
    print("   Run: pip install scikit-learn joblib numpy")
    sys.exit(1)
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    print("   This usually means the file is corrupted or saved from a different Python version.")
    sys.exit(1)

# --- 4. Check for critical libraries ---
print("\n📚 Checking critical imports...")
try:
    import fastapi
    import uvicorn
    import numpy
    print("✅ FastAPI, Uvicorn, and NumPy are installed.")
except ImportError as e:
    print(f"⚠️ Missing library: {e.name}. Run: pip install fastapi uvicorn joblib numpy scikit-learn")

# --- Final Verdict ---
print("\n" + "="*50)
print("✅✅✅ ALL CHECKS PASSED! You are ready to run:")
print("   uvicorn main:app --host 0.0.0.0 --port 8000")
print("="*50)