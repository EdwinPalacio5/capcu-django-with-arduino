#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);

byte LecturaUID[4];
byte Usuario[4] = {0x40, 0x3C, 0x81, 0xA6};
byte Usuario2[4] = {0x82, 0xCD, 0xCD, 0x73};

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  
}

void loop() {
  if (! mfrc522.PICC_IsNewCardPresent())
    return;
  if (! mfrc522.PICC_ReadCardSerial())
    return;
    
  for(byte i=0;i<mfrc522.uid.size;i++)
  {
    if(mfrc522.uid.uidByte[i] <0x10)
    {
      Serial.print("0");  
    }  
    else
    {
      Serial.print(" ");      
    }
  Serial.print(mfrc522.uid.uidByte[i], HEX);
  LecturaUID[i] = mfrc522.uid.uidByte[i];
  
  }
  Serial.println("\t");

  if(comparaUID(LecturaUID, Usuario)){
    Serial.println("Bienvenido edwincito");
    digitalWrite(3, HIGH);  
    delay(2000);
    digitalWrite(3,LOW);}
  else if(comparaUID(LecturaUID, Usuario2)){
    Serial.println("Bienvenido andreita");
    digitalWrite(3, HIGH);  
    delay(2000);
    digitalWrite(3,LOW);;     }
   else{
    Serial.println("nell no existes");
    digitalWrite(4, HIGH);  
    delay(2000);
    digitalWrite(4,LOW);
   }
  mfrc522.PICC_HaltA(); //FINALIZA LA COMUNICACION


    
  
}

boolean comparaUID(byte lectura[], byte usuario[])
{
  for (byte i=0; i< mfrc522.uid.size;i++)
  {
    if(lectura[i] != usuario[i])
    return (false);
  }  
  return(true);
}
