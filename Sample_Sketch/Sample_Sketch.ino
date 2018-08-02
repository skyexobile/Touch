
void setup() {
  Serial.begin(115200); 
}

void loop() {
  
  // put your main code here, to run repeatedly:
  while(!Serial.available()){
    Serial.println(1);
  }
   char input_value = Serial.read();
     Serial.println(2);
   

}
