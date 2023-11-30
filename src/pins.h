#ifndef __PINS__H__
#define __PINS__H__

#ifdef ARDUINO_LOLIN_S2_MINI
#define SX127x_SCK   36
#define SX127x_MISO  37
#define SX127x_MOSI  35
#define SX127x_SS  34
#define SX127x_RESET 39
#define SX127x_DIO0 33
#define LED 15

#define SDA 8
#define SCL 9
#endif

#ifdef LILYGO  //t3_v1.6.1
#define SX127x_RESET 23
#define SX127x_SCK   5
#define SX127x_MISO  19
#define SX127x_MOSI  27
#define SX127x_SS  18
#define SX127x_DIO0 26
#define LED 25
#endif


#endif