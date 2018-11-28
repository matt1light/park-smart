#include <ArduinoJson.h>

// Size of the displayState JSON buffer, used when serializing/deserializing.
// Derivation: there are as many ints in the lightState array as there are rows being tracked,
// and as 2 ints in the screenState array: current and max cars.
// Furthermore, there are 2 pointers, one for each of the arrays.
const int displayStateSize = (JSON_OBJECT_SIZE(2) + // current and max cars
                             JSON_ARRAY_SIZE(NUMROWS) + // lightState array
                             JSON_OBJECT_SIZE(1)); // pointer to lightState array

                         
JsonObject serialize(struct DisplayState currDS){
  // Create a buffer to store the JSON object in
  DynamicJsonBuffer jb(displayStateSize);
  // Create the JsonObject that elements will be added to
  JsonObject &root = jb.createObject();
  
  JsonArray &lightState = root.createNestedArray("displayState");
  // The number of rows is variable, so use a loop
  for(int i=0; i<NUMROWS; i++){
    lightState.add(currDS.lightState[i]);
  }
  root["emptySpots"] = currDS.emptySpots;
  #if DEBUGJSON  
  root.printTo(Serial);
  #endif
  //return root;
}

// TODO: Account for error messages in JSON objects

// Decode a JSON-formatted string and update the current displayState to match it
void deserialize(char* json){
  // Create a buffer to store the JSON object in
  DynamicJsonBuffer jsonBuffer(displayStateSize);
  JsonObject& root = jsonBuffer.parseObject(json);

  if(root.containsKey("error")){ // There was an error from the server
    const char* error = root.get<const char*> ("error");
    // Errors should be printed regardless of debug settings
    Serial.print("Encountered an error: ");
    Serial.print(error);
  }
  else {
    JsonArray& displayState = root["displayState"];
    for(int i=0; i<NUMROWS; i++){
      currentDisplay.lightState[i] = displayState[i];  
    }
    currentDisplay.emptySpots = root["emptySpots"];

    updateLightState();
    updateLCD(currentDisplay.emptySpots);
  }
}

int extractJSONFromMessage(void){
  int startPos = findChar('{');
  int endPos = findChar('}');
  int len = endPos - startPos + 1;

  memcpy(jsonBuffer, &messageBuffer[startPos], len);
  
  #if DEBUGJSON
  Serial.println("JSON message: ");
  Serial.write(jsonBuffer);
  Serial.println();
  #endif
}

int extractErrorFromMessage(void){
  // The HTTP response header always starts with the protocol version, a space, then the error code.
  int startPos = findChar(" ") + 1; // Look for the first space; the next character is the first digit of the error code
  int len = 3;

  memcpy(errorBuffer, &messageBuffer[startPos], len);
}

// Find the first instance of a given character in the messageBuffer, and return its position in the buffer.
// The position is zero-indexed; if the character is the first in the array, its position is 0.
int findChar(char target){
  int index = 0;
  
  while(1){
    if(index >= MSGBUFFERSIZE-1){ // Reached the end of the buffer; > for sanity
      #if DEBUGJSON
      Serial.println("Nothing found");
      #endif
      return -1; // Nothing was found
    }
    
    else if(messageBuffer[index] == target){
      #if DEBUGJSON
      Serial.print("Start of JSON object found at index ");
      Serial.println(index);
      #endif
      return index;
    }
    index++;
  }
}

// Convert a 3-digit HTTP error code stored in a char array into an int
int errorToInt(void){
  return (errorBuffer[0]*100 + errorBuffer[1]*10 + errorBuffer[2]*1);
}
