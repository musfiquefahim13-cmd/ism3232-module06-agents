# chatbot.py
# Author: MUSFIQUE HOSSAIN FAHIM

HANDOFF_WORDS = ["address", "payment", "card"]


class SupportChatbot:
    """A mock support chatbot using simple keyword rules."""

    def __init__(self, name, instructions, order_tool, stock_tool):
        """Set up the chatbot with its tools and history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.stock_tool = stock_tool
        self.history = []

    def respond(self, user_message):
        """Record the user message and chatbot reply."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply using keyword rules."""
        text = user_message.lower()

        if self.needs_human(text):
            return "I can't help with that here. I'm passing you to a human agent."

        if "stock" in text:
            return self.stock_reply(user_message)

        if "order" in text:
            return self.order_reply(user_message)

        if "hello" in text:
            return f"Hello! I'm {self.name}. I can check an order status for you."

        return "I'm not sure how to help with that. I can check an order status."

    def needs_human(self, text):
        """Check whether a request requires a human."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def order_reply(self, user_message):
        """Use the order tool to answer an order question."""
        order_id = self.order_tool.find_order_id(user_message)

        if order_id is None:
            return "Which order? Please send an order ID like A100."

        status = self.order_tool.find_status(order_id)
        return f"Order {order_id} is {status}."

    def count_user_messages(self):
        """Count the messages sent by the user."""
        count = 0
        for message in self.history:
            if message["role"] == "user":
                count += 1
        return count

    def stock_reply(self, user_message):
        """Use the stock tool to answer availability questions."""
        product = self.stock_tool.find_product(user_message)

        if product is None:
            return "Which product? Please name the item you want me to check."

        count = self.stock_tool.count_for(product)
        return f"We have {count} of the {product} in stock."
