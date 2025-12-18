from youtube_transcript_api import YouTubeTranscriptApi
from whisp import Transcriber


def get_transcript(video_id):
  """
  Method - A
  Use youtube_transcript_api to get transcript

  Method - B
  Download the audio file from youtube
  Use whisp to get transcript
  """

  try:
    yt_transcript = YouTubeTranscriptApi().fetch(video_id)
    for snippet in yt_transcript:
      print(snippet.text)
    return yt_transcript
  except Exception:
    try:
      whisp_transcript = Transcriber().transcribe(video_id)
      for segment in whisp_transcript:
        print(segment.text)
      return whisp_transcript
    except Exception:
      return None
      
  
  


