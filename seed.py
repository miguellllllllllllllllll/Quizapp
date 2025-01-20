from pymongo import MongoClient

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["quizApp"]
questions_collection = db["quiz_fragen"]
keywords_collection = db["quiz_schluesselwoerter"]

# Fragenvorlagen
questions = [
    { "template": "Was ist die Hauptstadt von {country}?", "answer": "Bern", "type": "city" },
    { "template": "Welcher ist der höchste Berg in {country}?", "answer": "Matterhorn", "type": "mountain" },
    { "template": "Wie viele Einwohner hat {city}?", "answer": "{population}", "type": "number" },
    { "template": "Wie groß ist die Fläche von {city} in Quadratkilometern?", "answer": "{area}", "type": "number" },
    { "template": "In welchem Kanton liegt {city}?", "answer": "{canton}", "type": "canton" }
]

# Schlüsselwörter mit falschen Antworten
keywords = [
    { "placeholder": "country", "value": "Schweiz", "incorrect": ["Deutschland", "Österreich", "Frankreich"] },
    {
        "placeholder": "Zürich",
        "value": {"city": "Zürich", "population": "415215", "area": "91.88", "canton": "Zürich"},
        "incorrect": [
            {"city": "Genf", "population": "201818", "area": "15.93", "canton": "Genf"},
            {"city": "Basel", "population": "177654", "area": "22.75", "canton": "Basel-Stadt"}
        ]
    },
    {
        "placeholder": "Genf",
        "value": {"city": "Genf", "population": "201818", "area": "15.93", "canton": "Genf"},
        "incorrect": [
            {"city": "Zürich", "population": "415215", "area": "91.88", "canton": "Zürich"},
            {"city": "Lausanne", "population": "140202", "area": "41.37", "canton": "Waadt"}
        ]
    },
    {
        "placeholder": "Basel",
        "value": {"city": "Basel", "population": "177654", "area": "22.75", "canton": "Basel-Stadt"},
        "incorrect": [
            {"city": "Bern", "population": "133883", "area": "51.62", "canton": "Bern"},
            {"city": "Luzern", "population": "82257", "area": "29.06", "canton": "Luzern"}
        ]
    },
    {
        "placeholder": "mountain",
        "value": "Matterhorn",
        "incorrect": ["Mont Blanc", "Dufourspitze", "Eiger", "Piz Bernina"]
    }
]

# Datenbank löschen und neue Daten hinzufügen
questions_collection.delete_many({})
keywords_collection.delete_many({})
questions_collection.insert_many(questions)
keywords_collection.insert_many(keywords)

print("Daten erfolgreich in die MongoDB geladen!")
