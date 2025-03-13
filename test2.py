from dotenv import load_dotenv
import os
from transformers import pipeline, AutoTokenizer
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

# Load environment variables
load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")

if not api_key:
    print(Fore.RED + "[Error]: Missing Hugging Face API key in .env file.")
    sys.exit(1)

# Load model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Ensure tokenizer has a pad token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Create text-generation pipeline
generator = pipeline("text-generation", model=model_name, tokenizer=tokenizer, pad_token_id=tokenizer.pad_token_id)

def load_knowledge_base(file_path):
    """
    Load questions and answers from a text file.
    Each line in the file should be in the format: "Question?|Answer."
    """
    knowledge_base = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    question, answer = line.split("|")
                    knowledge_base.append((question.strip(), answer.strip()))
    except FileNotFoundError:
        print(Fore.RED + f"[Error]: File '{file_path}' not found.")
        sys.exit(1)
    except ValueError:
        print(Fore.RED + f"[Error]: Invalid format. Each line must contain a question and answer separated by '|'.")
        sys.exit(1)
    return knowledge_base

# Default knowledge base file path
file_path = "c:/Users/Domin/OneDrive/Desktop/PythonBIT/SECOND/info.txt"
knowledge_base = load_knowledge_base(file_path)

def show_questions():
    """Display the list of questions."""
    print(Fore.CYAN + "\n════════════════════════════════════════")
    print(Fore.MAGENTA + "📚 Available Questions:")
    print(Fore.CYAN + "════════════════════════════════════════")
    for i, (question, _) in enumerate(knowledge_base, start=1):
        print(Fore.YELLOW + f"{i}. {question}")

while True:
    show_questions()
    try:
        choice = input(Fore.GREEN + "\n💡 Choose a question number (or type 'exit' to quit) > ").strip()
        if choice.lower() == "exit":
            print(Fore.CYAN + "👋 Goodbye!")
            break
        choice = int(choice) - 1  # Convert to zero-based index
        if 0 <= choice < len(knowledge_base):
            print(Fore.LIGHTGREEN_EX + "\n✅ Retrieved Answer:", Fore.WHITE + knowledge_base[choice][1])
        else:
            print(Fore.RED + "\n❌ Invalid choice! Please choose a valid number.")
            continue
        
        # Ask if the user wants to ask another question
        while True:
            more = input(Fore.MAGENTA + "\n🔄 Do you want to ask another question? (Y/N) > ").strip().lower()
            if more == "y":
                break
            elif more == "n":
                print(Fore.CYAN + "👋 Goodbye!")
                sys.exit(0)
            else:
                print(Fore.RED + "Invalid choice! Please enter Y or N.")
    except ValueError:
        print(Fore.RED + "\n❌ Invalid input! Please enter a number from the list.")