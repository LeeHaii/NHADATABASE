from pymongo import MongoClient, ReturnDocument
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ducthangdev2k3:17092003@cluster0.tt9lxn1.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Define database and collection
db = client.nhadatabase
collection_name = db["houses"]
counters_collection = db["counters"]

def get_next_sequence_value(sequence_name: str) -> int:
    sequence_document = counters_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return sequence_document["sequence_value"]