# Shell History Fixer

This tool helps to repair corrupted shell history files for both Zsh and Bash. It includes features for creating backups, cleaning corrupted history, and resetting file permissions.

## Features

- **Backup:** Creates a backup of the current shell history file.
- **Clean:** Fixes corruption by using the `strings` command to extract valid data.
- **Replace:** Replaces the corrupted history file with the cleaned version.
- **Permissions:** Sets secure permissions (`600`) for the history file.
- **Source Shell Configuration:** Sourcing the relevant shell configuration file to apply changes.
- **Interactive Mode:** Users can confirm actions before proceeding.
- **Dry Run Mode:** Test the process without making changes.

### Requirements

Make sure you have Python installed, and the following external library is required:

- `pyfiglet`: For rendering the ASCII art banner.
- `tqdm`: For showing the progress bar.

To install the dependencies, you can use the following command:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the Repository:

```bash
git clone https://github.com/Padmapriyan27/shell_history_fixer.git
```

2. Navigate to the Tool's Directory:

```bash
cd shell_history_fixer
```

### Usage

To run the script, execute the following command:

```bash
python shell_history_fixer.py
```

### Example Command

```bash
python shell_history_fixer.py --dry-run
```

### How it works

- Detect Shell Type: Automatically identifies whether the current shell is Zsh or Bash.
- Backup History File: Creates a secure backup of the existing history file.
- Clean History File: Cleans the history file using the `strings` command to remove corruption.
- Replace History File: Replaces the original history file with the cleaned version.
- Set Permissions: Ensures the history file has the correct permissions to enhance security.
- Source Shell Configuration: Reloads the relevant shell configuration file to apply changes

### License

This script is provided under the MIT License.