#include <HCSR04.h>

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

void setup() 
{
    //Initialize serial connection
    Serial.begin(9600);
}

void loop() 
{
    d1 = distanceSensor1.measureDistanceCm();
    d2 = distanceSensor2.measureDistanceCm();
    car = isCar(d1,d2); //test if car is there or not

    Serial.print("D1: ");
    Serial.print(d1);
    Serial.println("cm");
    Serial.print("D2: ");
    Serial.print(d2);
    Serial.println("cm");
    if (car)
    {
        Serial.println("There is a car");
    }else
    {
        Serial.println("There is not a car.");    
    }
    
    delay(wait); //using predetermined time, in milliseconds, delay after each measurement and return
    
}


bool isCar(double d1, double d2)
{
    if (d1 <=dTrig && d2 <= dTrig)
    {
        return true;
    }
    return false;
}
