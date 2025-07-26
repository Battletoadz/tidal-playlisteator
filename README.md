# 🎵 1001tracklists to Tidal Playlist Creator

Automatically create Tidal playlists from 1001tracklists.com URLs with smart track matching and rate limiting.

  ```bash
   python SPEEDOPTIMIZED.py  # For fast processing
   # or
   python STABLESLOW.py      # For maximum track finding
   ```

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Dependencies
- Python 3.6+
- Selenium 4.34
- Firefox browser 
- geckodriver (Firefox WebDriver)
- Tidal subscription and API credentials

## Installation

### 1. Install geckodriver
```bash

# Arch Linux
sudo pacman -S geckodriver"
   #or optionally build git branch with AUR
   # yay -S geckodriver-git

# macOS with Homebrew
brew install geckodriver

# Ubuntu/Debian
sudo apt-get install firefox-geckodriver

# Windows - Download from: https://github.com/mozilla/geckodriver/releases
# Extract to a folder in your PATH

```

### 2. Get Tidal API Credentials
1. Go to [Tidal Developer Portal](https://developer.tidal.com/)
2. Create a developer account
3. Create a new application  
4. Copy your **Client ID** and **Client Secret**

### 3. Install Python modules

```bash
# Really only necessary to explicitly install tidalapi, selenium, and python-dotenv.
# other modules are usually automatic

pip install -r requirements.txt
```
## Alternatively: Build from source

### Clone
```bash
git clone https://github.com/Battletoadz/tidal-playlisteator.git
cd tidal-playlisteator
```
### Create your python env and enable
```bash
#installing python modules globally can really mess with you and is not recommended
python -m venv ~/$yourfolder

source ~/../bin/activate
```
### install python modules
```bash
pip install -r requirements.txt
```
### configure and run
```bash
# Copy the sample config
cp sample.env conf.env

# Edit conf.env with your details:
# - Get Tidal API credentials from: https://developer.tidal.com/
# - Add your 1001tracklists.com URLs
nano conf.env  # or use any text editor
```

## Features
- 🚀 **Two Speed Modes**: Fast processing or maximum track finding
- 🎯 **Smart Track Matching**: Multiple search strategies with scoring
- ⚡ **Rate Limiting**: Prevents API flooding and "data" errors  
- 🔄 **Duplicate Removal**: Automatically removes duplicate tracks
- 📝 **Interactive Setup**: Runtime playlist naming and configuration
- 🛠️ **Flexible Config**: Support for both `.env` and `.ini` files

## Configuration
supports env and ini

### Using conf.env (recommended)

Edit your existing `conf.env` file:

```env
TIDAL_CLIENT_ID=your_actual_client_id
TIDAL_CLIENT_SECRET=your_actual_client_secret
PLAYLIST_NAME=My Awesome Playlist
TRACKLIST_URLS=https://www.1001tracklists.com/tracklist/example1.html,https://www.1001tracklists.com/tracklist/example2.html
```
### Using conf.ini
Edit the `conf.ini` file:
```ini
[tidal]
client_id = your_actual_client_id
client_secret = your_actual_client_secret
playlist_name = 'My Awesome Playlist'
[tracklists]
# comma seperated list of URLs
urls = https://www.1001tracklists.com/tracklist/example1.html,https://www.1001tracklists.com/tracklist/example2.html
```
## Usage

### Basic Usage (with configuration file)
```bash
python SPEEDOPTIMIZED.py
```
### Command Line Arguments
You can override configuration file settings:
```bash
python SPEEDOPTIMIZED.py --playlist-name "" --tracklist-urls ""
```
### Create Sample Configuration Files
```bash
python SPEEDOPTIMIZED.py --create-config
```
### Options
- `--client-id`
- `--client-secret`
- `--playlist-name`
- `--tracklist-urls`
- `--config-file`
- `--create-config`
- `--no-headless`
## Help
- **Rate limiting**: If you get "data" errors, use `STABLESLOW.py` for more conservative timing
- Make sure Firefox is installed
- Ensure geckodriver is in your PATH
- Try running with `--no-headless` to see what's happening
### Tidal 
- Verify your Client ID and Client Secret are correct
- Make sure you complete the OAuth flow in your browser
- Check that your Tidal account has playlist creation permissions
### Track Not Found
- Some tracks may not be available on Tidalheadless
- Track matching is done by searching "Artist - Title"
- **Rate limiting**: If you get "data" errors, use `STABLESLOW.py` for more conservative timing
- **Headless**: Run with arg --no-headless for debug info
- **Multiple tracklists**: The script automatically removes duplicates across all URLs
- **Retry failed tracks**: Run the script multiple times - different search strategies may find previously missed tracks
##### How It Works
1. **Scrape**The script uses Selenium to scrape track information from 1001tracklists.com
2. **Deduplication**: Removes duplicate tracks based on artist and title
3. **Tidal Integration**: Authenticates with Tidal using OAuth
4. **Playlist Creation**: Searches for each track on Tidal and adds found tracks to a new playlist

## Driver's License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer
Please don't break the law. This tool is for personal use only. Respect all documentation for the applied APIs. 

Script uses sensitive cryptographic keys and stores them in local files for operation so USE WITH CAUTION. you've been warned.

## Links
- [tidalapi](https://github.com/tamland/python-tidal) - Python library for Tidal API
- [Selenium](https://selenium.dev/) - Web scraping framework
- [1001tracklists.com](https://1001tracklists.com/) - DJ tracklist database
