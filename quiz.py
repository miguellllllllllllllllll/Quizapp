from pymongo import MongoClient
import random

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["quizApp"]
questions_collection = db["quiz_questions"]
keywords_collection = db["quiz_keywords"]

def get_questions():
    """Holt alle Fragenvorlagen aus der Datenbank."""
    return list(questions_collection.find({}, {"_id": 0}))

def get_keywords():
    """Holt alle Platzhalter-Werte aus der Datenbank."""
    keywords = list(keywords_collection.find({}, {"_id": 0}))
    return {kw["placeholder"]: kw["value"] for kw in keywords}

def fill_question_template(template, keywords):
    """Ersetzt Platzhalter in der Vorlage mit Werten aus der Datenbank."""
    for placeholder, value in keywords.items():
        template = template.replace(f"{{{placeholder}}}", value)
    return template

def start_quiz():
    """Startet das Quiz."""
    print("Willkommen zum Schweiz-Quiz!")
    print("Beantworte die folgenden Fragen (gib 'exit' ein, um zu beenden).\n")

    questions = get_questions()
    keywords = get_keywords()
    score = 0
    total_questions = len(questions)

    for i, question in enumerate(questions, 1):
        # Vorlage ausfüllen
        filled_question = fill_question_template(question["template"], keywords)

        print(f"Frage {i}: {filled_question}")
        user_answer = input("Deine Antwort: ").strip()

        if user_answer.lower() == "exit":
            print("\nBeende das Quiz...")
            break

        # Antwort überprüfen
        if user_answer.lower() == question["answer"].lower():
            print("Richtig!")
            score += 1
        else:
            print(f"Falsch! Die richtige Antwort ist: {question['answer']}")

        print("-" * 30)

    print(f"Quiz beendet! Deine Punktzahl: {score}/{total_questions}")

if __name__ == "__main__":
    start_quiz()
