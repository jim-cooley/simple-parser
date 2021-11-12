from collections import deque
from dataclasses import dataclass

from runtime import exceptions


@dataclass
class RuntimeStack(object):
    """
    RuntimeStack:
    Provides stack implementation on top of deque object
    """
    def __init__(self):
        self._stack = deque()

    def is_empty(self):
        return True if len(self._stack) == 0 else False

    def depth(self):
        return len(self._stack)

    def peek(self):
        return self._stack[-1]

    def push(self, x):
        self._stack.append(x)

    def push_all(self, l):
        for item in l:
            self.push(item)

    def pop(self):
        if self.is_empty():
            exceptions.runtime_error(f'Stack underflow', loc=None)
        return self._stack.pop()

    def clear(self):
        self._stack.clear()
        self._stack = deque()