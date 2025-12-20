import yt_dlp

class AudioDownloader:
    def __init__(self, user_id: str):
        self.USER_ID: str = user_id

    def download_audio(self, url, output_path='./downloads/'):
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

if __name__ == "__main__":
    user_id = ""
    downloader = AudioDownloader(user_id)
    downloader.download_audio('https://www.youtube.com/watch?v=H62Jfv1DJlU')
