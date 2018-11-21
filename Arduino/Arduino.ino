#include <LiquidCrystal.h>

int wait = 2500; //delay frequency of ultrasonic sensor readings in milliseconds

double d1, d2;//distance values, one for each ultrasonic sensor

double dTrig = 5;//Max triggering detected distance

bool car; //state variable if car is at parking lot entrance or not
bool carFlag; //variable to keep track of if a car has been betwen the sensors before incrementing numCars


////LED setup
#define YELLOW1 A0
#define GREEN1 A1
#define YELLOW2 A2
#define GREEN2 A3

//Arrray for Lights
uint8_t yellowLED[] = {YELLOW1,YELLOW2};
uint8_t greenLED[] = {GREEN1,GREEN2};

//colour definitions to be passed to light state
int off = 0;
int green = 1;
int yellow = 2;

//maximum number of spots in the lot
const int MAXSPOTS = 8;
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
  
  numCars = 0;
  carFlag = false;

  pinMode(YELLOW1,OUTPUT);
  pinMode(GREEN1, OUTPUT);
  pinMode(YELLOW2,OUTPUT);
  pinMode(GREEN2, OUTPUT);

  
  initDisplayState();
  int connected = setupEthernet();
  if(connected == 1){
    makeGetRequest();
  }
}

void loop()
{
  readIncomingBytes();
  delay(250);

      //test for lcd update
      lcd.setCursor(0, 1);
      updateLCD(numCars);
      
      car = isCar(); //test if car is there or not
      
      if (car)
      {
        Serial.println("There is a car");
        
          numCars+=1;
          Serial.println(numCars);
          lcd.setCursor(0,1);
          updateLCD(numCars);
          
      }
      else if(!car)
      {
        Serial.println("There is not a car");
        Serial.println(numCars);
      }
      
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

      //Test code for LED
//      delay(wait);
      setLightState(0,green);
      setLightState(1,green);
//      delay(wait);
//      setLightState(0,yellow);
//      setLightState(1,yellow);
//      delay(wait);
//      setLightState(0,off);
//      setLightState(1,off);
//      delay(wait);
      
  //delay for the car test
   delay(wait); //using predetermined time, in milliseconds, delay after each measurement and return

}


bool isCar()
{
  d1 = getDistanceStub(1);
  d2 = getDistanceStub(2);
  if (d1 <= dTrig && d2 <= dTrig)
  {
    return true;
  }
  return false;
}


void setLightState(int row, int colour)
{
    if (colour == green)//Light to be set to Green
    {
      digitalWrite(greenLED[row], HIGH);
      digitalWrite(yellowLED[row], LOW);
      Serial.println("green");
    }
    else if (colour == yellow)//Light to be set to yellow
    {
      digitalWrite(greenLED[row], LOW);
      digitalWrite(yellowLED[row], HIGH);
      Serial.println("yellow");
    }
    else if (colour == off) //Light is not set
    {
      digitalWrite(greenLED[row], LOW);
      digitalWrite(yellowLED[row], LOW);
      Serial.println("not set");
    }
  
}

void updateLCD(int numCars)
{

  if (numCars < MAXSPOTS)
  {
    freeSpots = MAXSPOTS - numCars;
    lcd.print(freeSpots);
  }
  else
  {
    lcd.print("No free spots");
  }
}
