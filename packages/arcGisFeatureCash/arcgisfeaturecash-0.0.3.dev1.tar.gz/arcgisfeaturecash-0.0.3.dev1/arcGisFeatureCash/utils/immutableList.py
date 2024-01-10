from typing import List, Iterator, TypeVar, SupportsIndex, overload, Iterable, Any

T = TypeVar("T")


class ImmutableList(list):
    def __init__(self, *args: List[T]) -> None:
        super().__init__(*args)
        self._items = list(args)

    @overload
    def __setitem__(self, i: SupportsIndex, o: T) -> None:
        ...

    @overload
    def __setitem__(self, s: slice, o: Iterable[T]) -> None:
        ...

    def __setitem__(self, *args: T) -> None:
        raise TypeError("ImmutableList is immutable, cannot modify elements")

    def __delitem__(self, index: SupportsIndex | slice) -> None:
        raise TypeError("ImmutableList is immutable, cannot delete elements")

    def append(self, value) -> None:
        raise TypeError("ImmutableList is immutable, cannot append elements")

    def extend(self, iterable: Iterable[Any]) -> None:
        raise TypeError("ImmutableList is immutable, cannot extend elements")

    def insert(self, index: SupportsIndex, value) -> None:
        raise TypeError("ImmutableList is immutable, cannot insert elements")

    def remove(self, value) -> None:
        raise TypeError("ImmutableList is immutable, cannot remove elements")

    def pop(self, index: SupportsIndex = -1):
        raise TypeError("ImmutableList is immutable, cannot pop elements")

    def clear(self) -> None:
        raise TypeError("ImmutableList is immutable, cannot clear elements")

    def reverse(self) -> None:
        raise TypeError("ImmutableList is immutable, cannot reverse elements")

    def sort(self, key=None, reverse: bool = False) -> None:
        raise TypeError("ImmutableList is immutable, cannot sort elements")

    def __iadd__(self, other: Iterable[T]) -> "ImmutableList":
        raise TypeError(
            "ImmutableList is immutable, cannot use '+=' to modify elements"
        )

    def __imul__(self, n: SupportsIndex) -> "ImmutableList":
        raise TypeError(
            "ImmutableList is immutable, cannot use '*=' to modify elements"
        )

    # Allow read-only access to the elements
    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"ImmutableList({self._items})"

    def __iter__(self) -> Iterator:
        return iter(self._items)

    def copy(self) -> "ImmutableList":
        return ImmutableList(self._items.copy())

    def count(self, value) -> int:
        return self._items.count(value)

    def index(self, value, start=0, stop=None) -> int:
        return self._items.index(value, start, stop)

    def __add__(self, other: List) -> "ImmutableList":
        return ImmutableList(self._items + other)

    def __mul__(self, n: SupportsIndex) -> "ImmutableList":
        return ImmutableList(self._items * n)

    def __contains__(self, value) -> bool:
        return value in self._items

    def __eq__(self, other) -> bool:
        if isinstance(other, ImmutableList):
            return self._items == other._items
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
