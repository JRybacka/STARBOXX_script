import subprocess
import logging
import os
import shlex
import glob

# Configure logging
logging.basicConfig(filename="training.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_training(command, index):
    """Execute a single training command."""
    try:
        logging.info(f"Starting training job {index+1}: {command}")
        print(f"\nRunning training job {index+1}...\n{command}")

        # Debug: Print the exact command being run
        print(f"\n[DEBUG] Running command: {shlex.split(command)}\n")

        # Run subprocess without shell=True for better Windows compatibility
        process = subprocess.run(shlex.split(command), check=True, text=True, capture_output=True)

        logging.info(f"Training job {index+1} completed successfully.")
        print(f"\nTraining job {index+1} completed successfully!\n")

    except subprocess.CalledProcessError as e:
        # Log stdout and stderr for detailed debugging
        logging.error(f"Training job {index+1} failed: {e}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
        print(f"\nTraining job {index+1} failed. Check training.log for details.\n")

    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
        print(f"\nFileNotFoundError: {e}\n")

def get_toml_files(directory):
    """Retrieve all .toml files from the specified directory."""
    if not os.path.isdir(directory):
        logging.error(f"Invalid directory: {directory}")
        print(f"\nError: Directory {directory} does not exist.\n")
        return []

    toml_files = sorted(glob.glob(os.path.join(directory, "*.toml")))  # Sort for consistent order
    if not toml_files:
        logging.warning(f"No TOML files found in {directory}")
        print(f"\nWarning: No TOML files found in {directory}\n")

    return toml_files

def build_command_from_toml(toml_file):
    """Generate a kohya_ss training command from a .toml file."""
    train_script = r"C:\\DYSK-F\\STARBOXX\\kohya_ss\\sd-scripts\\train_network.py"  # Full path to script
    accelerate_path = r"C:\\DYSK-F\\STARBOXX\\kohya_ss\\venv\\Scripts\\accelerate.exe"  # Replace with the actual path if needed

    # Verify if files exist before running
    if not os.path.isfile(train_script):
        logging.error(f"train_network.py not found at {train_script}")
        print(f"train_network.py not found at {train_script}")
        return None

    if not os.path.isfile(accelerate_path):
        logging.error(f"accelerate.exe not found at {accelerate_path}")
        print(f"accelerate.exe not found at {accelerate_path}")
        return None

    return f"{shlex.quote(accelerate_path)} launch {shlex.quote(train_script)} --config_file={shlex.quote(toml_file)}"

if __name__ == "__main__":
    # Prompt user for the directory
    print("\nPaste the directory containing TOML config files and press Enter:")
    toml_dir = input().strip()

    if not toml_dir:
        print("\nError: No directory provided.\n")
        logging.error("No directory provided.")
        input("Press Enter to exit...")
        exit()

    toml_files = get_toml_files(toml_dir)

    if not toml_files:
        print("\nNo valid TOML files found. Exiting...\n")
        logging.error("No valid TOML files found in the specified directory.")
        input("Press Enter to exit...")
        exit()

    for index, toml_file in enumerate(toml_files):
        command = build_command_from_toml(toml_file)
        if command:  # Only run if command was successfully built
            run_training(command, index)

    print("\nAll training jobs completed!\n")
    logging.info("All training jobs completed!")
    input("Press Enter to exit...")