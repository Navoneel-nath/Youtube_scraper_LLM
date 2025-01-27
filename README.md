# 🧠 YouTube Research Assistant

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Status](https://img.shields.io/badge/status-active-success.svg)]()

**A Local AI-Powered YouTube Research Tool**  
Scrape, transcribe, and chat with YouTube content - 100% local & private

## 🚀 Features

- 🔍 **YouTube Content Discovery**  
  Smart search for English educational videos
- 🎙️ **Multi-Modal Transcription**  
  Auto-detect subtitles or convert audio to text
- 🧩 **Local AI Processing**  
  Uses Ollama/Llama2 for private Q&A
- 📊 **Knowledge Base Building**  
  Stores transcripts in local vector database
- 🛡️ **No API Keys Required**  
  100% local execution with no external services

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/yourusername/youtube-research-assistant.git
cd youtube-research-assistant

# Install dependencies
pip install -r requirements.txt

# Install Ollama (Windows)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama2
🖥️ Usage
bash
Copy
python main.py
Scrape Videos
Enter topic (e.g., "Quantum Computing") and click "Start Research"

Chat with Content
Ask questions about the collected videos

Manage Data
Clear context when starting new research

🧠 Key Technologies
AI Framework: CrewAI + Ollama (Llama2)

Transcription: OpenAI Whisper (Local)

Vector DB: FAISS

Web Interface: Gradio

YouTube Handling: yt-dlp

📂 Data Flow
mermaid
Copy
graph TD
    A[YouTube Search] --> B[Video Filtering]
    B --> C{Subtitles?}
    C -->|Yes| D[Save Transcript]
    C -->|No| E[Audio Transcription]
    E --> D
    D --> F[FAISS Vector DB]
    F --> G[Llama2 Q&A]
🌟 Why This Matters?
Privacy First: No data leaves your machine

Research Efficiency: Process hours of video content in minutes

Education Focus: Perfect for students/researchers

Local AI Showcase: Demonstrates full local AI pipeline

🛣️ Roadmap
Batch processing for large research projects

Multi-modal analysis (video + text)

Automatic citation generation

Cross-platform mobile app

🤝 Acknowledgements
Inspired by recent advances in local LLMs

Built with help from OpenAI Whisper community

Special thanks to CrewAI developers
