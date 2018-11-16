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
  JsonObject &root = jb.createObject();
  
  JsonArray &lightState = root.createNestedArray("displayState");
  // The number of rows is variable, so use a loop
  for(int i=0; i<NUMROWS; i++){
    lightState.add(currDS.lightState[i]);
  }
  /*
  root["currentCars"] = (currDS.currentCars);
  root["maxCars"] = (currDS.maxCars); // maximum spots
  */
  root["emptySpots"] = currDS.emptySpots;

   root.printTo(Serial);
//  return root;
}

// Decode a JSON-formatted string and update the current displayState to match it
void deserialize(char* json){
  DynamicJsonBuffer jsonBuffer(displayStateSize);
  JsonObject& root = jsonBuffer.parseObject(json);

  JsonArray& displayState = root["displayState"];
  for(int i=0; i<NUMROWS; i++){
    currentDisplay.lightState[i] = displayState[i];  
  }
  /*
  currentDisplay.currentCars = root["currentCars"];
  currentDisplay.maxCars = root["maxCars"];
  */
  currentDisplay.emptySpots = root["emptySpots"];
}
