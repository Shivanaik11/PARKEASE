#include <Arduino.h>
#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define TRIG_PIN 5  // Connect to Trig pin on HC-SR04
#define ECHO_PIN 18  // Connect to Echo pin on HC-SR04

/* WiFi credentials */
#define WIFI_SSID "iPhone"
#define WIFI_PASSWORD "administrator"

/* Firebase credentials */
#define API_KEY "AIzaSyCEbevoIw6HvbRiOK5kJNbNoZ9Nou7ARow"
#define DATABASE_URL "parkeasetesting-f25e5-default-rtdb.firebaseio.com"

/* User credentials for authentication */
#define USER_EMAIL "parkeasetesting@gmail.com"
#define USER_PASSWORD "Shivan11$"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

unsigned long sendDataPrevMillis = 0;
unsigned long count = 0;

// OLED Display setup
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

float measureDistance()
{
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  float distance = duration * 0.034 / 2;

  return distance;
}

void updateFirebaseDistance(float distance)
{
  // Update Firebase with the status
  String path = "/Entry_Interface/status";

  if (distance <= 10.0)
  {
    // If distance is less than or equal to 10.0, update Firebase with "DETECTED"
    Serial.printf("Set status... %s\n", Firebase.setString(fbdo, path.c_str(), "ENTRY_DETECTED") ? "ok" : fbdo.errorReason().c_str());
  }
  else
  {
    // If distance is greater than 10.0, update Firebase with "DETECTING"
    Serial.printf("Set status... %s\n", Firebase.setString(fbdo, path.c_str(), "ENTRY_DETECTING") ? "ok" : fbdo.errorReason().c_str());
  }
}

void setup()
{
  Serial.begin(115200);

  // Initialize OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
  {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }

  display.display(); // Display splash screen

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  /* Assign the API key (required) */
  config.api_key = API_KEY;

  /* Assign the user sign-in credentials */
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  // Additional setup code if needed...

  Firebase.begin(&config, &auth);

  Firebase.setDoubleDigits(5);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop()
{
  if (Firebase.ready() && (millis() - sendDataPrevMillis > 100 || sendDataPrevMillis == 0))
  {
    sendDataPrevMillis = millis();

    // Measure distance
    float distance = measureDistance();

    // Update Firebase with the status
    updateFirebaseDistance(distance);

    // Display status on OLED
    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);

    if (distance <= 10.0)
    {
      display.print("ENTRY_DETECTED");
    }
    else
    {
      display.print("ENTRY_DETECTING");
    }

    display.display();

    count++;
  }

  // Your existing loop code...

  delay(1000); // Add a delay to prevent excessive Firebase requests
}
