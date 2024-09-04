/**
 * @file examples/Girs/config.h
 * @brief User configuration file.
 * This file determines the configuration of the built program.
 * Feel free to be creative here; you can include pre-built files, you can replace
 * the file with your content, you can include pre-built files and override values
 * in them, or ...
 */

#pragma once

#include "Board.h"

#include "GirsUIRB.config.h"


/*
* Serial options 
*/

#define SERIAL_9600BAUD_SEL_PIN             PIN_PC2 // Options switch 1
#define SERIAL_9600BAUD_SEL_PIN_ACTIVE      LOW     // Options switch 1 active state
#define SERIAL_19200BAUD_SEL_PIN            PIN_PC3 // Options switch 2
#define SERIAL_19200BAUD_SEL_PIN_ACTIVE     LOW     // Options switch 2 active state
#define SERIAL_250000BAUD_SEL_PIN           PIN_PC4 // Options switch 3
#define SERIAL_250000BAUD_SEL_PIN_ACTIVE    LOW     // Options switch 3 active state

/*
* eeprom addresses and lenghts
*/

#define INFO_HARDWARE_VERSION_ADDR 0x06
#define INFO_HARDWARE_VERSION_LEN sizeof(double)
#if defined(UIRB_V02)
#define HARDWARE_VERSION_CMP 0.2 // double hardware version x.x thats checked againt value stored in eeprom
#endif