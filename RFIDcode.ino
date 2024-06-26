#include <SPI.h>
#include <MFRC522.h>

#define sda_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(sda_PIN, RST_PIN);
const int buzzerPin = 8; // Change this to the desired digital pin for the buzzer
const String authorizedCardUID = "xxxxxxxxxx"; // Replace with the UID of your authorized RFID card
void setup() {
 Serial.begin(9600);
 SPI.begin();
 mfrc522.PCD_Init();
  pinMode(buzzerPin, OUTPUT);
  Serial.println("RFID Doorbell System Initialized");
void loop() {
  // Look for new cards
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String cardUID = getCardUID();
    Serial.println("Card UID: " + cardUID);
    if (cardUID == authorizedCardUID) {
      Serial.println("Access Granted!");
      playSound(); // You can customize this function to play different sounds
      delay(5000); // Delay to avoid rapid triggering
    } else {
      Serial.println("Access Denied!");
    }
  }
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}
String getCardUID() {
  String cardUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    cardUID.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
    cardUID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  cardUID.toUpperCase();
  return cardUID;
}
void playSound() {
  // Customize this function to play your desired sound
  tone(buzzerPin, 1000, 1000); // Example: Play a 1kHz tone for 1 second
}
