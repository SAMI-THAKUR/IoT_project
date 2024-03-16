import serial
from db import get_data

# Configure the serial port
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with the appropriate serial port
try:
    ser.open()
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()
ser.flushInput()

# Read data from the serial port
while True:
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode().strip()
            print("Arduino says:", data)
    except KeyboardInterrupt :
        ser.close()
        break
    except Exception as e:
        print(f"Error reading data from Arduino: {e}")
        break
