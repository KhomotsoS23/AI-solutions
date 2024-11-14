import os
import asyncio
from flask import Flask, request, jsonify, render_template
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
app = Flask(__name__)
# Configure IBM Watson Speech to Text
def configure_speech_to_text():
    authenticator = IAMAuthenticator(os.getenv('SPEECH_TO_TEXT_API_KEY'))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.getenv('SPEECH_TO_TEXT_URL'))
    return speech_to_text
# Configure WatsonX model for text generation
WATSONX_URL = os.getenv('WATSONX_URL', "https://us-south.ml.cloud.ibm.com")
def configure_watsonx():
    credentials = {
        "url": WATSONX_URL,
        "apikey": os.getenv("WATSONX_API_KEY")
    }
    project_id = os.getenv("PROJECT_ID")
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
# Process transcript with speaker identification
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
# Summarize transcript with WatsonX model with structured output
async def generate_structured_summary_async(model, transcript):
    prompt = (
        "Extract and concisely present the following from the transcript chunk: 1) New topics or developments, "
        "2) Key decisions or action items (if any), 3) Unresolved issues or ongoing discussions. Include any "
        "available context indicators (e.g., time stamps, speaker changes). Prioritize new information over repetition."
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
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/generateMeetingNotes', methods=['POST'])
def generate_meeting_notes():
    identify_speakers = request.form.get("identify_speakers", "off") == "on"
    option = request.form.get("option", "Manual Transcript")
    model = configure_watsonx()
    # Check if input is an audio file
    if option == "Audio File" and 'file' in request.files:
        audio_file = request.files['file']
        try:
            stt = configure_speech_to_text()
            result = stt.recognize(
                audio=audio_file,
                content_type=audio_file.content_type,
                model='en-US_BroadbandModel',
                speaker_labels=identify_speakers
            ).get_result()
            # Process transcript with or without speaker identification
            transcript = process_transcript_with_speakers(result) if identify_speakers else ' '.join(
                [r['alternatives'][0]['transcript'] for r in result['results']]
            )
            summary = asyncio.run(generate_structured_summary_async(model, transcript))
            return jsonify({"transcript": transcript, "summary": summary})
        except Exception as e:
            return jsonify({"error": f"Error during transcription or summarization: {str(e)}"}), 500
    # Manual Transcript Input
    elif option == "Manual Transcript" and request.form.get("transcript"):
        transcript = request.form.get("transcript")
        try:
            summary = asyncio.run(generate_structured_summary_async(model, transcript))
            return jsonify({"transcript": transcript, "summary": summary})
        except Exception as e:
            return jsonify({"error": f"Error during summarization: {str(e)}"}), 500
    else:
        return jsonify({"error": "Please upload an audio file or enter a transcript to proceed."}), 400
if __name__ == "__main__":
    app.run(debug=True)











