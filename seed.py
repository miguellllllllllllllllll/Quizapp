from pymongo import MongoClient

# Verbindung zu MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["quizApp"]
collection = db["quiz_keywords"]

# Quiz-Daten einfügen
data = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the largest mammal?", "answer": "Blue Whale"},
    {"question": "What is the boiling point of water?", "answer": "100°C"},
    {"question": "Who wrote 'Hamlet'?", "answer": "Shakespeare"}
]


# Vorherige Daten löschen und neue Daten einfügen
collection.delete_many({})
collection.insert_many(data)

print("Daten erfolgreich in die MongoDB geladen!")
