#include <ServoTimer2.h>  // the servo library
#define myAddress 0
#include <SPI.h>
#include <RH_NRF24.h>

#define LEFT 120
#define RIGHT 140

RH_NRF24 nrf24 (A4,A3);
ServoTimer2 myservo; 

class motor 
{
  public:
  int pin1,pin2,En;
  motor(int pinA,int pinB,int en=4)
  {
    pin1=pinA;
    pin2=pinB;
    En = en;
    pinMode(pin1,OUTPUT);
    pinMode(pin2,OUTPUT);
    pinMode(en,OUTPUT);
    digitalWrite(En,1);
  }
  void move(int val1,int val2)
  {
    analogWrite(pin1,val1);
    analogWrite(pin2,val2);
  }

  void fd()
  {
//    digitalWrite(pin1,1);
//    digitalWrite(pin2,0);

    analogWrite(pin1,100);
    analogWrite(pin2,0);
  }
  
  void bk()
  {
//    digitalWrite(pin1,0);
//    digitalWrite(pin2,1);

    analogWrite(pin1,0);
    analogWrite(pin2,100);
  }
  
  void stp()
  {
    digitalWrite(pin1,0);
    digitalWrite(pin2,0);
  }

}L(9, 10),R(6,5); // instances


uint8_t add,sign,spd2,misc;
int8_t spd1;

void unpack (uint8_t pack[])
{
  add=0;
  spd2=0;
  misc=0;
  spd1=0;
  uint8_t cnt=0;  

  sign = pack[1];
  
  if (pack[0] !=0){
    spd1 = pack[0]>>2;       
    add = pack[0]&3;
  }
}

void setup() 
{
  pinMode(A0,OUTPUT);
  myservo.attach(3);
  myservo.write(1120);
  delay(1000);
  pinMode (10,OUTPUT);
  digitalWrite(10,0);
  Serial.begin(9600);
  
  if (!nrf24.init())
    Serial.println("init failed");
    
  // Defaults after init are 2.402 GHz (channel 2), 2Mbps, 0dBm
  if (!nrf24.setChannel(1))
    Serial.println("setChannel failed");
    
  if (!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm))
    Serial.println("setRF failed");    
  
  myservo.write(-130);
  delay(1000);  
  myservo.write(1120);

//  R.move(RIGHT+(int)spd1,0);
//  L.move(LEFT-(int)spd1,0);
//  delay(1000);
}

uint8_t len;

void loop()
{
//  myservo.write(1130);
  if (nrf24.available())
  {
    uint8_t buf[RH_NRF24_MAX_MESSAGE_LEN];
    len = sizeof(buf);
  
    if (nrf24.recv(buf, &len))
    {

      Serial.print(buf[0]);
      Serial.print(" ");
      Serial.print(buf[1]);
        
      unpack(buf);

      Serial.print(" -> ");
      Serial.print(add);
      Serial.print(" ");
      Serial.println(spd1);
                 
      if(add == myAddress) // do anything only if the address matches
      {
        if (spd1>=0 && spd1 <= 55)
        {
          spd1 = sign == 1 ? -spd1 : spd1; // sign = 1 indicates that spd1 is negative

//          digitalWrite(A0,HIGH);
//          delay(500);
//          digitalWrite(A0,LOW);
//          delay(500);
           
          R.move(RIGHT + (int)spd1,0);
          L.move(LEFT  - (int)spd1,0);
          
        }
        // mode instances          
        else if(spd1 == 56)  
        {   // left
          L.stp();
          R.stp();
          delay(100);
          L.move(0,150);
          R.move(150,0);
          delay(290);
          L.move(150,0);
          R.move(0,150);
          delay(20);
          L.stp();
          R.stp();
          delay(50);
        }
        else if (spd1 == 57)
        {   // right
          L.stp();
          R.stp();
          delay(100);
          L.move(150,0);
          R.move(0,150);
          delay(330);
          L.move(0,150);
          R.move(150,0);
          delay(20);
          L.stp();
          R.stp();
          delay(50);
        }
        else if (spd1 == 58)
        {   // stop
          L.stp();
          R.stp();
        }
        else if(spd1 == 59){ 
          // drop
          L.stp();
          R.stp();
          delay(150);
          
          L.move(105,0);
          R.move(110,0);
          delay(640);
          L.stp();
          R.stp();
          myservo.write(-130);
          delay(1000);  
          myservo.write(1120);
          delay(100);
          L.move(0,105);
          R.move(0,110);
          delay(640);
          L.move(0,150);
          R.move(150,0);
          delay(450);
          L.move(150,0);
          R.move(0,150);
          delay(20);
          L.stp();
          R.stp();
          delay(50);       
        }
        else if(spd1 == 60)
        // slow
        {}
        else if (spd1 == 61)
        // reverse
        {}
        else if (spd1 == 62)
        {}
        //180
        else if (spd1 == 63);
        //null  
      }
    }
  }
}
