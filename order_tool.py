# order_tool.py
# Author: MUSFIQUE HOSSAIN FAHIM


class OrderLookup:
    """A tool that knows about orders. It knows nothing about chatting."""

    def __init__(self, orders):
        """Store the orders this tool can look up."""
        self.orders = orders

    def find_order_id(self, text):
        """Return the first known order ID mentioned in text, or None."""
        for order_id in self.orders:
            if order_id in text.upper():
                return order_id
        return None

    def find_status(self, order_id):
        """Return the status of one order, or None if there is no such order."""
        if order_id in self.orders:
            return self.orders[order_id]["status"]
        return None

    def look_up_order(self, order_id):
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        found = self.find_order_id(order_id)
        if found is None:
            return "No order with that ID was found. Order IDs look like A100."
        return f"Order {found} is {self.find_status(found)}."

    def change_address(self, order_id, new_address):
        """Change the shipping address on one order. Only an approval calls this."""
        self.orders[order_id]["address"] = new_address

    def check_return(self, order_id):
        """Check whether an order can be returned within 30 days.

        Args:
            order_id: The order ID, like A100.
        """
        order_id = order_id.strip().upper()

        if order_id not in self.orders:
            return "No order with that ID was found. Order IDs look like A100."

        if self.orders[order_id]["status"] == "delivered":
            return f"Order {order_id} may be returned within 30 days of delivery."

        return f"Order {order_id} is not eligible for a return yet."
