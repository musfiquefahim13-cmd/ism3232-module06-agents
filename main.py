# main.py
# Author: MUSFIQUE HOSSAIN FAHIM

from change_queue import ChangeQueue
from chatbot import SupportChatbot
from ollama_model import OllamaModel
from order_tool import OrderLookup
from stock_tool import StockLookup
from toolbox import Toolbox


def main():
    """Run the customer support chatbot with human approval."""

    orders = {
        "A100": {"status": "shipped", "address": "14 Bay Road"},
        "A101": {"status": "processing", "address": "3 Gull Lane"},
        "A102": {"status": "delivered", "address": "8 Oak Street"},
    }

    stock = {
        "rain jacket": 12,
        "day pack": 0,
    }

    order_tool = OrderLookup(orders)
    stock_tool = StockLookup(stock)
    change_queue = ChangeQueue(order_tool)
    tools = Toolbox(order_tool, stock_tool, change_queue)

    model = OllamaModel("granite4.1:3b")

    bot = SupportChatbot(
        "Sunny",
        (
            "You are a helpful customer support assistant. "
            "Use the available tools to check orders, stock, and request "
            "shipping address changes. "
            "Never invent an order ID or shipping address. "
            "Ask the customer for missing information. "
            "Address changes require staff approval."
        ),
        tools,
        model,
    )

    print("Sunny Customer Support Chatbot")
    print("Type 'quit' to finish.")

    while True:
        user_message = input("\nCustomer: ").strip()

        if user_message.lower() == "quit":
            break

        reply = bot.respond(user_message)
        print(f"Sunny: {reply}")

        for request in change_queue.waiting():
            print(f"\nStaff approval needed: {request}")
            decision = input("Approve (a), reject (r), or wait (w)? ").lower()

            if decision == "a":
                print(change_queue.approve(request["number"]))
            elif decision == "r":
                print(change_queue.reject(request["number"]))
            else:
                print("Request remains waiting.")


if __name__ == "__main__":
    main()
