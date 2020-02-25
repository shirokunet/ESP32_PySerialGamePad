#ifndef ESP32_SERIALTW_h
#define ESP32_SERIALTW_h

#include "Arduino.h"

class ESP32_SERIALTW
{
  public:
    ESP32_SERIALTW(int tx_size, int rx_size);
    void transmit(int tx_data[]);
    bool receive(int rx_data[]);
  private:
    int tx_size_, rx_size_;
};

#endif
