from pymongo import MongoClient
import random

# Verbindung zur MongoDB herstellen
client = MongoClient("mongodb://localhost:27017/")
db = client["quizApp"]
questions_collection = db["quiz_fragen"]
keywords_collection = db["quiz_schluesselwoerter"]

def get_random_question():
    """Zufällige Frage aus der Datenbank abrufen."""
    return questions_collection.aggregate([{ "$sample": { "size": 1 } }]).next()

def get_keywords():
    """Schlüsselwörter aus der Datenbank abrufen."""
    all_keywords = list(keywords_collection.find())
    keywords_dict = {}

    # Zufällige Stadt auswählen
    city_data = random.choice([kw for kw in all_keywords if isinstance(kw.get("value"), dict)])
    keywords_dict.update(city_data["value"])  # Stadt-spezifische Daten hinzufügen
    keywords_dict["incorrect_city"] = city_data.get("incorrect", [])  # Falsche Stadt-Daten

    # Generelle Schlüsselwörter hinzufügen
    for kw in all_keywords:
        if not isinstance(kw.get("value"), dict) and "placeholder" in kw:
            keywords_dict[kw["placeholder"]] = kw["value"]
            keywords_dict[f"incorrect_{kw['placeholder']}"] = kw.get("incorrect", [])

    return keywords_dict

def generate_question(question_template, keywords):
    """Frage generieren, indem Platzhalter ersetzt werden."""
    while "{" in question_template and "}" in question_template:
        start = question_template.find("{")
        end = question_template.find("}", start) + 1
        placeholder = question_template[start:end]
        key = placeholder.strip("{}")
        question_template = question_template.replace(placeholder, str(keywords.get(key, placeholder)))
    return question_template

def generate_incorrect_answers(correct_answer, keywords, question_template):
    """Falsche Antworten aus der Datenbank generieren."""
    incorrect_answers = []

    if "{city}" in question_template:
        incorrect_answers = [kw["city"] for kw in keywords["incorrect_city"]]
    elif "{canton}" in question_template:
        incorrect_answers = [kw["canton"] for kw in keywords["incorrect_city"]]
    elif "{country}" in question_template:
        incorrect_answers = keywords.get("incorrect_country", [])
    elif "{population}" in question_template:
        incorrect_answers = [kw["population"] for kw in keywords["incorrect_city"]]
    elif "{area}" in question_template:
        incorrect_answers = [kw["area"] for kw in keywords["incorrect_city"]]

    return incorrect_answers[:2]  # Nur zwei falsche Antworten zurückgeben

def quiz():
    """Das Quiz starten."""
    print("Willkommen zum Schweizer Quiz!")
    print("Beantworte die folgenden Fragen:\n")

    score = 0
    total_questions = 5  # Anzahl der Fragen, die gestellt werden sollen

    for i in range(total_questions):
        # Zufällige Frage und Schlüsselwörter abrufen
        random_question = get_random_question()
        keywords = get_keywords()

        # Frage generieren
        question_text = generate_question(random_question["template"], keywords)
        correct_answer = generate_question(random_question["answer"], keywords)

        # Falsche Antworten generieren
        incorrect_answers = generate_incorrect_answers(correct_answer, keywords, random_question["template"])
        options = [correct_answer] + incorrect_answers
        random.shuffle(options)

        # Frage und Optionen anzeigen
        print(f"Frage {i + 1}: {question_text}")
        for idx, option in enumerate(options):
            print(f"{idx + 1}. {option}")

        # Antwort des Spielers
        try:
            user_choice = int(input("Deine Antwort (1/2/3): ")) - 1
            if options[user_choice] == correct_answer:
                print("Richtig! 🎉\n")
                score += 1
            else:
                print(f"Falsch! Die richtige Antwort ist: {correct_answer}\n")
        except (ValueError, IndexError):
            print(f"Ungültige Eingabe! Die richtige Antwort war: {correct_answer}\n")

    print(f"Quiz beendet! Deine Punktzahl: {score} von {total_questions}")

if __name__ == "__main__":
    quiz()
