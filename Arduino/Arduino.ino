#include <timer.h>
#include <Event.h>
#include <ArduinoJson.h>
#include <LiquidCrystal.h>

//----------------------------------------------------------------------------
// CONFIGURATION
//----------------------------------------------------------------------------

#define DEBUGHARDWARE 0 // Set to 1 to have hardware and displayState information printed to serial

#define DEBUGNETWORK 1 // Set to 1 to have networking information printed to serial

#define DEBUGJSON 1// Set to 1 to have JSON encoding/decoding information printed to serial

#define WAIT 2000 //delay frequency of ultrasonic sensor readings in milliseconds
#define REQUESTDELAY 20000 // Time between requests made to the server. Does not account for processing time
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

char dTrig = 5;//Max triggering detected distance

bool car; //state variable if car is at parking lot entrance or not


//LCD Pin Setup
#define rs 4
#define en 5
#define d4 6
#define d5 7
#define d6 8
#define d7 9

//LCD Setup
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

////LED setup
#define YELLOW0 A0
#define GREEN0 A1
#define YELLOW1 A2
#define GREEN1 A3

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
  short emptySpots;
};

DisplayState currentDisplay;

short numCars = 0;
// on timer finish decrease exit
auto timer= timer_create_default();

//----------------------------------------------------------------------------
// STATE VARIABLES
//----------------------------------------------------------------------------


//Arrray for Lights
char yellowLED[NUMROWS] = {YELLOW0, YELLOW1};
char greenLED[NUMROWS] = {GREEN0, GREEN1};

bool carFlag = false;
short extraCars = 0;
const long ENTRANCE_DELAY = (long)1000 * 60 * 0.1; // 1 second * 1 minute * 2 = 2 minutes

//testing bool
bool isTesting = false;

// Buffer that incoming data will be written to.
// This will be read from when deserializing, or written to when serializing.
#define MSGBUFFERSIZE 300
char messageBuffer[MSGBUFFERSIZE];

#define JSONBUFFERSIZE 100
//char jsonBuffer[JSONBUFFERSIZE];
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

  pinMode(YELLOW0, OUTPUT);
  pinMode(GREEN0, OUTPUT);
  pinMode(YELLOW1, OUTPUT);
  pinMode(GREEN1, OUTPUT);


  initDisplayState();

  setupEthernet();
  int connected = attemptConnection();
  if (connected == CONNECTION_SUCCESS) {
    makeGetRequest();
  }
  else {
    Serial.println("Could not connect to the server");
    //throwFatalError("Could not connect to the server");
  }

}

void loop()
{ 
  if (bytesAvailable()) {
    Serial.println("bytes available");
    readIncomingBytes();
    delay(1000);
    extractJSONFromMessage();
    delay(1000);
    deserialize(messageBuffer);
  }
  
  if (loops >= LOOPITERATIONS) {
    loops = 0;
    // It's time to make a request from the server
    // Close the previous connection
    closeConnection();
    // Make a new connection
    attemptConnection();
    // Make the request
    makeGetRequest();
  }

  

  checkForCars();

  //delay for the car test
  delay(WAIT); //using predetermined time, in milliseconds, delay after each measurement and return
  loops++;
}

//----------------------------------------------------------------------------
// OTHER METHODS
//----------------------------------------------------------------------------

void checkForCars(){
  car = isCar(); //test if car is there or not

  if (car && !carFlag) //If there is a car and there was not one before
  {   
    carFlag = true; //Register that there is a car currently here
    carEntersLot(); 
    
    #if DEBUGHARDWARE
    Serial.println("There is a car");
    Serial.println(carFlag);
    #endif

  }
  else if (!car) //If there is not a car
  {
    #if DEBUGHARDWARE
    Serial.println("There is not a car");
    Serial.println(carFlag);
    #endif
    carFlag = false;
  }

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
     // Serial.print("Sensor 1: ");
      //Serial.println(d1);
      //Serial.print("Sensor 2: ");
      //Serial.println(d2);
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
  lcd.setCursor(0,0);
  //lcd.print("Available spots:");
  lcd.print("Extra cars:");
  lcd.setCursor(0,1);
  
  //Display the number of available cars
  //int availableSpots = getAvailableSpots();
  int availableSpots = 33;
  
  //lcd.print(availableSpots);
  Serial.println(extraCars);

  lcd.print(extraCars);
  /*

  Serial.print("Available spots:");
  Serial.println(availableSpots);
  Serial.print("Extra Cars:");
  Serial.println(extraCars);
  Serial.println(availableSpots - extraCars);

 */

}

int getAvailableSpots() {
  int availableSpots = currentDisplay.emptySpots;
  if ((availableSpots - extraCars) < 0) {
    return 0;
  }
  else {
    return availableSpots - extraCars;
  }
}

void carEntersLot(){
  extraCars += 1;
  updateLCD();
  // starts 2 minute timer
  timer.tick();
  timer.in(ENTRANCE_DELAY, removeExtraCar);
}

void removeExtraCar()
{
  extraCars -= 1;
  updateLCD();
}

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
    currentDisplay.lightState[i] = YELLOW;
  }
  */
 
  
  currentDisplay.emptySpots = 9999;
  updateLightState();
  updateLCD();

  Serial.println("FATAL ERROR OCCURRED, ABORTING");
  Serial.print("Error: ");
  Serial.println(errorMsg);
  Serial.println("Program terminating. Please restart the board and try again.");

  while (1) {
 
  } // Kill the program. Or at least put it in eternal limbo.
}
