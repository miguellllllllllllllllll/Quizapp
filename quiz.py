from pymongo import MongoClient
import random

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["quizApp"]
collection = db["quiz_keywords"]

def get_quiz_questions():
    """Holt alle Quizfragen aus der Datenbank."""
    return list(collection.find({}, {"_id": 0}))

def get_wrong_answers(correct_answer, all_answers):
    """Generiert zwei falsche Antworten, die sich von der richtigen unterscheiden."""
    wrong_answers = [ans for ans in all_answers if ans != correct_answer]
    return random.sample(wrong_answers, 2)  # Wähle 2 falsche Antworten zufällig aus

def start_quiz():
    """Startet das Quiz."""
    print("Willkommen zum Quiz mit Mehrfachauswahl!")
    print("Wähle die richtige Antwort aus (gib 'exit' ein, um zu beenden).\n")

    questions = get_quiz_questions()
    random.shuffle(questions)  # Fragen zufällig mischen

    # Liste aller möglichen Antworten für falsche Optionen
    all_answers = [q["answer"] for q in questions]

    score = 0
    for i, q in enumerate(questions, 1):
        correct_answer = q["answer"]
        wrong_answers = get_wrong_answers(correct_answer, all_answers)

        # Optionen mischen (eine richtige und zwei falsche Antworten)
        options = [correct_answer] + wrong_answers
        random.shuffle(options)

        print(f"Frage {i}: {q['question']}")
        for j, option in enumerate(options, 1):
            print(f"{j}. {option}")

        user_input = input("Wähle die richtige Antwort (1/2/3 oder 'exit'): ").strip()

        if user_input.lower() == "exit":
            print("\nBeende das Quiz...")
            break

        if user_input.isdigit() and 1 <= int(user_input) <= 3:
            selected_option = options[int(user_input) - 1]
            if selected_option == correct_answer:
                print("Richtig!")
                score += 1
            else:
                print(f"Falsch! Die richtige Antwort ist: {correct_answer}")
        else:
            print("Ungültige Eingabe! Bitte wähle eine Zahl zwischen 1 und 3.")

        print("-" * 30)

    print(f"Quiz beendet! Deine Punktzahl: {score}/{len(questions)}")

if __name__ == "__main__":
    start_quiz()
