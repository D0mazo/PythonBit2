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

# Knowledge base with predefined questions
knowledge_base = [
    ("What is a healthy relationship?", "A healthy relationship is built on trust, communication, respect, and mutual support."),
    ("How to improve communication in a relationship?", "To improve communication, listen actively, express your feelings honestly, and avoid blaming or criticizing."),
    ("What are the signs of a toxic relationship?", "Signs of a toxic relationship include constant criticism, lack of trust, controlling behavior, and emotional or physical abuse."),
    ("How to build trust in a relationship?", "Building trust requires honesty, consistency, keeping promises, and being open about your feelings."),
    ("What is emotional intimacy?", "Emotional intimacy is the closeness and connection you feel with someone when you share your thoughts, feelings, and vulnerabilities."),
    ("How to resolve conflicts in a relationship?", "To resolve conflicts, stay calm, listen to each other, find common ground, and work together to find a solution."),
    ("What is the importance of boundaries in a relationship?", "Boundaries are important because they help define what is acceptable and unacceptable, ensuring mutual respect and understanding."),
    ("How to maintain a long-distance relationship?", "Maintain a long-distance relationship by communicating regularly, setting goals, and planning visits to stay connected."),
    ("What is love?", "Love is a deep feeling of affection, care, and commitment towards someone."),
    ("How to show appreciation in a relationship?", "Show appreciation by expressing gratitude, giving compliments, and doing small acts of kindness."),
]

def show_questions():
    """Display the list of questions."""
    print("\nAvailable questions:")
    for i, (question, _) in enumerate(knowledge_base, start=1):
        print(f"{i}. {question}")

while True:
    show_questions()
    
    try:
        choice = input("\nChoose a question number (or type 'exit' to quit) > ").strip()

        if choice.lower() == "exit":
            print("Goodbye!")
            break

        choice = int(choice) - 1  # Convert to zero-based index

        if 0 <= choice < len(knowledge_base):
            print("\nRetrieved Answer:", knowledge_base[choice][1])
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
