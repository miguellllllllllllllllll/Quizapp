from pymongo import MongoClient

# Verbindung zur MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["quizApp"]
questions_collection = db["quiz_fragen"]
keywords_collection = db["quiz_schluesselwoerter"]

# Fragenvorlagen
questions = [
    { "template": "Was ist die Hauptstadt von {country}?", "answer": "Bern" },
    { "template": "Welcher ist der höchste Berg in {country}?", "answer": "Matterhorn" },
    { "template": "Welcher Fluss fließt durch {country}?", "answer": "Rhein" },
    { "template": "Wie heißt die offizielle Währung von {country}?", "answer": "Schweizer Franken" },
    { "template": "Wie viele Einwohner hat {city}?", "answer": "{population}" },
    { "template": "Wie groß ist die Fläche von {city} in Quadratkilometern?", "answer": "{area}" },
    { "template": "In welchem Kanton liegt {city}?", "answer": "{canton}" }
]

# Platzhalter-Werte für Städte und andere Fragen
keywords = [
    # Länderbezogene Daten
    { "placeholder": "country", "value": "Schweiz" },
    { "placeholder": "mountain", "value": "Matterhorn" },
    { "placeholder": "river", "value": "Rhein" },
    { "placeholder": "currency", "value": "Schweizer Franken" },
    # Städte
    # Zürich
    { "placeholder": "city", "value": "Zürich" },
    { "placeholder": "population", "value": "415215" },
    { "placeholder": "area", "value": "91.88" },
    { "placeholder": "canton", "value": "Zürich" },
    # Genf
    { "placeholder": "city", "value": "Genf" },
    { "placeholder": "population", "value": "201818" },
    { "placeholder": "area", "value": "15.93" },
    { "placeholder": "canton", "value": "Genf" },
    # Basel
    { "placeholder": "city", "value": "Basel" },
    { "placeholder": "population", "value": "177654" },
    { "placeholder": "area", "value": "22.75" },
    { "placeholder": "canton", "value": "Basel-Stadt" },
    # Bern
    { "placeholder": "city", "value": "Bern" },
    { "placeholder": "population", "value": "133883" },
    { "placeholder": "area", "value": "51.62" },
    { "placeholder": "canton", "value": "Bern" },
    # Lausanne
    { "placeholder": "city", "value": "Lausanne" },
    { "placeholder": "population", "value": "140202" },
    { "placeholder": "area", "value": "41.37" },
    { "placeholder": "canton", "value": "Waadt" },
    # Luzern
    { "placeholder": "city", "value": "Luzern" },
    { "placeholder": "population", "value": "82257" },
    { "placeholder": "area", "value": "29.06" },
    { "placeholder": "canton", "value": "Luzern" },
    # Lugano
    { "placeholder": "city", "value": "Lugano" },
    { "placeholder": "population", "value": "63743" },
    { "placeholder": "area", "value": "75.98" },
    { "placeholder": "canton", "value": "Tessin" },
    # Winterthur
    { "placeholder": "city", "value": "Winterthur" },
    { "placeholder": "population", "value": "114220" },
    { "placeholder": "area", "value": "68.04" },
    { "placeholder": "canton", "value": "Zürich" }
]

# Datenbank löschen und neue Daten hinzufügen
questions_collection.delete_many({})
keywords_collection.delete_many({})
questions_collection.insert_many(questions)
keywords_collection.insert_many(keywords)

print("Daten erfolgreich in die MongoDB geladen!")
