# Copyright 2026, Vanguard Center, University Mohammed VI Polytechnic

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


"""
This module provides a dynamic array of references to Python objects for
educational purposes. The array doubles its capacity when an append on a
full array, and halves its capacity when usage drops below 25%.
Adapted with modifications from:
Code Fragment 5.3 in "Data Structures and Algorithms in Python",
by Goodrich, Tamassia and Goldwasser
"""


import ctypes


class DynamicArray:
    """A dynamic array class."""

    def __init__(self, container=None):
        """
        Create an array containing the elements in container.
        If none provided, creates an empty array.
        """
        self._count = 0  # count actual elements
        if container is None:  # array capacity
            self._capacity = 1
        else:
            self._capacity = 1 if len(container) == 0 else 1 << (
                len(container) - 1
            ).bit_length()  # number of elements rounded up to a power of two
        self._arr = self._make_array(self._capacity)  # low-level array
        if container:  # not None and nonempty
            for element in container:  # copy elements into the array
                self._arr[self._count] = element
                self._count += 1

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._count

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._count:
            raise IndexError("dynamic array index out of range")
        return self._arr[k]  # retrieve from array

    def __iter__(self):
        """Make the class iterable."""
        for i in range(self._count):
            yield self._arr[i]

    def __repr__(self):
        return f"DynamicArray({list(self)!r})"

    def capacity(self):
        """Return the capacity of the array."""
        return self._capacity

    def insert_last(self, obj):
        """Add object to end of the array."""
        if self._count == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # double capacity
        self._arr[self._count] = obj
        self._count += 1

    def delete_last(self):
        """Removes the last element of the array and returns it."""
        if self._count == 0:
            raise IndexError("delete_last from empty dynamic array.")
        last_element = self._arr[self._count - 1]  # retrieve element to delete
        self._count -= 1
        if self._count <= self._capacity // 4:  # too much free rooms
            self._resize(self._capacity // 2)  # halve capacity
        return last_element

    def is_empty(self):
        """Return True if the array is empty"""
        return self._count == 0

    def print(self):
        """Prints the content of the array and its capacity."""
        if self._count == 0:
            print("The array is empty.")
        else:
            print("Array content: ", end='')
            for k in range(self._count - 1):
                print(self._arr[k], end=', ')
            print(self._arr[self._count - 1])
        print(f"Array capacity: {self._capacity}")

    def _resize(self, c):  # utility method
        """Resize internal array to capacity c."""
        c = max(c, 1)
        new_arr = self._make_array(c)  # new (bigger) array
        for k in range(self._count):  # copy existing elements to B
            new_arr[k] = self._arr[k]
        self._arr = new_arr  # make new_arr the low-level array
        self._capacity = c

    def _make_array(self, c):  # utility method
        """Return new array with capacity c."""
        return (c * ctypes.py_object)()
