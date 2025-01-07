# GirsUIRB 
**(Based on [AGirs](https://github.com/bengtmartensson/AGirs))**  
[![Linktree](https://img.shields.io/badge/LinkTree-1de9b6?logo=linktree&logoColor=white)](https://linktr.ee/djordjemandic)

**GirsUIRB** is an infrared server for Arduino, specifically adapted for the [Universal IR Blaster (UIRB) V0.2 board](https://github.com/DjordjeMandic/UIRBpio). It incorporates several enhancements and additional features to **enable integration with [UIRBcorelib](https://github.com/DjordjeMandic/UIRBcorelib)**, bringing extended capabilities for IR signal processing and hardware control. It remains compatible with tools like [IrScrutinizer](https://github.com/bengtmartensson/IrScrutinizer) and [LIRC](https://www.lirc.org/).

> **Note**: This project uses the [MiniCore hardware package](https://github.com/MCUdude/MiniCore/). For additional hardware details and an example PlatformIO project, see the [UIRBpio repository](https://github.com/DjordjeMandic/UIRBpio).

---

## Key Features

- **Adapted AGirs** firmware tailored for the Universal IR Blaster.  
- **Integration with UIRBcorelib** for convenient access to board-level functions.  
- **Configurable baud rates** via simple button presses at startup.  
- **Raw capture** mode using a non-demodulating sensor on `PB0` (`ICP1`).  
- **Demodulated receive** mode for standardized IR signals on `PB4` (or your chosen pin).  
- **Low battery notification** with user-configurable intervals.

---

## Table of Contents

1. [Hardware Requirements and Modifications](#hardware-requirements-and-modifications)  
2. [Software Requirements](#software-requirements)  
3. [IR Receiver / Non-Demodulating Capture Sensor](#ir-receiver--non-demodulating-capture-sensor)  
4. [Project Structure and Environment Configurations](#project-structure-and-environment-configurations)  
5. [Uploading Firmware](#uploading-firmware)  
6. [Baud Rate Selection at Startup](#baud-rate-selection-at-startup)  
7. [Flashing Bootloader and Fuses](#flashing-bootloader-and-fuses)  
8. [TODO](#todo)  
9. [License](#license)

---

## Hardware Requirements and Modifications

### 1. Lithium Battery

A Li-Po or Li-Ion battery (capable of delivering ~3A peak) ensures stable power for IR LEDs and other onboard components. A 600mAh drone-style battery works well in most cases.

### 2. Modifications / Add-Ons

- **ICSP Breakout**: For direct programming via a `USBasp` or another ISP tool if you choose not to use the `urboot` bootloader.  
- **UART/Serial Connection**: For bootloader-based uploading, monitoring, and debugging.

---

## IR Receiver / Non-Demodulating Capture Sensor

In **GirsUIRB**, the firmware can handle both demodulated and non-demodulated IR signals:

- **Demodulating Sensor** (e.g., [TSOP4838](https://www.vishay.com/docs/82459/tsop48.pdf))  
  - Ideal for standard consumer IR protocols (38 kHz carrier, etc.).  
  - Default input pin is `PB4` (MISO).  
  - The firmware **already enables the internal pullup**, but **make sure to add an external pullup of ~4.7 kΩ if required** for signal integrity.

- **Non-Demodulating Sensor** (e.g., [TSMP58000](https://www.micros.com.pl/mediaserver/info-ootsmp58000.pdf))  
  - Captures raw waveforms without relying on a carrier frequency.  
  - Wired to `PB0` (`ICP1`) for Timer1 input capture, usually via a 10 kΩ resistor to protect GPIO drivers.  
  - Useful for analyzing unknown or exotic IR signals.

> **Tip**: For the UIRB V0.2 board, you can route or combine signals to share a connector pin, but be mindful only one sensor should drive the line at a time (raw vs. demodulated). Alternatively, use separate pins and keep both sensors connected if you prefer.

---

## Software Requirements

1. [Visual Studio Code](https://code.visualstudio.com/) with [PlatformIO IDE](https://platformio.org/)  
2. [CP210x USB to UART Bridge VCP Drivers](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) (if using onboard USB-UART)  
3. Local clone of this repository:  
   ```bash
   git clone https://github.com/DjordjeMandic/GirsUIRB.git
   ```
4. For detailed hardware instructions and setup using PlatformIO, see the [UIRBpio repository](https://github.com/DjordjeMandic/UIRBpio).

---

## Project Structure and Environment Configurations

- **platformio.ini**: Defines multiple environments (e.g., `uirb-v02` for bootloader-based uploads, `uirb-v02-usbasp` for ISP uploads, etc.).  
- **src/**: Contains the main firmware logic (adapted from [AGirs](https://github.com/bengtmartensson/AGirs)).  
- **include/**, **lib/**, **test/**, etc.: Standard PlatformIO structure.

Each environment leverages [UIRBcorelib](https://github.com/DjordjeMandic/UIRBcorelib) and the [AGirs](https://github.com/bengtmartensson/AGirs) library. Different build types (release, debug, simulation) are available.

---

## Uploading Firmware

1. **Open the Project**: In VS Code, load this folder as a PlatformIO project.  
2. **Connect the Board**:  
   - If using `urboot`, connect via USB-UART.  
   - Otherwise, use a `USBasp` (ISP) programmer on the ICSP header.  
3. **Select the Environment**:  
   - **`[env:uirb-v02]`** for bootloader-based uploads.  
   - **`[env:uirb-v02-usbasp]`** for direct ISP.  
4. **Upload**:  
   - Via VS Code: Click “Project Tasks” → “General” → “Upload” under the appropriate environment.  
   - Or via CLI:  
   ```bash
   platformio run -e uirb-v02 --target upload
   ```
5. **Monitor**:  
   - If using serial (bootloader), open the serial monitor at 38400 (default).  
   ```bash
   platformio device monitor -b 38400
   ```
   Adjust if you selected a different baud rate at reset (see next section).

---

## Baud Rate Selection at Startup

- **Default**: `38400` baud.  
- **Option Switches** (held at reset):  
  - **Left (Option 1)**: `9600`  
  - **Middle (Option 2)**: `19200`  
  - **Right (Option 3)**: `250000`  

At reset, the firmware briefly communicates at `38400` to announce `BAUD:<chosen>:END`, then switches to the chosen baud rate. Some software might not list `250000` explicitly, but `256000` typically works well.

---

## Flashing Bootloader and Fuses

To burn the [urboot](https://github.com/stefanrueger/urboot) bootloader and set the fuses for 8 MHz operation:

1. **Connect an ISP Programmer** (e.g., `USBasp`) to the ICSP pins.  
2. **Choose the `uirb-v02-usbasp` Environment** (or similar).  
3. **Use the** `fuses` **target** in PlatformIO to set the fuses:  
   ```bash
   platformio run --target fuses --environment uirb-v02-usbasp 
   ```
4. **Use the** `bootloader` **target** in PlatformIO to burn the bootloader:  
   ```bash
   platformio run --target bootloader --environment uirb-v02-usbasp 
   ```
This will upload `urboot` to your ATmega328P and configure the fuses appropriately. See [UIRBpio repository](https://github.com/DjordjeMandic/UIRBpio) for more details.

---

## TODO

- [x] Write README  
- [x] Create library for Universal IR Blaster V0.2 hardware and use it here  
- [x] Add low battery indicator  
- [ ] Separate capture (raw) and receive (demodulated) signals (make them configurable via `platformio.ini`)  
- [ ] Create modules to leverage full UIRB hardware features  
- [ ] Implement autobaud
- [ ] Add status when idle

---

## License

This project is licensed under **GPLv2 or later**, just like AGirs & Infrared4Arduino. For more details, see the [AGirs License](https://github.com/bengtmartensson/AGirs#license).

> **Acknowledgment**: This firmware is originally based on [AGirs](https://github.com/bengtmartensson/AGirs) and has been enhanced to utilize [UIRBcorelib](https://github.com/DjordjeMandic/UIRBcorelib) for the Universal IR Blaster board.

---

**Happy hacking with GirsUIRB!** If you have questions or suggestions, please open an issue or pull request.