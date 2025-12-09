import requests

class LLMService:

    def __init__(self):
        pass

    def get_available_models(self, api_key: str):
        try:
            response = requests.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            
            if response.status_code == 200:
                models_data = response.json()
                return [model["id"] for model in models_data["data"]]
            else:
                return []
        
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    def generate_answer(self, query, context_chunks, model, api_key):
        context = "\n\n".join(context_chunks)
        
        system_prompt = """You are a helpful assistant that answers questions based on the provided context.
        Only use information from the context to answer. If the answer is not in the context, say you don't know."""
        
        user_prompt = f"""Context: {context}

        Question: {query}

        Answer:"""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
        
        except requests.exceptions.Timeout:
            return "Error: Request timed out"
        except Exception as e:
            return f"Error: {str(e)}"
