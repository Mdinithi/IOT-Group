#include <Firmata.h>
#include <Boards.h>
#include "SevSeg.h"
#include <IRremote.h>
#include <LiquidCrystal.h>

int buzzer=9;
const int RECV_PIN =7;
IRrecv irrecv(RECV_PIN);
decode_results results;
unsigned long key_value = 0;
int guessedVal=0;
int randomNum=0;
int continousRound=0;
int start_freq=100;
int start_duration=200;
int delayTime=200;
SevSeg sevseg;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn();//start receiving data
    byte numDigits = 1;
    byte digitPins[] = {};
    byte segmentPins[] = {6, 5, 2, 3, 4, 7, 8, 9};
    bool resistorsOnSegments = true;

    byte hardwareConfig = COMMON_CATHODE; 
    sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments);
    sevseg.setBrightness(90);

}

void loop()
{
  //show LED blinks
  playBuzzer(start_freq,start_duration,delayTime);
 
if(irrecv.decode(&results))
{
if(results.value == 0XFFFFFFFF)
  results.value=key_value;
  
  switch(results.value)
  {
    case 0xFF30CF://1
    guessedVal=1;
    break;
    case 0xFF18E7://2
    guessedVal=2;
    break;    
    case 0xFF7A85://3
    guessedVal=3;
    break;
    case 0xFF10EF://4
    guessedVal=4;
    break;
    case 0xFF38C7://5
    guessedVal=5;
    break;
    case 0xFF5AA5://6
    guessedVal=6;
    break;
    case 0xFF42BD://7
    guessedVal=7;
    break;
    case 0xFF4AB5://8
    guessedVal=8;
    break;
    case 0xFF52AD://9
    guessedVal=9;
    break;
    case 0xFF6897://10
    guessedVal=10;
    break;    
  }
  
  //check if guessed value is similar to actual
  if(randomNum==guessedVal)
   { //player continously guessing correct answer if it's not 0
     if(continousRound<3)
     {
       playBuzzer(100,200,200);
     }
     //player  guessed correct answer 3 times
     if(continousRound== 3)
     {
       //play sound
       //upgrade to next level
       start_freq=start_freq+50;
       start_duration=start_duration-50;
       delayTime=delayTime-50;
       continousRound=0;
     }
   }
   else
   {
     //make continousRound=0
     continousRound=0;
     //show the correct number using display
     sevseg.setNumber(randomNum);
     sevseg.refreshDisplay();
   
   }
  
}

}

void playBuzzer(int frequency, int duration,int delayTime)
{
   //generate random number
   randomNum= random(1,10);

  //buzz random number times
  for(int i=0;i<randomNum;i++)
  {
    //play it using beep
    tone(buzzer,frequency, duration);

    delay(delayTime);
  }
}



