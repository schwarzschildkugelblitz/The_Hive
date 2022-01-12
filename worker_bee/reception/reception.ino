/* RECEPTION CODE handles reception , decoding and execution of various commands
given by central tracking system 

written by Tanmay Vadhera
and minor changes made by Mudit Aggarwal, Rohan Deswal and Harshit Batra 


dependies  
    - ServoTimer2.h
    - SPI.h
    - RH_NRF24.h 
*/

#include <ServoTimer2.h>  // the servo library
#include <SPI.h>  // SPI library 
#include <RH_NRF24.h> //NRF library 

#define Worker_bee_Address 0
#define LEFT 107//149 // speed of left motor
#define RIGHT 111//140 // speed of right motor
#define tau 0.00016
#define a 0.0017
#define b 0.00000288
#define h 0.00102
#define l 0.00204
RH_NRF24 nrf24 (A4,A3);
ServoTimer2 flipper_servo; 


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

}L(10, 9),R(6,5); // instances


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
  pinMode(A2,OUTPUT);
  flipper_servo.attach(3);
  flipper_servo.write(1120);
  delay(1000);
  pinMode (10,OUTPUT);
  digitalWrite(10,0);
  Serial.begin(9600);
  
  if (!nrf24.init())
    Serial.println("init failed");
    
  // Defaults after init are 2.402 GHz (channel 2), 2Mbps, 0dBm
  if (!nrf24.setChannel(2))
    Serial.println("setChannel failed");
    
  if (!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm))
    Serial.println("setRF failed");    
  
  flipper_servo.write(-130);
  delay(1000);  
  flipper_servo.write(1120);

//  R.move(RIGHT+(int)spd1,0);
//  L.move(LEFT-(int)spd1,0);
//  delay(1000);
}

uint8_t len;
unsigned int num_trans = 0;
void loop()
{
//  myservo.write(1130);
  if (nrf24.available())
  {
    //Serial.println("Rohan");
    uint8_t buf[RH_NRF24_MAX_MESSAGE_LEN];
    len = sizeof(buf);
  
    if (nrf24.recv(buf, &len))
    {
        num_trans+=1;
        
//      Serial.print(buf[0]);
//      Serial.print(" ");
//      Serial.print(buf[1]);
        
      unpack(buf);
//
//      Serial.print(" -> ");
//      Serial.print(add);
//      Serial.print(" ");
//      Serial.println(spd1);
                 
      if(add == Worker_bee_Address) // do anything only if the address matches
      {
        
        if (num_trans++ >= 5 && num_trans < 10) // blinky blinky
          digitalWrite(A2,1);
         else if (num_trans >= 10) 
          {
            num_trans = 0;
            digitalWrite(A2,0);
          }
          
        if (spd1>=0 && spd1 <= 55)
        {
          spd1 = sign == 1 ? -spd1 : spd1; // sign = 1 indicates that spd1 is negative

//          digitalWrite(A0,HIGH);
//          delay(500);
//          digitalWrite(A0,LOW);
//          delay(500);
          
          R.move(RIGHT + spd1,0);
          L.move(LEFT  - spd1,0);
//          changes made 
//          delay(5); 
//          R.move(RIGHT,0);
//          L.move(LEFT,0);
          
        }
        // mode instances          
        else if(spd1 == 56)  
        {   // left
            L.move(0,200);
            R.move(0,200);
            delay(30);
            L.stp();
            R.stp();
            delay(100);
            L.move(0,150);
            R.move(150,0);
            delay(315);
            L.move(150,0);
            R.move(0,150);
            delay(20);
            L.stp();
            R.stp();
            delay(50);

        }
        else if (spd1 == 57)
        {   // right
            L.move(0,200);
            R.move(0,200);
            delay(30);
            L.stp();
            R.stp();
            delay(100);
            L.move(150,0);
            R.move(0,150);
            delay(315);
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
          // right_drop
          L.move(0,200);
          R.move(0,200);
          delay(30);
          L.stp();
          R.stp();
          delay(100);
          L.move(150,0);
          R.move(0,150);
          delay(315);
          L.move(0,150);
          R.move(150,0);
          delay(20);
          L.stp();
          R.stp();
          delay(50);
          
          
          L.move(0,200);
          R.move(0,200);
          delay(30);
          L.stp();
          R.stp();
          delay(150);
          
          flipper_servo.write(-130);
          delay(500);  
          flipper_servo.write(1120);
          delay(100);

          delay(20);
          L.move(0,150);
          R.move(0,150);
          delay(250);
          L.stp();
          R.stp();
        }
        else if(spd1 == 60)
        // left_drop
        {
          L.move(0,200);
          R.move(0,200);
          delay(30);
          L.stp();
          R.stp();
          delay(100);
          L.move(0,150);
          R.move(150,0);
          delay(315);
          L.move(150,0);
          R.move(0,150);
          delay(20);
          L.stp();
          R.stp();
          delay(50);
          
          
          L.move(0,200);
          R.move(0,200);
          delay(30);
          L.stp();
          R.stp();
          delay(150);
          
          flipper_servo.write(-130);
          delay(500);  
          flipper_servo.write(1120);
          delay(100);

          delay(20);
          L.move(0,150);
          R.move(0,150);
          delay(250);
          L.stp();
          R.stp();
        }
        else if (spd1 == 61)
        // drop
        {
          L.move(0,200);
          R.move(0,200);
          delay(30);
          L.stp();
          R.stp();
          delay(150);
          
          flipper_servo.write(-130);
          delay(500);  
          flipper_servo.write(1120);
          delay(100);

          delay(20);
          L.move(0,150);
          R.move(0,150);
          delay(250);
          L.stp();
          R.stp();
        }
        else if (spd1 == 62)
        //180
        {
          delay(100);
          L.move(0,150);
          R.move(0,150);
          
          delay(600);
          L.move(150,0);
          R.move(0,150);
          delay(500);
          L.move(0,200);
          R.move(200,0);
          delay(30);
          L.stp();
          R.stp();

          delay(20);
          L.move(0,150);
          R.move(0,150);
          delay(600);
          L.stp();
          R.stp();
        }
        else if (spd1 == 63);
        //null  
      }
    }
  }
}
