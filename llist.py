"""A doubly-linked list"""

class LLNode(object):
    """A single node in the list.

    The pointers to the next and previous nodes should not be manipulated
    directly, but only through the LList class. Directly setting the pointers
    can create an inconsistent LList object.

    Attributes:
        value: the value stored at this node
        prev: the previous node in the list
        next: the next node in the list
    """

    def __init__(self, value, prev_node, next_node):
        self.value = value
        self.prev = prev_node
        self.next = next_node

    def __repr__(self):
        return 'LLNode({})'.format(self.value)

class LList(object):
    """Doubly-linked list class.

    Implemented as a cycle of LLNode objects, with a single sentinel LLNode to
    delimit the start/end of the list.

    Args:
        values (optional): an iterable of values to initially populate the LList

    Attributes:
        sentinel: the LLNode pointing to the start and end of the LList
    """

    def __init__(self, values=None):
        self.sentinel = LLNode(None, None, None)
        self.sentinel.next = self.sentinel.prev = self.sentinel
        self._len = 0
        if values is not None:
            for val in values:
                self.append(val)
                self._len += 1

    def __bool__(self):
        return self.sentinel.next is not self.sentinel

    @property
    def head(self):
        """The first LLNode in the list, or None if it is empty."""
        if not self:
            return None
        else:
            return self.sentinel.next

    @property
    def tail(self):
        """The last LLNode in the list, or None if it is empty."""
        if not self:
            return None
        else:
            return self.sentinel.prev

    def insert(self, value, prev):
        """Insert `value` in a new LLNode immediately following `prev`."""
        node = LLNode(value, prev, prev.next)
        prev.next = node
        prev.next.prev = node
        self._len += 1
        return node

    def push(self, value):
        """Push `value` onto the beginning of the LList in a new LLNode."""
        return self.insert(value, self.sentinel)

    def append(self, value):
        """Append `value` to the end of the LList in a new LLNode."""
        return self.insert(value, self.sentinel.prev)

    def extend(self, other):
        """Append every value of LList `other` to the end of `self`.

        This removes all the nodes from `other`."""
        if not other:
            return
        tail = self.tail if self else self.sentinel
        tail.next = other.head
        other.head.prev = tail
        other.tail.next = self.sentinel
        self.sentinel.prev = other.tail
        self._len += len(other)
        other.sentinel.prev = other.sentinel.next = other.sentinel
        other.clear()

    def clear(self):
        """Remove every node from `self`.

        The nodes themselves will be left in an inconsistent state (i.e.,
        points will not be set to None).
        """
        self._len = 0
        self.sentinel.next = self.sentinel.prev = self.sentinel

    def remove(self, node):
        """Remove `node` from `self`."""
        if node is self.sentinel:
            raise ValueError("node out of bounds")
        node.prev.next, node.next.prev = node.next, node.prev
        node.next = node.prev = None

    def __len__(self):
        """Get the length of the list.

        This uses only O(1) time but the correctness requires that the linked
        list is only manipulated via the methods of this class (and any
        subclasses)

        Returns:
            int: the length of the list.
        """
        return self._len

    def __iter__(self):
        def llist_iter():
            """Generator yielding the list one node at a time."""
            node = self.sentinel
            while node.next != self.sentinel:
                node = node.next
                yield node
        return llist_iter()

    def __repr__(self):
        inner = ', '.join(node.value for node in self)
        return 'LList({})'.format(inner)
