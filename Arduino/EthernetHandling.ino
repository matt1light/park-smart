#include <Ethernet.h>
#include <SPI.h>

// Partially adapted from the WebClient sample program.
#define NUMROWS 3
#define MAXBUFFSIZE 80

struct DisplayState{
  int lightState[NUMROWS];
  /*
  int currentCars;
  int maxCars;
  */
  int emptySpots;
};

// ------------------------------------------------------------------------------
// WIRELESS SETUP
// ------------------------------------------------------------------------------
// A6:8F:4E:6E:F5:B0; this is a valid but entirely arbitrary MAC address.
// The shield does not come with a preset MAC so one needs to be set.
byte mac[] = {0xA6, 0x8F, 0x4E, 0x6E, 0xF5, 0xB0};

// 10.0.0.43 should be this device's static IP
IPAddress ip(10,0,0,43);
int port = 8000;

// Define a server to connect to by IP address
// 10.0.0.41 should be the Server Pi
//IPAddress server(10,0,0,41);
IPAddress server(172,17,150,223);

// Declare the client
EthernetClient client;

struct DisplayState currentDisplay;
int outputID = 1;

char incomingBuffer[800]; // Size is currently arbitrary
int bufferIndex = 0;

// Initialize the connection between this machine and the server.
void setupEthernet(void){
  Serial.begin(9600);
  while(!Serial){}; // Wait until the serial port is able to connect.
  delay(1000);

  // Set up the Arduino with a static IP.
  // Note that DHCP is possible, but not used for this project,
  // and bloats the sketch size significantly.
  Serial.println("Attempting to initialize Ethernet with static IP");
  Ethernet.begin(mac, ip);
  Serial.print("IP address is ");
  Serial.println(Ethernet.localIP()); 

  // client.connect() returns an error code
  // 1=success, -1=timeout, -2=invalid server, -3=truncated, -4=invalid response
  // 0=something, but this case is undocumented.
  int connectionStatus = client.connect(server, port);
  if(connectionStatus == 1){
    Serial.print("Connected successfully to ");
    Serial.print(client.remoteIP());
    Serial.print(" on port ");
    Serial.println(port);
  }
  else{
    Serial.print("Failed to connect on port ");
    Serial.println(port);
    Serial.print("Error code: ");
    Serial.println(connectionStatus);

    // TODO: Break this up into a function that returns the error code
  } 
}

// Perform a GET request for a given endpoint
// displayState/?=outputID
//void makeGetRequest(char* target){
void makeGetRequest(void){
  Serial.println("Trying a Get request");
  client.print("GET displayState/?=");
  client.print(outputID);
  client.println(" HTTP/1.1");
  client.println("Host: 10.0.0.41");
  client.println("Connection: close");
  client.println(); // Required newline to end the request
  Serial.println("Get request completed");
}

// Read some bytes from the incoming stream
void readIncomingBytes(void){
  // Check how much data is incoming
  int len = client.available();
  // Only do anything if there is data to process
  if(len > 0){
    // Cap the amount of data to read at once.
    // TODO: Find out why? This is code from the sample
    // Possibly packet size
    if (len > MAXBUFFSIZE){
      len = MAXBUFFSIZE;
    }
    readNBytes(len);
  }
}

// Read n bytes of data from the incoming buffer and print them to serial.
void readNBytes(int n){
  byte buffer[n];
  client.read(buffer, n);
  Serial.write(buffer, n);
  //memcpy(&incomingBuffer[bufferIndex], buffer, n*sizeof(byte));
  //Serial.write(incomingBuffer);
}

// Create dummy values for the current displayState
void initDisplayState(){
  // NB: I don't know if we've altered the details of displaystate?
  // I'm going off the latest version of the class diagram.
  /*
  currentDisplay.lightState[0] = 1;
  currentDisplay.lightState[1] = 2;
  currentDisplay.lightState[2] = 1;
  */
  for(int i=0; i<NUMROWS; i++){
    currentDisplay.lightState[i] = 0;
  }
  /*
  currentDisplay.currentCars = 0;
  currentDisplay.maxCars = 6;
  */
  currentDisplay.emptySpots = 9999;
}

//void setup(){}
//void loop(){}
