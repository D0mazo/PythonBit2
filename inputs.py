import os
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# File path for the knowledge base
file_path = "brain.txt"

def add_to_knowledge_base():
    """
    Add new questions and answers to the knowledge base.
    """
    # Check if the file exists, create it if not
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass

    while True:
        # Input from the user
        question = input(Fore.CYAN + "🧐 Enter your question: ").strip()
        if not question:
            print(Fore.RED + "❌ Question cannot be empty!")
            continue

        answer = input(Fore.LIGHTGREEN_EX + "💡 Enter the answer: ").strip()
        if not answer:
            print(Fore.RED + "❌ Answer cannot be empty!")
            continue

        # Save to the file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{question}|{answer}\n")

        print(Fore.YELLOW + "✅ Successfully added to the knowledge base!")

        # Ask if user wants to add more
        another = input(Fore.MAGENTA + "➕ Add another? (Y/N): ").strip().lower()
        if another != 'y':
            break

if __name__ == "__main__":
    add_to_knowledge_base()