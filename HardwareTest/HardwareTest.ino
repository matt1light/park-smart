#include <ArduinoUnit.h>
#include <ArduinoUnitMock.h>
double expected[] = {10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300, 350, 400};
// expected values measurements
int freq = 5000;
int count = 0;
void setup()
{
  //Initialize serial connection
  Serial.begin(9600);
}
void loop()
{
  double distance = getDistance(1);
  Serial.println(distance);
  Serial.println(expected[count]);
  assertNear(distance, expected[count], 0.5 ); //(abs(b-a)<=maxerror)
  Serial.println("pasted");
  
  delay(freq); //using predetermined time, in milliseconds,            //delay after each measurement and print
    count++;
}
