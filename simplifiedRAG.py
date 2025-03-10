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

# Ensure tokenizer has a pad token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Create text-generation pipeline
generator = pipeline("text-generation", model=model_name, tokenizer=tokenizer, pad_token_id=tokenizer.pad_token_id)

# Load knowledge base from info.txt
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
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except ValueError:
        print(f"Error: File '{file_path}' has an invalid format. Each line must contain a question and answer separated by '|'.")
        sys.exit(1)
    return knowledge_base

# Define the file path
file_path = "/Users/Domin/OneDrive/Desktop/PythonBIT/SECOND/info.txt"

# Load the knowledge base
knowledge_base = load_knowledge_base(file_path)

# Display menu of questions
def show_questions():
    """Display the list of questions."""
    print("\nAvailable questions:")
    for i, (question, _) in enumerate(knowledge_base, start=1):
        print(f"{i}. {question}")

# Start chat loop
while True:
    show_questions()
    
    try:
        choice = input("\nChoose a question number (or type 'exit' to quit) > ").strip()

        if choice.lower() == "exit":
            print("Goodbye!")
            break

        choice = int(choice) - 1  # Convert to zero-based index

        if 0 <= choice < len(knowledge_base):
            print("\nAnswer:", knowledge_base[choice][1])
        else:
            print("\nInvalid choice! Please choose a valid number.")
            continue  # Go back to the menu

        # Ask if the user wants to ask another question
        while True:
            more = input("\nDo you want to ask another question? (Y/N) > ").strip().lower()
            if more == "y":
                break  # Show questions menu again
            elif more == "n":
                print("Goodbye!")
                sys.exit(0)  # Exit program
            else:
                print("Invalid choice! Please enter Y or N.")

    except ValueError:
        print("\nInvalid input! Please enter a number from the list.")