#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN 10
#define RST PIN 9
#define LED_G 5 //define green LED pin
#define LED_B 8 //define red LED
int BUZZER1
=
6; //buzzer pin
int BUZZER2 =4;//buzzer pin
MFRC522 mfrc522 (SS_PIN, RST_PIN); // Create MFRC522 instance.
void setup()
}
Serial.begin(9600); // Initialize serial communications with the PC
while (!Serial); // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4) SPI.begin(); // Init SPI bus
mfrc522.PCD_Init(); // Init MFRC522
mfrc522.PCD_DumpVersionToSerial(); // Show details of PCD - MFRC522 Card Reader details Serial.println (F("Scan PICC to see UID, SAK, type, and data blocks..."));
pinMode (LED_G, OUTPUT);
pinMode (LED B, OUTPUT); pinMode (BUZZER1, OUTPUT); pinMode (BUZZER2, OUTPUT);
}
void loop()
{
// Look for new cards
if (mfrc522.PICC_IsNewCardPresent ())
{
return;
}
// Select one of the cards
if (!mfrc522. PICC_ReadCardSerial())
{
return;
}
//Show UID on serial monitor
Serial.print ("UID tag :"); 
String content= "";
byte letter;
for (byte i = 0; i < mfrc522.uid.size; i++)
{
Serial.print (mfrc522.uid.uidByte[i] <0x10 ?"0":"");
Serial.print (mfrc522.uid.uidByte[i], HEX);
content.concat (String (mfrc522.uid.uidByte[i] < 0x10?" 0" : " ")); content.concat (String (mfrc522.uid.uidByte[i], HEX));
}
Serial.println();
Serial.print ("Message: ");
content.toUpperCase();
if (content.substring(1)
"83 F8 20 OF")
//change here the UID of the card/cards that you want to give access
{
digitalWrite (LED_G, HIGH);
digitalWrite(LED_B, LOW);
tone (BUZZER1, 450);
delay (500);
noTone (BUZZER1);
delay (500);
digitalWrite(LED_G, LOW);
}
else if (content.substring(1)
"OC OB 56 4A")
//change here the UID of the card/cards that you want to give access
}
digitalWrite(LED_G, LOW);
digitalWrite (LED_B, HIGH);
tone (BUZZER2, 450);
}
delay(500);
noTone (BUZZER2);
delay(500);
tone (BUZZER2, 450);
delay(500);
noTone (BUZZER2);
delay (500);
digitalWrite(LED_B, LOW);
}