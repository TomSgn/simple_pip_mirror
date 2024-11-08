# Download and Organize Python Packages
This script is the FASTEST way to create pip-mirror, for every version of python !

This script downloads packages listed in `requirements.txt` and organizes them by Python version into folders `python27`, `python36`, `python38`, and `python39`. Each package is also categorized into a folder with its own name, providing a structured mirror layout.

## Usage

1. Place your `requirements.txt` file in the same directory as the script.
2. Run the script using Python 3:
   ```bash
   python3 download_and_classify_packages.py
   ```
3. After running, packages will be organized into subfolders within each Python version directory.

## Configuring `pip` to Use a Mirror

To configure `pip` to use your mirror, you can set up a `pip.conf` file to point to the directory where packages are stored.

### Example `pip.conf`

#### For Linux or macOS
Save this file as `~/.pip/pip.conf`:

```ini
[global]
index-url = http://<mirror_url>/simple
trusted-host = <mirror_url>
timeout = 600
```

#### For Windows
Save this file as `%APPDATA%\pip\pip.ini`:

```ini
[global]
index-url = http://<mirror_url>/simple
trusted-host = <mirror_url>
timeout = 600
```

### Explanation of Parameters

- **index-url**: Set this to the URL of your local package mirror. Replace `<mirror_url>` with the domain or IP of your mirror server.
- **trusted-host**: If your mirror is on a server without HTTPS, specify it here to bypass security warnings. Replace `<mirror_url>` with the mirror’s address.
- **timeout**: Set a higher timeout to accommodate slower responses, if needed.

### Example Usage

If your mirror is hosted locally, your `index-url` might look like this:
```ini
index-url = http://localhost:8080/simple
trusted-host = localhost
```

This configuration will direct `pip` to use the local mirror for package downloads, ensuring that the packages are sourced from your custom repository.

This example `pip.conf` can be easily adapted for any URL or mirror server. Make sure to replace `<mirror_url>` with the actual mirror URL you’re using.
