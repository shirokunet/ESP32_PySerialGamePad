#include "esp32_serial_twoways.h"

/* macro */
#define TX_SIZE 3
#define RX_SIZE 6

/* instance */
ESP32_SERIALTW serial_parse = ESP32_SERIALTW(TX_SIZE, RX_SIZE);

/* grobal */
int _tx_data[TX_SIZE];
int _rx_data[RX_SIZE];


void setup() {
  Serial.begin(115200);
}

void loop() {
  bool is_received = serial_parse.receive(_rx_data);
  if(!is_received)
    return;

  // Update sensor
  // _tx_data[0] = analogRead(A14);
  // _tx_data[1] = analogRead(A15);
  // _tx_data[2] = analogRead(A16);
  for (int i = 0; i < TX_SIZE; ++i)
  {
    _tx_data[i] = _rx_data[i*2] + _rx_data[i*2+1];
  }

  serial_parse.transmit(_tx_data);
}