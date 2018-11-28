#include <Ethernet.h>
#include <SPI.h>

// Partially adapted from the WebClient sample program.

#define NUMROWS 3




#define TARGETPATH "/displayState/?output="

// Connection status codes
#define CONNECTION_SUCCESS 1
#define CONNECTION_FAILURE_GENERIC 0
#define CONNECTION_FAILURE_TIMEOUT -1
#define CONNECTION_FAILURE_INVALID_SERVER -2
#define CONNECTION_FAILURE_TRUNCATED -3
#define CONNECTION_FAILURE_INVALID_RESPONSE -4

#define MAXCONNECTIONATTEMPTS 3


// A6:8F:4E:6E:F5:B0; this is a valid but entirely arbitrary MAC address.
// The shield does not come with a preset MAC so one needs to be set.
byte mac[] = {0xA6, 0x8F, 0x4E, 0x6E, 0xF5, 0xB0};

// 10.0.0.43 should be this device's static IP
#define CLIENTIP 10,0,0,43
IPAddress ip(10,0,0,43);
int port = 8000;

// Define a server to connect to by IP address
// 10.0.0.41 should be the Server Pi
//#define SERVERIP 10,0,0,41
IPAddress server(10,0,0,41);

// Declare the client
EthernetClient client;




//struct DisplayState currentDisplay;

int outputID = 1;






void setupEthernet(void){
  // Set up the Arduino with a static IP.
  // Note that DHCP is possible, but not used for this project,
  // and bloats the sketch size significantly.
  #if DEBUGNETWORK
  Serial.println("Attempting to initialize Ethernet with static IP");
  #endif
  Ethernet.begin(mac, ip);
  delay(2000); 
  #if DEBUGNETWORK
  Serial.print("IP address is ");
  Serial.println(Ethernet.localIP()); 
  #endif
}

// Attempt to initialize the connection between this machine and the server.
int attemptConnection(){
  for(int i=0; i<MAXCONNECTIONATTEMPTS; i++){
    // client.connect() returns an error code
    // 1=success, -1=timeout, -2=invalid server, -3=truncated, -4=invalid response
    // 0=something, but this case is undocumented. Treated here as a generic failure.
    int connectionStatus = client.connect(server, port);
    
    #if DEBUGNETWORK
    Serial.print("Attempting to connect to ");
    Serial.println(client.remoteIP());
    #endif
    
    if(connectionStatus == CONNECTION_SUCCESS){
      #if DEBUGNETWORK
      Serial.print("Connected successfully to ");
      Serial.print(client.remoteIP());
      Serial.print(" on port ");
      Serial.println(port);
      #endif
    
      return 1; // Connection succeeded, break
    }
    
    else{
      #if DEBUGNETWORK
      Serial.print("Failed to connect on port ");
      Serial.println(port);
      Serial.print("Error code: ");
      Serial.println(connectionStatus);
      #endif
    }
  }
  // Connection did not succeed within the allowed number of attempts
  return -1; 
}


// Perform a GET request for a given endpoint
// TODO: Make this take a char* array?
void makeGetRequest(void){
  #if DEBUGNETWORK
  Serial.println("Trying a Get request");
  #endif
  // GET /displayState/?output=outputID HTTP/1.1
  client.print("GET ");
  client.print(TARGETPATH);
  client.print(outputID);
  client.println(" HTTP/1.1");
  client.println("Host: 10.0.0.41:8000");
  client.println("Cache-Control: no-cache");
  client.println();
  
}

// Read some bytes from the incoming stream.
// If there is an incoming message, save it.
int readIncomingBytes(void){
  // Check how much data is incoming
  int len = client.available();
  
  // Only do anything if there is data to process
  if(len > 0){
     client.read(messageBuffer, len);
     #if DEBUGNETWORK
     Serial.write(messageBuffer, len);
     #endif
    }
  
  else{
   // Do nothing
  }
}
