"""Tests for the Trie class and subclasses."""

import unittest
import collections

from py_data_structures import Trie, StringTrie


class TrieTestCase(unittest.TestCase):
    """TestCase class for Trie, Trie.View, and StringTrie"""
    word_list = ("able", "about", "above", "accept",
                 "baby", "back", "bag", "ball")

    @staticmethod
    def get_contents(itr):
        """Get a Counter of tuples for the sequences in itr"""
        return collections.Counter(tuple(x) for x in itr)

    def test_construction(self):
        """Test initialization and Trie.add"""
        test_trie = Trie()
        self.assertNotIn(self.word_list[0], test_trie)

        test_trie = Trie(self.word_list[:-1])
        for word in self.word_list[:-1]:
            self.assertIn(word, test_trie)
        self.assertNotIn(self.word_list[-1], test_trie)
        test_trie.add(self.word_list[-1])
        # representation of the sequence shouldn't matter (tuple vs string)
        self.assertIn(tuple(self.word_list[-1]), test_trie)
        # empty sequences are okay
        self.assertNotIn((), test_trie)
        test_trie.add(())
        self.assertIn((), test_trie)

    def test_len(self):
        """Test Trie.__len__"""
        test_trie = Trie()
        self.assertEqual(len(test_trie), 0)
        test_trie |= self.word_list
        self.assertEqual(len(test_trie), len(self.word_list))

    def test_removal(self):
        """Test remove and discard methods"""
        test_trie = Trie(self.word_list)
        for word in self.word_list:
            self.assertIn(word, test_trie)
            test_trie.remove(word)
            self.assertNotIn(word, test_trie)
        with self.assertRaises(KeyError):
            test_trie.remove(self.word_list[0])
        # discard shouldn't raise an exception
        test_trie.discard(self.word_list[0])

    def test_iteration(self):
        """Test iteration protocol on Trie"""
        test_trie = Trie(self.word_list)
        self.assertEqual(self.get_contents(test_trie),
                         self.get_contents(self.word_list))

    def test_view(self):
        """Test View object returned by Trie.__getitem__"""
        test_trie = Trie(self.word_list)
        test_view = test_trie['ab']
        ab_words = (w for w in self.word_list if w[:2] == 'ab')
        self.assertEqual(self.get_contents(test_view),
                         self.get_contents(ab_words))
        test_trie.clear()
        self.assertEqual(list(test_view), list())
        test_trie.add('abstruse')
        self.assertEqual(self.get_contents(test_view),
                         self.get_contents(['abstruse']))
        with self.assertRaises(ValueError):
            iterator_view = test_trie[iter('ab')]

    def test_strings(self):
        """Test use of string sequences in StringTrie"""
        test_trie = StringTrie(self.word_list)
        for word in test_trie:
            self.assertIsInstance(word, str)
        self.assertEqual(set(test_trie['a']),
                         set(w for w in self.word_list if w[0] == 'a'))

    def test_nonstrings(self):
        """Test use of non-string sequences in Trie"""
        test_trie = Trie()
        test_trie.add(range(5))
        tuple_list = set(tuple(x) for x in test_trie)
        self.assertEqual(tuple_list, set([tuple(range(5))]))
