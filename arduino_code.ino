#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10  // Slave Select Pin
#define RST_PIN 9  // Reset Pin

MFRC522 rfid(SS_PIN, RST_PIN); // Create MFRC522 instance

void setup() {
  Serial.begin(9600); // Initialize serial communication
  SPI.begin();        // Init SPI bus
  rfid.PCD_Init();    // Init MFRC522
  Serial.println("RFID Attendance System Initialized");
}

void loop() {
  // Look for new RFID cards
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    // If a card is detected, print its UID to serial monitor
    Serial.print("RFID Tag ID: ");
    printUid(rfid.uid);
    Serial.println();
    
    // Example of a valid RFID tag ID (change this value according to your RFID tags)
    byte validUid[] = {0x11, 0x22, 0x33, 0x44}; // Example UID
    
    // Compare the detected UID with the valid UID
    if (compareUid(rfid.uid.uidByte, validUid, rfid.uid.size)) {
      Serial.println("Approved: Access Granted");
    } else {
      Serial.println("Access Denied");
    }
    // Halt PICC
    rfid.PICC_HaltA();
    // Stop encryption on PCD
    rfid.PCD_StopCrypto1();
  }
}

// Function to print UID of RFID tag
void printUid(byte *uid) {
  for (byte i = 0; i < 4; i++) {
    Serial.print(uid[i], HEX);
    Serial.print(" ");
  }
}

// Function to compare two UIDs
bool compareUid(byte *uid1, byte *uid2, byte size) {
  for (byte i = 0; i < size; i++) {
    if (uid1[i] != uid2[i]) {
      return false;
    }
  }
  return true;
}
