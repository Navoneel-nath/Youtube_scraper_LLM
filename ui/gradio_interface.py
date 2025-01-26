import gradio as gr
from typing import List, Tuple
from pathlib import Path
from tool.youtube_tools import YouTubeTools
from services.rag_service import RAGService
from services.ollama_service import OllamaService

class YouTubeSubtitleRAG:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.tools = YouTubeTools(self.data_dir)
        self.rag = RAGService(self.data_dir)
        self.llm = OllamaService()
        self.target_count = 10

    def process_topic(self, topic: str) -> Tuple[str, List[Tuple[str, str]]]:
        try:
            video_urls = self.tools.search_videos(topic)[:20]
            results = self.tools.process_batch(video_urls[:self.target_count])
            count, _ = self.rag.add_documents(results)
            transcripts = self.get_transcript_info()
            status = f"✅ Loaded {count} transcripts" if count > 0 else "❌ No valid content found"
            return status, transcripts
        except Exception as e:
            return f"🚨 Error: {str(e)}", []

    def ask_question(self, question: str) -> Tuple[str, str, List[str]]:
        try:
            context, sources = self.rag.query(question)
            answer = self.llm.generate(question, context)
            return answer, context, sources
        except Exception as e:
            return f"⚠️ Error: {str(e)}", "", []

    def get_transcript_info(self) -> List[Tuple[str, str]]:
        return [
            (f.name, f.read_text()[:500] + "...") 
            for f in self.rag.transcripts_dir.glob("*.txt")
        ]

def create_interface() -> gr.Blocks:
    DATA_DIR = r"C:\Users\navon\Documents\LLM_youtube\data"
    system = YouTubeSubtitleRAG(DATA_DIR)
    
    with gr.Blocks(title="YouTube Research", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🔍 YouTube Video Research Assistant")
        
        with gr.Row():
            topic_input = gr.Textbox(label="Research Topic", placeholder="Enter topic...")
            load_btn = gr.Button("Load Videos", variant="primary")
        
        status = gr.Textbox(label="Status")
        
        with gr.Row():
            question_input = gr.Textbox(label="Your Question", placeholder="Ask something...", lines=3)
            ask_btn = gr.Button("Get Answer", variant="secondary")
        
        answer_output = gr.Textbox(label="Response", lines=5)
        
        with gr.Accordion("📚 Saved Transcripts", open=False):
            transcript_viewer = gr.DataFrame(
                headers=["Filename", "Content Preview"],
                datatype=["str", "str"],
                interactive=False
            )
        
        clear_btn = gr.Button("Reset System", variant="stop")

        load_btn.click(
            lambda t: system.process_topic(t),
            inputs=topic_input,
            outputs=[status, transcript_viewer]
        )
        
        ask_btn.click(
            lambda q: system.ask_question(q),
            inputs=question_input,
            outputs=[answer_output]
        )
        
        clear_btn.click(
            lambda: (system.rag.clear_data(), "♻️ System reset", []),
            outputs=[status, transcript_viewer]
        )
        
        demo.load(
            lambda: system.get_transcript_info(),
            outputs=transcript_viewer
        )
    
    return demo