import serial
import db

ser = serial.Serial(port='COM4',baudrate=9600)

while True:
    value= ser.readline()
    print(value)
    valueInString=str(value,'UTF-8')
    numbers_only = ''.join(filter(str.isdigit, valueInString)) # Example string containing numbers

# Check if the string is not empty before converting to integer
    if numbers_only:
        numbers_only = int(numbers_only)
        print("Converted integer:", numbers_only)
    else:
        print("String is empty, cannot convert to integer.")
    print(numbers_only)
    db.get_data(numbers_only)
