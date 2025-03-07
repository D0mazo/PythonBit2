from dotenv import load_dotenv
import os
from huggingface_hub import login
from transformers import pipeline, AutoTokenizer
from colorama import init, Fore, Style  # For colored console output
import sys

# Initialize colorama for cross-platform colored output
init()

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    print(Fore.RED + "Error: HUGGINGFACE_API_KEY is missing in .env file" + Style.RESET_ALL)
    sys.exit(1)

# Log in to Hugging Face
try:
    login(api_key)
    print(Fore.GREEN + "Successfully logged into Hugging Face!" + Style.RESET_ALL)
except Exception as e:
    print(Fore.RED + f"Login failed: {e}" + Style.RESET_ALL)
    sys.exit(1)

# Load the model and tokenizer
model_name = "gpt2"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    generator = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=tokenizer,
        pad_token_id=tokenizer.eos_token_id
    )
    print(Fore.GREEN + f"Model '{model_name}' loaded successfully!" + Style.RESET_ALL)
except Exception as e:
    print(Fore.RED + f"Error loading model: {e}" + Style.RESET_ALL)
    sys.exit(1)

# Store conversation history
history = []

# Welcome message
print(Fore.CYAN + "\n=== Welcome to the Text Generation Console ===" + Style.RESET_ALL)
print("Type a prompt to generate text, or use these commands:")
print("- 'thx' to exit")
print("- 'history' to view past prompts and responses")
print("- 'set length <number>' to change max length (e.g., 'set length 100')")
print("- 'set temp <number>' to change temperature (e.g., 'set temp 0.9')")
print(Fore.CYAN + "===========================================" + Style.RESET_ALL)

# Default generation parameters
max_length = 50
temperature = 1.0

# Start the conversation loop
while True:
    try:
        # Get user input with a styled prompt
        prompt = input(Fore.YELLOW + "\nYour prompt > " + Style.RESET_ALL).strip()

        # Handle commands
        if prompt.lower() == "thx":
            print(Fore.GREEN + "Goodbye!" + Style.RESET_ALL)
            break

        elif prompt.lower() == "history":
            if not history:
                print(Fore.YELLOW + "No history yet!" + Style.RESET_ALL)
            else:
                print(Fore.CYAN + "\n=== Conversation History ===" + Style.RESET_ALL)
                for i, (p, r) in enumerate(history, 1):
                    print(f"{i}. Prompt: {p}")
                    print(f"   Response: {r}")
                print(Fore.CYAN + "===========================" + Style.RESET_ALL)

        elif prompt.lower().startswith("set length "):
            try:
                new_length = int(prompt.split("set length ")[1])
                if new_length > 0:
                    max_length = new_length
                    print(Fore.GREEN + f"Max length set to {max_length}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Length must be positive!" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid length! Use a number (e.g., 'set length 100')" + Style.RESET_ALL)

        elif prompt.lower().startswith("set temp "):
            try:
                new_temp = float(prompt.split("set temp ")[1])
                if 0 < new_temp <= 2.0:
                    temperature = new_temp
                    print(Fore.GREEN + f"Temperature set to {temperature}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Temperature must be between 0 and 2!" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid temperature! Use a number (e.g., 'set temp 0.9')" + Style.RESET_ALL)

        # Generate text for regular prompts
        elif prompt:
            print(Fore.BLUE + "Generating..." + Style.RESET_ALL)
            text = generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                truncation=True,
                do_sample=True  # Adds randomness to generation
            )
            response = text[0]['generated_text']
            print(Fore.GREEN + "Generated Text: " + Style.RESET_ALL + response)
            # Save to history
            history.append((prompt, response))

        else:
            print(Fore.YELLOW + "Please enter a prompt or command!" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Try again or type 'thx' to exit." + Style.RESET_ALL)

print(Fore.CYAN + "\n=== Console Closed ===" + Style.RESET_ALL)