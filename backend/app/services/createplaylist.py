#!/usr/bin/env python3
"""
YouTube Playlist Creator
Creates a new playlist and adds videos using YouTube Data API v3
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# API Configuration
CLIENT_SECRETS_FILE = "client-secret.json"
CREDENTIALS_PICKLE_FILE = "token.pickle"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


class YouTubePlaylistCreator:
    def __init__(self):
        self.youtube = self.get_authenticated_service()

    @staticmethod
    def get_authenticated_service():
        """
        Authenticate and return YouTube API service object.
        Saves credentials to pickle file for reuse.
        """
        credentials = None
        
        # Load saved credentials if they exist
        if os.path.exists(CREDENTIALS_PICKLE_FILE):
            with open(CREDENTIALS_PICKLE_FILE, 'rb') as token:
                credentials = pickle.load(token)
        
        # Refresh or get new credentials if needed
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if not os.path.exists(CLIENT_SECRETS_FILE):
                    raise FileNotFoundError(
                        f"Please download OAuth credentials as '{CLIENT_SECRETS_FILE}' "
                        "from Google Cloud Console"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRETS_FILE, SCOPES
                )
                credentials = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(CREDENTIALS_PICKLE_FILE, 'wb') as token:
                pickle.dump(credentials, token)
        
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def create_playlist(self, title, description="", privacy_status="private"):
        """
        Create a new YouTube playlist.
        
        Args:
            title: Playlist title
            description: Playlist description (optional)
            privacy_status: 'public', 'private', or 'unlisted'
        
        Returns:
            Playlist ID of the created playlist
        """
        try:
            request = self.youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "defaultLanguage": "en"
                    },
                    "status": {
                        "privacyStatus": privacy_status
                    }
                }
            )
            response = request.execute()
            playlist_id = response['id']
            print(f"✓ Created playlist: '{title}'")
            print(f"  Playlist ID: {playlist_id}")
            print(f"  URL: https://youtube.com/playlist?list={playlist_id}")
            return playlist_id
        
        except HttpError as e:
            print(f"✗ Error creating playlist: {e}")
            return None

    def add_video_to_playlist(self, playlist_id, video_id):
        """
        Add a video to an existing playlist.
        
        Args:
            playlist_id: Target playlist ID
            video_id: YouTube video ID to add
        
        Returns:
            True if successful, False otherwise
        """
        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            response = request.execute()
            print(f"✓ Added video: {video_id}")
            return True
        
        except HttpError as e:
            print(f"✗ Error adding video {video_id}: {e}")
            return False

    def list_user_playlists(self, max_results=25):
        """
        List all playlists owned by the authenticated user.
        
        Args:
            max_results: Maximum number of playlists to retrieve
        """
        try:
            request = self.youtube.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results
            )
            response = request.execute()
            
            print(f"\n{'='*60}")
            print(f"Your Playlists ({len(response.get('items', []))}):")
            print(f"{'='*60}")
            
            for playlist in response.get('items', []):
                title = playlist['snippet']['title']
                playlist_id = playlist['id']
                video_count = playlist['contentDetails']['itemCount']
                print(f"\n• {title}")
                print(f"  ID: {playlist_id}")
                print(f"  Videos: {video_count}")
                print(f"  URL: https://youtube.com/playlist?list={playlist_id}")
        
        except HttpError as e:
            print(f"✗ Error listing playlists: {e}")
     

if __name__ == "__main__":
    yt = YouTubePlaylistCreator()
    yt.create_playlist("My Awesome Playlist", "Created via Python YouTube API script", "private")
    yt.add_video_to_playlist("My Awesome Playlist", "dQw4w9WgXcQ")
    yt.list_user_playlists()
