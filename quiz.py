from pymongo import MongoClient
import random

# Verbindung zur MongoDB herstellen
client = MongoClient("mongodb://localhost:27017/")
db = client["quizApp"]
questions_collection = db["quiz_fragen"]
keywords_collection = db["quiz_schluesselwoerter"]

def get_random_question(asked_questions):
    """Zufällige Frage aus der Datenbank abrufen, die noch nicht gestellt wurde."""
    while True:
        random_question = questions_collection.aggregate([{ "$sample": { "size": 1 } }]).next()
        # Überprüfen, ob die Frage bereits gestellt wurde
        if random_question["_id"] not in asked_questions:
            return random_question

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

def generate_incorrect_answers(correct_answer, keywords, question_template, question_type):
    """Falsche Antworten basierend auf dem Fragetyp generieren."""
    incorrect_answers = []

    if question_type == "city":
        incorrect_answers = [kw["city"] for kw in keywords["incorrect_city"]]
    elif question_type == "canton":
        incorrect_answers = [kw["canton"] for kw in keywords["incorrect_city"]]
    elif question_type == "number":
        incorrect_answers = [kw["population"] for kw in keywords["incorrect_city"]]
    elif question_type == "mountain":
        incorrect_answers = keywords.get("incorrect_mountain", [])

    return incorrect_answers[:2]  # Nur zwei falsche Antworten zurückgeben

def remove_duplicates(correct_answer, incorrect_answers):
    """Duplikate der richtigen Antwort aus den falschen Antworten entfernen."""
    unique_answers = set(incorrect_answers)
    unique_answers.add(correct_answer)  # Die richtige Antwort hinzufügen
    return list(unique_answers)

def quiz():
    """Das Quiz starten."""
    print("Willkommen zum Schweizer Quiz!")
    print("Beantworte die folgenden Fragen:\n")

    score = 0
    total_questions = 5  # Anzahl der Fragen, die gestellt werden sollen
    asked_questions = set()  # IDs der gestellten Fragen speichern

    for i in range(total_questions):
        # Zufällige Frage und Schlüsselwörter abrufen
        random_question = get_random_question(asked_questions)
        asked_questions.add(random_question["_id"])  # Frage als gestellt markieren
        keywords = get_keywords()

        # Frage generieren
        question_text = generate_question(random_question["template"], keywords)
        correct_answer = generate_question(random_question["answer"], keywords)

        # Falsche Antworten generieren
        question_type = random_question.get("type", "generic")
        incorrect_answers = generate_incorrect_answers(correct_answer, keywords, random_question["template"], question_type)

        # Duplikate entfernen und einzigartige Antworten erzeugen
        options = remove_duplicates(correct_answer, incorrect_answers)
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
