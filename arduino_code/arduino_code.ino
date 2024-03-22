#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 49      // Configurable, see typical pin layout above
#define SS_PIN 53       // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance

void setup() {
  Serial.begin(9600);  // Initialize serial communications with the PC
  SPI.begin();          // Init SPI bus
  mfrc522.PCD_Init();   // Init MFRC522
  Serial.println("Scan RFID tag...");
}

void loop() {
  // Look for new cards
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    // Show some details of the PICC (that is: the tag/card)
    Serial.print("UID tag :");
    String content= "";
    byte letter;
    for (byte i = 0; i < mfrc522.uid.size; i++) {
       Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
       Serial.print(mfrc522.uid.uidByte[i], HEX);
       content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
       content.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    Serial.println();
    Serial.print("Message : ");
    content.toUpperCase();
    if (content.substring(1) == "3A 6E C3 6F") //change here the UID of the card/cards that you want to give access
    {
      Serial.println("Authorized access");
      Serial.println();
      delay(3000);
    }
  
   else {
      Serial.println(" Access denied");
      delay(3000);
    }
   } 
}
