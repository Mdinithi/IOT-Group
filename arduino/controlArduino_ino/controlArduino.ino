int Temp = 1;
float val;
int fanPin=9;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  delay(2000);
  val = analogRead(Temp);
  float celVal=(val/1024.0)*500;
  Serial.print(celVal);
  Serial.println();

}

void ControlFan(int n)
{
  if(n == 0)
    digitalWrite(fanPin,LOW);
   if(n == 1)
     digitalWrite(fanPin,HIGH);
}
