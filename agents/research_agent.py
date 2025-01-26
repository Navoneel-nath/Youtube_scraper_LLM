from typing import List, Tuple
from pathlib import Path
from tqdm import tqdm
import concurrent.futures
from tool.youtube_tools import YouTubeTools

class ResearchAgent:
    def __init__(self, data_dir: str = "data"):
        self.tools = YouTubeTools(data_dir)
        self.target_count = 10
        self.data_dir = Path(data_dir)
        self.transcripts_dir = self.data_dir / "transcripts"
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)

    def research_topic(self, topic: str) -> Tuple[List[str], List[Tuple[str, bool]]]:
        try:
            video_urls = self.tools.search_videos(topic)[:20]
            results = self._process_videos(video_urls[:self.target_count])
            return video_urls, results
        except Exception as e:
            raise RuntimeError(f"Research failed: {str(e)}")

    def _process_videos(self, urls: List[str]) -> List[Tuple[str, bool]]:
        results = []
        with tqdm(total=len(urls), desc="Processing Videos", unit="video") as pbar:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(self._process_single_video, url): url for url in urls}
                for future in concurrent.futures.as_completed(futures):
                    url = futures[future]
                    try:
                        success = future.result()
                        results.append((url, success))
                    except Exception:
                        results.append((url, False))
                    pbar.update(1)
        return results

    def _process_single_video(self, url: str) -> bool:
        try:
            video_id = url.split("v=")[-1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            text = " ".join([t['text'] for t in transcript])
            (self.transcripts_dir / f"{video_id}.txt").write_text(text)
            return True
        except Exception:
            return False