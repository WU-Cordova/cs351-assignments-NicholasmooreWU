from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, List

from datastructures.avltree import AVLTree


@dataclass
class IntervalNode:
    key: Tuple[int, int]
    value: Any
    left: Optional['IntervalNode'] = None
    right: Optional['IntervalNode'] = None
    height: int = 1
    max_end: int = 0
    intervals_at_low: AVLTree = field(default_factory=AVLTree)


class IntervalTree:
    def __init__(self):
        self.root: Optional[IntervalNode] = None

    def insert(self, low: int, high: int, value: Any):
        self.root = self._insert(self.root, low, high, value)

    def _insert(self, node: Optional[IntervalNode], low: int, high: int, value: Any) -> IntervalNode:
        if not node:
            return IntervalNode(key=(low, high), value=value, max_end=high)

        if low < node.key[0]:
            node.left = self._insert(node.left, low, high, value)
        else:
            node.right = self._insert(node.right, low, high, value)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        node.max_end = max(node.max_end, high)

        balance = self._get_balance(node)

        if balance > 1 and low < node.left.key[0]:
            return self._right_rotate(node)
        if balance < -1 and low > node.right.key[0]:
            return self._left_rotate(node)
        if balance > 1 and low > node.left.key[0]:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and low < node.right.key[0]:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, low: int, high: int):
        self.root = self._delete(self.root, low, high)

    def _delete(self, node: Optional[IntervalNode], low: int, high: int) -> Optional[IntervalNode]:
        if not node:
            return node

        if low < node.key[0]:
            node.left = self._delete(node.left, low, high)
        elif low > node.key[0]:
            node.right = self._delete(node.right, low, high)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key[0], temp.key[1])

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        node.max_end = max(node.key[1], self._get_max_end(node.left), self._get_max_end(node.right))

        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def update(self, low: int, high: int, new_low: int, new_high: int, value: Any):
        self.delete(low, high)
        self.insert(new_low, new_high, value)

    def range_query(self, low: int, high: int) -> List[Any]:
        result = []
        self._range_query(self.root, low, high, result)
        return result

    def _range_query(self, node: Optional[IntervalNode], low: int, high: int, result: List[Any]):
        if not node:
            return
        if node.key[0] <= high and node.key[1] >= low:
            result.append(node.value)
        if node.left and node.left.max_end >= low:
            self._range_query(node.left, low, high, result)
        if node.right and node.key[0] <= high:
            self._range_query(node.right, low, high, result)

    def top_k_stocks(self, k: int) -> List[Any]:
        result = []
        self._top_k_stocks(self.root, k, result)
        return result

    def _top_k_stocks(self, node: Optional[IntervalNode], k: int, result: List[Any]):
        if not node or len(result) >= k:
            return
        self._top_k_stocks(node.right, k, result)
        if len(result) < k:
            result.append(node.value)
            self._top_k_stocks(node.left, k, result)

    def bottom_k_stocks(self, k: int) -> List[Any]:
        result = []
        self._bottom_k_stocks(self.root, k, result)
        return result

    def _bottom_k_stocks(self, node: Optional[IntervalNode], k: int, result: List[Any]):
        if not node or len(result) >= k:
            return
        self._bottom_k_stocks(node.left, k, result)
        if len(result) < k:
            result.append(node.value)
            self._bottom_k_stocks(node.right, k, result)

    def _min_value_node(self, node: IntervalNode) -> IntervalNode:
        current = node
        while current.left:
            current = current.left
        return current

    def _get_height(self, node: Optional[IntervalNode]) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: Optional[IntervalNode]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_max_end(self, node: Optional[IntervalNode]) -> int:
        if not node:
            return 0
        return node.max_end

    def _right_rotate(self, z: IntervalNode) -> IntervalNode:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        z.max_end = max(z.key[1], self._get_max_end(z.left), self._get_max_end(z.right))
        y.max_end = max(y.key[1], self._get_max_end(y.left), self._get_max_end(y.right))
        return y

    def _left_rotate(self, z: IntervalNode) -> IntervalNode:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        z.max_end = max(z.key[1], self._get_max_end(z.left), self._get_max_end(z.right))
        y.max_end = max(y.key[1], self._get_max_end(y.left), self._get_max_end(y.right))
        return y