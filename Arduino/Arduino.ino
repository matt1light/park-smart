#include <ArduinoJson.h>

#include <LiquidCrystal.h>

int wait = 2000; //delay frequency of ultrasonic sensor readings in milliseconds

double d1, d2;//distance values, one for each ultrasonic sensor

double dTrig = 5;//Max triggering detected distance

bool car; //state variable if car is at parking lot entrance or not

//
#ifndef NUMROWS
    #define NUMROWS 3
#endif

//LCD Pin Setup
#define rs 7
#define en 6
#define d4 5
#define d5 4
#define d6 3
#define d7 2

//LCD Setup
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

////LED setup
#define YELLOW1 A0
#define GREEN1 A1
#define YELLOW2 A2
#define GREEN2 A3

#ifndef CONNECTION_SUCCESS
  #define CONNECTION_SUCCESS 1
#endif

//Arrray for Lights
uint8_t yellowLED[NUMROWS] = {YELLOW1, YELLOW2};
uint8_t greenLED[NUMROWS] = {GREEN1, GREEN2};

//colour definitions to be passed to light state
#define OFF 0
#define GREEN 1
#define YELLOW 2

//testing bool
bool isTesting = false;

struct DisplayState{
  char lightState[NUMROWS];
  int emptySpots;
};

DisplayState currentDisplay;

void setup()
{
  //Initialize serial connection
  Serial.begin(9600);

  //Initialize lcd interface and set dimentions
  lcd.begin(16, 2);
  lcd.print("Free spots:");

  pinMode(YELLOW1, OUTPUT);
  pinMode(GREEN1, OUTPUT);
  pinMode(YELLOW2, OUTPUT);
  pinMode(GREEN2, OUTPUT);

 
  initDisplayState();
  int connected = setupEthernet();
  if (connected == CONNECTION_SUCCESS) {
    makeGetRequest();
  }
}

void loop()
{
  readIncomingBytes();
  car = isCar(); //test if car is there or not

  if (car)
  {
    lcd.setCursor(0, 1);
    updateLCD(currentDisplay.emptySpots);
  }

  //delay for the car test
  delay(wait); //using predetermined time, in milliseconds, delay after each measurement and return

}

bool isCar()
{
  if (isTesting) {
    //If testung, use the stub file
    d1 = getDistanceStub(1);
    d2 = getDistanceStub(2);
  }
  else
  {
    //if not testing, run with regular file
    d1 = getDistance(1);
    d2 = getDistance(2);
  }
  //compare the distance detected by each ultrasonic sensor and compare it to the predetermined maximum
  if (d1 <= dTrig && d2 <= dTrig)
  {
    //Set is car to true
    return true;
  }
  return false;
}

void setLightState(int row, int colour)
{
  if (colour == GREEN)//Light to be set to Green
  {
    digitalWrite(greenLED[row], HIGH);
    digitalWrite(yellowLED[row], LOW);
  }
  else if (colour == YELLOW)//Light to be set to yellow
  {
    digitalWrite(greenLED[row], LOW);
    digitalWrite(yellowLED[row], HIGH);
  }
  else if (colour == OFF) //Light is not set, turn off
  {
    digitalWrite(greenLED[row], LOW);
    digitalWrite(yellowLED[row], LOW);
  }

}

void updateLCD(int availableSpots)
{
  //Display the number of available cars
  lcd.print(availableSpots);

}
