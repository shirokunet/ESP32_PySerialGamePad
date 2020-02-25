#include "esp32_serial_twoways.h"

ESP32_SERIALTW::ESP32_SERIALTW(int tx_size, int rx_size)
{
  tx_size_ = tx_size;
  rx_size_ = rx_size;
}

void ESP32_SERIALTW::transmit(int tx_data[])
{
  Serial.print("#,");
  for (int i = 0; i < tx_size_; ++i)
  {
    Serial.print(tx_data[i]);
    Serial.print(',');
  }
  Serial.print('\n');
}

bool ESP32_SERIALTW::receive(int rx_data[]){
  static String str= "";
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
          if (str.substring(i, i+1) == "," && counter < rx_size_) {
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