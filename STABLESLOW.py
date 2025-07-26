#!/usr/bin/env python3
"""
1001tracklists.com to Tidal Playlist Creator

This script scrapes track information from 1001tracklists.com and creates
a Tidal playlist with those tracks.

Requirements:
- selenium
- tidalapi
- python-dotenv
- configparser
- geckodriver (Firefox WebDriver)
"""

import argparse
import sys
import os
import json
import time
import configparser
from pathlib import Path
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import tidalapi


class Config:
    """Configuration manager that supports both .env and .ini files"""

    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.playlist_name = None
        self.tracklist_urls = []

    def load_from_env(self, env_file='.env'):
        """Load configuration from .env file"""
        if os.path.exists(env_file):
            load_dotenv(env_file)
            self.client_id = os.getenv('TIDAL_CLIENT_ID')
            self.client_secret = os.getenv('TIDAL_CLIENT_SECRET')
            self.playlist_name = os.getenv('PLAYLIST_NAME', 'My 1001tracklists Playlist')
            urls = os.getenv('TRACKLIST_URLS', '')
            self.tracklist_urls = [url.strip() for url in urls.split(',') if url.strip()]
            return True
        return False

    def load_from_ini(self, ini_file='conf.ini'):
        """Load configuration from .ini file"""
        if os.path.exists(ini_file):
            config = configparser.ConfigParser()
            config.read(ini_file)

            if 'tidal' in config:
                self.client_id = config['tidal'].get('client_id')
                self.client_secret = config['tidal'].get('client_secret')
                self.playlist_name = config['tidal'].get('playlist_name', 'My 1001tracklists Playlist')

            if 'tracklists' in config:
                urls = config['tracklists'].get('urls', '')
                self.tracklist_urls = [url.strip() for url in urls.split(',') if url.strip()]

            return True
        return False

    def load_from_args(self, args):
        """Load configuration from command line arguments"""
        if args.client_id:
            self.client_id = args.client_id
        if args.client_secret:
            self.client_secret = args.client_secret
        if args.playlist_name:
            self.playlist_name = args.playlist_name
        if args.tracklist_urls:
            self.tracklist_urls = args.tracklist_urls

    def is_valid(self):
        """Check if configuration is complete"""
        return all([
            self.client_id,
            self.client_secret,
            self.playlist_name,
            self.tracklist_urls
        ])

    def create_sample_files(self):
        """Create sample configuration files"""
        # Create sample .env file
        env_content = """# Tidal API Credentials
TIDAL_CLIENT_ID=your_client_id_here
TIDAL_CLIENT_SECRET=your_client_secret_here
PLAYLIST_NAME=My 1001tracklists Playlist
TRACKLIST_URLS=https://www.1001tracklists.com/tracklist/example1.html,https://www.1001tracklists.com/tracklist/example2.html
"""

        # Create sample .ini file
        ini_content = """[tidal]
client_id = your_client_id_here
client_secret = your_client_secret_here
playlist_name = My 1001tracklists Playlist

[tracklists]
urls = https://www.1001tracklists.com/tracklist/example1.html,https://www.1001tracklists.com/tracklist/example2.html
"""

        with open('sample.env', 'w') as f:
            f.write(env_content)

        with open('sample.ini', 'w') as f:
            f.write(ini_content)

        print("Created sample configuration files:")
        print("- sample.env")
        print("- sample.ini")
        print("\nRename one to 'conf.env' or 'conf.ini' and fill in your credentials.")


class TracklistScraper:
    """Scraper for 1001tracklists.com"""

    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless

    def start_browser(self):
        """Initialize the Firefox WebDriver"""
        try:
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            self.driver = webdriver.Firefox(options=options)
            return True
        except WebDriverException as e:
            print(f"Error starting browser: {e}")
            print("Make sure geckodriver is installed and Firefox is available.")
            return False

    def stop_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

    def scrape_tracklist(self, url):
        """Scrape tracks from a 1001tracklists URL"""
        if not self.driver:
            print("Browser not started!")
            return []

        print(f"Scraping: {url}")
        tracks = []

        try:
            self.driver.get(url)
            time.sleep(5)

            for row in self.driver.find_elements(By.CSS_SELECTOR, 'div.tlpTog.bItm.tlpItem'):
                try:
                    # Everything is in one span
                    trackval = row.find_element(By.CSS_SELECTOR, '.trackValue.notranslate.blueTxt').text.strip()
                    # It's usually "ARTIST(S) - TITLE"
                    if " - " in trackval:
                        artist, title = trackval.split(" - ", 1)
                    else:
                        # fallback if weird format
                        artist = trackval
                        title = ""
                    tracks.append({'artist': artist.strip(), 'title': title.strip()})
                except NoSuchElementException:
                    continue

        except Exception as e:
            print(f"Error scraping {url}: {e}")

        print(f"Found {len(tracks)} tracks")
        return tracks




