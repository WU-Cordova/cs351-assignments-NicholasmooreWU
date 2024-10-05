import pytest

from datastructures.avltree import AVLTree

class TestAVLInserts():
    @pytest.fixture
    def avltree(self) -> AVLTree:
        tree = AVLTree[int, int]()
        for node in [8, 9, 10, 2, 1, 5, 3, 6, 4, 7]:
            tree.insert(node, node)
        return tree
    
    def test_insert_bforder(self, avltree: AVLTree) -> None: assert avltree.bforder() == [5, 3, 8, 2, 4, 6, 9, 1, 7, 10]
    def test_insert_inorder(self, avltree: AVLTree) -> None: assert avltree.inorder() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    def test_insert_preorder(self, avltree: AVLTree) -> None: assert avltree.preorder() == [5, 3, 2, 1, 4, 8, 6, 7, 9, 10]
    def test_insert_postorder(self, avltree: AVLTree) -> None: assert avltree.postorder() == [1, 2, 4, 3, 7, 6, 10, 9, 8, 5]
    def test_size(self, avltree: AVLTree) -> None: assert avltree.size() == 10
    def test_delete(self, avltree: AVLTree) -> None: 
        avltree.delete(5)
        assert avltree.size() == 9
        assert avltree.bforder() == [6, 3, 8, 2, 4, 7, 9, 1, 10]
        assert avltree.inorder() == [1, 2, 3, 4, 6, 7, 8, 9, 10]
        assert avltree.preorder() == [6, 3, 2, 1, 4, 8, 7, 9, 10]
        assert avltree.postorder() == [1, 2, 4, 3, 7, 10, 9, 8, 6]
    def test_insert(self,avltree:AVLTree)->None:
        avltree.insert(11,11)
        assert avltree.size()==11
        assert avltree.bforder()==[5, 3, 8, 2, 4, 6, 10, 1, 7, 9, 11]
        assert avltree.inorder()==[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        assert avltree.preorder()==[5, 3, 2, 1, 4, 8, 6, 7, 10, 9, 11]
        assert avltree.postorder()==[1, 2, 4, 3, 7, 6, 9, 11, 10, 8, 5]