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

unsigned long t;

void setup() {
	

	Serial.begin(115200);

	LoadCell.begin();

	long stabilisingtime = 2000; // tare preciscion can be improved by adding a few seconds of stabilising time
	LoadCell.start(stabilisingtime);

}

void loop() {
	LoadCell.update();

	//get smoothed value from data set
	if (millis() > t + 10) {
		float i = LoadCell.getData();
		t = millis();
		Serial.print(t);
		Serial.print('\t');
		Serial.print(i);
	}
}
