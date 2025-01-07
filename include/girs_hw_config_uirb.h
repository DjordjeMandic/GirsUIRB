#pragma once

#include <UIRBcore_Pins.h>

/*  
 *  Same signal is used for both non-demodulating and demodulating sensors!
 *  When using expansion board with non-demodulating sensor, use CAPTURE module
 *  When using expansion board with demodulating sensor, use RECEIVE module
 *
 */

#define SIGNAL_LED_1        PIN_STAT_LED

#define IRSENSOR_1_PIN      PIN_IR_CAPTURE

#define IRRECEIVER_1_PIN    PIN_IR_RECEIVE

#if IR_RECEIVE_PIN_PULLUP
    #define IRRECEIVER_1_PULLUP
#endif

#if IR_CAPTURE_PIN_PULLUP
    #define IRSENSOR_1_PULLUP
#endif
