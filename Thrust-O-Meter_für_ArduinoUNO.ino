//-------------------------------------------------------------------------------------
// HX711_ADC.h
// Arduino master library for HX711 24-Bit Analog-to-Digital Converter for Weigh Scales
// Olav Kallhovd sept2017
// Tested with      : HX711 asian module on channel A and YZC-133 3kg load cell
// Tested with MCU  : Arduino Nano, ESP8266
//-------------------------------------------------------------------------------------
// This is an example sketch on how to use this library
// Settling time (number of samples) and data filtering can be adjusted in the config.h file

#include <HX711_ADC.h>

//HX711 constructor (dout pin, sck pin):
HX711_ADC LoadCell(4, 5);
HX711_ADC LoadCell2(7, 6);

unsigned long t;

void setup() {
	

	Serial.begin(115200);

	LoadCell.begin();
  LoadCell2.begin();

	long stabilisingtime = 2000; // tare preciscion can be improved by adding a few seconds of stabilising time
	LoadCell.start(stabilisingtime);
  LoadCell2.start(stabilisingtime);
}

void loop() {
	LoadCell.update();
  LoadCell2.update();
	//get smoothed value from data set
	if (millis() > t + 10) {
		float i = LoadCell.getData();
    float ii= LoadCell2.getData();
		t = millis();
		Serial.print(t);
		Serial.print('\t');
		Serial.print(i);
    Serial.print('\t');
    Serial.println(ii);
	}
}
