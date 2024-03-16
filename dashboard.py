import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()

# Get MongoDB URI from environment variables
mongo_uri = os.getenv("MONGO_URI")
uri = mongo_uri
client = MongoClient(uri)
db = client["iot_project"]
collection_names = db.list_collection_names()  # Get list of collection names



# Function to fetch attendance data for a given date
def fetch_attendance_for_date(date):
    try:
        # Fetch attendance data for the given date
        return list(db[date].find())
    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        return None

# Streamlit UI
st.title("Attendance Viewer")

# Dropdown - Select date collection
selected_date = st.date_input("Select a date")

# Fetch attendance data for selected date collection
attendance_data = fetch_attendance_for_date(selected_date)

# Display selected date
st.subheader("Attendance for Date: "+ selected_date.strftime("%d-%m-%Y").replace("/", "-"))

# Filter out collection names with "D6ADA_" prefix
date_collection_name = "D6ADA_" + selected_date.strftime("%d-%m-%Y").replace("/", "-")
if date_collection_name not in collection_names:
    st.write("No attendance data found for the selected date.")
    st.stop()

attendance_data = fetch_attendance_for_date(date_collection_name)

# Display attendance entries
if attendance_data:
    print(attendance_data)
    st.write("Attendance Entries:")
    for entry in attendance_data:
        tag = str(entry["rfid_tag"])
        st.write('<div style="font-size: 20px; font-family: monospace;" >' + entry["name"] + " - " + entry["division"] + " - " + entry["timestamp"] + '</div>', unsafe_allow_html=True)
        st.write(f'<div style="font-size: 20px; font-family: monospace; color: #16FF00; background-color: #31363F; padding-left: 5px; padding-right: 5px; display: inline-block;">{tag}</div>', unsafe_allow_html=True)
        st.divider()

else:
    st.write("No attendance entries found for the selected date.")










