/*************************************************** 
  This is a library for the Adafruit PT100/P1000 RTD Sensor w/MAX31865

  Designed specifically to work with the Adafruit RTD Sensor
  ----> https://www.adafruit.com/products/3328

  This sensor uses SPI to communicate, 4 pins are required to  
  interface
  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Adafruit_MAX31865.h>
// Use software SPI: CS, DI, DO, CLK
Adafruit_MAX31865 thermo1 = Adafruit_MAX31865(30, 31, 32, 33);
Adafruit_MAX31865 thermo2 = Adafruit_MAX31865(34, 35, 36, 37);
Adafruit_MAX31865 thermo3 = Adafruit_MAX31865(38, 39, 40, 41);
Adafruit_MAX31865 thermo4 = Adafruit_MAX31865(42, 43, 44, 45);
Adafruit_MAX31865 thermo5 = Adafruit_MAX31865(46, 47, 48, 49);
Adafruit_MAX31865 thermo6 = Adafruit_MAX31865(50, 51, 52, 53);

// use hardware SPI, just pass in the CS pin
//Adafruit_MAX31865 thermo = Adafruit_MAX31865(10);

// The value of the Rref resistor. Use 430.0 for PT100 and 4300.0 for PT1000
#define RREF      4300.0
// The 'nominal' 0-degrees-C resistance of the sensor
// 100.0 for PT100, 1000.0 for PT1000
#define RNOMINAL  1000.0


void setup() {
  Serial.begin(115200);
  //Serial.println("Adafruit MAX31865 PT1000 Sensor Test!");

  thermo1.begin(MAX31865_2WIRE);  // set to 2WIRE or 4WIRE as necessary
  thermo2.begin(MAX31865_2WIRE);  // set to 2WIRE or 4WIRE as necessary
  thermo3.begin(MAX31865_2WIRE);  // set to 2WIRE or 4WIRE as necessary
  thermo4.begin(MAX31865_2WIRE);  // set to 2WIRE or 4WIRE as necessary
  thermo5.begin(MAX31865_2WIRE);  // set to 2WIRE or 4WIRE as necessary
  thermo6.begin(MAX31865_2WIRE);  // set to 2WIRE or 4WIRE as necessary
}


void loop() {
  //Serial.println("In loop().");
  char data = Serial.read();
  char str[2];
  str[0] = data;
  str[1] = '\0';
  //printf("data %s\n", str);
  
  if( str[0] == '1' )
  {  
    uint16_t rtd1 = thermo1.readRTD();
    uint16_t rtd2 = thermo2.readRTD();
    uint16_t rtd3 = thermo3.readRTD();
    uint16_t rtd4 = thermo4.readRTD();
    uint16_t rtd5 = thermo5.readRTD();
    uint16_t rtd6 = thermo6.readRTD();
    
    Serial.print(thermo1.temperature(RNOMINAL, RREF));  
    Serial.print(" ");
    Serial.print(thermo2.temperature(RNOMINAL, RREF));
    Serial.print(" ");
    Serial.print(thermo3.temperature(RNOMINAL, RREF));
    Serial.print(" ");
    Serial.print(thermo4.temperature(RNOMINAL, RREF));
    Serial.print(" ");
    Serial.print(thermo5.temperature(RNOMINAL, RREF));
    Serial.print(" ");
    Serial.print(thermo6.temperature(RNOMINAL, RREF));
    Serial.print("\n");
        
    // Check and print any faults
    //uint8_t fault = thermo1.readFault();
    uint8_t fault = thermo1.readFault() || thermo2.readFault() || thermo3.readFault() ||
                    thermo4.readFault() || thermo5.readFault() || thermo6.readFault();
    if (fault) {
      Serial.print("Fault 0x"); Serial.println(fault, HEX);
      if (fault & MAX31865_FAULT_HIGHTHRESH) {
       Serial.println("RTD High Threshold"); 
      }
      if (fault & MAX31865_FAULT_LOWTHRESH) {
        Serial.println("RTD Low Threshold"); 
     }
      if (fault & MAX31865_FAULT_REFINLOW) {
        Serial.println("REFIN- > 0.85 x Bias"); 
     }
      if (fault & MAX31865_FAULT_REFINHIGH) {
        Serial.println("REFIN- < 0.85 x Bias - FORCE- open"); 
      }
      if (fault & MAX31865_FAULT_RTDINLOW) {
        Serial.println("RTDIN- < 0.85 x Bias - FORCE- open"); 
      }
      if (fault & MAX31865_FAULT_OVUV) {
        Serial.println("Under/Over voltage"); 
      }
      thermo1.clearFault();
      thermo2.clearFault();
      thermo3.clearFault();
      thermo4.clearFault();
      thermo5.clearFault();
      thermo6.clearFault();
    }
  }
  
}
