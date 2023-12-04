import serial
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_url = 'https://arduino-temp-api.replit.app/temperature/insert_data'
api_key = os.environ.get('ARDUINO_TEMP_API_KEY')
headers = {"arduino-temp-api": api_key}

def setup_serial_connection():
    ser = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize
    ser.flushInput()  # Clear the serial buffer
    return ser

def read_temperature(ser):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Received: {line}")
        return line
    return None

def send_temperature_to_api(temperature):
    response = requests.post(api_url, json={"temperature": temperature}, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")

def main():
    ser = setup_serial_connection()
    try:
        while True:
            temperature_line = read_temperature(ser)
            if temperature_line:
                try:
                    temperature_str = temperature_line.split(':')[1].strip().split()[0]
                    temperature = float(temperature_str)
                    send_temperature_to_api(temperature)
                except (ValueError, IndexError):
                    print("Invalid data received")
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
            time.sleep(10)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        ser.close()
        main()  # Restart the main function to re-establish serial connection
    except KeyboardInterrupt:
        print("Interrupted by the user")
        ser.close()

if __name__ == "__main__":
    main()