"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log2
import time
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxLeft(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current = top.left
            while current.right is not None:
                parent = current
                current = current.right
            top.data = current.data
            if parent == top:
                top.left = current.left
            else:
                parent.right = current.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        removed = None
        pre = BSTNode(None)
        pre.left = self._root
        parent = pre
        direction = 'L'
        current = self._root
        while current is not None:
            if current.data == item:
                removed = current.data
                break
            parent = current
            if current.data > item:
                direction = 'L'
                current = current.left
            else:
                direction = 'R'
                current = current.right

        # Return None if the item is absent
        if removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current.left == None \
                and not current.right == None:
            liftMaxLeft(current)
        else:

            # Case 2: The node has no left child
            if current.left == None:
                new = current.right

                # Case 3: The node has no right child
            else:
                new = current.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new
            else:
                parent.right = new

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre.left
        return removed

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old = probe.data
                probe.data = newItem
                return old
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            return 0 if top.left is None and top.right is None else 1 + max([
                height1(top.left) if top.left else 0,
                height1(top.right) if top.right else 0
            ])
        return height1(self._root)

    def __count(self, node):
        """
        Counts the nodes of the tree
        :param node: int
        :return: int
        """
        return 0 if node is None else 1 + self.__count(node.left) + self.__count(node.right)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log2(self.__count(self._root) + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        ans = []
        for i in self.inorder():
            if low <= i <= high:
                ans.append(i)
        return ans

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        ans = [self.remove(i) for i in self.inorder()]
        def rec(elements):
            if len(elements) == 0:
                return None
            mid = len(elements) // 2
            node = BSTNode(elements[mid])
            node.left = rec(elements[:mid])
            node.right = rec(elements[mid + 1:])

            return node

        self._root = rec(ans)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for i in self.inorder():
            if i > item:
                return i
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        previous = None
        for i in self.inorder():
            if i >= item:
                return previous
            previous = i
        return previous

    @staticmethod
    def reader(path):
        """
        Reads the tree and returns the list.
        """
        ans = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                ans.append(line.strip('\n'))
        return ans

    @staticmethod
    def begin():
        """
        Starts the time.
        """
        return time.process_time()

    @staticmethod
    def stop():
        """
        Stops the time
        """
        return time.process_time()

    @staticmethod
    def finder_of_list(tree, finder):
        """
        Finds the list of 10000 words and returns the time.
        """
        begin = tree.begin()
        for i in finder:
            for j in tree:
                if i == j:
                    break
        stop = tree.stop()
        return stop - begin

    @staticmethod
    def ordered_finder(dct_ordered, lst):
        """
        Finds 10000 words in an ordered dictionary and returns the time.
        """
        tree = LinkedBST()
        for i in dct_ordered:
            tree.add(i)
        begin = tree.begin()
        for i in lst:
            tree.find(i)
        stop = tree.stop()
        return stop - begin

    @staticmethod
    def not_ordered_finder(dct_not_ordered, lst):
        """
        Finds 10000 words in a not ordered dictionary and returns the time.
        """
        random.shuffle(dct_not_ordered)
        tree = LinkedBST()
        for i in dct_not_ordered:
            tree.add(i)
        begin = tree.begin()
        for j in lst:
            tree.find(j)
        stop = tree.stop()
        return stop - begin

    @staticmethod
    def balance_finder(dct_of_words, lst):
        """
        Returns the time for the making of the balanced tree with 10000 words.
        """
        tree = LinkedBST()
        for i in dct_of_words:
            tree.add(i)
        tree.rebalance()
        begin = tree.begin()
        for i in lst:
            tree.find(i)
        stop = tree.stop()
        return stop - begin

    def demo_bst(self, path, lst):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param lst: list
        :param path: path to the tree
        :type path: str
        :return: list of words
        :rtype: list
        """
        return self.balance_finder(self.reader(path), lst)
