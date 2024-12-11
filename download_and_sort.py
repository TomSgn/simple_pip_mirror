import os
import subprocess
import sys
import re

# Check if requirements.txt exists
if not os.path.isfile('requirements.txt'):
    print("Le fichier requirements.txt est introuvable !")
    sys.exit(1)

# List of targeted Python versions
PYTHON_VERSIONS = ['27', '36', '38', '39']

# Dictionary to map versions to their details
PYTHON_DETAILS = {
    '27': {'version': '2.7', 'abi': 'cp27mu', 'platform': 'manylinux1_x86_64'},
    '36': {'version': '3.6', 'abi': 'cp36m', 'platform': 'manylinux1_x86_64'},
    '38': {'version': '3.8', 'abi': 'cp38', 'platform': 'manylinux2014_x86_64'},
    '39': {'version': '3.9', 'abi': 'cp39', 'platform': 'manylinux2014_x86_64'},
}

for version in PYTHON_VERSIONS:
    # Create the target directory
    dir_name = f'python{version}'
    os.makedirs(dir_name, exist_ok=True)

    if version not in PYTHON_DETAILS:
        print(f"Version Python non prise en charge : {version}")
        continue

    details = PYTHON_DETAILS[version]
    python_version = details['version']
    abi = details['abi']
    platform = details['platform']

    print(f"\nTéléchargement des paquets pour Python {python_version}...")

    # Read the requirements.txt file
    with open('requirements.txt', 'r') as req_file:
        packages = [line.strip() for line in req_file if line.strip() and not line.startswith('#')]

    # Download main packages
    for package in packages:
        cmd = [
            'python3', '-m', 'pip', 'download',
            '--dest', dir_name,
            '--python-version', python_version,
            '--abi', abi,
            '--implementation', 'cp',
            '--platform', platform,
            '--only-binary=:all:',
            package
        ]

        try:
            result = subprocess.run(
                cmd,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            if result.returncode != 0:
                print(f"Impossible de télécharger {package} pour Python {python_version}.")
                print(result.stderr)
                continue
        except Exception as e:
            print(f"Erreur lors du téléchargement de {package} pour Python {python_version}: {e}")
            continue

    # Organize packages like a pip mirror
    print(f"Organisation des paquets dans le dossier {dir_name}...")

    package_files = [f for f in os.listdir(dir_name) if f.endswith(('.whl', '.tar.gz', '.zip'))]

    for pkg_file in package_files:
        # Extract the package name
        match = re.match(r'^([A-Za-z0-9_.]+)-.+\.(whl|tar\.gz|zip)$', pkg_file)
        if match:
            pkg_name = match.group(1).lower().replace('_', '-')
            pkg_dir = os.path.join(dir_name, pkg_name)
            os.makedirs(pkg_dir, exist_ok=True)
            src_path = os.path.join(dir_name, pkg_file)
            dest_path = os.path.join(pkg_dir, pkg_file)
            if not os.path.exists(dest_path):
                os.rename(src_path, dest_path)

    print(f"Téléchargement et organisation terminés pour Python {python_version}.")

print("\nTous les paquets ont été téléchargés et organisés avec succès.")
