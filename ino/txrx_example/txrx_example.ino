
#define TX_SIZE 3
#define RX_SIZE 6

int _tx_data[TX_SIZE];
int _rx_data[RX_SIZE];
String str= "";

void serial_send(int tx_data[]){
  Serial.print("#,");
  for (int i = 0; i < TX_SIZE; ++i)
  {
    Serial.print(tx_data[i]);
    Serial.print(',');
  }
  Serial.print('\n');
}

bool serial_receive(int rx_data[]){
  if(Serial.available() > 0)
  {
    char ch = Serial.read();
    if (ch == '\n')
    {
      if(str.substring(0, 1) == "#")
      {
        int lastIndex = 2;  // skip '#,'
        int counter = 0;
        for (int i = lastIndex; i < str.length(); i++) {
          if (str.substring(i, i+1) == ",") {
            rx_data[counter] = str.substring(lastIndex, i).toInt();
            lastIndex = i + 1;
            counter++;
          }
        }
      }
      str = "";
      return true;
    }
    else{
      str += ch;
    }
  }
  return false;
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  bool is_received = serial_receive(_rx_data);
  if(!is_received)
    return;

  for (int i = 0; i < TX_SIZE; ++i)
  {
    _tx_data[i] = _rx_data[i*2] + _rx_data[i*2+1];
  }
  serial_send(_tx_data);
}