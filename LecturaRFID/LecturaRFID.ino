#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);
const int pinBuzzer = 4; 
const int tonos1[] = {261, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494};
byte LecturaUID[4];
byte Usuario[4] = {0x40, 0x3C, 0x81, 0xA6};
byte Usuario2[4] = {0x82, 0xCD, 0xCD, 0x73};
int option;
int confirmacion;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  
  
}

void loop() {
  if (Serial.available() > 0)
   {
      char option = Serial.read();
      
 
      if(option == 'a')
      {
        digitalWrite(2,HIGH);
        delay(100);
      
        for (int iTono = 0; iTono < 10; iTono++)
        {
         tone(pinBuzzer, tonos1[iTono]);
         delay(100);
        }
        noTone(pinBuzzer);
        digitalWrite(2,LOW);
      }
      if(option == 'b')
      {
        digitalWrite(3,HIGH);
        delay(100);
        tone(pinBuzzer, 400);
        delay(1000);
        digitalWrite(3,LOW);
        noTone(pinBuzzer);
      }
      
   }
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
    
  
 /*
      if(x == 1)
      {
        
        
        
      }
      
   }
  /*if(comparaUID(LecturaUID, Usuario)){
    Serial.println("Bienvenido edwincito");
    digitalWrite(2,HIGH);
    delay(100);
  
    for (int iTono = 0; iTono < 10; iTono++)
    {
     tone(pinBuzzer, tonos1[iTono]);
     delay(100);
    }
    
    noTone(pinBuzzer);
    digitalWrite(2,LOW);
    }
    
  else if(comparaUID(LecturaUID, Usuario2))
  {
    Serial.println("Bienvenido andreita");
    digitalWrite(2,HIGH);
    delay(100);
    
    for (int iTono = 0; iTono < 10; iTono++)
    {
     tone(pinBuzzer, tonos1[iTono]);
     delay(100);
     
    }
    noTone(pinBuzzer);
    digitalWrite(2,LOW);
  }
   else{
    Serial.println("nell no existes");    
    
   }*/
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
