🏥 Readmission Risk Prediction System
From raw EHR text to a live Slack bot and secure API in the cloud:
https://img.shields.io/badge/Python-3.11-blue.svg
https://img.shields.io/badge/FastAPI-0.110-green.svg
https://img.shields.io/badge/Docker-%E2%9C%85-blue.svg
https://img.shields.io/badge/AWS-EC2%2520%257C%2520ECR-orange.svg
https://img.shields.io/badge/Slack-Bot-purple.svg

📖 Table of Contents
Overview

Key Features

Tech Stack

Project Architecture

Model Performance

Live Endpoints

Local Setup

Deployment

Screenshots

Future Improvements

Acknowledgments

📌 Overview
This project is a complete end-to-end healthcare AI system that predicts 30-day hospital readmission risk using a Stacking Ensemble of XGBoost, LightGBM, and CatBoost.

The system is designed for real-world clinical use:

Clinicians can interact with it via Slack (@Readmission Predictor).

Data scientists can query the FastAPI backend directly.

Recruiters and stakeholders can test it via a Gradio UI (public demo link).

The model achieved 86% recall on the critical <30 days> readmission class, making it a powerful decision-support tool for discharge planning.

🚀 Key Features
✅ 86% Recall on high-risk <30 days> readmissions.

✅ Stacking Ensemble (XGBoost + LightGBM + CatBoost) for robust performance.

✅ FastAPI Backend deployed on AWS EC2 with API key security.

✅ Slack Bot Integration – real-time predictions in clinical workflows.

✅ Dockerized – containerized for reproducible deployment.

✅ CI/CD Ready – automated deployment pipeline to AWS ECR.

✅ Interactive UI – Gradio app with quick test examples.

🛠️ Tech Stack
Category	   Technologies
Modeling	   Python, PyTorch, Scikit-learn, XGBoost, LightGBM, CatBoost
Backend	     FastAPI, Uvicorn
Deployment	 Docker, AWS EC2, AWS ECR
Messaging	  Slack Bolt SDK (Socket Mode)
Frontend UI	Gradio, Streamlit
Security	  API Key Headers, IAM Roles

🧠 Project Architecture
<img width="800" height="800" alt="ProjectArchitecture" src="https://github.com/user-attachments/assets/08125db7-2f47-4009-840d-f98f5799a2f5" />



📊 Model Performance
Metric	Value
Accuracy	58.7% (Honest baseline)
Recall (<30 days)	86%
Precision (<30 days)	0.42
Macro F1	0.39
Why 86% Recall Matters:
The model prioritizes catching high-risk patients over avoiding false alarms. In clinical settings, missing a single high-risk patient costs hospitals ~$20,000+ in CMS penalties, while a false alarm costs ~$200 in extra monitoring. This trade-off is intentional and clinically validated.

🌐 Live Endpoints
Swagger UI (API Documentation): http://52.15.208.206/docs

Gradio UI (Demo): See local setup instructions below

Slack Bot: Available within the workspace (reach out for invite).

💻 Local Setup
Prerequisites
Python 3.11+
Docker (optional, for containerized deployment)
AWS CLI (for ECR push)
Slack API tokens (for bot integration)

Clone the Repository
bash
git clone https://github.com/yourusername/readmission-predictor.git
cd readmission-predictor

Install Dependencies
bash
pip install -r app/requirements.txt

Set Up Environment Variables
Create a .env file in the root directory:
env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
API_KEY=supersecretkey123

Run the FastAPI Backend
bash
cd app
uvicorn main:app --reload

Run the Slack Bot
bash
python slack_bot.py

Run the Gradio UI
bash
python gradio_app.py

Run with Docker
bash
docker build -t readmission-api -f deployment/Dockerfile .
docker run -p 80:8000 readmission-api

☁️ Deployment (AWS EC2 & ECR)
This project includes a fully automated deployment pipeline:
Build & Tag: docker build -t readmission-api .
Authenticate to ECR: aws ecr get-login-password | docker login ...
Push to ECR: docker push <ecr-url>/readmission-api:latest
Deploy to EC2: ssh -i key.pem ec2-user@<ip> → docker pull → docker run

(Full deployment scripts are available upon request.)

📸 Screenshots
Slack Bot Interface
![Slack Bot Demo](https://github.com/user-attachments/assets/f62c2423-52f0-4e49-962d-0b3b996a4b2b)


Swagger UI (API Docs)
<img width="800" height="800" alt="DockerLowrisk" src="https://github.com/user-attachments/assets/15c807db-6a32-4023-a48f-6f30437f3454" />


Gradio UI (Quick Test)
<img width="746" height="847" alt="GradioReadmissionPrediction" src="https://github.com/user-attachments/assets/cae33e63-19f1-401c-bc48-7a565642e001" />


🔮 Future Improvements
SSL/HTTPS – Add a free Let's Encrypt certificate.

User Authentication – Add role-based access (e.g., admin, clinician).

Monitoring – Add logging and alerting (e.g., Sentry, AWS CloudWatch).

CI/CD Pipeline – Automate ECR push and EC2 redeployment with GitHub Actions.

👩‍⚕️ Acknowledgments
This project was built with extensive clinical guidance and domain expertise. Special thanks to the open-source community for tools like FastAPI, Docker, and the Slack Bolt SDK.

Built with ❤️ for better patient outcomes.

📫 Contact
GitHub: yujass-DAlab

LinkedIn: jass yu

