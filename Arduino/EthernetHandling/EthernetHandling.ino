#include <Ethernet.h>
#include <SPI.h>

// Partially adapted from the WebClient sample program.

// A6:8F:4E:6E:F5:B0; this is a valid but entirely arbitrary MAC address.
byte mac[] = {0xA6, 0x8F, 0x4E, 0x6E, 0xF5, 0xB0};

// 192.168.0.99; another arbitrary static IP
// TODO: Work out our static IP assignments
byte ip[] = {192, 168, 0, 99};

// Define a server to connect to by IP address
IPAddress server(169,254,45,60);

// Declare the client
EthernetClient client;

void setup() {
  Serial.begin(9600);
  while(!Serial){}; // Wait until the serial port is able to connect.

  // 
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
