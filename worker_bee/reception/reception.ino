/* RECEPTION CODE handles reception , decoding and execution of various commands
given issued by central tracking system 


written by Tanmay Vadhera , Harshit Batra ,Mudit Aggarwal and Rohan Deswal 


Dependencies :  
    - ServoTimer2.h
    - SPI.h
    - RH_NRF24.h 
*/

#include <ServoTimer2.h>  // the servo library
#include <SPI.h>  // SPI library 
#include <RH_NRF24.h> //Radio Head library 

#define Worker_bee_Address 1 // bot address 
#define LEFT 95 // speed of left motor
#define RIGHT 106 // speed of right motor

#define RED_LED A0 
#define GREEN_LED A1
#define BLUE_LED A2

//intializing NRf and Servo 

RH_NRF24 nrf24 (A4,A3);
ServoTimer2 flipper_servo; 

class motor 
{

  public:
  int pin1 , pin2 , En
  motor(int pinA,int pinB,int en=4)
  {
    pin1 = pinA ;
    pin2 = pinB ;
    En = en ;
    pinMode(pin1,OUTPUT);
    pinMode(pin2,OUTPUT);
    pinMode(En,OUTPUT);
    digitalWrite(En,1);
  }
  void move_command(int val1,int val2)
  {
    analogWrite(pin1,val1);
    analogWrite(pin2,val2);
  }

  void forward_command()
  {
    // moves motor forward
    analogWrite(pin1,200);
    analogWrite(pin2,0);
  }
  
  void backward_command()
  {
    // moves motor backwards
    analogWrite(pin1,0);
    analogWrite(pin2,200);
  }
  
  void stop_command()
  {
    // stops the motor 
    digitalWrite(pin1,0);
    digitalWrite(pin2,0);
  }

}Left_motor(10, 9),Right_motor(6,5); // instances


uint8_t address,sign;
int8_t offset_speed;

void unpack (uint8_t pack[])
{
  /* 
    Reading received Data
  */  
  address=0;
  offset_speed=0; 

  sign = pack[1];
  
  if (pack[0] !=0){
    offset_speed = pack[0]>>2;       
    address = pack[0]&3;
  }
}

void setup() 
{
  pinMode(RED_LED,OUTPUT);
  pinMode(GREEN_LED,OUTPUT);
  pinMode(BLUE_LED,OUTPUT);
  flipper_servo.attach(3);
  flipper_servo.write(1120);
  delay(1000);
  pinMode (10,OUTPUT);
  digitalWrite(10,0);
  Serial.begin(9600);

  // Verifying Configration 
  if (!nrf24.init()){
    // verifying nrf initialization
    Serial.println("init failed"); 
    // if init fails blink green led 10 times
    for(int i = 0 ; i <10 ; i ++){
      digitalWrite(GREEN_LED,0);
      delay(100);
      digitalWrite(GREEN_LED,1);
      delay(100);
    }
    digitalWrite(A1,0);
  }
  if (!nrf24.setChannel(1)){
    // verifying nrf set channel 
    // Channel frequency used is (2400 + channel) MHz  
    Serial.println("setChannel failed"); 
    // if setChannel fails turn on green led 
    for(int i = 0 ; i <20 ; i ++){
      digitalWrite(GREEN_LED,1);
      delay(100);
    } 
    digitalWrite(A1,0);
  } 
  if (!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm)){
    Serial.println("setRF failed");
    // if setRF fails blink green and red led alternatively 5 times 
    for(int i = 0 ; i <5 ; i ++){
      digitalWrite(GREEN_LED,0);
      delay(100);
      digitalWrite(GREEN_LED,1);
      delay(100);
      digitalWrite(RED_LED,0);
      delay(100);
      digitalWrite(RED_LED,1);
      delay(100);
    }
    digitalWrite(A1,0);
    digitalWrite(A0,0);
  }   
}

