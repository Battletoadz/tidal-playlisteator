# 🎵 1001tracklists to Tidal Playlist Creator

Automatically create Tidal playlists from 1001tracklists.com URLs with smart track matching and rate limiting.

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🚀 **Two Speed Modes**: Fast processing or maximum track finding
- 🎯 **Smart Track Matching**: Multiple search strategies with scoring
- ⚡ **Rate Limiting**: Prevents API flooding and "data" errors  
- 🔄 **Duplicate Removal**: Automatically removes duplicate tracks
- 📝 **Interactive Setup**: Runtime playlist naming and configuration
- 🛠️ **Flexible Config**: Support for both `.env` and `.ini` files

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/tidal-playlisteator.git
   cd tidal-playlisteator
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv .
   source bin/activate  # On Windows: bin/activate.bat
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your credentials**:
   ```bash
   cp sample.env conf.env
   # Edit conf.env with your Tidal API credentials and tracklist URLs
   ```

5. **Run the script**:
   ```bash
   python SPEEDOPTIMIZED.py  # For fast processing
   # or
   python STABLESLOW.py      # For maximum track finding
   ```

## 📋 Requirements

- Python 3.6+
- Firefox browser
- geckodriver (Firefox WebDriver)
- Tidal subscription and API credentials

## 🔧 Installation

### 1. Install geckodriver
```bash
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

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Configuration

The script supports both `.env` and `.ini` configuration files. Choose one method:

### Option 1: Using conf.env (recommended)

Edit your existing `conf.env` file:

```env
TIDAL_CLIENT_ID=your_actual_client_id
TIDAL_CLIENT_SECRET=your_actual_client_secret
PLAYLIST_NAME=My Awesome Playlist
TRACKLIST_URLS=https://www.1001tracklists.com/tracklist/example1.html,https://www.1001tracklists.com/tracklist/example2.html
```

### Option 2: Using conf.ini

Edit the `conf.ini` file:

```ini
[tidal]
client_id = your_actual_client_id
client_secret = your_actual_client_secret
playlist_name = My Awesome Playlist

[tracklists]
urls = https://www.1001tracklists.com/tracklist/example1.html,https://www.1001tracklists.com/tracklist/example2.html
```

## 🎛️ Available Versions

### ⚡ SPEEDOPTIMIZED.py (Recommended)
- **Faster processing**: ~40% faster than stable version
- **Reduced delays**: 0.1-0.2s between requests
- **Higher match threshold**: 40% confidence for faster decisions
- **Best for**: Popular tracks, large playlists, when speed matters

### 🐌 STABLESLOW.py (Maximum Coverage)
- **Maximum track finding**: More thorough search strategies
- **Conservative delays**: 0.5-2s between requests  
- **Lower match threshold**: 30% confidence for broader matching
- **Best for**: Obscure tracks, small playlists, when quality > speed

## Usage

### Basic Usage (with configuration file)

```bash
python dev.py
```

### Command Line Arguments

You can override configuration file settings:

```bash
python dev.py --playlist-name "My Custom Playlist" --tracklist-urls https://www.1001tracklists.com/tracklist/example.html
```

### Show Browser Window (for debugging)

```bash
python dev.py --no-headless
```

### Create Sample Configuration Files

```bash
python dev.py --create-config
```

## Available Options

- `--client-id`: Tidal Client ID
- `--client-secret`: Tidal Client Secret  
- `--playlist-name`: Name for the Tidal playlist
- `--tracklist-urls`: Space-separated list of 1001tracklists URLs
- `--config-file`: Path to custom configuration file
- `--create-config`: Generate sample configuration files
- `--no-headless`: Show browser window (useful for debugging)

## How It Works

1. **Scraping**: The script uses Selenium to scrape track information from 1001tracklists.com
2. **Deduplication**: Removes duplicate tracks based on artist and title
3. **Tidal Integration**: Authenticates with Tidal using OAuth
4. **Playlist Creation**: Searches for each track on Tidal and adds found tracks to a new playlist

## Troubleshooting

### Browser Issues

- Make sure Firefox is installed
- Ensure geckodriver is in your PATH
- Try running with `--no-headless` to see what's happening

### Tidal Authentication

- Verify your Client ID and Client Secret are correct
- Make sure you complete the OAuth flow in your browser
- Check that your Tidal account has playlist creation permissions

### Track Not Found

- Some tracks may not be available on Tidal
- The script will report which tracks couldn't be found
- Track matching is done by searching "Artist - Title"

## 📊 Example Output

```bash
$ python SPEEDOPTIMIZED.py

Configuration loaded:
- Playlist name: Deep House Mix 2025
- Tracklist URLs: 3

Current playlist name: 'Deep House Mix 2025'
Press Enter to keep, or type new name: 

Scraping: https://www.1001tracklists.com/tracklist/example1.html
Found 45 tracks
Scraping: https://www.1001tracklists.com/tracklist/example2.html  
Found 38 tracks
Scraping: https://www.1001tracklists.com/tracklist/example3.html
Found 52 tracks

Total tracks found: 135
Unique tracks: 118

Please log in to Tidal in your browser...
Visit https://link.tidal.com/XXXXX to log in...

Processing track 1/118: Kx5 ft. HAYLA - Escape(Spencer Brown Remix)
  Searching: 'Kx5 ft. HAYLA Escape(Spencer Brown Remix)'
    Found 3 results
✓ Added: Kx5 ft. HAYLA - Escape(Spencer Brown Remix) -> Escape (Spencer Brown Remix) (score: 0.85)

Processing track 2/118: Jamie Jones & The Martinez Brothers - Bappi
  Searching: '"Jamie Jones & The Martinez Brothers" "Bappi"'
    Found 1 results
✓ Added: Jamie Jones & The Martinez Brothers - Bappi -> Bappi (score: 0.90)

...

Playlist created: Deep House Mix 2025
Tracks added: 89
Tracks not found: 29
Playlist creation completed successfully!
```

## 💡 Tips & Tricks

- **Use descriptive playlist names** to organize your music library
- **Multiple tracklists**: The script automatically removes duplicates across all URLs
- **Missing tracks**: Some tracks may not be available on Tidal due to licensing
- **Retry failed tracks**: Run the script multiple times - different search strategies may find previously missed tracks
- **Rate limiting**: If you get "data" errors, use `STABLESLOW.py` for more conservative timing
- **Large playlists**: For 100+ tracks, consider running during off-peak hours

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for personal use only. Please respect Tidal's Terms of Service and 1001tracklists.com's robots.txt. The developers are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- [tidalapi](https://github.com/tamland/python-tidal) - Python library for Tidal API
- [Selenium](https://selenium.dev/) - Web scraping framework
- [1001tracklists.com](https://1001tracklists.com/) - DJ tracklist database