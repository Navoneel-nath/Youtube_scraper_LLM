import os
from pathlib import Path
from crewai import Agent
from tools.transcription_tool import VideoTranscriptionTool

class TranscriptionAgent:
    def __init__(self, llm, data_dir):
        self.data_dir = data_dir
        self.transcripts_dir = data_dir / "transcripts"
        self.transcripts_dir.mkdir(exist_ok=True)
        
        self.agent = Agent(
            role="Video Transcription Expert",
            goal="Accurately transcribe educational video content",
            backstory="Specialist in audio processing and technical transcription",
            verbose=True,
            llm=llm,
            tools=[VideoTranscriptionTool()]
        )
    
    def process_video(self, url):
        video_id = url.split("v=")[-1].split("&")[0]
        save_path = self.transcripts_dir / f"{video_id}.txt"
        
        if not save_path.exists():
            task = f"Download and transcribe video from {url}"
            transcript = self.agent.execute_task(task)
            if transcript:
                save_path.write_text(transcript)
        return str(save_path)