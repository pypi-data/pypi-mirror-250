"""
Python library for instantiating and working with permutation collections
that provide efficient implementations of all sequence methods (including
random-access retrieval by index).
"""
from __future__ import annotations
from typing import Any, Iterable
import doctest
import collections.abc
import operator
import functools

class permutations(collections.abc.Sequence):
    """
    Sequence of all permutations of a specific collection of elements.

    >>> list(permutations(range(3)))
    [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]

    An optional length parameter ``r`` can be supplied to restrict the output
    to only permutations of ``r`` elements.

    >>> list(permutations(range(3), 2))
    [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

    Individual permutations within an instance can be retrieved by their
    index.

    >>> ps = permutations(range(5))
    >>> ps[37]
    (1, 3, 0, 4, 2)

    The code below confirms that the functional behavior of this class is
    equivalent to the built-in :obj:`itertools.permutations` function over
    a range of small inputs.

    >>> import itertools
    >>> for n in range(2, 7):
    ...     for r in range(0, n + 3):
    ...         reference = list(itertools.permutations(range(n), r))
    ...         candidate = permutations(range(n), r)
    ...         assert(reference == list(candidate))
    ...         assert(all(candidate[i] == reference[i] for i in range(len(reference))))

    An exception is raised when arguments are not of a correct type or
    our outside the supported range.

    >>> permutations(123)
    Traceback (most recent call last):
      ...
    TypeError: object is not iterable
    >>> permutations(range(3), 'abc')
    Traceback (most recent call last):
      ...
    TypeError: Expected int as r
    >>> permutations(range(3), -2)
    Traceback (most recent call last):
      ...
    ValueError: r must be non-negative
    """
    def __init__(self: permutations, iterable: Iterable, r: int = None):
        """
        Instantiate an instance for an iterable of elements and an optional
        permutation length.
        """
        if not isinstance(iterable, collections.abc.Iterable):
            raise TypeError('object is not iterable')

        self._iterable = tuple(iterable)
        self._n = len(self._iterable)

        if r is not None:
            if not isinstance(r, int):
                raise TypeError('Expected int as r')

            if r < 0:
                raise ValueError('r must be non-negative')

        self._r = self._n if r is None else r
        self._length = functools.reduce(
            operator.mul,
            range(self._n, self._n - self._r, -1),
            1
        )

    def __len__(self: permutations) -> int:
        """
        Return the number of distinct permutations in the collection
        represented by this instance.

        >>> len(permutations(range(8))) == 8 * 7 * 6 * 5 * 4 * 3 * 2 * 1
        True
        """
        return self._length

    def __getitem__(self: permutations, key: int) -> Any:
        """
        Return a specific permutation corresponding to the supplied index.
        Permutations are indexed in the same order as that used by the
        built-in :obj:`itertools.permutations` function.

        >>> ps = permutations(range(5))
        >>> ps[37]
        (1, 3, 0, 4, 2)

        This method makes it possible to retrieve a permutation that
        appears anywhere in the sequence using its index. The permutation
        is built directly using the supplied index (*i.e.*, no iteration
        occurs over the elements in this instance).

        >>> permutations(range(20))[7**20]
        (0, 13, 9, 6, 14, 8, 17, 1, 5, 12, 15, 18, 11, 16, 10, 2, 3, 4, 19, 7)

        An exception is raised when the supplied argument is not of the
        correct type or is out of range.

        >>> ps['abc']
        Traceback (most recent call last):
          ...
        TypeError: indices must be integers
        >>> ps[-1]
        (4, 3, 2, 1, 0)
        >>> ps[(5 * 4 * 3 * 2 * 1) + 1]
        Traceback (most recent call last):
          ...
        IndexError: index out of range
        """
        if not isinstance(key, int):
            raise TypeError('indices must be integers')

        i = key # Only integer indices are supported.

        if i >= self._length or i < -self._length:
            raise IndexError('index out of range')

        i = i % self._length # Handle negative indices.

        # Build up the specific permutation by using the supplied integer
        # as a "variable-base" representation of the particular permutation.
        ns = list(range(self._n))
        remainders = []
        permutation = []
        for j in range(self._n - self._r, self._n):
            (i, remainder) = divmod(i, j + 1)
            remainders.append(remainder)
        for remainder in reversed(remainders):
            element = ns[remainder]
            del ns[remainder]
            permutation.append(element)

        return tuple(permutation)

    def __iter__(self: permutations) -> collections.abc.Iterator:
        """
        Return an iterator that yields every permutation included in
        this instance.

        >>> [p for p in permutations(range(3), 2)]
        [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

        Permutations appear in the same order as that
        used by the built-in :obj:`itertools.permutations` function.

        >>> import itertools
        >>> [p for p in itertools.permutations(range(3), 2)]
        [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
        """
        return (self[i] for i in range(self._length))

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
