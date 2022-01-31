/*
Transmission.ino handles the tarnsmission of commands issued by Central Tracking System 

transmitts 1 byte data at a time 
--> 1st 8 bit number => 2 bit for address + 6 bit for modes

flow : s1 -> recv -> parsedData -> transmision 
+ kill switch interrupt 

written by Tanmay Vadhera
and minor fixes by Harshit Batra 


dependies  
    - ServoTimer2.h
    - SPI.h
*/
#include <SPI.h>
#include <RH_NRF24.h>

#define stopButton  2

RH_NRF24 nrf24(9, 10);
uint8_t data[2];
int x =0,y=0;
uint8_t parsedData[2];

void KILLAll() {
  /* function to stop all bot motion
  issues 2 stop command for each bot   
  */
  while (digitalRead(2)==HIGH){
    // Iterating for all Bots 
    for(x = 0; x < 4;x++){
      // 2 stop command for each bot 
      for(y = 0; Y < 2 ;y++){
      // XXXX(A1)(A0) & 000011 + 1110 1000 = 1110 10(A1)(A0) : 58 is the stop code
      parsedData[0] = x+4*58; 
      // send data
      nrf24.send(parsedData, sizeof(parsedData)); // send data
      nrf24.waitPacketSent();
      }
    }
  }
}


void setup(){
  Serial.begin(115200);

  // interrupt to kill all transmission 
  pinMode(stopButton, INPUT_PULLUP); // already refrenced to +5v / HIGH via pullup
  attachInterrupt(digitalPinToInterrupt(stopButton), KILLAll(), RISING);

  // verifying configuration 
  if (!nrf24.init());
//    Serial.println("init failed");
  if (!nrf24.setChannel(1));
//    Serial.println("setChannel failed");
  if (!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm));
//    Serial.println("setRF failed");    

}
int i,k; // index vars

void loop(){
  // default state 
  parsedData[0] =0;
  parsedData[1] =0;
  String s1;
  char recv[10];//max
  
  // Waiting for response from central tracking system 
  while (!Serial.available());  
  
  // Reading Data from command system 
  s1 = Serial.readStringUntil('\n');  
  s1.toCharArray(recv,sizeof(recv)); 
  
  // index vars 
  i=0,k=0; 
  
  // Parsing Data
  while(recv[i]!='\0')
  {
    if(recv[i] == ' ')
      k++; // skip to next pack
    else
      parsedData[k]=parsedData[k]*10+recv[i]-48; // add the new digit
    i++;
  }
  // Transmitting Data
  nrf24.send(parsedData, sizeof(parsedData)); 
  nrf24.waitPacketSent();
}
