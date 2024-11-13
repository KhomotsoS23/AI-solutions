import logging
import os
import multiprocessing
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv
import inputConfigToMeetingNotesChunk
import inputConfigToMeetingNotesFinal
from generatedMeetingNotes import contentGenerationAPI # type: ignore
# Load environment variables
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# Configure IBM Watson Speech to Text
def configure_speech_to_text():
    authenticator = IAMAuthenticator(os.getenv('SPEECH_TO_TEXT_API_KEY'))
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(os.getenv('SPEECH_TO_TEXT_URL'))
    return speech_to_text
# Home route
@app.route("/")
def home():
    return "Home"
# Say Hello route
@app.route("/sayHello", methods=["POST"])
def sayHello():
    return jsonify("Hello!"), 201
# Generate Meeting Notes route
@app.route("/generateMeetingNotes", methods=["POST"])
def generateMeetingNotes():
    logger.info("Received request to generate meeting notes")
    try:
        # Check if request contains audio file
        if 'audio' in request.files:
            logger.info("Audio file received, transcribing...")
            transcript = transcribe_audio(request.files['audio'])
        else:
            # Use text data directly if audio is not provided
            transcript = request.get_data(as_text=True)
        logger.debug(f"Received transcript of length: {len(transcript)}")
        meeting_summary = orchestrateMeetingNotesGeneration(transcript)
        response = {"meeting_summary": meeting_summary}
        logger.info("Successfully generated meeting notes")
        return jsonify(response), 201
    except Exception as e:
        logger.error(f"Error generating meeting notes: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred while processing the request"}), 500
# Transcribe audio file using Watson Speech to Text
def transcribe_audio(audio_file):
    speech_to_text = configure_speech_to_text()
    try:
        result = speech_to_text.recognize(
            audio=audio_file,
            content_type=audio_file.content_type,
            model='en-US_BroadbandModel'
        ).get_result()
        transcript = ' '.join([r['alternatives'][0]['transcript'] for r in result['results']])
        logger.info("Audio transcription completed successfully")
        return transcript
    except Exception as e:
        logger.error(f"Error during audio transcription: {str(e)}", exc_info=True)
        raise
# Chunk transcript into manageable pieces
def chunk_transcript(transcript, chunk_size=3500, overlap=500):
    logger.debug(f"Chunking transcript of length {len(transcript)}")
    chunks = []
    start = 0
    while start < len(transcript):
        end = start + chunk_size
        chunk = transcript[start:end]
        chunks.append(chunk)
        if end >= len(transcript):
            break
        start = end - overlap
    logger.debug(f"Created {len(chunks)} chunks")
    return chunks
# Generate content using Watson API
def watsonxContentGeneration(data):
    logger.debug("Calling Watson API for content generation")
    try:
        analysis = contentGenerationAPI(
            data["exampleInputs"],
            data["exampleOutputs"],
            data["systemPrompt"],
            data["userPrompt"],
            data["inputData"]
        )
        analysis.callMultiShot()
        result = analysis.contentResponse["watsonxGeneratedResult"]
        logger.debug("Successfully generated content from Watson API")
        return result
    except Exception as e:
        logger.error(f"Error in Watson API call: {str(e)}", exc_info=True)
        raise
# Process individual transcript chunk
def process_transcript_chunk(chunk_data):
    return watsonxContentGeneration(chunk_data)
# Orchestrate the generation of meeting notes
def orchestrateMeetingNotesGeneration(transcript):
    logger.info("Starting meeting notes generation process")
    chunks = chunk_transcript(transcript)
    logger.info(f"Transcript chunked into {len(chunks)} parts")
    # Use multiprocessing to handle chunk processing
    pool = multiprocessing.Pool(processes=9)
    logger.debug(f"Created multiprocessing pool with {min(len(chunks), multiprocessing.cpu_count())} processes")
    # Prepare chunk data for processing
    inputs = []
    for chunk in chunks:
        inputs.append({
            "systemPrompt": inputConfigToMeetingNotesChunk.systemPrompt,
            "userPrompt": inputConfigToMeetingNotesChunk.userPrompt,
            "exampleInputs": inputConfigToMeetingNotesChunk.exampleInputs,
            "exampleOutputs": inputConfigToMeetingNotesChunk.exampleOutputs,
            "inputData": chunk
        })
    # Process chunks and combine results
    chunk_summaries = pool.map(process_transcript_chunk, inputs)
    logger.info(f"Processed {len(chunk_summaries)} chunk summaries")
    combined_summary = " ".join(chunk_summaries) + "\n"
    # Final summary generation
    final_summary_input = {
        "systemPrompt": inputConfigToMeetingNotesFinal.systemPrompt,
        "userPrompt": inputConfigToMeetingNotesFinal.userPrompt,
        "exampleInputs": inputConfigToMeetingNotesFinal.exampleInputs,
        "exampleOutputs": inputConfigToMeetingNotesFinal.exampleOutputs,
        "inputData": combined_summary
    }
    logger.info("Generating final summary")
    final_summary = watsonxContentGeneration(final_summary_input)
    logger.info("Final summary generated successfully")
    return final_summary
# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=8002)





