from flask import Flask, render_template, request, redirect, session, url_for
import os
import asyncio
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")  # Required for sessions

# Route to handle API key input
@app.route("/", methods=["GET", "POST"])
def index():
    # Check if API keys are already set in the session
    api_keys_set = 'speechApiKey' in session and 'watsonxApiKey' in session and 'projectId' in session
    
    if request.method == "POST":
        # Store API keys and project ID in session
        session['speechApiKey'] = request.form['speechApiKey']
        session['watsonxApiKey'] = request.form['watsonxApiKey']
        session['projectId'] = request.form['projectId']
        return redirect(url_for('index'))

    return render_template('index.html', api_keys_set=api_keys_set)

@app.route("/set_keys", methods=["POST"])
def set_keys():
    # Store API keys and project ID in session
    session['speechApiKey'] = request.form['speechApiKey']
    session['watsonxApiKey'] = request.form['watsonxApiKey']
    session['projectId'] = request.form['projectId']
    return redirect(url_for('index'))

@app.route("/generateMeetingNotes", methods=["POST"])
def generate_meeting_notes():
    # Check if the user has set their API keys
    if 'speechApiKey' not in session or 'watsonxApiKey' not in session or 'projectId' not in session:
        return redirect(url_for('index'))  # Redirect to the form if API keys are not set

    # Retrieve user API keys and project ID from session
    speech_api_key = session['speechApiKey']
    watsonx_api_key = session['watsonxApiKey']
    project_id = session['projectId']
    
    # Handle file upload and manual transcript here, then generate meeting notes as before
    transcript = request.form.get('manualTranscript')
    if 'audio' in request.files:
        audio_file = request.files['audio']
        # Add transcription logic here (same as before)
        transcript = "This is a dummy transcript."  # Replace with real transcript logic

    meeting_summary = None
    if transcript:
        model = configure_watsonx(watsonx_api_key, project_id)
        call_summary = asyncio.run(generate_structured_summary_async(model, transcript))
        meeting_summary = call_summary

    return render_template('index.html', meeting_summary=meeting_summary, api_keys_set=True)

def configure_speech_to_text(speech_api_key):
    authenticator = IAMAuthenticator(speech_api_key)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.getenv('SPEECH_TO_TEXT_URL'))
    return speech_to_text

def configure_watsonx(watsonx_api_key, project_id):
    credentials = {
        "apikey": watsonx_api_key
    }
    model_id = "ibm/granite-13b-chat-v2"
    parameters = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MIN_NEW_TOKENS: 100,
        GenParams.MAX_NEW_TOKENS: 2000,
        GenParams.TOP_P: 0.9,
        GenParams.TEMPERATURE: 0.7
    }
    model = ModelInference(
        model_id=model_id,
        params=parameters,
        credentials=credentials,
        project_id=project_id
    )
    return model

async def generate_structured_summary_async(model, transcript):
    prompt = (
        "Extract and concisely present the following from the transcript chunk: 1) New topics or developments, 2) Key decisions or action items (if any), 3) Unresolved issues or ongoing discussions. Include any available context indicators (e.g., time stamps, speaker changes). Prioritize new information over repetition."
        "Analyze the transcript below and provide a structured meeting summary with the following sections:\n\n"
        "1. **Context**: Briefly describe the meeting purpose and participants.\n"
        "2. **Key Points**: Summarize main topics and discussion points.\n"
        "3. **Action Items**: List assigned tasks.\n"
        "4. **Next Steps**: Describe planned follow-ups.\n"
        "5. **Conclusion**: Summarize the overall status and outcome.\n\n"
        "Transcript:\n\n"
        f"{transcript}"
    )
    response =await asyncio.to_thread(model.generate, prompt)
    return response.get("results")[0]["generated_text"]

if __name__ == "__main__":
    app.run(debug=True)
