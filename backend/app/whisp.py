from faster_whisper import WhisperModel
import torch

class Transcriber:
    def __init__(self):
        self.model = WhisperModel(
            "large-v3-turbo",  # or "medium"
            device=device,
            compute_type=compute_type,
            num_workers=4  # Parallel processing
        )
        if torch.cuda.is_available():
            device = "cuda"
            compute_type = "float16"
        else:
            device = "cpu"
            compute_type = "int8"

    def transcribe(self, audio_path):
        segments, info = self.model.transcribe(
            audio_path,
            beam_size=5,
            language="en",  # Specify if known
            vad_filter=True,  # Voice activity detection
            word_timestamps=True  # Get word-level timing
        )

        print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

        for segment in segments:
            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

        return segments


if __name__ == "__main__":
    transcriber = Transcriber()
    transcriber.transcribe("audio.mp3")
