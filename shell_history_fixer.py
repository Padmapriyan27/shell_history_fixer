import os
import shutil
import subprocess
import platform
from datetime import datetime
from pyfiglet import figlet_format
import time
from tqdm import tqdm

# ANSI escape sequences for colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[39m'

# Detect the shell type
def get_shell_type():
    """Detect the current shell type (Zsh or Bash)."""
    shell = os.environ.get('SHELL', '')
    if 'zsh' in shell:
        return 'zsh'
    elif 'bash' in shell:
        return 'bash'
    else:
        print(Colors.FAIL + "Unsupported shell detected. Exiting..." + Colors.RESET)
        exit(0)

# Paths
home_dir = os.path.expanduser("~")
shell = get_shell_type()
history_file = os.path.join(home_dir, f".{shell}_history")
backup_file = os.path.join(home_dir, f".{shell}_history_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}")
cleaned_file = os.path.join(home_dir, f".{shell}_history_clean")

def show_progress(message):
    print(f"{Colors.OKBLUE}[INFO] {message}...{Colors.RESET}")
    for _ in tqdm(range(100), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
        time.sleep(0.01)

def confirm_action(message):
    """Prompt the user for confirmation before proceeding."""
    while True:
        response = input(f"{Colors.OKCYAN}{message} (y/n): {Colors.RESET}").strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        else:
            print(Colors.WARNING + "Invalid input. Please enter 'y' or 'n'." + Colors.RESET)


def backup_history(dry_run=False):
    """Backup the existing shell history file securely."""
    show_progress(f"Backing up the {shell} history file")
    if os.path.exists(history_file):
        if not dry_run and confirm_action(f"Are you sure you want to backup the {shell} history file?"):
            try:
                shutil.copy(history_file, backup_file)
                print(f"{Colors.OKGREEN}Backup created: {backup_file}{Colors.RESET}")
            except Exception as e:
                print(Colors.FAIL + f"Error during backup: {e}" + Colors.RESET)
                exit(1)
        else:
            print(Colors.WARNING + "Backup skipped." + Colors.RESET)
    else:
        print(Colors.WARNING + f"No {shell} history file found to backup." + Colors.RESET)

def clean_history(dry_run=False):
    """Clean the corrupt shell history using strings command."""
    show_progress(f"Cleaning the {shell} history file")
    if not dry_run and confirm_action(f"Are you sure you want to clean the {shell} history file?"):
        try:
            with open(cleaned_file, 'w') as outfile:
                result = subprocess.run(["strings", history_file], stdout=outfile, check=True)
                if result.returncode == 0:
                    print(f"{Colors.OKGREEN}Cleaned history created: {cleaned_file}{Colors.RESET}")
                else:
                    print(Colors.FAIL + f"Failed to clean history, return code: {result.returncode}" + Colors.RESET)
                    exit(1)
        except Exception as e:
            print(Colors.FAIL + f"Error cleaning history: {e}" + Colors.RESET)
            exit(1)
    else:
        print(Colors.WARNING + "Cleaning skipped." + Colors.RESET)

def replace_history(dry_run=False):
    """Replace the corrupt shell history with the cleaned one."""
    show_progress(f"Replacing the {shell} history file with the cleaned version")
    if os.path.exists(cleaned_file):
        if not dry_run and confirm_action(f"Are you sure you want to replace the {shell} history file?"):
            try:
                shutil.move(cleaned_file, history_file)
                print(f"{Colors.OKGREEN}Replaced {shell} history with cleaned version.{Colors.RESET}")
            except Exception as e:
                print(Colors.FAIL + f"Error replacing history: {e}" + Colors.RESET)
                exit(1)
    else:
        print(Colors.WARNING + "Cleaned history file not found." + Colors.RESET)

def set_permissions(dry_run=False):
    """Set correct permissions for shell history file."""
    show_progress(f"Setting correct permissions for {shell} history file")
    if not dry_run and confirm_action(f"Are you sure you want to set permissions for {shell} history?"):
        try:
            os.chmod(history_file, 0o600)
            print(f"{Colors.OKGREEN}Permission set to 600 for {shell} history.{Colors.RESET}")
        except Exception as e:
            print(Colors.FAIL + f"Error setting permissions: {e}" + Colors.RESET)
            exit(1)

def source_shellrc(dry_run=False):
    """Source the shell configuration file based on detected shell type."""
    show_progress("Sourcing the shell configuration file")
    shellrc_path = os.path.join(home_dir, f".{shell}rc")
    if os.path.exists(shellrc_path):
        if not dry_run and confirm_action(f"Are you sure you want to source {shellrc_path}?"):
            try:
                result = subprocess.run([shell, "-c", f"source {shellrc_path}"], check=True)
                if result.returncode == 0:
                    print(f"{Colors.OKGREEN}Sourced {shellrc_path} successfully.{Colors.RESET}")
                else:
                    print(Colors.FAIL + f"Error sourcing {shellrc_path}, return code: {result.returncode}" + Colors.RESET)
            except Exception as e:
                print(Colors.FAIL + f"Error sourcing {shellrc_path}: {e}" + Colors.RESET)
        else:
            print(Colors.WARNING + f"Sourcing of {shellrc_path} skipped." + Colors.RESET)
    else:
        print(Colors.WARNING + f"{shellrc_path} file not found, skipping sourcing." + Colors.RESET)

def delete_backup():
    """Delete the backup file after process completion."""
    if os.path.exists(backup_file):
        try:
            os.remove(backup_file)
            print(f"{Colors.OKGREEN}Backup file deleted: {backup_file}{Colors.RESET}")
        except Exception as e:
            print(Colors.FAIL + f"Error deleting backup file: {e}" + Colors.RESET)

def main():
    banner = figlet_format("0xD4rKEYe", font='slant')
    print(Colors.OKGREEN + banner + Colors.ENDC + Colors.RESET)
    author = "0xD4rKEYe"
    print(Colors.HEADER + "\t\t\t\t\t", "- ", author + Colors.RESET)
    print(f"{Colors.HEADER}Starting secure {shell} history repair process...{Colors.RESET}")
    time.sleep(1)

    dry_run = '--dry-run' in os.sys.argv

    backup_history(dry_run)
    clean_history(dry_run)
    replace_history(dry_run)
    set_permissions(dry_run)
    source_shellrc(dry_run)
    
    if not dry_run:
        delete_backup()
        print(f"{Colors.OKGREEN}Process completed successfully!{Colors.RESET}")
    else:
        print(f"{Colors.OKGREEN}Dry run completed. No changes made.{Colors.RESET}")

if __name__ == "__main__":
    main()
