#include <OneWire.h>
#include <DallasTemperature.h>

// Define pin connections
const int greenLED = 4; // Green LED connected to digital pin 4
const int blueLED = 3; // Blue LED connected to digital pin 3
const int redLED = 2; // Red LED connected to digital pin 2

// Data wire for DS18B20 is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 5

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature
DallasTemperature sensors(&oneWire);

// Function prototypes
void blinkLED(int ledPin, int blinkRate);
float readTemperatureDS18B20();

void setup() {
  pinMode(greenLED, OUTPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  Serial.begin(9600); // Initialize serial communication at 9600 baud rate

  sensors.begin(); // Start up the DallasTemperature library
}

void loop() {
  float temperatureC = readTemperatureDS18B20(); // Read temperature from DS18B20

  // Print the temperature to the Serial Monitor
  Serial.print("Temperature: ");
  Serial.print(temperatureC);
  Serial.println(" C");

  // Turn off all LEDs to start
  digitalWrite(greenLED, LOW);
  digitalWrite(blueLED, LOW);
  digitalWrite(redLED, LOW);

  // Define blink rates based on temperature
  int blueBlinkRate = map(constrain(temperatureC, -40, 15), -40, 15, 1000, 100); // Colder = faster blink
  int redBlinkRate = map(constrain(temperatureC, 40, 100), 40, 100, 100, 1000); // Hotter = faster blink

  // Check the temperature ranges and adjust the blink rate of the corresponding LED
  if (temperatureC >= 15 && temperatureC < 40) {
    blinkLED(greenLED, 500); // Blink green LED for moderate temperatures
  } else if (temperatureC < 15) {
    blinkLED(blueLED, blueBlinkRate); // Blink blue LED for colder temperatures
  } else if (temperatureC >= 40) {
    blinkLED(redLED, redBlinkRate); // Blink red LED for warmer temperatures
  }
}

// Function to blink an LED with a variable rate
void blinkLED(int ledPin, int blinkRate) {
  digitalWrite(ledPin, HIGH);
  delay(blinkRate);
  digitalWrite(ledPin, LOW);
  delay(blinkRate);
}

// Function to read temperature from DS18B20 sensor
float readTemperatureDS18B20() {
  sensors.requestTemperatures(); // Send the command to get temperatures
  return sensors.getTempCByIndex(0); // Returns the temperature in Celsius
}
