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
  #define NUMROWS 2
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
#define OFF 3
#define GREEN 1
#define YELLOW 2

// Struct to represent the system's display state
struct DisplayState {
  char lightState[NUMROWS];
  short emptySpots;
};

// Declare our DisplayState
DisplayState currentDisplay;


// Create a timer object
auto timer= timer_create_default();

//----------------------------------------------------------------------------
// STATE VARIABLES
//----------------------------------------------------------------------------


//Arrray for Lights
char yellowLED[NUMROWS] = {YELLOW0, YELLOW1};
char greenLED[NUMROWS] = {GREEN0, GREEN1};

bool carFlag = false;
short extraCars = 0;
const long ENTRANCE_DELAY = (long)1000 * 20; // 1 second * 1 minute * 2 = 20 seconds

//testing bool
bool isTesting = false;

// Buffer that incoming data will be written to.
// This will be read from when deserializing, or written to when serializing.
#define MSGBUFFERSIZE 300
char messageBuffer[MSGBUFFERSIZE];

#define JSONBUFFERSIZE 100
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

  // Set the LED pins to operate as outputs
  pinMode(YELLOW0, OUTPUT);
  pinMode(GREEN0, OUTPUT);
  pinMode(YELLOW1, OUTPUT);
  pinMode(GREEN1, OUTPUT);

  // Fill the display state with placeholder values until
  // the first request is unpacked.
  initDisplayState();

  // Setup the Ethernet shield
  setupEthernet();

  // Attempt to make an inital connection to the server.
  // If successful, make a GET request to populate the
  // display state.
  int connected = attemptConnection();
  if (connected == CONNECTION_SUCCESS) {
    //makeGetRequest();
  }
  else {
    Serial.println("Could not connect to the server");
  }
}

void loop()
{ 
  // If there is incoming data:
  // Read it,
  // Separate the JSON body from the header,
  // Parse the JSON and update the display state.
  if (bytesAvailable()) {
    readIncomingBytes();
    delay(1000);
    extractJSONFromMessage();
    delay(1000);
    deserialize(messageBuffer);
  }

  // If a set interval has expired, make a new GET request
  // to the server.
  // NB: This is not done with a timer object, in order
  // to the very sparse memory available.
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

  // Check the ultrasonic sensors for whether there is a car present at the entrance.
  checkForCars();

  // Increment the timer
  timer.tick();

  
  //using predetermined time, in milliseconds, delay after each measurement and return
  delay(WAIT); 
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

// Test whether a car is present between the two ultrasonic sensors.
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

// Change the output of the LEDs for a given row.
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

// Update the LEDs for all rows in the lot, based on the current lightState.
void updateLightState()
{
  for (int i = 0; i < NUMROWS; i++)
  {
    setRowColour(i, currentDisplay.lightState[i]);
  }
}

// Refresh the LCD to reflect an update in the number of available spots.
void updateLCD()
{
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Available spots:");
  lcd.setCursor(0,1);
  
  // Display the number of available cars
  int availableSpots = getAvailableSpots();
  
  lcd.print(availableSpots);
}

// Determine the number of free spots available.
// For this purpose, the number of cars that have entered the lot but are
// "floating", having not yet parked, count as having occupied a spot.
int getAvailableSpots() {
  int availableSpots = currentDisplay.emptySpots;
  if ((availableSpots - extraCars) < 0) {
    return 0;
  }
  else {
    return availableSpots - extraCars;
  }
}

// A car has entered the lot; increment the tally of "floating" extra
// cars, and update the LCD accordingly.
void carEntersLot(){
  extraCars += 1;
  updateLCD();
  // starts 2 minute timer
  timer.in(ENTRANCE_DELAY, removeExtraCar);
}

// The timer has elapsed, so decrement the tally of "floating" cars
// and update the LCD accordingly
void removeExtraCar()
{
  Serial.println("Removing car");
  extraCars -= 1;
  updateLCD();
}

// Create dummy values for the current displayState
void initDisplayState() {
  for (int i = 0; i < NUMROWS; i++) {
    currentDisplay.lightState[i] = 2;
  }
  currentDisplay.emptySpots = 999;
  updateLCD();
  updateLightState();
}

// Print the current LightState to serial for debugging.
void printLightState(){
  for(int i=0; i<NUMROWS; i++){
    Serial.print("State of row ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(digitToChar(currentDisplay.lightState[i]));
  }
}
