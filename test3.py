from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Access an environment variable (e.g., OpenAI API key)
api_key = os.getenv("OPENAI_API_KEY")

print(f"Your API key: {api_key}")