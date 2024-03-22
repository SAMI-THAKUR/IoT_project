import pymongo
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
from datetime import datetime
import dotenv 
import os


dotenv.load_dotenv()

# Get MongoDB URI from environment variables
mongo_uri = os.getenv("MONGO_URI")

# MongoDB Atlas connection URI
uri = mongo_uri
client = MongoClient(uri)
db = client["iot_project"]
data_collection = db["data"]
current_date = datetime.now().strftime("%d/%m/%Y")
# Create a new collection with the current date #


def get_data(rfid):
    student_info = data_collection.find_one({"rfid": rfid})

    if student_info:
        student_name = student_info["name"]
        division = student_info["division"]
        current_time = datetime.now().strftime("%I:%M:%S %p")
         # Create a new document with student information and timestamp
        attendance_entry = {
            "name": student_name,
            "division": division,
            "rfid_tag": rfid,
            "timestamp": current_time
        }
        collection_name = division + "_" + current_date.replace("/", "-")
        insert_data(attendance_entry , collection_name=collection_name)
    else:
        return "Unknown"


def create_collection(collection_name):
    # Check if the collection already exists
    if collection_name not in db.list_collection_names():
        # Create a new collection
        try:
            db.create_collection(collection_name)
            db[collection_name].create_index("rfid_tag", unique=True)
            print(f"Collection '{collection_name}' created successfully.")
        except Exception as e:
            print(f"Error creating collection: {e}")
    else:
        print(f"Collection '{collection_name}' already exists.")




# Insert a new document into the collection #
def insert_data(data , collection_name):
    create_collection(collection_name=collection_name)
    try:
        # Insert attendance entry into the new collection
        db[collection_name].insert_one(data)
        print("Attendance recorded for:", data["name"])
    except pymongo.errors.DuplicateKeyError:
        print("Attendance already recorder for ", data["name"])




