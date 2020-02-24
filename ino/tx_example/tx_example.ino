
void setup() {
  Serial.begin(115200);
}

void loop() {
  static int counter = 0;

  Serial.print('#,');
  Serial.print(analogRead(A14));
  Serial.print(',');
  Serial.print(counter + 1);
  Serial.print(',');
  Serial.print(counter + 2);
  Serial.print(',');
  Serial.print('\n');

  counter++;

  delay(50);
}