uint8_t len;
unsigned int number_of_transmission = 0;
void loop()
{
  if (nrf24.available())
  {
    uint8_t buf[RH_NRF24_MAX_MESSAGE_LEN];
    len = sizeof(buf);

    // decoding received signal 
    if (nrf24.recv(buf, &len))
    {

      number_of_transmission +=1;     
      unpack(buf);       
      if(address == Worker_bee_Address) // do anything only if the address matches - thats what she said ;)
      {
        // blinking blue led for every 10 Transmission
        if (number_of_transmission % 10 > 3 && number_of_transmission < 9) // blinky blinky - Tanmay 2021 ;)
          digitalWrite(BLUE_LED,1);
        else if (number_of_transmission % 10 == 0)
        {
          digitalWrite(BLUE_LED, 0);
        }
        // PID commands 
        if (offset_speed >=0 && offset_speed <= 55)
        {
          offset_speed = sign == 1 ? -offset_speed : offset_speed; // sign = 1 indicates that offset_speed is negative

          Right_motor.move_command(RIGHT + offset_speed,0);
          Left_motor.move_command(LEFT  - offset_speed,0);
          
        }
        // 56-63 special commands           
        else if(offset_speed == 56)  
        {
          // Special command => left Trun 

          // retardation by inverting speed 
          Left_motor.backward__command();
          Right_motor.backward_command();

          delay(30);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();

          delay(100);

          // 90 deg counter clock wise rotation
          Left_motor.move_command(0, 150);
          Right_motor.move_command(150, 0);
          delay(330);

          // retardation by inverting speed 
          Left_motor.move_command(150, 0);
          Right_motor.move_command(0, 150);
          delay(20);

          //stopping bot to remove any prexisting motion 
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(50);
        }
        else if (offset_speed == 57)
        {  
          // Special command => Right Trun

          // retardation by inverting speed 
          Left_motor.backward_command();
          Right_motor.backward_command();
          delay(30);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(100);

          // 90 deg clock wise rotation 
          Left_motor.move_command(150, 0);
          Right_motor.move_command(0, 150);
          delay(370);

          // retardation by inverting speed 
          Left_motor.move_command(0, 150);
          Right_motor.move_command(150, 0);
          delay(20);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(50);

        }
        else if (offspeed == 58)
        {
          // Special command => Stop 
          Left_motor.stop_command();
          Right_motor.stop_command();
        }
        else if(offspeed == 59){ 
          // Special command => right drop

          // retardation by inverting speed 
          Left_motor.backward_command();
          Right_motor.backward_command();
          delay(30);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(100);

          // 90 deg clock wise rotation 
          Left_motor.move_command(150, 0);
          Right_motor.move_command(0, 150);
          delay(370);

          // retardation by inverting speed 
          Left_motor.move_command(0, 150);
          Right_motor.move_command(150, 0);
          delay(20);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(50);

          //Moving bot towards dropchute
          Left_motor.forward_command(150,0);
          Right_motor.forward_command(150,0);
          delay(300);

          //stopping bot 
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(100);
          
          //flipping the flipper 
          flipper_servo.write(-130);
          delay(500);  
          flipper_servo.write(1120);
          delay(100);

          //Moving bot away from dropchute
          Left_motor.backward_command();
          Right_motor.backward_command();
          delay(200);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
        }
        else if(offspeed == 60)
        {
          // Special command => left drop

          // retardation by inverting speed 
          Left_motor.backward_command();
          Right_motor.backward_command();
          delay(30);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(100);

          // 90 deg counter clock wise rotation
          Left_motor.move_command(0, 150);
          Right_motor.move_command(150, 0);
          delay(330);

          // retardation by inverting speed 
          Left_motor.move_command(0, 150);
          Right_motor.move_command(150, 0);
          delay(20);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(50);

          //Moving bot towards dropchute
          Left_motor.forward_command(150,0);
          Right_motor.forward_command(150,0);
          delay(300);

          //stopping bot 
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(100);
          
          //flipping the flipper 
          flipper_servo.write(-130);
          delay(500);  
          flipper_servo.write(1120);
          delay(100);

          //Moving bot away from dropchute
          Left_motor.backward_command();
          Right_motor.backward_command();
          delay(200);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
        }
        else if (offspeed == 61)
        {
          // Special command => drop

          //Moving bot towards dropchute
          Left_motor.forward_command(150,0);
          Right_motor.forward_command(150,0);
          delay(300);

          //stopping bot 
          Left_motor.stop_command();
          Right_motor.stop_command();
          delay(100);
          
          //flipping the flipper 
          flipper_servo.write(-130);
          delay(500);  
          flipper_servo.write(1120);
          delay(100);

          //Moving bot away from dropchute
          Left_motor.backward_command();
          Right_motor.backward_command();
          delay(200);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
        }
        else if (offspeed == 62)
        {
          // Special command => 180 turn

          // 180 deg clock wise rotation
          Left_motor.move_command(150, 0);
          Right_motor.move_command(0, 160);
          delay(640);

          // retardation by inverting speed 
          L.move(0, 200);
          R.move(200, 0);
          delay(30);

          //stopping bot to remove any prexisting motion
          Left_motor.stop_command();
          Right_motor.stop_command();
        }
        else if (offspeed == 62); 
      }
    }
  }
}
