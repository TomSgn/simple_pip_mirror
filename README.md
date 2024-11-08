# Download and Organize Python Packages
This script is the FASTEST way to create pip-mirror, for every version of python !


This script, `download_and_organize_packages.py`, is designed to download Python packages specified in a `requirements.txt` file and organize them into folders based on Python versions (e.g., `python27`, `python36`, `python38`, `python39`). Each package downloaded is then placed in a subdirectory within the corresponding Python version folder, organized by package name.

## Features

- **Multiple Python Version Support**: Downloads packages for Python 2.7, 3.6, 3.8, and 3.9 using only `pip3`.
- **Organized Downloaded Packages**: Each package is placed in its own folder inside the designated Python version directory, allowing easy navigation and separation.
- **Compatibility Filtering**: The script uses version constraints to download compatible packages for each Python version, ensuring that only the latest compatible versions are downloaded.

## Requirements

- Python 3 installed on your system.
- `pip3` (Python 3's package manager).

## Setup

1. Clone or copy the script file `download_and_organize_packages.py` to your working directory.
2. Prepare a `requirements.txt` file listing the packages to be downloaded. Specify version compatibility using Python version constraints if needed, for example:
   ```
   numpy; python_version == "3.6"
   pandas; python_version >= "3.8"
   ```

## Usage

1. Place the `requirements.txt` file in the same directory as the script.
2. Run the script as follows:

   ```bash
   python3 download_and_organize_packages.py
   ```

3. The script will:
   - Parse the `requirements.txt` file.
   - Download the packages compatible with each specified Python version (2.7, 3.6, 3.8, 3.9).
   - Organize downloaded packages into folders by Python version and package name, with this structure:
     ```
     pip-mirror/
     ├── python27/
     │   ├── numpy/
     │   │   └── numpy-1.16.6.whl
     │   └── pandas/
     ├── python36/
     └── python38/
     └── python39/
     ```

## Notes

- **Only Latest Versions**: The script downloads only the latest compatible version of each package for each Python version.
- **Dependencies**: The script uses `--no-deps` to skip dependencies for faster and targeted downloads. Ensure all desired packages are listed explicitly in `requirements.txt`.
- **Temporary Requirement Files**: Temporary requirement files (`requirements_temp.txt`) are created for each Python version and removed after use.

## Troubleshooting

If you encounter any errors, ensure that:
- `pip3` is correctly installed and accessible in your system's PATH.
- The `requirements.txt` file is formatted correctly.

Enjoy organized package management with this Python utility!
