import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print(f"WatsonX URL: {os.getenv('WATSONX_URL')}")
print(f"API Key: {os.getenv('WATSONX_API_KEY')}")
