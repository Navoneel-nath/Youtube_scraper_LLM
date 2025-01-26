from services.ollama_service import OllamaService
from services.rag_service import RAGService
from typing import Tuple, List

class QAAgent:
    def __init__(self, rag_service: RAGService):
        self.llm = OllamaService()
        self.rag = rag_service

    def answer_question(self, question: str) -> Tuple[str, str, List[str]]:
        try:
            context, sources = self.rag.query(question)
            answer = self.llm.generate(question, context)
            return answer, context, sources
        except Exception as e:
            raise RuntimeError(f"QA failed: {str(e)}")