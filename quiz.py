import time
import random
from pymongo import MongoClient

# MongoDB-Verbindung herstellen
client = MongoClient("mongodb://localhost:27017/")
db = client["quiz_db"]
keywords_collection = db["quiz_schluesselwoerter"]
stats_collection = db["quiz_statistiken"]

def get_keywords(attribute):
    """Daten zu einem Attribut aus der MongoDB holen."""
    pipeline = [
        {"$match": {"attribute": attribute, "value": {"$exists": True, "$ne": None}}}
    ]
    entries = list(keywords_collection.aggregate(pipeline))

    if len(entries) < 3:
        raise ValueError("Nicht genügend Daten für das Attribut vorhanden.")

    correct_entry = random.choice(entries)
    correct_value = correct_entry["value"]
    correct_name = correct_entry["name"]

    # Sicherstellen, dass der richtige Wert numerisch ist, falls erforderlich
    if attribute in ["Fläche", "Einwohner"]:
        if not isinstance(correct_value, (int, float)):
            try:
                correct_value = float(correct_value)
            except ValueError:
                raise TypeError(f"Der richtige Wert '{correct_value}' ist weder numerisch noch konvertierbar.")

    # Falsche Werte filtern
    incorrect_entries = [entry for entry in entries if entry["name"] != correct_name]
    
    # Zufällige falsche Optionen auswählen
    incorrect_values = random.sample(incorrect_entries, k=2)

    return correct_entry, incorrect_values

def quiz():
    """Quiz ausführen."""
    name = input("Geben Sie Ihren Namen ein: ")
    attributes = ["Fläche", "Einwohner", "Hauptstadt", "Höchster Berg"]
    print("Wählen Sie ein Attribut:", ", ".join(attributes))
    attribute = input("> ")

    if attribute not in attributes:
        print("Ungültiges Attribut.")
        return

    start_time = time.time()
    score = 0
    asked_questions = set()

    for i in range(5):
        correct_entry, incorrect_entries = get_keywords(attribute)
        correct_value = correct_entry["value"]
        correct_name = correct_entry["name"]

        # Verhindern, dass die gleiche Frage mehrmals gestellt wird
        while correct_name in asked_questions:
            correct_entry, incorrect_entries = get_keywords(attribute)
            correct_value = correct_entry["value"]
            correct_name = correct_entry["name"]

        # Frage formulieren
        if attribute in ["Fläche", "Einwohner"]:
            question = f"Wie viel {attribute} hat {correct_name}?"
        elif attribute == "Hauptstadt":
            question = f"Was ist die Hauptstadt von {correct_name}?"
        elif attribute == "Höchster Berg":
            question = f"Welcher Berg ist der höchste in {correct_name}?"

        # Optionen generieren
        all_options = [correct_value] + [entry["value"] for entry in incorrect_entries]
        random.shuffle(all_options)

        # Frage stellen
        print(f"Frage {i + 1}:")
        print(question)
        for idx, option in enumerate(all_options, start=1):
            print(f"{idx}: {option}")

        try:
            answer = int(input("> "))
            if all_options[answer - 1] == correct_value:
                print("Richtig!")
                score += 1
            else:
                print(f"Falsch. Die richtige Antwort war: {correct_value}")
        except (ValueError, IndexError):
            print(f"Ungültige Eingabe. Die richtige Antwort war: {correct_value}")
        
        asked_questions.add(correct_name)

    elapsed_time = time.time() - start_time
    print(f"Spiel beendet! Punkte: {score}, Zeit: {elapsed_time:.2f} Sekunden")

    # Statistik speichern
    stats_collection.insert_one({
        "name": name,
        "score": score,
        "time": elapsed_time
    })

    # Top 3 Ergebnisse anzeigen
    top_stats = stats_collection.find().sort([("score", -1), ("time", 1)]).limit(3)
    print("Top 3 Ergebnisse:")
    for stat in top_stats:
        print(f"{stat['name']}: {stat['score']} Punkte, {stat['time']:.2f} Sekunden")

if __name__ == "__main__":
    quiz()
