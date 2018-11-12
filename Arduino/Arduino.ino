#include <Ethernet.h>
#include <HCSR04.h>
#include <LiquidCrystal.h>

////Ultrasonic initial settings
////Initialize Ultrasonic Sensors and the pins it uses
#define trigPin1 A5//trigger pin for ultrasonic sensor 1 connected to pin 6
#define echoPin1 A4//echo Pin for ultrasonic sensor 1 connected to pin 7
#define trigPin2 8//trigger pin for ultrasonic sensor 2 connected to pin 8
#define echoPin2 9//echo Pin for ultrasonic sensor 2 connected to pin 9

double d1, d2;//distance values, one for each ultrasonic sensor

int wait = 2500; //delay frequency of ultrasonic sensor readings in milliseconds

double dTrig = 7;//Max triggering dectected distance

UltraSonicDistanceSensor distanceSensor1(trigPin1, echoPin1);
UltraSonicDistanceSensor distanceSensor2(trigPin2, echoPin2);

bool car; //state variable if car is at parking lot entrance or not

////LED setup
#define YELLOW1 A0
#define GREEN1 A1
#define YELLOW2 A2
#define GREEN2 A3

//colour definitions to be passed to light state
int off = 0;
int green = 1;
int yellow = 2;

//maximum number of spots in the lot
int maxSpots = 12;
int numCars = 0;
int freeSpots;

//LCD Setup
const int rs = 7, en = 6, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup()
{
  //Initialize serial connection
  Serial.begin(9600);

  //Initialize lcd interface and set dimentions
  lcd.begin(16, 2);
  lcd.print("Free spots:");

  pinMode(YELLOW1,OUTPUT);
  pinMode(GREEN1, OUTPUT);
  pinMode(YELLOW2,OUTPUT);
  pinMode(GREEN2, OUTPUT);

}

void loop()
{

  //test for lcd update
  lcd.setCursor(0, 1);
  numCars = 7;
  updateLCD(numCars);
    
      //Test code for LED
      delay(wait);
      lightState(1,green);
      lightState(2,green);
      delay(wait);
      lightState(1,yellow);
      lightState(2,yellow);
      delay(wait);
      lightState(1,off);
      lightState(2,off);
      delay(wait);


  //    car = isCar(d1, d2); //test if car is there or not
  //    if (car)
  //    {
  //        numCars+=1;
  //        updateLCD(numCars);
  //    }
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



void lightState(int row, int colour)
{
  if (row == 1)
  {
    if (colour == green)//Light to be set to Green
    {
      digitalWrite(GREEN1, HIGH);
      digitalWrite(YELLOW1, LOW);
      Serial.println("green");
    }
    else if (colour == yellow)//Light to be set to yellow
    {
      digitalWrite(GREEN1, LOW);
      digitalWrite(YELLOW1, HIGH);
      Serial.println("yellow");
    }
    else if (colour == off) //Light is not set
    {
      digitalWrite(GREEN1, LOW);
      digitalWrite(YELLOW1, LOW);
      Serial.println("not set");
    }
  }

  else if (row == 2)
  {
    if (colour == green)//Light to be set to Green
    {
      digitalWrite(GREEN2, HIGH);
      digitalWrite(YELLOW2, LOW);
      Serial.println("green");
    }
    else if (colour == yellow)//Light to be set to yellow
    {
      digitalWrite(GREEN2, LOW);
      digitalWrite(YELLOW2, HIGH);
      Serial.println("yellow");
    }
    else if(colour == off) //Light is not set
    {
      digitalWrite(GREEN2, LOW);
      digitalWrite(YELLOW2, LOW);
      Serial.println("not set");
    }
  }

}

void updateLCD(int numCars)
{

  if (numCars <= maxSpots)
  {
    freeSpots = maxSpots - numCars;
    lcd.print(freeSpots);
  }
  else
  {
    lcd.print("No free spots");
  }
}
