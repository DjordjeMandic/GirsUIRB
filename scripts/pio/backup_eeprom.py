Import("env")
import os
from datetime import datetime
import zipfile
import shutil

# Configuration Section
# =====================
# Define constants for paths, timestamps, and other settings for easier maintenance.

BACKUPS_DIR = os.path.join(env['PROJECT_DIR'], 'uirb', 'data', 'eeprom', 'backups')  # Directory for EEPROM backups
ARCHIVES_DIR = os.path.join(env['PROJECT_DIR'], 'uirb', 'data', 'eeprom', 'backup_archives')  # Directory for backup archives
TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'  # Timestamp format for naming backup folders and files

# Functions
# =========

def prepare_read_eeprom_env(source, target, env):
    """
    Prepares the environment for reading EEPROM data.
    - Creates a timestamped backup directory.
    - Defines the output file paths for EEPROM data.
    - Sets the EEPROM read command based on the upload protocol.

    Args:
        source: Source argument passed by PlatformIO (not used).
        target: Target argument passed by PlatformIO (not used).
        env: The PlatformIO environment object.
    """
    # Ensure the EEPROM backup directory exists
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    backups_subdir = os.path.join(BACKUPS_DIR, timestamp)
    os.makedirs(backups_subdir, exist_ok=True)

    # Define file paths for output
    filepath_bin = os.path.join(backups_subdir, "eeprom.bin")
    print(f"Binary path: {os.path.relpath(filepath_bin, env['PROJECT_DIR'])}")

    env.Replace(EEPROM_BACKUP_BIN_PATH=filepath_bin)

    # Define EEPROM read command
    READ_EEP_CMD = ""
    print("Warning: The upload and EEPROM read flags may conflict!")

    if 'UPLOAD_PROTOCOL' in env and env['UPLOAD_PROTOCOL'] == 'urclock':
        env.AutodetectUploadPort()
        READ_EEP_CMD = "$UPLOADER $UPLOADERFLAGS -P $UPLOAD_PORT -b $UPLOAD_SPEED -U eeprom:r:\"$EEPROM_BACKUP_BIN_PATH\":r"
    else:
        READ_EEP_CMD = "$UPLOADER $UPLOADERFLAGS -U eeprom:r:\"$EEPROM_BACKUP_BIN_PATH\":r"

    env.Replace(READ_EEP_CMD=READ_EEP_CMD)


def delete_empty_directories(source, target, env):
    """
    Deletes empty directories within the EEPROM backups folder.

    Args:
        source: Source argument passed by PlatformIO (not used).
        target: Target argument passed by PlatformIO (not used).
        env: The PlatformIO environment object.
    """
    try:
        if os.path.exists(BACKUPS_DIR):
            for root, dirs, files in os.walk(BACKUPS_DIR, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    if not os.listdir(dir_path):  # Check if the directory is empty
                        os.rmdir(dir_path)
                        print(f"Deleted empty backup directory: {os.path.relpath(dir_path, env['PROJECT_DIR'])}")
    except Exception as e:
        print(f"Error deleting empty backup directories: {e}")


def archive_all_backups(source, target, env):
    """
    Archives all existing EEPROM backups into a timestamped ZIP file.
    - Creates a ZIP file containing all backup files.
    - Deletes original backups after archiving.

    Args:
        source: Source argument passed by PlatformIO (not used).
        target: Target argument passed by PlatformIO (not used).
        env: The PlatformIO environment object.
    """
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

    # Ensure the archives directory exists
    os.makedirs(ARCHIVES_DIR, exist_ok=True)

    # Define the output ZIP file path
    zip_filename = os.path.join(ARCHIVES_DIR, f"{timestamp}.zip")

    try:
        # Create a ZIP file and add all backup files
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(BACKUPS_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, BACKUPS_DIR)
                    zipf.write(file_path, arcname)
        relative_zip_path = os.path.relpath(zip_filename, env['PROJECT_DIR'])
        print(f"All backups archived successfully to {relative_zip_path}")
    except Exception as e:
        print(f"Error archiving backups: {e}")
        env.Exit(1)

    try:
        # Delete all original backup files and folders
        for item in os.listdir(BACKUPS_DIR):
            item_path = os.path.join(BACKUPS_DIR, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print("All original backup files and folders have been deleted.")
    except Exception as e:
        print(f"Error deleting original backups: {e}")
        env.Exit(1)


# Add Targets
# ===========
env.AddTarget(
    "backupeep",
    None,
    [
        env.VerboseAction(prepare_read_eeprom_env, "Preparing env for EEPROM backup..."),
        env.VerboseAction("$READ_EEP_CMD", "Reading EEPROM."),
    ],
    group="Platform",
    title="Backup EEPROM",
    description="Reads EEPROM in binary format."
)

env.AddTarget(
    "archiveeep",
    None,
    [
        env.VerboseAction(archive_all_backups, "Archiving all EEPROM backups..."),
    ],
    group="General",
    title="Archive EEPROM Backups",
    description="Archives all EEPROM backups into a single ZIP file."
)

env.AddTarget(
    "cleaneep",
    None,
    [
        env.VerboseAction(delete_empty_directories, "Deleting empty backup directories..."),
    ],
    group="General",
    title="Clean EEPROM Backups",
    description="Deletes empty EEPROM backup directories."
)
