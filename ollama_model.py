
# ollama_model.py
# Author: Musfique Hossain Fahim

from ollama import (
    ChatResponse,
    Client,
    ResponseError,
)


class OllamaModel:
    """Connect to Ollama and generate chatbot responses."""

    def __init__(self, model_name="llama3.2"):
        """Set up the Ollama model."""
        self.model_name = model_name
        self.client = Client()

    def reply(self, instructions, history):
        """Generate a reply using instructions and chat history."""

        messages = [
            {
                "role": "system",
                "content": instructions,
            }
        ]

        messages.extend(history)

        try:
            response: ChatResponse = self.client.chat(
                model=self.model_name,
                messages=messages,
            )

            return response.message.content

        except (ResponseError, ConnectionError, OSError) as error:
            print(f"Ollama error: {error}")
            return None
