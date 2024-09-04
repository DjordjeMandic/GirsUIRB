#pragma once

/*  
 *  Same signal is used for both non-demodulating and demodulating sensors!
 *  When using expansion board with non-demodulating sensor, use CAPTURE module
 *  When using expansion board with demodulating sensor, use RECEIVE module
 *
*/

#define SIGNAL_LED_1        PIN_PB5 // STAT LED

#define IRSENSOR_1_PIN      PIN_PB0 // PB0 (ICP1) PIN, Capture signal, connected with PB4 (MISO) via 10k resistor. Comes from  Non-demodulating sensor

#define IRRECEIVER_1_PIN    PIN_PB4 // PB4 (MISO) PIN, direct signal from expansion board
#define IRRECEIVER_1_PULLUP         // Enable pull up in case no expansion board is connected

//#define IRRECEIVER_2_PIN IRSENSOR_1_PIN // Non-demodulating sensor signal


