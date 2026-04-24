import json

def load_faqs(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def find_answer(question, faqs):
    question = question.lower()

    for topic, content in faqs.items():
        for keyword in content["keywords"]:
            if keyword in question:
                return content["answer"]

    return "I don’t have enough information to answer confidently. The host should confirm."

def main():
    faqs = load_faqs("knowledge_base/faq_answers.json")

    print("Welcome to STR Concierge")
    question = input("Guest question: ")
    print(find_answer(question, faqs))

if __name__ == "__main__":
    main()
