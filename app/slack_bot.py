import os
import re
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# --- Configuration ---
SLACK_BOT_TOKEN = "your-bot-token"
SLACK_APP_TOKEN = "your-app-token"
API_URL = "http://52.15.208.206/predict"

# --- Initialize the app ---
app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_mention(event, say):
    # Extract the text after the bot mention
    user_text = event.get('text', '')
    # Remove the bot's user ID (e.g., <@U12345>)
    clean_text = re.sub(r'<@[A-Z0-9]+>', '', user_text).strip()

    if not clean_text:
        say("⚠️ Please provide a patient context after mentioning me. Example: `@Readmission Predictor predict Patient's context...`")
        return

    # --- NEW: Check for the command ---
    command_pattern = r'^(predict|analyze|risk)\s+'
    match = re.match(command_pattern, clean_text, re.IGNORECASE)

    if not match:
        say("🤖 I'm here to help with readmission predictions!\n"
            "Use: `@Readmission Predictor predict <patient context>`\n"
            "Or: `@Readmission Predictor analyze <patient context>`")
        return

    # Remove the command from the text, leaving only the patient context
    patient_text = re.sub(command_pattern, '', clean_text, flags=re.IGNORECASE).strip()

    if not patient_text:
        say("⚠️ Please provide a patient context after the command. Example: `@Readmission Predictor predict Patient's context...`")
        return

    # --- Send to AWS API ---
    payload = {
        "patient_id": "slack_user_001",
        "clinical_text": patient_text
    }

    try:          
        # --- INSERT THE HEADERS RIGHT HERE (before the POST) ---
        headers = {"x-api-key": "ssk7326"}          
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)      

        if response.status_code == 200:
            data = response.json()

            risk_class = data.get("risk_class", "Unknown")
            probs = data.get("probabilities", {})
            prob_no = probs.get("NO", 0)
            prob_30 = probs.get(">30 days", 0)
            prob_less = probs.get("<30 days", 0)
            alert = data.get("risk_alert", False)

            if risk_class == "<30 days":
                emoji = "🔴"
                alert_text = "🚨 **HIGH RISK**"
            elif risk_class == ">30 days":
                emoji = "🟡"
                alert_text = "⚠️ **MEDIUM RISK**"
            else:
                emoji = "🟢"
                alert_text = "✅ **LOW RISK**"

            prob_text = (
                f"NO: {prob_no:.1%}, "
                f">30 days: {prob_30:.1%}, "
                f"<30 days: {prob_less:.1%}"
            )

            result = (
                f"{emoji} *Predicted Risk Class:* {risk_class}\n"
                f"{alert_text}\n"
                f"*Probabilities:* {prob_text}\n"
                f"_Disclaimer: This is a decision-support tool. Do not replace clinical judgment._"
            )
            say(result)

        else:
            say(f"❌ API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        say("❌ Connection Error: Could not reach the AWS prediction API. Is the server running?")
    except Exception as e:
        say(f"❌ Unexpected Error: {str(e)}")

# --- Run the app ---
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()