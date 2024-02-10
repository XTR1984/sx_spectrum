#include <Arduino.h>
//#include <ESP32Time.h>
#include <esp_task_wdt.h>
//#include <LoRa.h>
#include "sx127x.h"
#include "pins.h"
#include "functions.h"

//#define FREQUENCY 868000000

uint64_t freq;
uint8_t gain = 1; 
uint8_t rxbwmant=2;
uint8_t rxbwexp=5;
uint8_t avgsamples = 2;
int delay_us = 2000;


void init(){
    SX127x_begin();
    SX127x_scan_mode( gain, avgsamples,rxbwmant,rxbwexp);
    delay(100);
    Serial.println("Init ok");
    Serial.flush();
}

void setup(){
    esp_task_wdt_init(120, true);
    esp_task_wdt_add(NULL);  
    Serial.begin(115200);
    Serial.setTimeout(1);
    pinMode(LED, OUTPUT);
    delay(1000);
}



void doSweep(uint64_t freq, int step, int size){
    for (int i=0;i<size;i++){
      SX127x_set_frequency(&freq);
      delayMicroseconds(delay_us);
      Serial.write(SX127x_getRSSI_raw());
      freq+=step;
    }
}


void loop(){
  esp_task_wdt_reset();
  if (Serial.available() > 0) {
    String str = Serial.readString();
    if (str.startsWith("Sweep")){
      digitalWrite(LED, HIGH);
      int f = getValue(str,':',1).toInt();
      int step = getValue(str,':',2).toInt();
      int size = getValue(str,':',3).toInt();
      doSweep(f, step, size);
      Serial.flush();
      digitalWrite(LED, LOW);
    }
    else if (str.startsWith("GetRSSI")){
      digitalWrite(LED, HIGH);
      delayMicroseconds(delay_us);
      Serial.write(SX127x_getRSSI_raw());
      Serial.flush();
      digitalWrite(LED, LOW);
    }
    else if (str.startsWith("Init")){
      digitalWrite(LED, HIGH);
      gain = getValue(str,':',1).toInt();
      avgsamples = getValue(str,':',2).toInt();
      rxbwmant = getValue(str,':',3).toInt();
      rxbwexp = getValue(str,':',4).toInt();
      delay_us = getValue(str,':',5).toInt();
      init();
      digitalWrite(LED, LOW);
    }
    else if (str.startsWith("SetFreq")){
      digitalWrite(LED, HIGH);
      int f = getValue(str,':',1).toInt();
      uint64_t freq = f;
      SX127x_set_frequency(&freq);
      Serial.write("OK");
      Serial.flush();
      digitalWrite(LED, LOW);
    }

  }
  delay(5);
}



