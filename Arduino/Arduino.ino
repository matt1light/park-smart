#include <Ethernet.h>
#include <HCSR04.h>
#include <LiquidCrystal.h>

//Ultrasonic initial settings
//Initialize Ultrasonic Sensors and the pins it uses
int trigPin1 = 10; //trigger pin connected to pin 11
int echoPin1 = 11; //echo Pin connected to pin 12
int trigPin2 = 12;
int echoPin2 = 13;

double d1, d2;

int wait = 2500; //delay frequency of ultrasonic sensor readings in milliseconds

double dTrig = 7;

UltraSonicDistanceSensor distanceSensor1(trigPin1, echoPin1);
UltraSonicDistanceSensor distanceSensor2(trigPin2, echoPin2);

bool car; //state variable if car is at parking lot entrance or not

//LED setup
#define redPort A0
#define greenPort A1
#define bluePort A2
//colour definitions to be passed to light state
int red = 0;
int green = 1;
int blue = 2;
int yellow = 3;


void setup()
{
    //Initialize serial connection
    Serial.begin(9600);
}

void loop()
{
    lightState(red);
    delay(wait);
    lightState(green);
    delay(wait);
    lightState(blue);
    delay(wait);
    lightState(yellow);
    delay(wait);
//    d1 = distanceSensor1.measureDistanceCm();
//    d2 = distanceSensor2.measureDistanceCm();
//    car = isCar(d1, d2); //test if car is there or not
//    
//    Serial.print("D1: ");
//    Serial.print(d1);
//    Serial.println("cm");
//    Serial.print("D2: ");
//    Serial.print(d2);
//    Serial.println("cm");
//    if (car)
//    {
//        Serial.println("There is a car");
//        }
//    else
//    {
//        Serial.println("There is not a car.");
//    }
//
//    delay(wait); //using predetermined time, in milliseconds, delay after each measurement and return

}


bool isCar(double d1, double d2)
{
  if (d1 <= dTrig && d2 <= dTrig)
  {
    return true;
  }
  return false;
}


void lightState(int colour)
{
    if (colour == 0) // Light to be set to red
    {
        digitalWrite(redPort, HIGH);
        digitalWrite(greenPort, LOW);
        digitalWrite(bluePort, LOW);
        Serial.println("red");
    }   
    else if (colour == 1)//Light to be set to Green
    {
        digitalWrite(redPort, LOW);
        digitalWrite(greenPort, HIGH);
        digitalWrite(bluePort, LOW);
        Serial.println("green");
    }
    else if (colour == 2)//Light to be set to blue
    {
        digitalWrite(redPort, LOW);
        digitalWrite(greenPort, LOW);
        digitalWrite(bluePort, HIGH);
        Serial.println("blue");
    }
    else if (colour == 3)//Light to be set to yellow
    {
        digitalWrite(redPort, HIGH);
        digitalWrite(greenPort, HIGH);
        digitalWrite(bluePort, LOW);
        Serial.println("yellow");
    }
    else //Light is not set
    {
        digitalWrite(redPort, HIGH);
        digitalWrite(greenPort, LOW);
        digitalWrite(bluePort, LOW);
        Serial.println("not set");
    }
}
