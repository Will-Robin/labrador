int LED = 13; // LED to flash when drop is detected
int isObstaclePin = 2;  // input pin
int isObstacle = HIGH;  // HIGH mean no drop
int waitTime = 1000; // Minimum time to wait between drops
int baudRate = 9600;

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(isObstaclePin, INPUT);
  Serial.begin(baudRate);
  digitalWrite(LED, LOW);
}

void loop() {
  isObstacle = digitalRead(isObstaclePin);
  if (isObstacle == HIGH) // drop detected
  {
    Serial.println(1);
    digitalWrite(LED, HIGH);
    delay(waitTime); // Wait before next trigger
  } else if (isObstacle == LOW) {
    Serial.println(0);
    digitalWrite(LED, LOW);
  }
}