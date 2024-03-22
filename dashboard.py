from numpy import flexible
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt


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


def count_students_status(date):
    # Get list of all student RFID tags from 'data' collection
    student_rfid_tags = [student["rfid"] for student in db[selected_class+"_data"].find()]
    print(student_rfid_tags)
    present_count = 0
    absent_count = 0
    for rfid_tag in student_rfid_tags:
        # Check if student has attendance entry for the selected date
        attendance_entry = db[date_collection_name].find_one({"rfid_tag": rfid_tag})
        if attendance_entry:
            present_count += 1
        else:
            absent_count += 1
    
    return present_count, absent_count

# Streamlit UI
st.header("Attendance Dashboard")

st.sidebar.title("RFID attendance system")
st.sidebar.subheader("D6ADA Batch-3 Group-1")
st.sidebar.divider()
# Dropdown - Select date collection
selected_date = st.sidebar.date_input("Select a date to view attendance:")
selected_class= st.sidebar.selectbox("Select Class", ["D6ADA", "D6ADB"])


# Fetch attendance data for selected date collection
attendance_data = fetch_attendance_for_date(selected_date)

# Display selected date
st.subheader("Attendance for Date: "+ selected_date.strftime("%d-%m-%Y").replace("/", "-"))
# Filter out collection names with "D6ADA_" prefix
date_collection_name = selected_class + "_" + selected_date.strftime("%d-%m-%Y").replace("/", "-")

if date_collection_name not in collection_names:
    st.write("No attendance data found for the selected date.")
    st.stop()

attendance_data = fetch_attendance_for_date(date_collection_name)

# Display total number of students
total_students = db[selected_class+"_data"].count_documents({})

st.divider()
st.subheader("Attendance Summary:")
col1 , col2 = st.columns(2)
# Count present and absent students
with col1:
    present_count, absent_count = count_students_status(selected_date.strftime("%d/%m/%Y"))
    st.write(f'<div style="font-size: 17px; font-family: monospace; color: #2192FF; background-color: #31363F; margin:5px ; padding-left: 5px; padding-right: 5px; display: inline-block;">Total Student : {total_students}</div>', unsafe_allow_html=True)
    st.write(f'<div style="font-size: 17px; font-family: monospace; color: #2192FF; background-color: #31363F; margin:5px ;padding-left: 5px; padding-right: 5px; display: inline-block;">Present Student : {present_count}</div>', unsafe_allow_html=True)
    st.write(f'<div style="font-size: 17px; font-family: monospace; color: #2192FF; background-color: #31363F; margin:5px ;padding-left: 5px; padding-right: 5px; display: inline-block;">Absent Student : {absent_count}</div>', unsafe_allow_html=True)

# Create labels and sizes for the pie chart
labels = ['Absent', 'Present']
sizes = [absent_count, present_count]

# Create a pie chart
fig, ax = plt.subplots(figsize=(2, 2))
fig.set_facecolor('#B9FFF8')
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90 , colors=['#FF5733', '#33FF57'] , textprops={'fontsize': 6} , )
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circl

with col2:
    st.pyplot(fig)

st.divider()
# Display attendance entries
if attendance_data:
    print(attendance_data)
    st.subheader("Attendance Entries:")
    count  = 0
    for entry in attendance_data:
        tag = str(entry["rfid_tag"])
        count = count + 1
        count_s = str(count)
        
        st.write('<div style="font-size: 18px; font-family: monospace;" >'+ count_s + ": " +entry["name"] + " - " + entry["division"] + " - " + entry["timestamp"] + '</div>', unsafe_allow_html=True)
        st.write(f'<div style="font-size: 15px; font-family: monospace; color: #16FF00; background-color: #31363F;margin-left:30px; margin-bottom:5px ;padding:2px; display: inline-block;">Id: {tag}</div>', unsafe_allow_html=True)
        st.container()

else:
    st.write("No attendance entries found for the selected date.")












