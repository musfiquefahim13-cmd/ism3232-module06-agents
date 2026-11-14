class Toolbox:
    """Run customer support tools with safety checks."""

    def __init__(self, order_tool, stock_tool, change_queue):
        self.order_tool = order_tool
        self.stock_tool = stock_tool
        self.change_queue = change_queue

    def tool_list(self):
        """List the tools available to the chatbot."""
        return [
            self.order_tool.look_up_order,
            self.stock_tool.check_stock,
            self.change_queue.request_address_change,
            self.order_tool.check_return,
        ]

    def run(self, name, arguments, history):
        """Check tool arguments before running a tool."""

        if not isinstance(arguments, dict):
            arguments = {}

        if name == "look_up_order":
            order_id = self.clean(arguments, "order_id").upper()

            if not order_id:
                return "Please provide an order ID."

            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID."

            return self.order_tool.look_up_order(order_id)

        if name == "check_stock":
            item = self.clean(arguments, "item")

            if not item:
                return "Please provide a product name."

            if not self.customer_said(history, item):
                return "The customer has not given that product name."

            return self.stock_tool.check_stock(item)

        if name == "request_address_change":
            order_id = self.clean(arguments, "order_id").upper()
            new_address = self.clean(arguments, "new_address")

            if not order_id:
                return "Please provide an order ID."

            if not new_address:
                return "Please provide a new address."

            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID."

            if not self.customer_said(history, new_address):
                return "The customer has not given that address."

            return self.change_queue.request_address_change(order_id, new_address)

        if name == "check_return":
            order_id = self.clean(arguments, "order_id").upper()

            if not order_id:
                return "Please provide an order ID."

            if not self.customer_said(history, order_id):
                return "The customer has not given that order ID."

            return self.order_tool.check_return(order_id)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Convert an argument into clean text."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Check whether the customer actually provided this text."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True

        return False
