import unittest
from datastructures.intervaltree import IntervalTree

class TestIntervalTree(unittest.TestCase):

    def setUp(self):
        self.tree = IntervalTree()
        self._load_sample_data()

    def _load_sample_data(self):
        sample_data = [
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "low": 300, "high": 360},
            {"symbol": "UBER", "name": "Uber Technologies", "low": 196, "high": 220},
            {"symbol": "ORCL", "name": "Oracle Corp.", "low": 180, "high": 210}
        ]
        for stock in sample_data:
            self.tree.insert(stock["low"], stock["high"], stock)

    def test_node_structure(self):
        node = self.tree.root
        self.assertIsNotNone(node)
        self.assertEqual(node.key, (196, 220))
        self.assertEqual(node.value["symbol"], "UBER")
        self.assertEqual(node.value["name"], "Uber Technologies")
        self.assertEqual(node.value["low"], 196)
        self.assertEqual(node.value["high"], 220)

    def test_delete_stock(self):
        self.tree.delete(300, 360)
        node = self.tree.root
        self.assertIsNotNone(node)
        self.assertNotEqual(node.key, (300, 360))
        self.assertEqual(node.max_end, 220)

    def test_range_query(self):
        result = self.tree.range_query(180, 220)
        self.assertEqual(len(result), 2)
        symbols = [stock["symbol"] for stock in result]
        self.assertIn("UBER", symbols)
        self.assertIn("ORCL", symbols)

    def test_top_k_stocks(self):
        result = self.tree.top_k_stocks(2)
        self.assertEqual(len(result), 2)
        symbols = [stock["symbol"] for stock in result]
        self.assertIn("GOOGL", symbols)
        self.assertIn("UBER", symbols)

    def test_bottom_k_stocks(self):
        result = self.tree.bottom_k_stocks(2)
        self.assertEqual(len(result), 2)
        symbols = [stock["symbol"] for stock in result]
        self.assertIn("UBER", symbols)
        self.assertIn("ORCL", symbols)

if __name__ == "__main__":
    unittest.main()