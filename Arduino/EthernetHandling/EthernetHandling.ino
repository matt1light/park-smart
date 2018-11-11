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

// Define a server to connect to by IP address
// 10.0.0.41 should be the Server Pi
//IPAddress server(10,0,0,41);
IPAddress server(169,254,45,60);

// Declare the client
EthernetClient client;

void startEthernet(void){
Serial.begin(9600);
  while(!Serial){}; // Wait until the serial port is able to connect.

  // Set up the Arduino with a static IP
  Serial.println("Attempting to initialize Ethernet with static IP");
  Ethernet.begin(mac, ip);
  Serial.print("IP address is ");
  Serial.println(Ethernet.localIP()); 

  // TODO: Work in lab with linux router and connect to a Pi or something
  if(client.connect(server, 80)){
    Serial.print("Connected successfully to ");
    Serial.print(client.remoteIP());

  }
  else{
    Serial.println("Failed to connect");
  }
}

struct DisplayState sendDisplayState(int displaySystemID){
  // Dummy function for now
  // NB: I don't know if we've altered the details of displaystate?
  // I'm going off the latest version of the class diagram.
  struct DisplayState currentDisplay;
  int currLS[] = {1,2,3};
  int currSS[] = {44,45};
  // memcpy copies data from a source into a memory block
  memcpy(currentDisplay.lightState, currLS, sizeof currLS);
  memcpy(currentDisplay.screenState, currSS, sizeof currSS);
  return currentDisplay;
}

void setup(){}
void loop(){}
