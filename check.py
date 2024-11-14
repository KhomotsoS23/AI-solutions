import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print(os.getenv('WATSONX_URL'))
print(f"WatsonX URL: {os.getenv('WATSONX_URL')}")
print(f"API Key: {os.getenv('WATSONX_API_KEY')}")
print(f"WatsonX URL: {os.getenv('SPEECH_TO_TEXT_URL')}")