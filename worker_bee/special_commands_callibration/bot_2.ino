//#include <ServoTimer2.h>  // the servo library
//#define LEFT 185 // speed of left motor
//#define RIGHT 185 // spped of right motor
//
//class motor 
//{
//  public:
//  int pin1,pin2,En;
//  motor(int pinA,int pinB,int en=4)
//  {
//    pin1=pinA;
//    pin2=pinB;
//    En = en;
//    pinMode(pin1,OUTPUT);
//    pinMode(pin2,OUTPUT);
//    pinMode(en,OUTPUT);
//    digitalWrite(En,1);
//  }
//  void move(int val1,int val2)
//  {
//    analogWrite(pin1,val1);
//    analogWrite(pin2,val2);
//  }
//
//  void fd()
//  {
////    digitalWrite(pin1,1);
////    digitalWrite(pin2,0);
//
//    analogWrite(pin1,100);
//    analogWrite(pin2,0);
//  }
//  
//  void bk()
//  {
////    digitalWrite(pin1,0);
////    digitalWrite(pin2,1);
//
//    analogWrite(pin1,0);
//    analogWrite(pin2,100);
//  }
//  
//  void stp()
//  {
//    digitalWrite(pin1,0);
//    digitalWrite(pin2,0);
//  }
//
//}L(10, 9),R(6,5); // instances
//
//ServoTimer2 flipper_servo; 
//
//void setup() {
//  // put your setup code here, to run once:
//  flipper_servo.attach(3);
//  flipper_servo.write(1120);
//  
//  // left
//  L.stp();
//  R.stp();
//  delay(100);
//  L.move(0,150);
//  R.move(150,0);
//  delay(340);
//  L.move(150,0);
//  R.move(0,150);
//  delay(20);
//  L.stp();
//  R.stp();
//  delay(50);
//
//  delay(5000);
//
//  //right
//  L.stp();
//  R.stp();
//  delay(100);
//  L.move(150,0);
//  R.move(0,150);
//  delay(330);
//  L.move(0,150);
//  R.move(150,0);
//  delay(20);
//  L.stp();
//  R.stp();
//  delay(50);
//
//  delay(5000);
//
//  // drop
//  L.stp();
//  R.stp();
//  delay(150);
//  
//  L.move(110,0);
//  R.move(110,0);
//  delay(640);
//  L.stp();
//  R.stp();
//  flipper_servo.write(-130);
//  delay(1000);  
//  flipper_servo.write(1120);
//  delay(100);
//  L.move(0, 150);
//  R.move(150, 0);
//  delay(540);
//  L.move(0,150);
//  R.move(150,0);
//  delay(20);
//  L.stp();
//  R.stp();
//  delay(50);
//
//}
//
//void loop() {
//  // put your main code here, to run repeatedly:
//
//}
