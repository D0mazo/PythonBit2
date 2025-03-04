from dotenv import load_dotenv
import os
from huggingface_hub import login
from transformers import pipeline, AutoTokenizer

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv("HUGGINGFACE_API_KEY")

# Check if API key is available
if not api_key:
    raise ValueError("HUGGINGFACE_API_KEY is missing in .env file")

# Log in to Hugging Face using the API key
login(api_key)

# Load tokenizer to set pad_token_id
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create a text-generation pipeline
generator = pipeline(
    "text-generation",
    model=model_name,
    pad_token_id=tokenizer.eos_token_id  # Avoids warning
)

# Start the conversation loop
while True:
    # Get user input from the console
    prompt = input("Enter a prompt (or type 'thx' to exit): ")

    # If the user types "Aciu", exit the loop and end the program
    if prompt.lower() == "thx":
        print("Goodbye!")
        break

    # Generate text based on the input prompt
    text = generator(prompt, max_length=50, truncation=True)

    # Print the generated text
    print("\nGenerated Text: ", text[0]['generated_text'])
