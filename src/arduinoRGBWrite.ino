
//Variable for rgb state
char rgbState = 'p';


void setup() {
Serial.begin(9600); // set the baud rate


//PinMode
pinMode(7,INPUT);

pinMode(9,OUTPUT);
pinMode(10,OUTPUT);
pinMode(11,OUTPUT);

}

void loop() {

  //Increment the pulse variable

  
  //If serial is avilable
   if (!Serial.available()) {
    
       //do list of commands
       Serial.println(digitalRead(7)); // send the data back in a new line so that it is not all one long line
       
  
       
  }
  //If serial is not avilable
  else {
    
       //do list of commands
       rgbState = Serial.read();
       
      
  }
  
  //If red state
   if (rgbState == 'r') {
    
       //Write to the pins
       digitalWrite(9,HIGH);
       digitalWrite(10,LOW);
       digitalWrite(11,LOW);
  }
  //If GREEN state
   if (rgbState == 'g') {
    
       //Write to the pins
       digitalWrite(9,LOW);
       digitalWrite(10,HIGH);
       digitalWrite(11,LOW);
  }
  //If BLUE state
   if (rgbState == 'b') {
    
       //Write to the pins
       digitalWrite(9,LOW);
       digitalWrite(10,LOW);
       digitalWrite(11,HIGH);
  }
   //If PURPLE state
   if (rgbState == 'p') {
    
       //Write to the pins
       analogWrite(9,35);
       digitalWrite(10,LOW);
       analogWrite(11,15);
  }
   //If YELLOW state
   if (rgbState == 'y') {
    
       //Write to the pins
       analogWrite(9,HIGH);
       analogWrite(10,25);
       digitalWrite(11,LOW);
  }
  //If AQUA state
   if (rgbState == 'a') {
    
       //Write to the pins
       digitalWrite(9,LOW);
       analogWrite(10,25);
       analogWrite(11,25);
  }
  
  delay(1); // delay for 1/10 of a second

}
