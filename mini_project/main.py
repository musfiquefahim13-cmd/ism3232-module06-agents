
# main.py
# Author: Musfique Hossain Fahim

from chatbot import SupportChatbot
from ollama_model import OllamaModel
from order_tool import OrderLookup
from stock_tool import StockLookup

INSTRUCTIONS = """
You are Sunny, a helpful support assistant for Bayside Outfitters.
Answer customer questions clearly and briefly.
"""

order_tool = OrderLookup({
    "A100": "shipped",
    "A101": "processing",
})

stock_tool = StockLookup({
    "shirt": 10,
    "shoes": 5,
    "hat": 0,
})

model = OllamaModel()

bot = SupportChatbot(
    "Sunny",
    INSTRUCTIONS,
    order_tool,
    stock_tool,
    model,
)

print("Welcome to Bayside Outfitters!")
print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message.lower() != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
