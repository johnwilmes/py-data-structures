"""A simple trie, or prefix tree, data structure."""

import itertools

class Trie(object):
    """A simple prefix tree data structure.

    A Trie is data structure for storing sequences of "names," which can be
    aribtrary hashable objects. In the prototypical trie, names are characters
    from an alphabet, and the trie is used to store words (see the subclass
    StringTrie). The Trie is implemented internally as a tree, each node of
    which is a Trie.Node object.

    Attributes:
        root (Trie.Node): the root node of the trie, corresponding to the empty
            prefix
    """
    class Node(object):
        """A node of a Trie object.

        An instance represents a single node of a trie, corresponding a
        specific prefix sequence of names, which may or may not be a complete
        sequence.

        Attributes:
            children (dict): mapping from names to child Nodes
            terminal (bool): True if a complete sequence ends here,
                             False otherwise
        """
        def __init__(self):
            self.children = dict()
            self.terminal = False

        def __iter__(self):
            """Iterate over complete suffixes from `self`."""
            if self.terminal:
                yield iter(())
            for name, child in self.children.items():
                for suffix in child:
                    yield itertools.chain((name,), suffix)

    class View(object):
        """A view of a sub-trie of a Trie object.

        This class allows accessing (but not modifying) the sequences in the
        Trie completing a given prefix.

        Attributes:
            prefix: the sequence of names prefixing everything in this
                sub-trie, corresponding to the path from the root of the
                original Trie to this sub-trie
            root (Node): the root of this sub-trie
        """
        def __init__(self, prefix, root):
            self.prefix = prefix
            self.root = root

        def __iter__(self):
            for suffix in self.root:
                yield itertools.chain(self.prefix, suffix)

    def __init__(self):
        self.root = self.Node()

    def insert(self, seq):
        """Insert a sequence into the Trie.

        After insertion, `seq` will be a valid suffix of `self`.

        Args:
            seq: an iterable of names to be inserted"""
        node = self.root
        for name in seq:
            if name not in node.children:
                node.children[name] = self.Node()
            node = node.children[name]
        node.terminal = True

    def remove(self, seq):
        """Remove `seq` from the Trie.

        Prunes the trie to remove all prefixes for which `seq` is the only
        valid completion

        Args:
            seq: an iterable of names to be removed

        Raises:
            ValueError: if `seq` is not a complete word in the trie
        """
        parent_stack = list()
        node = self.root
        # Traverse to node representing `seq`
        for name in seq:
            parent_stack.append((node, name))
            if name not in node.children:
                raise ValueError('sequence not valid trie prefix')
            node = node.children[name]
        if not node.terminal:
            raise ValueError('sequence not terminal in trie')
        node.terminal = False
        descendents = node.children
        while parent_stack and not descendents:
            node, child_name = parent_stack.pop()
            del node.children[child_name]
            descendents = node.children

    def __contains__(self, seq):
        """Check if `seq` is a complete sequence in the Trie.

        Returns:
            True if `seq` is a valid suffix of `self, False otherwise.
        """
        node = self.root
        for name in seq:
            if name not in node.children:
                return False
            node = node.children[name]
        return node.terminal

    def __getitem__(self, prefix):
        """Get a view of the Trie corresponding to `prefix`, or raise KeyError."""
        if prefix is iter(prefix):
            raise ValueError('prefix must be a container, not an iterator')
        node = self.root
        for name in prefix:
            if name not in node.children:
                raise KeyError('prefix not in Trie')
            node = node.children[name]
        return self.View(prefix, node)

    def __iter__(self):
        """Iterate over complete suffixes from `self`."""
        return iter(self.root)

class StringTrie(Trie):
    """A Trie class specialized for storing strings, rather than arbitrary
    sequences of objects."""
    class View(Trie.View):
        """A view of a sub-trie of a StringTrie object.

        This class specializes the Trie.View class to yield strings as
        appropriate, rather than generic iterators.
        """
        def __iter__(self):
            for word in super().__iter__():
                yield ''.join(word)

    def __iter__(self):
        """Override the default iterator to yield strings instead of
        iterators"""
        for word in super().__iter__():
            yield ''.join(word)
