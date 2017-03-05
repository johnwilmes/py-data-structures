"""A singly-linked list"""

class SLNode(object):
    """A single node in the list.

    Attributes:
        value: the value stored at this node
        next: the next node in the list
    """

    def __init__(self, value, next_node):
        self.value = value
        self.next = next_node

    def __repr__(self):
        return 'SLNode({})'.format(self.value)

class SList(object):
    """Singly-linked list class.

    Implemented as a cycle of SLNode objects, with a single sentinel SLNode at
    the end, pointing to the beginning.

    Args:
        values (optional): an iterable of values to initially populate the
        LList

    Attributes:
        sentinel: the SLNode at the end of the list, pointing to the start
    """
    def __init__(self, values=None):
        self.sentinel = SLNode(None, None)
        self.sentinel.next = self.sentinel
        self._tail = None
        self._len = 0
        if values is not None:
            for value in values:
                self.append(value)
                self._len += 1

    def __bool__(self):
        return self.sentinel.next is not self.sentinel

    @property
    def head(self):
        """The first SLNode in the list, or None if it is empty."""
        if not self:
            return None
        else:
            return self.sentinel.next

    @property
    def tail(self):
        """The last SLNode in the list, or None if it is empty."""
        if not self:
            return None
        else:
            return self._tail

    def insert(self, value, prev):
        """Insert `value` in a new SLNode immediately following `prev`.

        Args:
            value: the value to insert
            prev: the SLNode that should precede the newly created node

        Returns:
            the new SLNode containing `value`
        """
        node = SLNode(value, prev.next)
        if prev.next is self.sentinel:
            self._tail = node
        prev.next = node
        self._len += 1
        return node

    def push(self, value):
        """Push `value` to the front of the SList in a new SLNode.

        Args:
            value: the value to push onto the front of the list

        Returns:
            the new SLNode containing `value`
        """
        return self.insert(value, self.sentinel)

    def append(self, value):
        """Append `value` to the end of the SList in a new SLNode.

        Args:
            value: the value to append

        Returns:
            the new SLNode containing `value`
        """
        tail = self.tail if self else self.sentinel
        return self.insert(value, tail)

    def clear(self):
        """Remove all nodes from the list.

        The nodes themselves will be left in an inconsistent state (i.e.,
        pointers will not be set to None).
        """
        self._len = 0
        self.sentinel.next = self.sentinel

    def extend(self, other):
        """Append every value of SList `other` to the end of `self`.

        This removes all the nodes from `other`."""
        if not other:
            return
        self._len += len(other)
        tail = self._tail if self else self.sentinel
        tail.next = other.head
        self._tail = other.tail
        self._tail.next = self.sentinel
        other.sentinel.next = other.sentinel
        other.clear()

    def remove_next(self, node):
        """Remove `node.next` from the linked list."""
        if node.next is self.sentinel:
            raise ValueError("node out of bounds")
        self._len -= 1
        removed_node = node.next
        node.next = removed_node.next
        if node.next is self.sentinel:
            self._tail = node
        removed_node.next = None

    def __len__(self):
        """Get the length of the list.

        This requires O(1) time, but correctness requires that the linked list
        is only manipulated via the methods of this class (and any subclasses)

        Returns:
            int: the length of the list.
        """
        return self._len

    def __iter__(self):
        def slist_iter():
            """Generator yielding the list one node at a time."""
            node = self.sentinel
            while node.next != self.sentinel:
                node = node.next
                yield node
        return slist_iter()

    def __repr__(self):
        inner = ', '.join(node.value for node in self)
        return 'SList({})'.format(inner)
