#include <Ethernet.h>
#include <SPI.h>

// Partially adapted from the WebClient sample program.

#define NUMROWS 3
// The number of bytes to read at once
#define PACKETSIZE 128

#define MSGBUFFERSIZE 640

#define TARGETPATH "/displayState/?output="

// Connection status codes
#define CONNECTION_SUCCESS 1
#define CONNECTION_FAILURE_GENERIC 0
#define CONNECTION_FAILURE_TIMEOUT -1
#define CONNECTION_FAILURE_INVALID_SERVER -2
#define CONNECTION_FAILURE_TRUNCATED -3
#define CONNECTION_FAILURE_INVALID_RESPONSE -4



// ------------------------------------------------------------------------------
// WIRELESS SETUP
// ------------------------------------------------------------------------------
// A6:8F:4E:6E:F5:B0; this is a valid but entirely arbitrary MAC address.
// The shield does not come with a preset MAC so one needs to be set.
byte mac[] = {0xA6, 0x8F, 0x4E, 0x6E, 0xF5, 0xB0};

// 10.0.0.43 should be this device's static IP
#define CLIENTIP 10,0,0,43
IPAddress ip(10,0,0,43);
int port = 8000;

// Define a server to connect to by IP address
// 10.0.0.41 should be the Server Pi
#define SERVERIP 10,0,0,41
IPAddress server(SERVERIP);

// Declare the client
EthernetClient client;


struct DisplayState{
  char lightState[NUMROWS];
  int emptySpots;
};

struct DisplayState currentDisplay;

int outputID = 1;

// Buffer that incoming data will be written to
// This will be read from when deserializing, or written to when serializing
// NB: Work in progress
byte messageBuffer[MSGBUFFERSIZE]; // Size is currently arbitrary

// Initialize the connection between this machine and the server.
int setupEthernet(void){
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
  Serial.print("Attempting to connect to ");
  Serial.print(client.remoteIP());
  if(connectionStatus == CONNECTION_SUCCESS){
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
  } 
  return connectionStatus;
}

// Perform a GET request for a given endpoint
// TODO: Make this take a char* array?
void makeGetRequest(void){
  Serial.println("Trying a Get request");
  // GET /displayState/?output=outputID HTTP/1.1
  client.print("GET ");
  client.print(TARGETPATH);
  client.print(outputID);
  client.println(" HTTP/1.1");
  client.println("Host: 10.0.0.41:8000");
  client.println("Cache-Control: no-cache");
  client.println();
  
}

// Read some bytes from the incoming stream
void readIncomingBytes(void){
  // Check how much data is incoming
  int len = client.available();
  
  // Only do anything if there is data to process
  if(len > 0){
     readNBytes(PACKETSIZE);
    }
  
  else{
   // Do nothing
  }
}


// Read n bytes of data from the incoming buffer and print them to serial.
void readNBytes(int n){
  byte buffer[n];
  client.read(buffer, n);
  Serial.write(buffer, n);
}


// Create dummy values for the current displayState
void initDisplayState(){
  for(int i=0; i<NUMROWS; i++){
    currentDisplay.lightState[i] = 0;
  }
  currentDisplay.emptySpots = 9999;
}
