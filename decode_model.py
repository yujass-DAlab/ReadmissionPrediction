# decode_model.py
import base64
import os

print("📦 Decoding Base64 model...")

# Read the massive text file
with open("model_b64.txt", "r") as f:
    b64_string = f.read()

print(f"✅ Read {len(b64_string)} characters.")

# Decode back to binary
model_bytes = base64.b64decode(b64_string)

# Save as a proper pickle file
with open("readmission_stack_ensemble_final.pkl", "wb") as f:
    f.write(model_bytes)

print("✅ Model saved as 'readmission_stack_ensemble_final.pkl'")

# Verify the size
size = os.path.getsize("readmission_stack_ensemble_final.pkl") / (1024 * 1024)
print(f"✅ File size: {size:.2f} MB")

if size > 80:
    print("🎉 SUCCESS! You now have the real 84 MB model.")
else:
    print("❌ Something went wrong. The file is still too small.")