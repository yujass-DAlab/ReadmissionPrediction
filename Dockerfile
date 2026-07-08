dockerfile
# ============================================================
# Readmission Risk API - Dockerfile 
# ============================================================

# 1. Use a lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. (Critical fix) Update package sources and install libgomp1
#    This installs the system library required by the LightGBM model
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. Copy requirements.txt first (for better caching)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY main.py .
COPY readmission_stack_ensemble_final.pkl .

# 7. Expose the port the API runs on
EXPOSE 8000

# 8. Command to start the API service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
