// TX <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
// flow : s1 -> recv -> parsedData -> address , angle + sign , distance + sign -> PID -> V 
//-> signed speed -> unsigned speed + sign bit - > TX

#include <SPI.h>
#include <RH_NRF24.h>


// 1st 8 bit number -> 2 bit address + 6 bit differential speed
// 2nd 8 bit number => 1 sign bit , 4 bit base speed , 3 empty bits
RH_NRF24 nrf24(9, 10);

void setup()
{
  Serial.begin(115200);

  if (!nrf24.init());
//    Serial.println("init failed");
  if (!nrf24.setChannel(2));
//    Serial.println("setChannel failed");
  if (!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm));
//    Serial.println("setRF failed");    

}

float timi=millis(),timf,D,x,V=0,filter_state=0,integrator_state=0;
float Kp=0.00025,Kd=0.0155,Ki=0.000085,N=34;// tuned values
int add,speed,sign,speed2=0,misc=0;
int theta,dist,i,k; // index vars
uint8_t data[2];

void loop()
{
  // 0 1 2 3 -> angle +ve , distance +ve , 4 5  
  uint8_t parsedData[] = {0,0}; // do not change default state 
  String s1;
  char recv[10];//max
  
  while (!Serial.available());  // w8 until serial monitor sends out a response
  
  s1 = Serial.readStringUntil('\n');
  s1.toCharArray(recv,sizeof(recv)); 
  
  // process the char array
  i=0;
  k=0; // index vars
  // 1 2 3 
  
  while(recv[i]!='\0')
  {
    if(recv[i] == ' ')
      k++; // skip to next pack
    else
      parsedData[k]=parsedData[k]*10+recv[i]-48; // add the new digit
   
    i++;
  }
  
  nrf24.send(parsedData, sizeof(parsedData)); // send data
  nrf24.waitPacketSent();
  //delay(22); // maintain sync
}
