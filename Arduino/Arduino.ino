#include <Ethernet.h>
#include <HCSR04.h>
#include <LiquidCrystal.h>

//Ultrasonic initial settings
//Initialize Ultrasonic Sensors and the pins it uses
int trigPin1 = 6;//trigger pin for ultrasonic sensor 1 connected to pin 6
int echoPin1 = 7;//echo Pin for ultrasonic sensor 1 connected to pin 7
int trigPin2 = 8;//trigger pin for ultrasonic sensor 2 connected to pin 8
int echoPin2 = 9;//echo Pin for ultrasonic sensor 2 connected to pin 9

double d1, d2;//distance values, one for each ultrasonic sensor

int wait = 2500; //delay frequency of ultrasonic sensor readings in milliseconds

double dTrig = 7;//Max triggering dectected distance

UltraSonicDistanceSensor distanceSensor1(trigPin1, echoPin1);
UltraSonicDistanceSensor distanceSensor2(trigPin2, echoPin2);

bool car; //state variable if car is at parking lot entrance or not

//LED setup
#define redPort 2 //LED red pin set to port 2
#define greenPort 3 //LED green pin set to port 3
#define bluePort 4 //LED blue pin set to port 4

//colour definitions to be passed to light state
int red = 0;
int green = 1;
int blue = 2;
int yellow = 3;

//LCD Setup
LiquidCrystal lcd(19,18,17,16,15,14); //Declaration of lcd using LiquidCrystal library setup

void setup()
{
    //Initialize serial connection
    Serial.begin(9600);

    //Initialize lcd interface and set dimentions
    lcd.begin(16,2);

    setupEthernet();
}

void loop()
{

    //Test code for LED
    lightState(red);
    delay(wait);
    lightState(green);
    delay(wait);
    lightState(blue);
    delay(wait);
    lightState(yellow);
    delay(wait);

//    car = isCar(d1, d2); //test if car is there or not
//   
//Test code to see if car is present and display info for it 
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
//delay for the car test
//    delay(wait); //using predetermined time, in milliseconds, delay after each measurement and return

}


bool isCar()
{
    d1 = distanceSensor1.measureDistanceCm();
    d2 = distanceSensor2.measureDistanceCm();
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


void updateLCD()
{
    
}
