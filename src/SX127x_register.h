/* based on code by Amon Schumann / DL9AS   https://github.com/DL9AS
*/ 

#ifndef __SX1276_REGISTER__H__
#define __SX1276_REGISTER__H__

#define REG_DETECT_OPTIMIZE 0x31
#define REG_OP_MODE 0x01

#define REG_FR_MSB 0x06
#define REG_FR_MID 0x07
#define REG_FR_LSB 0x08

#define REG_PA_DAC 0x4D
#define REG_PA_CONFIG 0x09

#define REG_FDEV_MSB 0x04
#define REG_FDEV_LSB 0x05

#define REG_IMAGE_CAL 0x3B
#define REG_TEMP 0x3C

#define REG_PLL_HOP 0x44
#define REG_RSSI_VALUE 0x11
#define REG_RSSI_CONFIG 0x0E
#define REG_RXBW 0x12
#define REG_LNA 0xC
#define REG_RX_CONFIG 0Xd
#endif