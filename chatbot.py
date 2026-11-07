
# chatbot.py
# Author: Musfique Hossain Fahim


class SupportChatbot:
    """A support chatbot that uses rules, tools, and an AI model."""

    def __init__(self, name, instructions, order_tool, stock_tool, model):
        """Set up the chatbot with its tools, model, and history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.stock_tool = stock_tool
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Save the conversation and return a reply."""
        self.history.append({
            "role": "user",
            "content": user_message
        })

        reply = self.choose_reply(user_message)

        self.history.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    def choose_reply(self, user_message):
        """Use a rule when possible, otherwise ask the AI model."""
        text = user_message.lower()

        if self.needs_human(text):
            return (
                "I can't help with that here. "
                "I'm passing you to a human agent."
            )

        if "order" in text:
            return self.order_reply(user_message)

        if "stock" in text:
            return self.stock_reply(user_message)

        return self.model_reply()

    def model_reply(self):
        """Get a response from the AI model."""
        reply = self.model.reply(
            self.instructions,
            self.history
        )

        if reply is None:
            return (
                "Sorry, I can't answer that right now. "
                "Please try again in a moment."
            )

        return reply

    def needs_human(self, text):
        """Check whether the customer needs human assistance."""
        keywords = [
            "address",
            "payment",
            "card",
            "refund"
        ]

        for keyword in keywords:
            if keyword in text:
                return True

        return False

    def order_reply(self, user_message):
        """Find an order and return its status."""
        order_id = self.order_tool.find_order_id(user_message)

        if order_id is None:
            return "I couldn't find that order."

        status = self.order_tool.find_status(order_id)

        if status is None:
            return "I couldn't find that order."

        return f"Order {order_id} is {status}."

    def stock_reply(self, user_message):
        """Find a product and check its stock quantity."""
        product = self.stock_tool.find_product(user_message)

        if product is None:
            return "I couldn't find that item."

        quantity = self.stock_tool.count_for(product)

        if quantity is None:
            return "I couldn't find that item."

        if quantity == 0:
            return f"The {product} is out of stock."

        return f"We have {quantity} of the {product} in stock."
