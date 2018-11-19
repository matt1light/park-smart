
// expected values measurements
int freq = 2500;
void setup()
{
  //Initialize serial connection
  Serial.begin(9600);
}
void loop()
{
  double distance = getDistance(2);
  Serial.println(distance);
  
  delay(freq); //using predetermined time, in milliseconds,            //delay after each measurement and print
}
