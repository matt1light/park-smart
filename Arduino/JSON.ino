// Size of the displayState JSON buffer, used when serializing/deserializing.
// Derivation: there are as many ints in the lightState array as there are rows being tracked,
// and as 2 ints in the screenState array: current and max cars.
// Furthermore, there are 2 pointers, one for each of the arrays.
const int displayStateSize = (JSON_OBJECT_SIZE(2) + // pointers
                             JSON_ARRAY_SIZE(NUMROWS) + // lightState array
                             JSON_ARRAY_SIZE(2)); // signState array
                             
void serialize(struct DisplayState currDS){
  DynamicJsonBuffer jb(displayStateSize);
  JsonObject &root = jb.createObject();
  
  JsonArray &lightState = root.createNestedArray("displayState");
  for(int i=0; i<NUMROWS; i++){
    lightState.add(currDS.lightState[i]);
  }

  JsonArray &screenState = root.createNestedArray("screenState");
  screenState.add(currDS.screenState[0]); // free spots
  screenState.add(currDS.screenState[1]); // maximum spots

  root.printTo(Serial);
}

void deserialize(char* json){
  DynamicJsonBuffer jsonBuffer(displayStateSize);
  JsonObject& root = jsonBuffer.parseObject(json);

  JsonArray& displayState = root["displayState"];
  for(int i=0; i<NUMROWS; i++){
    currentDisplay.lightState[i] = displayState[i];  
  }

  JsonArray& screenState = root["screenState"];
  currentDisplay.screenState[0] = screenState[0];
  currentDisplay.screenState[0] = screenState[1];
}
