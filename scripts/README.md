# Scripts Directory

This folder contains utility scripts designed to enhance and automate certain tasks for the **Universal Infrared Blaster (UIRB)** project. These scripts are specifically created to work with PlatformIO and facilitate tasks like managing EEPROM backups.

## Structure

### [`scripts/pio`](./pio/)
This subfolder holds PlatformIO-specific scripts. Currently, it includes:

- **[`backup_eeprom.py`](./pio/backup_eeprom.py)**:
  - Adds custom targets to manage EEPROM data:
    - `backupeep`: Creates EEPROM backups and saves them in the `uirb/data/eeprom/backups` directory.
    - `archiveeep`: Archives EEPROM backups into ZIP files and stores them in the `uirb/data/eeprom/backup_archives` directory.
    - `cleaneep`: Removes empty backup directories from the `uirb/data/eeprom/backups` directory.

## Usage

To use the scripts in this folder, simply call the respective targets.

## Notes

- Ensure that the paths and configurations in [`backup_eeprom.py`](./pio/backup_eeprom.py) align with your project's structure.
- These scripts are tailored for use with the UIRB project and may not work with other setups without modifications.

For more details on using custom scripts with PlatformIO, refer to the [official documentation](https://docs.platformio.org/en/latest/scripting/index.html).