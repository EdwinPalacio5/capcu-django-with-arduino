#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN); // Crea instancia de MFRC522.
const int pinBuzzer = 4; 
const int tonos1[] = {261, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494};
byte LecturaUID[4];

int option;


void setup() {
  Serial.begin(9600); // Inicializa una comunicación serial
  SPI.begin(); // Inicializa el bus SPI
  mfrc522.PCD_Init(); // Inicializa MFRC522
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  
  
}

void loop() {
	//si existen datos disponibles en el puerto serie los leemos
  if (Serial.available() > 0)
   {
   	//leemos la respuesta de Python
      char option = Serial.read();
      
      if(option == 'a')
      {
      //Acceso valido
        digitalWrite(2,HIGH);
        digitalWrite(3,HIGH);
        delay(100);
      
        for (int iTono = 0; iTono < 10; iTono++)
        {
         tone(pinBuzzer, tonos1[iTono]);
         delay(100);
        }
        noTone(pinBuzzer);
        digitalWrite(2,LOW);
        digitalWrite(3,LOW);
      }
      if(option == 'b')
      {
      //Acceso denegado
        digitalWrite(5,HIGH);
        digitalWrite(6,HIGH);
        delay(100);
        tone(pinBuzzer, 400);
        delay(1000);
        digitalWrite(5,LOW);
        digitalWrite(6,LOW);
        noTone(pinBuzzer);
      }
      
   }

   // Busca nuevas tarjetas
  if (! mfrc522.PICC_IsNewCardPresent())
    return;
     // Selecciona una de las tarjetas y la lee
  if (! mfrc522.PICC_ReadCardSerial())
    return;
  //Enviamos el ID de la tarjeta leida a Python
  for(byte i=0;i<mfrc522.uid.size;i++)
  {
    if(mfrc522.uid.uidByte[i] < 0x10)
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
    
  
 
  mfrc522.PICC_HaltA(); //FINALIZA LA COMUNICACION


    
  
}
