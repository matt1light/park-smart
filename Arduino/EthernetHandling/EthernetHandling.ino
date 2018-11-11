#include <Ethernet.h>
#include <SPI.h>

// Partially adapted from the WebClient sample program.

// A6:8F:4E:6E:F5:B0; this is a valid but entirely arbitrary MAC address.
// The shield does not come with a preset MAC so one needs to be set.
byte mac[] = {0xA6, 0x8F, 0x4E, 0x6E, 0xF5, 0xB0};

// 10.0.0.43 should be this device's static IP
//byte ip[] = {192, 168, 0, 99};
IPAddress ip(10,0,0,43);

// Define a server to connect to by IP address
// 10.0.0.41 should be the Server Pi
IPAddress server(10,0,0,41);

// Declare the client
EthernetClient client;

void setup() {
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

void loop() {
  while(1){}; // Do nothing for now
}