class TidalPlaylistCreator:
    """Creates Tidal playlists from track lists"""

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = None

    def authenticate(self):
        """Authenticate with Tidal"""
        try:
            self.session = tidalapi.Session()
            print("Please log in to Tidal in your browser...")
            self.session.login_oauth_simple()
            return True
        except Exception as e:
            print(f"Tidal authentication failed: {e}")
            return False

    def create_playlist(self, playlist_name, tracks, description=""):
        """Create a Tidal playlist with the given tracks"""
        if not self.session:
            print("Not authenticated with Tidal!")
            return False

        try:
            # Try alternative approach - create playlist using session request directly
            import requests

            # Get user playlists first to see the format
            user = self.session.user

            # Try creating playlist with minimal request
            try:
                # Method 1: Try the standard approach but catch specific error
                playlist = user.create_playlist(playlist_name, description)
            except Exception as e:
                print(f"Standard method failed: {e}")

                # Method 2: Try creating without description first
                try:
                    playlist = user.create_playlist(playlist_name, "")
                except Exception as e2:
                    print(f"No description method failed: {e2}")

                    # Method 3: Use session's internal request method
                    try:
                        session_id = self.session.session_id
                        country_code = self.session.country_code

                        url = f"https://api.tidal.com/v1/users/{user.id}/playlists"
                        headers = {
                            'X-Tidal-Token': self.session.access_token,
                            'Authorization': f'Bearer {self.session.access_token}',
                            'Content-Type': 'application/json'
                        }
                        data = {
                            'title': playlist_name,
                            'description': description[:500]  # Limit description length
                        }

                        response = requests.post(url, json=data, headers=headers)
                        if response.status_code == 201:
                            playlist_data = response.json()
                            # Create a mock playlist object for adding tracks
                            class MockPlaylist:
                                def __init__(self, uuid, session):
                                    self.uuid = uuid
                                    self.session = session

                                def add(self, track_ids):
                                    add_url = f"https://api.tidal.com/v1/playlists/{self.uuid}/items"
                                    add_headers = {
                                        'X-Tidal-Token': self.session.access_token,
                                        'Authorization': f'Bearer {self.session.access_token}',
                                        'Content-Type': 'application/json'
                                    }
                                    add_data = {'trackIds': track_ids}
                                    return requests.post(add_url, json=add_data, headers=add_headers)

                            playlist = MockPlaylist(playlist_data['uuid'], self.session)
                            print(f"Created playlist using direct API: {playlist_name}")
                        else:
                            print(f"Direct API failed: {response.status_code} - {response.text}")
                            return False
                    except Exception as e3:
                        print(f"Direct API method failed: {e3}")
                        return False

            added_count = 0
            not_found_count = 0

            # Use improved search logic with multiple strategies and rate limiting
            for i, tr in enumerate(tracks):
                print(f"Processing track {i+1}/{len(tracks)}: {tr['artist']} - {tr['title']}")
                track_found = False

                # Smart search strategies - avoid overly generic queries
                search_queries = []

                # Always start with full artist + title combinations
                search_queries.extend([
                    f"{tr['artist']} {tr['title']}",  # Original
                    f"{tr['artist']} - {tr['title']}",  # With dash
                    f'"{tr['artist']}" "{tr['title']}"',  # Quoted for exact match
                ])

                # Add variations only if title is long enough to be specific
                if len(tr['title']) > 8:  # Avoid generic short titles like "Midnight"
                    search_queries.extend([
                        f"{tr['title']} {tr['artist']}",  # Reversed
                        tr['title'],  # Title only if specific enough
                    ])

                # Add remix/version variations
                if '(' in tr['title']:
                    base_title = tr['title'].split('(')[0].strip()
                    if len(base_title) > 8:  # Only if base title is specific enough
                        search_queries.append(f"{tr['artist']} {base_title}")

                if '[' in tr['title']:
                    base_title = tr['title'].split('[')[0].strip()
                    if len(base_title) > 8:
                        search_queries.append(f"{tr['artist']} {base_title}")

                for query_idx, query in enumerate(search_queries):
                    if track_found:
                        break

                    # Rate limiting - wait between searches to avoid flooding
                    if query_idx > 0:
                        time.sleep(0.5)  # 500ms delay between searches

                    # Skip overly generic queries
                    if len(query.strip()) < 5:
                        continue

                    try:
                        print(f"  Searching: '{query}'")
                        search_result = self.session.search(query)

                        # Handle different response structures
                        tracks_list = []
                        if isinstance(search_result, dict):
                            if 'tracks' in search_result and search_result['tracks']:
                                tracks_list = search_result['tracks']
                            elif hasattr(search_result, 'tracks') and search_result.tracks:
                                tracks_list = search_result.tracks
                        elif hasattr(search_result, 'tracks'):
                            tracks_list = search_result.tracks

                        if tracks_list:
                            print(f"    Found {len(tracks_list)} results")
                            # Try to find the best match with better matching logic
                            for idx, tidal_track in enumerate(tracks_list[:10]):  # Check first 10 results
                                try:
                                    # Score the match quality
                                    match_score = self._calculate_match_score(tr, tidal_track)

                                    # Only add if it's a reasonable match
                                    if match_score > 0.3:  # Minimum threshold
                                        # Add track to playlist
                                        if hasattr(playlist, 'add'):
                                            result = playlist.add([tidal_track.id])
                                        else:
                                            # Fallback for direct API method
                                            result = playlist.add([tidal_track.id])

                                        print(f"✓ Added: {tr['artist']} - {tr['title']} -> {tidal_track.name} (score: {match_score:.2f})")
                                        added_count += 1
                                        track_found = True
                                        time.sleep(0.2)  # Brief pause after successful add
                                        break
                                    else:
                                        print(f"    Skipped: {tidal_track.name} (low score: {match_score:.2f})")

                                except Exception as add_error:
                                    print(f"    Failed to add track {tidal_track.name}: {add_error}")
                                    continue

                            if track_found:
                                break
                        else:
                            print(f"    No tracks found for: '{query}'")

                    except Exception as search_error:
                        if "data" in str(search_error).lower():
                            print(f"    Rate limited, waiting...")
                            time.sleep(2)  # Longer wait for rate limiting
                        else:
                            print(f"    Search error for '{query}': {search_error}")
                        continue

                if not track_found:
                    print(f"NOT FOUND after all strategies: {tr['artist']} - {tr['title']}")
                    not_found_count += 1

            print(f"\nPlaylist created: {playlist_name}")
            print(f"Tracks added: {added_count}")
            print(f"Tracks not found: {not_found_count}")

            return True

        except Exception as e:
            print(f"Error creating playlist: {e}")
            return False

    def _calculate_match_score(self, original_track, tidal_track):
        """Calculate how well a Tidal track matches the original track"""
        try:
            orig_artist = original_track['artist'].lower()
            orig_title = original_track['title'].lower()

            tidal_artist = tidal_track.artist.name.lower() if hasattr(tidal_track.artist, 'name') else str(tidal_track.artist).lower()
            tidal_title = tidal_track.name.lower()

            # Simple scoring based on substring matches
            artist_score = 0
            title_score = 0

            # Artist matching
            if orig_artist in tidal_artist or tidal_artist in orig_artist:
                artist_score = 0.8
            elif any(word in tidal_artist for word in orig_artist.split() if len(word) > 2):
                artist_score = 0.5

            # Title matching
            if orig_title in tidal_title or tidal_title in orig_title:
                title_score = 0.8
            elif any(word in tidal_title for word in orig_title.split() if len(word) > 2):
                title_score = 0.5

            # Bonus for exact matches
            if orig_artist == tidal_artist:
                artist_score = 1.0
            if orig_title == tidal_title:
                title_score = 1.0

            return (artist_score + title_score) / 2

        except Exception:
            return 0.1  # Low score if we can't compare


