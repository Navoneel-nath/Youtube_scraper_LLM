import requests
import os  

class OllamaService:
    def generate(self, prompt: str, context: str) -> str:
        try:
            host = os.getenv("OLLAMA_HOST", "http://localhost:11436")
            url = f"{host.rstrip('/')}/api/chat"
            messages = [
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nQuestion: {prompt}"
                }
            ]
            
            response = requests.post(
                url,
                json={
                    "model": "llama3.1:8b",  
                    "messages": messages,  
                    "stream": False,
                    "options": {
                        "temperature": 0.7 
                    }
                },
                timeout=30  
            )
            response.raise_for_status() 
           
            return response.json()['message']['content']
            
        except requests.exceptions.ConnectionError:
            return "Error: Failed to connect to Ollama - make sure it's running with 'ollama serve'"
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error {e.response.status_code}: {e.response.text}"
        except KeyError:
            return "Error: Unexpected response format from Ollama"
        except Exception as e:
            return f"LLM Error: {str(e)}"
