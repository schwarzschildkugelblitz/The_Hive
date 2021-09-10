
#include <Servo.h>

Servo Worker_bee_servo; 
void setup() {
  Worker_bee_servo;.attach(3);  
}

void loop() {
    Worker_bee_servo;.write(15);         
    delay(15);                      
}
