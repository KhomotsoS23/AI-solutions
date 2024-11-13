import os
import asyncio
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams 
# Load environment variables
load_dotenv()
# Set up credentials
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
SPEECH_TO_TEXT_API_KEY = os.getenv("SPEECH_TO_TEXT_API_KEY")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID")
IBM_API_URL = os.getenv("IBM_API_URL")
# Initialize Flask app
app = Flask(__name__)
# Configure Watson Speech to Text and WatsonX functions
def configure_speech_to_text():
    authenticator = IAMAuthenticator(SPEECH_TO_TEXT_API_KEY)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(IBM_API_URL)
    return speech_to_text
def configure_watsonx():
    #from ibm_watsonx import WatsonXAI  # Assuming WatsonX library usage
    credentials = {
        "url": os.getenv("https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-2", "https://us-south.ml.cloud.ibm.com"),
        "apikey": os.getenv("WATSONX_API_KEY")
    }
    model_id = "ibm/granite-13b-chat-v2"
    parameters = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MIN_NEW_TOKENS: 100,
        GenParams.MAX_NEW_TOKENS: 2000,
        GenParams.TOP_P: 0.9,
        GenParams.TEMPERATURE: 0.7
    }
    model = ModelInference(model_id=model_id,params=parameters,credentials=credentials, project_id=IBM_PROJECT_ID)
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
    response = await asyncio.to_thread(model.generate, prompt)
    return response.get("results")[0]["generated_text"]
# Route for home page
@app.route("/")
def home():
    return render_template("index.html")
# Route to handle file upload and transcription
@app.route("/transcribe", methods=["POST"])
def transcribe():
    identify_speakers = request.form.get("identify_speakers", "off") == "on"
    option = request.form.get("option")
    if option == "Audio File" and "file" in request.files:
        audio_file = request.files["file"]
        # Transcribe audio file
        speech_to_text = configure_speech_to_text()
        try:
            result = speech_to_text.recognize(
                audio=audio_file,
                content_type=audio_file.content_type,
                model='en-US_BroadbandModel',
                speaker_labels=identify_speakers
            ).get_result()
            # Process transcript with or without speakers
            if identify_speakers:
                transcript = process_transcript_with_speakers(result)
            else:
                transcript = ' '.join([r['alternatives'][0]['transcript'] for r in result['results']])
        except Exception as e:
            return jsonify({"error": f"Error during transcription: {str(e)}"}), 500
    elif option == "Manual Transcript":
        transcript = request.form.get("transcript", "")
        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400
    else:
        return jsonify({"error": "No valid input provided"}), 400
    # Generate structured summary
    model = configure_watsonx()
    summary = asyncio.run(generate_structured_summary_async(model, transcript))
    return jsonify({"transcript": transcript, "summary": summary})
# Helper function to process transcript with speaker labels
def process_transcript_with_speakers(result):
    transcript = []
    current_speaker = None
    for utterance in result['results']:
        if 'speaker_labels' in utterance:
            speaker = utterance['speaker_labels'][0]['speaker']
            if speaker != current_speaker:
                current_speaker = speaker
                transcript.append(f"\nSpeaker {speaker}:")
        if 'alternatives' in utterance and len(utterance['alternatives']) > 0:
            transcript.append(utterance['alternatives'][0]['transcript'])
    return ' '.join(transcript)
if __name__ == "__main__":
    app.run(debug=True)