def remove_duplicates(tracks):
    """Remove duplicate tracks based on artist and title"""
    seen = set()
    unique_tracks = []

    for track in tracks:
        key = (track['artist'].lower(), track['title'].lower())
        if key not in seen:
            unique_tracks.append(track)
            seen.add(key)

    return unique_tracks


def main():
    parser = argparse.ArgumentParser(
        description="Create Tidal playlists from 1001tracklists.com URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Configuration:
  The script looks for configuration in this order:
  1. Command line arguments
  2. conf.ini file
  3. conf.env file

  Use --create-config to generate sample configuration files.
        """
    )

    parser.add_argument('--client-id', help='Tidal Client ID')
    parser.add_argument('--client-secret', help='Tidal Client Secret')
    parser.add_argument('--playlist-name', help='Name for the Tidal playlist')
    parser.add_argument('--tracklist-urls', nargs='+', help='1001tracklists URLs to scrape')
    parser.add_argument('--config-file', help='Path to configuration file (.ini or .env)')
    parser.add_argument('--create-config', action='store_true', help='Create sample configuration files')
    parser.add_argument('--no-headless', action='store_true', help='Show browser window (for debugging)')

    args = parser.parse_args()

    # Create sample config files if requested
    if args.create_config:
        config = Config()
        config.create_sample_files()
        return

    # Load configuration
    config = Config()

    # Try to load from specified config file or default locations
    config_loaded = False

    if args.config_file:
        if args.config_file.endswith('.ini'):
            config_loaded = config.load_from_ini(args.config_file)
        elif args.config_file.endswith('.env'):
            config_loaded = config.load_from_env(args.config_file)
    else:
        # Try default locations
        config_loaded = config.load_from_ini('conf.ini') or config.load_from_env('conf.env')

    # Override with command line arguments
    config.load_from_args(args)

    # Check if playlist name is missing and prompt for it
    if not config.playlist_name:
        config.playlist_name = input("Enter playlist name: ").strip()
        if not config.playlist_name:
            config.playlist_name = "My 1001tracklists Playlist"

    # Validate configuration
    if not config.is_valid():
        print("Error: Missing required configuration!")
        print("\nRequired:")
        print("- Tidal Client ID")
        print("- Tidal Client Secret")
        print("- Playlist name")
        print("- At least one tracklist URL")
        print("\nUse --create-config to generate sample configuration files.")
        print("Or provide values via command line arguments.")
        sys.exit(1)

    print(f"Configuration loaded:")
    print(f"- Playlist name: {config.playlist_name}")
    print(f"- Tracklist URLs: {len(config.tracklist_urls)}")

    # Allow runtime playlist name change
    change_name = input(f"\nCurrent playlist name: '{config.playlist_name}'\nPress Enter to keep, or type new name: ").strip()
    if change_name:
        config.playlist_name = change_name
        print(f"Updated playlist name to: '{config.playlist_name}'")

    # Scrape tracks
    scraper = TracklistScraper(headless=not args.no_headless)

    if not scraper.start_browser():
        sys.exit(1)

    all_tracks = []
    try:
        for url in config.tracklist_urls:
            tracks = scraper.scrape_tracklist(url)
            all_tracks.extend(tracks)
    finally:
        scraper.stop_browser()

    if not all_tracks:
        print("No tracks found!")
        sys.exit(1)

    # Remove duplicates
    unique_tracks = remove_duplicates(all_tracks)
    print(f"\nTotal tracks found: {len(all_tracks)}")
    print(f"Unique tracks: {len(unique_tracks)}")

    # Create Tidal playlist
    creator = TidalPlaylistCreator(config.client_id, config.client_secret)

    if not creator.authenticate():
        sys.exit(1)

    description = f"Created from 1001tracklists: {', '.join(config.tracklist_urls)}"

    if creator.create_playlist(config.playlist_name, unique_tracks, description):
        print("Playlist creation completed successfully!")
    else:
        print("Playlist creation failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
