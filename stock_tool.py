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
