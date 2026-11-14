# ollama_model.py
# Author: Musfique Hossain Fahim

from ollama import ChatResponse, Client, ResponseError


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

    def decide(self, instructions, history, tools):
        """Send the conversation and tools. Return a reply or tool request."""
        messages = [{"role": "system", "content": instructions}]

        for message in history:
            if message["role"] == "tool":
                messages.extend(self.tool_messages(message))
            else:
                messages.append(message)

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                tools=tools,
            )
        except (ResponseError, ConnectionError, OSError) as error:
            print(f"Ollama error: {error}")
            return None

        if response.message.tool_calls:
            call = response.message.tool_calls[0]
            return {
                "tool": call.function.name,
                "arguments": call.function.arguments,
            }

        return {"text": response.message.content}

    def tool_messages(self, message):
        """Turn one tool entry into the two messages Ollama expects."""
        name = message["tool_name"]
        request = {
            "function": {
                "name": name,
                "arguments": message["arguments"],
            }
        }

        return [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [request],
            },
            {
                "role": "tool",
                "tool_name": name,
                "content": message["content"],
            },
        ]
