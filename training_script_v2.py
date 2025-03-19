import subprocess
import logging
import os

# Configure logging
logging.basicConfig(filename="training.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_training(command, index):
    """Execute a single training command."""
    try:
        logging.info(f"🟢 Starting training job {index+1}:")
        logging.info(command)  # Log the command
        print(f"\n🟢 Running training job {index+1}...\n")
        print(command)  # Show the command
        
        process = subprocess.run(command, shell=True, check=True, text=True)

        logging.info(f"✅ Training job {index+1} completed successfully.")
        print(f"\n✅ Training job {index+1} completed successfully!\n")

    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Training job {index+1} failed: {e}")
        print(f"\n❌ Training job {index+1} failed. Check training.log for details.\n")

def load_commands_from_file(file_path):
    """Load multiple training commands from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            commands = [line.strip() for line in file.readlines() if line.strip()]  # Remove empty lines
        return commands
    except Exception as e:
        logging.error(f"Error loading command file: {e}")
        return None

if __name__ == "__main__":
    command_file = "training_command.txt"  # File where commands are saved

    # Check if the file exists
    if os.path.isfile(command_file):
        print(f"\n📄 Loading training queue from {command_file}...\n")
        commands = load_commands_from_file(command_file)
    else:
        print("\n✏️ Paste training commands below (one per line, press Enter twice when done):\n")
        commands = []
        while True:
            command = input().strip()
            if not command:
                break  # Stop when user presses Enter on an empty line
            commands.append(command)

    if not commands:
        logging.error("❌ No commands provided. Please provide at least one training command.")
        print("\n❌ Error: No training commands found.\n")
        input("🔹 Press Enter to exit...")  # Keep the script open on error
    else:
        for index, command in enumerate(commands):
            run_training(command, index)  # Run each command sequentially
        
        print("\n🎉 All training jobs completed!\n")
        logging.info("🎉 All training jobs completed!")
        input("🔹 Press Enter to exit...")  # Keep script open at the end
