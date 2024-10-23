from datetime import datetime
from typing import List, Tuple, Optional
from datastructures.intervaltree import IntervalTree
from datastructures.avltree import AVLTree

class Stock:
    def __init__(self, symbol: str, name: str, low: int, high: int):
        self.symbol = symbol
        self.name = name
        self.low = low
        self.high = high

class StockManager:
    def __init__(self):
        self._interval_tree = IntervalTree()
        self._price_history = {}  # Dictionary to store AVL trees for price history
        stocks = [
            Stock("GOOGL", "ALPHABET INC", 173, 213),
        ]
        for stock in stocks:
            self.add_stock(stock)

    def add_stock(self, stock: Stock):
        self._interval_tree.insert(stock.low, stock.high, stock)

    def delete_stock(self, symbol: str):
        stock = self._find_stock(symbol)
        if stock:
            self._interval_tree.delete(stock.low, stock.high)

    def update_stock(self, symbol: str, new_low: int, new_high: int):
        stock = self._find_stock(symbol)
        if stock:
            self._interval_tree.update(stock.low, stock.high, new_low, new_high, stock)

    def track_market_trends(self, symbol: str) -> List[Tuple[datetime, int]]:
        avl_tree = self._price_history.get(symbol)
        if avl_tree:
            return avl_tree.get(symbol)
        return []

    def _add_price_data(self, symbol: str, price: int):
        timestamp = datetime.now()
        if symbol not in self._price_history:
            self._price_history[symbol] = AVLTree()
        self._price_history[symbol].insert(timestamp, price)

    def _find_stock(self, symbol: str) -> Optional[Stock]:
        for node in self._interval_tree.range_query(float('-inf'), float('inf')):
            if node.symbol == symbol:
                return node
        return None

    def range_query(self, low: int, high: int) -> List[Stock]:
        return [node for node in self._interval_tree.range_query(low, high)]

    def top_k_stocks(self, k: int) -> List[Stock]:
        return [node for node in self._interval_tree.top_k_stocks(k)]

    def bottom_k_stocks(self, k: int) -> List[Stock]:
        return [node for node in self._interval_tree.bottom_k_stocks(k)]

def main():
    manager = StockManager()
    manager.add_stock(Stock("AAPL", "APPLE INC", 150, 200))
    manager.add_stock(Stock("GOOGL", "ALPHABET INC", 100, 250))
    manager.add_stock(Stock("MSFT", "MICROSOFT CORP", 50, 150))

if __name__ == "__main__":
    main()