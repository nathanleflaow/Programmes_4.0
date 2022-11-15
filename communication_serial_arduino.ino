int x;
const int PorteAv = 2;
const int PorteAr = 4;
void setup() {
 pinMode(PorteAv,OUTPUT);
 pinMode(PorteAr,OUTPUT);
 Serial.begin(9600);
 Serial.setTimeout(1);
 digitalWrite(PorteAv,HIGH);
 digitalWrite(PorteAr,HIGH);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 if (x==1){
  digitalWrite(PorteAv,LOW);
  }
 else if (x==2){
  digitalWrite(PorteAr,LOW);
  }
  
  delay(1000);
  digitalWrite(PorteAv,HIGH);
  digitalWrite(PorteAr,HIGH);
}