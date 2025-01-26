from typing import List, Tuple
from pathlib import Path
from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from faster_whisper import WhisperModel
import requests
from tqdm import tqdm
import concurrent.futures

class YouTubeTools:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.transcripts_dir = self.data_dir / "transcripts"
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }

    def search_videos(self, query: str, max_results: int = 20) -> List[str]:
        results = YoutubeSearch(query, max_results=max_results).to_dict()
        return [f"https://youtube.com/watch?v={res['id']}" for res in results]

    def process_batch(self, urls: list) -> list:
         results = []
         with tqdm(total=len(urls), desc="📥 Processing Videos", unit="video") as pbar:
             with concurrent.futures.ThreadPoolExecutor() as executor:
              futures = {executor.submit(self.get_subtitles, url): url for url in urls}
              for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
                pbar.update(1)
                pbar.set_postfix_str(f"Last: {result[0][:30]}... ({result[1]})")
              return results

    def get_subtitles(self, url: str) -> Tuple[str, str, bool]:
        video_id = url.split("v=")[-1].split("&")[0]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            text = " ".join([t['text'] for t in transcript])
            self._save_transcript(video_id, text)
            return (url, "subtitles", True)
        except Exception:
            return self._fallback_transcription(url, video_id)

    def _fallback_transcription(self, url: str, video_id: str) -> Tuple[str, str, bool]:
        try:
            yt = YouTube(url, headers=self.headers)
            audio = yt.streams.filter(only_audio=True).first()
            path = audio.download(output_path=str(self.transcripts_dir), filename_prefix="temp_")
            
            model = WhisperModel("tiny")
            segments, _ = model.transcribe(path)
            text = " ".join([segment.text for segment in segments])
            
            Path(path).unlink()
            self._save_transcript(video_id, text)
            return (url, "audio", True)
        except Exception as e:
            return (url, "failed", False)

    def _save_transcript(self, video_id: str, text: str):
        (self.transcripts_dir / f"{video_id}.txt").write_text(text)