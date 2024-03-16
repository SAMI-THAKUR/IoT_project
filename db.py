import pymongo
from pymongo.mongo_client import MongoClient
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas connection URI
uri = "mongodb+srv://iot_project:iot@cluster0.xn1d2wy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["iot_project"]
data_collection = db["data"]
current_date = datetime.now().strftime("%d/%m/%Y")
collection_name = "D6ADA_" + current_date.replace("/", "-")
# Create a new collection with the current date #
def create_collection():
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
        insert_data(attendance_entry)
    else:
        return "Unknown"


# Insert a new document into the collection #
def insert_data(data):
    create_collection()
    try:
        # Insert attendance entry into the new collection
        db[collection_name].insert_one(data)
        print("Attendance recorded for:", data["name"])
    except pymongo.errors.DuplicateKeyError:
        print("Attendance already recorder for ", data["name"])

get_data(1234)



