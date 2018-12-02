#include <LinkedList.h>
#include <Event.h>
#include <Timer.h>

#include <ArduinoJson.h>

#include <LiquidCrystal.h>



//----------------------------------------------------------------------------
// CONFIGURATION
//----------------------------------------------------------------------------

#define DEBUGHARDWARE 0 // Set to 1 to have hardware and displayState information printed to serial
#define DEBUGNETWORK 0 // Set to 1 to have networking information printed to serial
#define DEBUGJSON 1 // Set to 1 to have JSON encoding/decoding information printed to serial

#define WAIT 2000 //delay frequency of ultrasonic sensor readings in milliseconds
#define REQUESTDELAY 5000 // Time between requests made to the server. Does not account for processing time
#define LOOPITERATIONS (REQUESTDELAY / WAIT) // How many times loop() should run before another request should be sent
char loops = 0;


// Currently hardcoded.
// If given the chance to make full production code, there would be a request
// made that would be run on startup, fetch the config (output ID, number of
// rows, etc).
#ifndef NUMROWS
  #define NUMROWS 3
#endif

#ifndef OUTPUTID
  #define OUTPUTID 1
#endif


//----------------------------------------------------------------------------
// HARDWARE SETUP
//----------------------------------------------------------------------------


double d1, d2;//distance values, one for each ultrasonic sensor

double dTrig = 5;//Max triggering detected distance

bool car; //state variable if car is at parking lot entrance or not


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

//colour definitions to be passed to light state
#define OFF 0
#define GREEN 1
#define YELLOW 2

// Struct to represent the system's display state
struct DisplayState {
  char lightState[NUMROWS];
  int emptySpots;
};

DisplayState currentDisplay;

int numCars = 0;

//----------------------------------------------------------------------------
// STATE VARIABLES
//----------------------------------------------------------------------------

//Arrray for Lights
uint8_t yellowLED[NUMROWS] = {YELLOW1, YELLOW2};
uint8_t greenLED[NUMROWS] = {GREEN1, GREEN2};

bool carFlag = false;
int extraCars = 0;
const long ENTRANCE_DELAY = (long)1000 * 60 * 2; // 1 second * 1 minute * 2 = 2 minutes

//testing bool
bool isTesting = false;

// Buffer that incoming data will be written to.
// This will be read from when deserializing, or written to when serializing.
#define MSGBUFFERSIZE 300
byte messageBuffer[MSGBUFFERSIZE];

#define JSONBUFFERSIZE 200
char jsonBuffer[JSONBUFFERSIZE];
char errorBuffer[3]; // HTTP error codes are only ever 3 digits long

//----------------------------------------------------------------------------
// MAIN PROGRAM
//----------------------------------------------------------------------------

void setup()
{
  // Initialize serial connection
  Serial.begin(9600);
  while (!Serial) {}; // Wait until the serial port is able to connect.
  delay(1000);

  //Initialize lcd interface and set dimensions
  lcd.begin(16, 2);
  lcd.print("Free spots:");

  pinMode(YELLOW1, OUTPUT);
  pinMode(GREEN1, OUTPUT);
  pinMode(YELLOW2, OUTPUT);
  pinMode(GREEN2, OUTPUT);

  initDisplayState();

  //setRowColour(1, YELLOW);

  setupEthernet();
  //int connected = attemptConnection();
  //if (connected == CONNECTION_SUCCESS) {
    
    //makeGetRequest();
  //}
  //else {
    //throwFatalError("Could not connect to the server");
  //}
  //throwFatalError("False alarm");
}

void loop()
{
  
  if (loops >= LOOPITERATIONS) {
    loops = 0;
    // It's time to make a request from the server
    if(attemptConnection()){
      makeGetRequest();
    }
  }

  if (readIncomingBytes()) {
    //closeConnection();
    extractJSONFromMessage();
    deserialize(jsonBuffer);
   
  }

  
  car = isCar(); //test if car is there or not

  if (car)
  {
    
    updateLCD();
  }
  if (car && !carFlag)
  {
  #if DEBUGHARDWARE
    Serial.println("There is a car");
    Serial.println(carFlag);
  #endif

    carFlag = true;

    carEntersLot();
    //lcd.setCursor(0, 1);

  }
  else if (!car)
  {
    #if DEBUGHARDWARE
      Serial.println("There is not a car");
      Serial.println(carFlag);
    #endif
    carFlag = false;
  }

  //delay for the car test
  delay(WAIT); //using predetermined time, in milliseconds, delay after each measurement and return
  loops++;
}

bool isCar()
{
  if (isTesting) {
    //If testing, use the stub file
    d1 = getDistanceStub(1);
    d2 = getDistanceStub(2);
  }
  else
  {
    //if not testing, run with regular file
    d1 = getDistance(1);
    d2 = getDistance(2);
    #if DEBUGHARDWARE
    Serial.print("Sensor 1: ");
    Serial.println(d1);
    Serial.print("Sensor 2: ");
    Serial.println(d2);
    #endif
  }
  //compare the distance detected by each ultrasonic sensor and compare it to the predetermined maximum
  if (d1 <= dTrig && d2 <= dTrig)
  {
    //Set is car to true
    return true;
  }
  return false;
}

void setRowColour(int row, int colour)
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

void updateLightState()
{
  for (int i = 0; i < NUMROWS; i++)
  {
    setRowColour(i, currentDisplay.lightState[i]);
  }
}

void updateLCD()
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Available spots:");
  lcd.setCursor(0,2);
  
  //Display the number of available cars
  int availableSpots = getAvailableSpots();
  lcd.print(availableSpots);
  /*
  Serial.print("Available spots:");
  Serial.println(availableSpots);
  Serial.print("Extra Cars:");
  Serial.println(extraCars);
  Serial.println(availableSpots);
  */
}

int getAvailableSpots() {
  int availableSpots = currentDisplay.emptySpots;
  if (availableSpots - extraCars < 0) {
    return 0;
  }
  else {
    return availableSpots - extraCars;
  }
}

void carEntersLot()
{
  extraCars += 1;
  // starts 2 minute timer
  // on timer finish decrease ext
  Timer t;
  int timer_event_id = t.after(ENTRANCE_DELAY, removeExtraCar, 0);
}

void removeExtraCar()
{
  extraCars -= 1;
}

//void getNewStateFromServer()
//{
//    makeGetRequest()
//    readIncomingBytes()
//}

// Create dummy values for the current displayState
void initDisplayState() {
  for (int i = 0; i < NUMROWS; i++) {
    currentDisplay.lightState[i] = 0;
  }
  currentDisplay.emptySpots = 0;
}

void throwFatalError(char* errorMsg) {
  /*
  for (int i=0; i<NUMROWS; i++){
    //currentDisplay.lightState[i] = YELLOW;
    setRowColour(i, YELLOW);
  }
  */
 
  
  currentDisplay.emptySpots = 9999;
  updateLightState();
  updateLCD();
  digitalWrite(YELLOW2, HIGH);
  digitalWrite(GREEN1, HIGH);
  Serial.println("FATAL ERROR OCCURRED, ABORTING");
  Serial.print("Error: ");
  Serial.println(errorMsg);
  Serial.println("Program terminating. Please restart the board and try again.");
  while (1) {
 
  } // Kill the program. Or at least put it in eternal limbo.
}
