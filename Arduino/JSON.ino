// Size of the displayState JSON buffer, used when serializing/deserializing.
// Derivation: there are as many ints in the lightState array as there are rows being tracked,
// and as 2 ints in the screenState array: current and max cars.
// Furthermore, there are 2 pointers, one for each of the arrays.
const int displayStateSize = (JSON_OBJECT_SIZE(2) + // current and max cars
                             JSON_ARRAY_SIZE(NUMROWS) + // lightState array
                             JSON_OBJECT_SIZE(1)); // pointer to lightState array


// Decode a JSON-formatted string and update the current displayState to match it
void deserialize(char* json){
  // Create a buffer to store the JSON object in
  DynamicJsonBuffer buf(displayStateSize);
  JsonObject& root = buf.parseObject(json);

  if(root.containsKey("error")){ // There was an error from the server
    const char* error = root.get<const char*> ("error");
    // Errors should be printed regardless of debug settings
    
    Serial.print("HTTP error code: ");
    extractErrorFromMessage();
    Serial.println(errorToInt());

    Serial.print("Server error message: ");
    Serial.println(error);
    
  }

  else { // The request is valid

    root.prettyPrintTo(Serial);
    
    updateLightState();
    updateLCD();
  }
}

// Find the JSON in the body of an HTTP message stored in messageBuffer, and save it to jsonBuffer.
int extractJSONFromMessage(void){
  short startPos = findChar('{');
  short endPos = findLastChar('}');
  short len = (endPos - startPos) + 1;

  memcpy(jsonBuffer, &messageBuffer[startPos], len);
  
  #if DEBUGJSON
  Serial.println("JSON message: ");
  Serial.write(jsonBuffer);
  Serial.println();
  #endif
  
}

// Find the error code from an HTTP message stored in messageBuffer, and save it to errorBuffer.
int extractErrorFromMessage(void){
  // The HTTP response header always starts with the protocol version, a space, then the error code.
  int startPos = findChar(' ') + 1; // Look for the first space; the next character is the first digit of the error code
  int len = 3;

  memcpy(errorBuffer, &messageBuffer[startPos], len);
  Serial.println("ERROR:");
  Serial.write(errorBuffer, 3);
  Serial.println();
}


// Find the first instance of a given character in the messageBuffer, and return its position in the buffer.
// The position is zero-indexed; if the character is the first in the array, its position is 0.
short findChar(char target){
  short index = 0;
  
  while(1){
    if(index >= MSGBUFFERSIZE){
      return -1; // Target character was not found within the buffer
    }
    else if(messageBuffer[index] == target){
      return index;
    }
    index++;
  }
}

short findLastChar(char target){
  short index = 0;
  short pos = -1;

  while(index >= MSGBUFFERSIZE){
    if(messageBuffer[index] == target){
      pos = index;
    }
    index++;
  }
  return pos;
}

// Convert a 3-digit HTTP error code stored in a char array into an int.
short errorToInt(void){
  return (100* charToDigit(errorBuffer[0]) + 10*charToDigit(errorBuffer[1]) + charToDigit(errorBuffer[2]));
}

// Convert a char encoded as an ASCII value into its numerical value.
// i.e. '3' will be converted to 0x03.
char charToDigit(char in){
  if(in >= 48 && in <= 57){
    return in - '0'; // 0 is the first digit in the ASCII table
  }
  else{
    Serial.print("Character is not a digit");
    return -1;
  }
}
