import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_property_knowledge_base():
    with open("knowledge_base/property_knowledge_base.md", "r", encoding="utf-8") as file:
        return file.read()


def generate_guest_response(question, knowledge_base):
    prompt = f"""
You are an AI concierge for a short-term rental host.

Use only the property information below to answer the guest question.
If the answer is not available, say that the host should confirm.
Keep the tone warm, clear, and concise.

Property information:
{knowledge_base}

Guest question:
{question}

Suggested response:
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


def main():
    knowledge_base = load_property_knowledge_base()

    print("Welcome to STR Concierge")
    print("Ask a guest question. Type 'exit' to stop.\n")

    while True:
        question = input("Guest question: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer = generate_guest_response(question, knowledge_base)

        print("\nSuggested response:")
        print(answer)
        print()


if __name__ == "__main__":
    main()
