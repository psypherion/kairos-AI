import asyncio
from createplaylist import YouTubePlaylistCreator
from audiodownloader import AudioDownloader
from geminiServices import GeminiService
from transcript import Transcript
from ytsearch import YtSearch
from videoids import VideoIds
import json

async def main():
    user_goal_context: str = input("Enter the user goal context: ")
    gemini_service = GeminiService(user_goal_context)
    gemini_service.run()
    user_id = gemini_service.user_id()
    yt_search = YtSearch(user_id)
    directory = yt_search.run()
    video_ids = VideoIds(directory).ids()
    
    yt = YouTubePlaylistCreator()
    playlist_id = yt.create_playlist(title=f"{user_goal_context}", description="Created with Kairos-AI", privacy_status="private")
    for video_id in video_ids:
        yt.add_video_to_playlist(playlist_id=playlist_id, video_id=video_id)
        transcript = Transcript(video_id)
        transcript.get_transcript()
        data = {
            "video_id": video_id,
            "transcript": transcript.get_transcript()
        }
        # store all the data in a single json file
        with open(f"{directory}/transcripts.json", "a") as f:
            json.dump(data, f)


if __name__ == "__main__":
    asyncio.run(main())
