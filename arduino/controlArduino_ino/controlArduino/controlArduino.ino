int Temp = 1;
float val;
int fanPin=9;


void setup()
{
  Serial.begin(9600);

}

void loop()
{
  RecordTempreture();
  delay(1000);
//read temperature 
if(Serial.available())
{
  ControlFan(Serial.parseInt());
  Serial.flush();
}

  

}

void RecordTempreture()
{
  val = analogRead(Temp);
  float celVal=(val/1024.0)*500;
  Serial.print(celVal);
  Serial.println();
  
}

void ControlFan(int n)
{
  if(n == 0)
    Serial.println("fan turned off");
    //digitalWrite(fanPin,LOW);
   if(n == 1)
     Serial.println("fan turned on");
    // digitalWrite(fanPin,HIGH);
}
