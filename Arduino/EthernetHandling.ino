#include <Ethernet.h>
#include <SPI.h>
// Partially adapted from the WebClient sample program.

struct DisplayState{
  int lightState[];
  int screenState[];
};
// A6:8F:4E:6E:F5:B0; this is a valid but entirely arbitrary MAC address.
// The shield does not come with a preset MAC so one needs to be set.
byte mac[] = {0xA6, 0x8F, 0x4E, 0x6E, 0xF5, 0xB0};

// 10.0.0.43 should be this device's static IP
IPAddress ip(10,0,0,43);

int port = 8000;

// Define a server to connect to by IP address
// 10.0.0.41 should be the Server Pi
IPAddress server(10,0,0,41);
//IPAddress server(169,254,45,60);

// Declare the client
EthernetClient client;

unsigned long byteCount = 0;

void setupEthernet(void){
  Serial.begin(9600);
  while(!Serial){}; // Wait until the serial port is able to connect.
  delay(1000);

  // Set up the Arduino with a static IP
  Serial.println("Attempting to initialize Ethernet with static IP");
  Ethernet.begin(mac, ip);
  Serial.print("IP address is ");
  Serial.println(Ethernet.localIP()); 

 
  int connectionStatus = 999;
  connectionStatus = client.connect(server, 8000);
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
  }

  sampleGetRequest();

  
}

void sampleGetRequest(void){
  Serial.println("Trying a Get request");
  client.println("GET index.html HTTP/1.1");
  client.println("Host: 10.0.0.41");
  client.println("Connection: close");
  client.println();
}

void readIncomingBytes(void){
  Serial.println("Checking buffer");
  int len = client.available();
  if (len > 0) {
    byte buffer[80];
    if (len > 80) len = 80;
    client.read(buffer, len);
    Serial.write(buffer, len); // show in the serial monitor (slows some boards)
    
    byteCount = byteCount + len; 
  }
}

struct DisplayState sendDisplayState(int displaySystemID){
  // Dummy function for now
  // NB: I don't know if we've altered the details of displaystate?
  // I'm going off the latest version of the class diagram.
  //foobar
  struct DisplayState currentDisplay;
  int currLS[] = {1,2,3};
  int currSS[] = {44,45};
  // memcpy copies data from a source into a memory block
  memcpy(currentDisplay.lightState, currLS, sizeof currLS);
  memcpy(currentDisplay.screenState, currSS, sizeof currSS);
  return currentDisplay;
}

//void setup(){}
//void loop(){}
