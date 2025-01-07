#pragma once

#if __has_include(<UIRBcore_Pins.h>)
#include <UIRBcore_Pins.h>
#define SIGNAL_LED_1        PIN_STAT_LED

#define IRSENSOR_1_PIN      PIN_IR_CAPTURE

#define IRRECEIVER_1_PIN    PIN_IR_RECEIVE
#else
#define SIGNAL_LED_1        LED_BUILTIN

#define IRSENSOR_1_PIN      (8)

#define IRRECEIVER_1_PIN    PIN_SPI_MISO

#define IRRECEIVER_1_PULLUP
#endif  // __has_include(<UIRBcore_Pins.h>)

#if IR_RECEIVE_PIN_PULLUP
    #define IRRECEIVER_1_PULLUP
#endif

#if IR_CAPTURE_PIN_PULLUP
    #define IRSENSOR_1_PULLUP
#endif
