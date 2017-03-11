"""A simple trie, or prefix tree, data structure."""

import itertools
import collections.abc

class Trie(collections.abc.MutableSet):
    """A simple prefix tree data structure.

    A Trie is data structure for storing sequences of "names," which can be
    aribtrary hashable objects. In the prototypical trie, names are characters
    from an alphabet, and the trie is used to store words (see the subclass
    StringTrie). The Trie is implemented internally as a tree, each node of
    which is a Trie.Node object.
    """
    class Node(object):
        """A node of a Trie object.

        An instance represents a single node of a trie, corresponding a
        specific prefix sequence of names, which may or may not be a complete
        sequence. All attributes must be maintained by the user (Trie).

        Attributes:
            children (dict): mapping from names to child Nodes
            terminal (bool): True if a complete sequence ends here,
                False otherwise
            size (int): the number of complete sequences for which this is a
                prefix
        """
        def __init__(self):
            self.children = dict()
            self.terminal = False
            self.size = 0

        def __len__(self):
            return self.size

        def __iter__(self):
            """Iterate over complete suffixes from `self`."""
            if self.terminal:
                yield iter(())
            for name, child in self.children.items():
                for suffix in child:
                    yield itertools.chain((name,), suffix)

        def __contains__(self, seq):
            """Check if `seq` is a complete suffix from `self`

            Returns:
                True if `seq` is a valid suffix of `self, False otherwise.
            """
            node = self
            for name in seq:
                if name not in node.children:
                    return False
                node = node.children[name]
            return node.terminal

    class View(collections.abc.Set):
        """A view of a sub-trie of a Trie object.

        This class allows accessing (but not modifying) the sequences in the
        Trie completing a given prefix.

        Args:
            trie_root: the root node of the original Trie object of which this
                is a sub-trie
            prefix: the sequence of names prefixing everything in this
                sub-trie, corresponding to the path from the root of the
                original Trie to this sub-trie
        """
        def __init__(self, trie_root, prefix):
            self.prefix = prefix
            self._trie_root = trie_root
            # The root node of this sub-trie, corresponding to prefix. It will
            # be found when needed
            self._prefix_root = None

        def _validate_root(self):
            """Ensure that `self._prefix_root` is valid for `self._trie_root`
            and `self.prefix`.

            If the entire sub-Trie at `self._prefix_root` is removed, then
            `self._prefix_root` will no longer be a descendant of
            `self._trie_root`.  If a sequence with prefix `self.prefix` is
            added back into the Trie, it will use a new Trie.Node in place of
            self._prefix_root. We need to find that node and use it in place of
            self._prefix_root.
            """
            root = self._prefix_root
            # check if root is still okay
            if root is not None and (root.children or root.terminal):
                return # everything is still okay
            # self._root is invalid; check for a replacement node
            self._prefix_root = None
            node = self._trie_root
            for name in self.prefix:
                if name not in node.children:
                    return
                node = node.children[name]
            self._prefix_root = node

        def __iter__(self):
            self._validate_root()
            if self._prefix_root is None:
                return
            for suffix in self._prefix_root:
                yield itertools.chain(self.prefix, suffix)

        def __len__(self):
            self._validate_root()
            if self._prefix_root is not None:
                return self._prefix_root.size
            return 0

        def __contains__(self, seq):
            self._validate_root()
            if self._prefix_root is None:
                return False
            seq = iter(seq)
            for name in self.prefix:
                if name != next(seq):
                    return False
            return seq in self._prefix_root

    def __init__(self):
        self._root = self.Node() # root node corresponding to empty prefix

    def __len__(self):
        return self._root.size

    def __iter__(self):
        """Iterate over complete suffixes from `self`."""
        return iter(self._root)

    def __contains__(self, seq):
        """Check if `seq` is a complete sequence in the Trie.

        Returns:
            True if `seq` is a valid suffix of `self, False otherwise.
        """
        return seq in self._root

    def add(self, seq):
        """Insert a sequence into the Trie.

        After insertion, `seq` will be a valid suffix of `self`.

        Args:
            seq: an iterable of names to be inserted"""
        node = self._root
        for name in seq:
            if name not in node.children:
                node.children[name] = self.Node()
            node = node.children[name]
        node.terminal = True

    def discard(self, seq):
        """Remove `seq` from the Trie.

        Prunes the trie to remove all prefixes for which `seq` is the only
        valid completion

        Args:
            seq: an iterable of names to be removed
        """
        parent_stack = list()
        node = self._root
        # Traverse to node representing `seq`
        for name in seq:
            parent_stack.append((node, name))
            if name not in node.children:
                return
            node = node.children[name]
        if not node.terminal:
            return
        node.terminal = False
        descendents = node.children
        while parent_stack and not descendents:
            node, child_name = parent_stack.pop()
            del node.children[child_name]
            descendents = node.children

    def __getitem__(self, prefix):
        """Get a view of the Trie corresponding to `prefix`.

        `prefix` does not necessarily need to currently be in Trie. This view
        will be dynamically updated as sequences are added or removed from
        `self`.

        Args:
            prefix: a container (not a single-use iterator) with the sequence
                of names identifying the sub-Trie to be viewed.
        """
        if prefix is iter(prefix):
            raise ValueError('prefix must be a container, not an iterator')
        return self.View(self._root, prefix)

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
