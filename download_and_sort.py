import subprocess
import os
import shutil
import re

def parse_requirements(requirements_file):
    """
    Parses the requirements.txt file and groups packages by Python version compatibility.
    """
    print(f"Analyzing the dependency file '{requirements_file}'...")
    packages = {}
    with open(requirements_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ';' in line:
                package_spec, condition = line.split(';')
                package_name = package_spec.strip().split('==')[0]  # Ignore version specification
                condition = condition.strip()
                if 'python_version' in condition:
                    version_match = re.search(r'python_version\s*([!=<>]+)\s*([\'"]?)([\d\.]+)\2', condition)
                    if version_match:
                        operator = version_match.group(1)
                        version = version_match.group(3)
                        if operator == '==':
                            print(f"Package '{package_name}' is for Python {version}.")
                            packages.setdefault(version, set()).add(package_name)
                        else:
                            print(f"Package '{package_name}' has an unsupported operator '{operator}', ignored.")
                    else:
                        print(f"Unable to parse condition '{condition}' for package '{package_name}', ignored.")
                else:
                    print(f"Package '{package_name}' has an unsupported condition '{condition}', ignored.")
            else:
                # Ignore version specifications to take the latest available version
                package_name = line.split('==')[0]
                for version in target_versions:
                    packages.setdefault(version, set()).add(package_name)
                    print(f"Package '{package_name}' added for Python {version}.")
    print("Analysis completed.")
    return packages

def download_packages(python_version, target_dir, package_list):
    """
    Downloads the latest versions of the specified packages for a given Python version and stores them in a target directory.
    """
    print(f"Preparing to download packages for Python {python_version}...")
    os.makedirs(target_dir, exist_ok=True)

    for package in package_list:
        try:
            print(f"Downloading package '{package}' for Python {python_version}...")
            subprocess.check_call([
                'pip3', 'download',
                package,
                '-d', target_dir,
                '--no-deps',
                '--python-version', python_version.replace('.', ''),
                '--no-cache-dir',
                '--only-binary=:all:',
            ])
            print(f"Package '{package}' downloaded successfully for Python {python_version}.")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading package '{package}' for Python {python_version}: {e}")

    print(f"Organizing downloaded packages in '{target_dir}'...")
    organize_downloaded_packages(target_dir)
    print(f"Organization completed for Python {python_version}.")

def organize_downloaded_packages(target_dir):
    """
    Moves downloaded package files into subdirectories based on their package names.
    """
    # Regular expression to extract the package name
    pattern = re.compile(r'^(?P<name>.+?)-\d')

    # Iterate over all files in the target directory
    for file in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file)
        # Check if it's a .whl or .tar.gz file
        if (file.endswith('.whl') or file.endswith('.tar.gz')) and os.path.isfile(file_path):
            # Use the regular expression to extract the package name
            match = pattern.match(file)
            if match:
                package_name = match.group('name')
                # Replace underscores with hyphens
                folder_name = package_name.replace('_', '-')
                # Create the folder if it doesn't exist
                folder_path = os.path.join(target_dir, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                # Move the file into the corresponding folder
                shutil.move(file_path, os.path.join(folder_path, file))
            else:
                print(f"Unable to extract package name for file: {file}")
        else:
            pass  # Ignore non-files

def parse_package_name(filename):
    """
    Extracts the package name from the filename using regular expressions.
    """
    # Handles wheel files
    wheel_match = re.match(r'([A-Za-z0-9_\-\.]+)-([\d\.\-]+)(?:-.*)?\.whl', filename)
    if wheel_match:
        package_name = wheel_match.group(1)
        return package_name.lower()
    # Handles source distributions
    sdist_match = re.match(r'([A-Za-z0-9_\-\.]+)-([\d\.\-]+)\.(?:tar\.gz|zip|tar\.bz2|tar\.xz)', filename)
    if sdist_match:
        package_name = sdist_match.group(1)
        return package_name.lower()
    return None

# Defines the target Python versions
target_versions = ['2.7', '3.6', '3.8', '3.9']

print("Starting the package download script...")

# Parse the requirements.txt file
packages_by_version = parse_requirements('requirements.txt')

# Download and organize packages for each Python version
for version in target_versions:
    package_list = packages_by_version.get(version, set())
    if package_list:
        target_dir = f'./python{version.replace(".", "")}/'
        print(f"Downloading packages for Python {version}...")
        download_packages(version, target_dir, package_list)
    else:
        print(f"No packages to download for Python {version}.")
