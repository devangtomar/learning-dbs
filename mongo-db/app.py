from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017/")

# Select the database
db = client.testdatabase

# Select the collection
collection = db.testcollection

# Perform a select query
documents = collection.find()

# Print the documents
for document in documents:
    print(document)
