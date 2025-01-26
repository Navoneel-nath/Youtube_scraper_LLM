from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path
from typing import List, Tuple

class RAGService:
    def __init__(self, data_dir: str):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = FAISS.from_texts([""], self.embeddings)
        self.data_dir = Path(data_dir)
        self.transcripts_dir = self.data_dir / "transcripts"
        self.transcripts_dir.mkdir(parents=True, exist_ok=True)

    def add_documents(self, results: list) -> Tuple[int, List[str]]:
        valid_texts = []
        saved_files = []
        
        for url, method, success in results:
            if success:
                video_id = url.split("v=")[-1].split("&")[0]
                file_path = self.transcripts_dir / f"{video_id}.txt"
                
                if file_path.exists():
                    text = file_path.read_text()
                    metadata = {"source": f"Video {video_id}", "url": url}
                    valid_texts.append((text, metadata))
                    saved_files.append(f"{video_id}.txt")
        
        if valid_texts:
            # Separate texts and metadata
            texts, metadatas = zip(*valid_texts)
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            
        return len(valid_texts), saved_files

    def query(self, question: str, k=3) -> Tuple[str, List[str]]:
        docs = self.vector_store.similarity_search(question, k=k)
        context = "\n".join([d.page_content for d in docs])
        sources = [f"{d.metadata['source']} ({d.metadata['url']})" for d in docs]
        return context, sources

    def get_transcript_list(self) -> List[str]:
        return [f.name for f in self.transcripts_dir.glob("*.txt")]

    def get_transcript_content(self, filename: str) -> str:
        return (self.transcripts_dir / filename).read_text()

    def clear_data(self) -> int:
        count = len(list(self.transcripts_dir.glob("*.txt")))
        for f in self.transcripts_dir.glob("*.txt"):
            f.unlink()
        self.vector_store = FAISS.from_texts([""], self.embeddings)
        return count