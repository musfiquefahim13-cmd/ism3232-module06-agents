
# ollama_model.py
# Author: Musfique Hossain Fahim

from ollama import chat


class OllamaModel:
    """Connect the support chatbot to a local Ollama model."""

    def __init__(self, model_name="granite4.1:3b"):
        """Store the name of the model."""
        self.model_name = model_name

    def reply(self, instructions, history):
        """Send the conversation to Ollama and return its reply."""
        messages = [
            {"role": "system", "content": instructions}
        ]

        messages.extend(history)

        try:
            response = chat(
                model=self.model_name,
                messages=messages
            )
            return response.message.content

        except Exception:
            return None
