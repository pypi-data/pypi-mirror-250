from typing import Protocol, Self, TypeAlias, TypeVar, Sequence

GenePosition: TypeAlias = int
Qualifier: TypeAlias = Sequence[int | float | str | bool]


class CytogeneticIndex(Protocol):
    def __lt__(self, other: Self) -> bool: ...

    def __eq__(self, other: object) -> bool: ...

    def __hash__(self) -> int: ...

    def qualifier(self) -> Qualifier:
        ...


class TrivialCytogeneticIndex(CytogeneticIndex):
    def __lt__(self, other: Self): return False

    def __eq__(self, other: object): return True if self is other else False

    def qualifier(self) -> Qualifier:
        return []




class SequentialCytogenticIndex(CytogeneticIndex, Protocol):
    index: int


class ComplexCytogeneticIndex(CytogeneticIndex, Protocol):
    chromosome_number: int


class PolyploidCytogeneticIndex(CytogeneticIndex, Protocol):
    set_index: int


class ComplexPolyploidCytogeneticIndex(
    ComplexCytogeneticIndex, PolyploidCytogeneticIndex, SequentialCytogenticIndex, Protocol
):
    def reindex(self, chromosome_number: int, set_index: int, index: int) -> Self:  ...


IndexType = TypeVar('IndexType', bound=CytogeneticIndex)
SecondaryIndexType = TypeVar('SecondaryIndexType', bound=CytogeneticIndex)
PolyploidIndexType = TypeVar('PolyploidIndexType', bound=PolyploidCytogeneticIndex)
ComplexPolyploidIndexType = TypeVar('ComplexPolyploidIndexType', bound=ComplexPolyploidCytogeneticIndex)

