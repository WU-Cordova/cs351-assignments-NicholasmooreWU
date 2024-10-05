from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Callable, Generic, List, Optional, Sequence, Tuple
from datastructures.iavltree import IAVLTree, K, V

class AVLNode(Generic[K, V]):
    def __init__(self, key: K, value: V, left: Optional[AVLNode] = None, right: Optional[AVLNode] = None):
        self._key = key
        self._value = value
        self._left = left
        self._right = right
        self._height = 1

    @property
    def key(self) -> K:
        return self._key

    @key.setter
    def key(self, new_key: K) -> None:
        self._key = new_key

    @property
    def value(self) -> V:
        return self._value

    @value.setter
    def value(self, new_value: V) -> None:
        self._value = new_value

    @property
    def left(self) -> Optional[AVLNode]:
        return self._left

    @left.setter
    def left(self, new_left: Optional[AVLNode]) -> None:
        self._left = new_left

    @property
    def right(self) -> Optional[AVLNode]:
        return self._right

    @right.setter
    def right(self, new_right: Optional[AVLNode]) -> None:
        self._right = new_right

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, new_height: int) -> None:
        self._height = new_height
@dataclass
class AVLTree(IAVLTree[K, V], Generic[K, V]):
    def __init__(self, starting_sequence: Optional[Sequence[Tuple[K, V]]] = None):
        self._root = None
        if starting_sequence:
            for key, value in starting_sequence:
                self.insert(key, value)

    def insert(self, key: K, value: V) -> None:
        def _insert(node: Optional[AVLNode], key: K, value: V) -> AVLNode:
            if not node:
                return AVLNode(key, value)
            if key < node.key:
                node.left = _insert(node.left, key, value)
            else:
                node.right = _insert(node.right, key, value)
            node.height = 1 + max(self._height(node.left), self._height(node.right))
            return self._balance(node)
        self._root = _insert(self._root, key, value)

    def search(self, key: K) -> V | None:
        def _search(node: AVLNode, key: K) -> V | None:
            if not node:
                return None
            if key == node.key:
                return node.value
            if key < node.key:
                return _search(node.left, key)
            return _search(node.right, key)
        return _search(self._root, key)

    def delete(self, key: K) -> None:
        def _delete(node: Optional[AVLNode[K, V]], key: K) -> Optional[AVLNode[K, V]]:
            if not node:
                return node
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                temp = self._min_value_node(node.right)
                node.key = temp.key
                node.value = temp.value
                node.right = _delete(node.right, temp.key)
            node.height = 1 + max(self._height(node.left), self._height(node.right))
            return self._balance(node)
        self._root = _delete(self._root, key)

    def _min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _height(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return node.height

    def _balance(self, node: AVLNode[K, V]) -> AVLNode[K, V]:
        balance_factor = self._get_balance(node)
        if balance_factor > 1:
            if self._get_balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance_factor < -1:
            if self._get_balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _get_balance(self, node: AVLNode) -> int:
        if not node:
            return 0
        balance = self._height(node.left) - self._height(node.right)
        return balance

    def _rotate_left(self, z: AVLNode[K, V]) -> AVLNode[K, V]:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _rotate_right(self, z: AVLNode[K, V]) -> AVLNode[K, V]:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def inorder(self, visit: Optional[Callable[[V], None]] = None) -> List[K]:
        def _inorder(node: Optional[AVLNode[K, V]]) -> None:
            if not node:
                return
            _inorder(node.left)
            if visit:
                visit(node.value)
            keys.append(node.key)
            _inorder(node.right)
        keys: List[K] = []
        _inorder(self._root)
        return keys

    def preorder(self, visit: Optional[Callable[[V], None]] = None) -> List[K]:
        def _preorder(node: Optional[AVLNode[K, V]]) -> None:
            if not node:
                return
            if visit:
                visit(node.value)
            keys.append(node.key)
            _preorder(node.left)
            _preorder(node.right)
        keys: List[K] = []
        _preorder(self._root)
        return keys

    def postorder(self, visit: Optional[Callable[[V], None]] | None = None) -> List[K]:
        def _postorder(node: Optional[AVLNode[K, V]]) -> None:
            if not node:
                return
            _postorder(node.left)
            _postorder(node.right)
            if visit:
                visit(node.value)
            keys.append(node.key)
        keys: List[K] = []
        _postorder(self._root)
        return keys

    def bforder(self, visit: Optional[Callable[[V], None]] = None) -> List[K]:
        if not self._root:
            return []
        keys: List[K] = []
        queue = deque([self._root])
        while queue:
            node = queue.popleft()
            if visit:
                visit(node.value)
            keys.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return keys

    def size(self) -> int:
        def _size(node: Optional[AVLNode[K, V]]) -> int:
            if not node:
                return 0
            return 1 + _size(node.left) + _size(node.right)
        return _size(self._root)