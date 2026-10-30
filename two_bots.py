# two_bots.py
# Author: MUSFIQUE HOSSAIN FAHIM

from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup

# Create tools shared by both chatbots
order_tool = OrderLookup(
    {
        "A100": "shipped",
        "A101": "processing",
    }
)

stock_tool = StockLookup(
    {
        "rain jacket": 12,
        "hiking boots": 5,
    }
)

# Create two chatbots from the same class
sunny = SupportChatbot(
    "Sunny",
    "You are cheerful and brief.",
    order_tool,
    stock_tool,
)

river = SupportChatbot(
    "River",
    "You are formal and detailed.",
    order_tool,
    stock_tool,
)

# Send two messages to Sunny
sunny.respond("hello")
sunny.respond("Where is order A100?")

# Send one message to River
river.respond("hello")

# Display names and conversation history lengths
print(sunny.name, len(sunny.history))
print(river.name, len(river.history))

# Display the first reply from each chatbot
print(sunny.history[1]["content"])
print(river.history[1]["content"])

# Display each chatbot's instructions
print(sunny.instructions)
print(river.instructions)
