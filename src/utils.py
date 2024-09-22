# Utility functions for LorcanaTTSManager
import os
import shutil
import datetime
import json

def get_tts_directory():
    """
    Returns the platform-specific path to the Tabletop Simulator Saved Objects directory.
    Handles Windows, macOS, and Linux.
    """
    system = os.name
    if system == "nt":  # Windows
        return os.path.join(os.path.expanduser('~'), "Documents", "My Games", "Tabletop Simulator", "Saves", "Saved Objects")
    elif system == "posix":
        if 'darwin' in os.uname().sysname.lower():  # macOS
            return os.path.join(os.path.expanduser('~'), "Library", "Tabletop Simulator", "Saves", "Saved Objects")
        else:  # Linux
            return os.path.join(os.path.expanduser('~'), ".local", "share", "Tabletop Simulator", "Saves", "Saved Objects")
    else:
        raise ValueError("Unsupported operating system")


def backup_file(file_path, backup_dir_name="backups"):
    """
    Creates a timestamped backup of a given file.

    :param file_path: Path to the file to backup.
    :param backup_dir_name: Name of the directory where backups will be stored.
    :return: Path to the backup file created.
    """
    try:
        # Ensure backup directory exists
        backup_dir = os.path.join(os.path.dirname(file_path), backup_dir_name)
        os.makedirs(backup_dir, exist_ok=True)

        # Create timestamp for the backup
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_name = f"backup_{os.path.basename(file_path)}_{timestamp}"
        backup_file_path = os.path.join(backup_dir, backup_file_name)

        # Copy the file to the backup location
        shutil.copy(file_path, backup_file_path)
        return backup_file_path
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None


def format_timestamp():
    """
    Returns a formatted timestamp string in 'YYYY-MM-DD_HH-MM-SS' format.
    This can be used for file naming, logging, etc.

    :return: Formatted timestamp string.
    """
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def list_json_files(directory):
    """
    Lists all JSON files in a given directory.

    :param directory: The directory to search for JSON files.
    :return: A list of JSON file paths.
    """
    try:
        return [f for f in os.listdir(directory) if f.endswith('.json')]
    except FileNotFoundError:
        print(f"Error: Directory {directory} not found.")
        return []


def is_valid_json(file_path):
    """
    Checks if a file is a valid JSON file by attempting to load it.

    :param file_path: Path to the file to validate.
    :return: True if the file contains valid JSON, False otherwise.
    """
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False

