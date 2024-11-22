import subprocess
import os
import shutil
import re

def parse_requirements(requirements_file):
    """
    Analyse le fichier requirements.txt et groupe les paquets par compatibilité avec la version de Python.
    """
    print(f"Analyse du fichier de dépendances '{requirements_file}'...")
    packages = {}
    with open(requirements_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ';' in line:
                package_spec, condition = line.split(';')
                package_name = package_spec.strip().split('==')[0]  # Ignore la spécification de version
                condition = condition.strip()
                if 'python_version' in condition:
                    version_match = re.search(r'python_version\s*([!=<>]+)\s*([\'"]?)([\d\.]+)\2', condition)
                    if version_match:
                        operator = version_match.group(1)
                        version = version_match.group(3)
                        if operator == '==':
                            print(f"Le paquet '{package_name}' est pour Python {version}.")
                            packages.setdefault(version, set()).add(package_name)
                        else:
                            print(f"Le paquet '{package_name}' a un opérateur '{operator}' non supporté, ignoré.")
                    else:
                        print(f"Impossible d'analyser la condition '{condition}' pour le paquet '{package_name}', ignoré.")
                else:
                    print(f"Le paquet '{package_name}' a une condition non supportée '{condition}', ignoré.")
            else:
                # Ignore les spécifications de version pour prendre la dernière version disponible
                package_name = line.split('==')[0]
                for version in target_versions:
                    packages.setdefault(version, set()).add(package_name)
                    print(f"Le paquet '{package_name}' ajouté pour Python {version}.")
    print("Analyse terminée.")
    return packages

def download_packages(python_version, target_dir, package_list):
    """
    Télécharge les dernières versions des paquets spécifiés pour une version de Python donnée et les stocke dans un répertoire cible.
    """
    print(f"Préparation du téléchargement des paquets pour Python {python_version}...")
    os.makedirs(target_dir, exist_ok=True)

    for package in package_list:
        try:
            print(f"Téléchargement du paquet '{package}' pour Python {python_version}...")
            subprocess.check_call([
                'pip3', 'download',
                package,
                '-d', target_dir,
                '--no-deps',
                '--python-version', python_version.replace('.', ''),
                '--no-cache-dir',
                '--only-binary=:all:',
            ])
            print(f"Paquet '{package}' téléchargé avec succès pour Python {python_version}.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors du téléchargement du paquet '{package}' pour Python {python_version}: {e}")

    print(f"Organisation des paquets téléchargés dans '{target_dir}'...")
    organize_downloaded_packages(target_dir)
    print(f"Organisation terminée pour Python {python_version}.")

def organize_downloaded_packages(target_dir):

    # Expression régulière pour extraire le nom du package
    pattern = re.compile(r'^(?P<nom>.+?)-\d')

    # Parcourt tous les fichiers du répertoire cible
    for fichier in os.listdir(target_dir):
        chemin_fichier = os.path.join(target_dir, fichier)
        # Vérifie si c'est un fichier .whl ou .tar.gz
        if (fichier.endswith('.whl') or fichier.endswith('.tar.gz')) and os.path.isfile(chemin_fichier):
            # Utilise l'expression régulière pour extraire le nom du package
            match = pattern.match(fichier)
            if match:
                nom_package = match.group('nom')
                # Remplace les underscores par des tirets
                nom_dossier = nom_package.replace('_', '-')
                # Crée le dossier s'il n'existe pas
                chemin_dossier = os.path.join(target_dir, nom_dossier)
                os.makedirs(chemin_dossier, exist_ok=True)
                # Déplace le fichier dans le dossier correspondant
                shutil.move(chemin_fichier, os.path.join(chemin_dossier, fichier))
            else:
                print(f"Impossible d'extraire le nom du package pour le fichier : {fichier}")
        else:
            pass  # Ignore les non-fichiers

def parse_package_name(filename):
    """
    Extrait le nom du paquet à partir du nom de fichier en utilisant des expressions régulières.
    """
    # Gère les fichiers wheel
    wheel_match = re.match(r'([A-Za-z0-9_\-\.]+)-([\d\.\-]+)(?:-.*)?\.whl', filename)
    if wheel_match:
        package_name = wheel_match.group(1)
        return package_name.lower()
    # Gère les distributions source
    sdist_match = re.match(r'([A-Za-z0-9_\-\.]+)-([\d\.\-]+)\.(?:tar\.gz|zip|tar\.bz2|tar\.xz)', filename)
    if sdist_match:
        package_name = sdist_match.group(1)
        return package_name.lower()
    return None

# Définit les versions cibles de Python
target_versions = ['2.7', '3.6', '3.8', '3.9']

print("Démarrage du script de téléchargement des paquets...")

# Analyse du fichier requirements.txt
packages_by_version = parse_requirements('requirements.txt')

# Téléchargement et organisation des paquets pour chaque version de Python
for version in target_versions:
    package_list = packages_by_version.get(version, set())
    if package_list:
        target_dir = f'./python{version.replace(".", "")}/'
        print(f"Téléchargement des paquets pour Python {version}...")
        download_packages(version, target_dir, package_list)
    else:
        print(f"Aucun paquet à télécharger pour Python {version}.")
