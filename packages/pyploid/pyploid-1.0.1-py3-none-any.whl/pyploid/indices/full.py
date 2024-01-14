from collections.abc import Iterator
from dataclasses import dataclass, replace
from typing import Self, Sequence


@dataclass(frozen=True)
class FullCytogeneticIndex:
    chromosome_number: int
    set_index: int
    index: int

    def __iter__(self) -> Iterator[int | str]:
        return iter((self.chromosome_number, self.index))

    def __lt__(self, other: Self) -> bool:
        return tuple(self) < tuple(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FullCytogeneticIndex):
            return NotImplemented
        return tuple(self) == tuple(other)

    def qualifier(self) -> tuple[int]:
        return self.chromosome_number,


    def reindex(self, chromosome_number: int, set_index: int, index: int) -> Self:
        return replace(self, chromosome_number=chromosome_number, set_index=set_index, index=index)
