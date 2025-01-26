from crewai.tools import BaseTool
from youtube_transcript_api import YouTubeTranscriptApi

class VideoTranscriptionTool(BaseTool):
    name: str = "Subtitle Extractor"
    description: str = "Gets English subtitles from YouTube videos"
    
    def _run(self, url: str) -> str:
        try:
            video_id = url.split("v=")[-1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            return " ".join([t['text'] for t in transcript])
        except Exception as e:
            return f"Subtitle error: {str(e)}"