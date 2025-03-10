from dotenv import load_dotenv
import os
from transformers import pipeline, AutoTokenizer
import sys

# Load environment variables
load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")

if not api_key:
    print("Error: Missing Hugging Face API key in .env file.")
    sys.exit(1)

# Load model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
generator = pipeline("text-generation", model=model_name, tokenizer=tokenizer, pad_token_id=tokenizer.eos_token_id)

# Start chat loop
while True:
    prompt = input("\nYour prompt > ").strip()

    if prompt.lower() == "exit":
        print("Goodbye!")
        break

    response = generator(prompt, max_length=50, temperature=1.0, do_sample=True)
    print("Generated Text:", response[0]['generated_text'])
