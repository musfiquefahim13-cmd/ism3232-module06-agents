# stock_tool.py
# Author: MUSFIQUE HOSSAIN FAHIM


class StockLookup:
    """A tool that knows about product stock."""

    def __init__(self, stock):
        """Store the product stock dictionary."""
        self.stock = stock

    def find_product(self, text):
        """Find a known product mentioned in a message."""
        for product in self.stock:
            if product.lower() in text.lower():
                return product
        return None

    def count_for(self, product):
        """Return the stock count or None."""
        return self.stock.get(product)

    def check_stock(self, item):
        """Check how many of one product are in stock.

        Args:
            item: The product name, like rain jacket.
        """
        product = self.find_product(item)
        if product is None:
            return "That product was not found."
        return f"We have {self.count_for(product)} of the {product} in stock."
