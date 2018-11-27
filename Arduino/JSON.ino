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

   root.printTo(Serial);
   //return root;
}

// TODO: Account for error messages in JSON objects

// Decode a JSON-formatted string and update the current displayState to match it
void deserialize(char* json){
  // Create a buffer to store the JSON object in
  DynamicJsonBuffer jsonBuffer(displayStateSize);
  JsonObject& root = jsonBuffer.parseObject(json);

  JsonArray& displayState = root["displayState"];
  for(int i=0; i<NUMROWS; i++){
    currentDisplay.lightState[i] = displayState[i];  
  }
  currentDisplay.emptySpots = root["emptySpots"];
}

int extractJSONFromMessage(void){
  int startPos = findChar('{');
  int endPos = findChar('}');
  int len = endPos - startPos + 1;

  memcpy(jsonBuffer, &messageBuffer[startPos], len);
  Serial.println("JSON message: ");
  Serial.write(jsonBuffer);
  
}

int findChar(char target){
  int index = 0;
  
  while(1){
    if(index >= MSGBUFFERSIZE-1){ // Reached the end of the buffer; > for sanity
      Serial.println("Nothing found");
      return -1; // Nothing was found
    }
    else if(messageBuffer[index] == target){
      Serial.print("Start of JSON object found at index ");
      Serial.println(index);
      return index;
    }
    index++;
  }
}
