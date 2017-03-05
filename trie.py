"""A simple trie, or prefix tree, data structure."""

import itertools

class Trie(object):
    """A simple prefix tree data structure.

    A Trie is data structure for storing sequences of "names," which can be
    aribtrary hashable objects. In the prototypical trie, names are characters
    from an alphabet, and the trie is used to store words (see the subclass
    StringTrie). The Trie is implemented as a mapping from names to children;
    each child is itself a Trie.

    Attributes:
        children: mapping from names to child Tries
        terminal (bool): True if a complete sequence ends here,
                         False otherwise
    """

    def __init__(self):
        self.children = dict()
        self.terminal = False

    def insert(self, seq):
        """Insert a sequence into the Trie.

        After insertion, `seq` will be a valid suffix of `self`.

        Args:
            seq: an iterable of names to be inserted"""
        node = self
        for name in seq:
            if name not in node.children:
                node.children[name] = Trie()
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
        current = self
        # Traverse to node representing `seq`
        for name in seq:
            parent_stack.append((current, name))
            if name not in current.children:
                raise ValueError('sequence not valid trie prefix')
            current = current.children[name]
        if not current.terminal:
            raise ValueError('sequence not terminal in trie')
        current.terminal = False
        descendents = current.children
        while parent_stack and not descendents:
            current, child_name = parent_stack.pop()
            del current.children[child_name]
            descendents = current.children

    def __contains__(self, seq):
        """Check if `seq` is a complete sequence in the Trie.

        Returns:
            True if `seq` is a valid suffix of `self, False otherwise.
        """
        node = self
        for name in seq:
            if name not in node.children:
                return False
            node = node.children[name]
        return node.terminal

    def __getitem__(self, prefix):
        """Get the Trie corresponding to `prefix`, or raise KeyError."""
        node = self
        for name in prefix:
            if name not in node.children:
                raise KeyError('prefix {} not in Trie'.format(prefix))
            node = node.children[name]
        return node

    def iter_completions(self, prefix=None):
        """Iterate over all complete sequences starting with `prefix`.

        Args:
            prefix: a container of names (can't just be an iterator)

        Returns:
            An iterator over all complete sequences starting with `prefix`.
            Each sequence is itself yielded as an iterator, starting with
            prefix
        """

        if prefix is None:
            prefix = ()
            prefix_node = self
        else:
            if prefix is iter(prefix):
                raise ValueError('prefix must be a whatsit, not an iterator')
            try:
                prefix_node = self[prefix]
            except KeyError:
                return iter(())

        def iterator():
            """Generator producing all complete sequences starting with
            prefix."""
            for suffix in prefix_node:
                yield itertools.chain(prefix, suffix)

        return iterator()

    def __iter__(self):
        """Iterate over complete suffixes from `self`."""

        if self.terminal:
            yield iter(())
        for name, child in self.children.items():
            for suffix in child:
                yield itertools.chain((name,), suffix)

class StringTrie(Trie):
    """A Trie class specialized for storing strings, rather than arbitrary
    sequences of objects."""

    def iter_completions(self, prefix=None):
        """Override to yield strings instead of iterators"""
        for word in super().iter_completions(None):
            yield ''.join(word)

    def __iter__(self):
        """Override the default iterator to yield strings instead of
        iterators"""
        for word in super().__iter__():
            yield ''.join(word)
