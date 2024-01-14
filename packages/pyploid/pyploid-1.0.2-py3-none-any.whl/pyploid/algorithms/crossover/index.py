from collections.abc import Iterable
from dataclasses import dataclass
from functools import partial
from operator import contains
from typing import TypeAlias, Callable, Sequence

from toolz import flip

from pyploid.types.algorithms.crossover import CrossingOver, ChromosomeOrigin, ChromosomeAssignment, \
    index_predicate_xover, XoverResult
from pyploid.types.cytogenetic_index import SequentialCytogenticIndex
from pyploid.types.gene import Gene

RandomBelow: TypeAlias = Callable[[int], int]
GeneCount: TypeAlias = int


@dataclass(frozen=True)
class XoverRegion:
    start: int
    end: int

    def __contains__(self, position: int) -> bool:
        return self.start <= position <= self.end


def half_half(left: GeneCount, right: GeneCount) -> set[XoverRegion]:
    midpoint: int = max(left, right) // 2
    return {XoverRegion(0, midpoint), XoverRegion(midpoint + 1, max(left, right))}


def create_index_base_xover(
        overlap_sections: Callable[[GeneCount, GeneCount], set[XoverRegion]] = half_half
) -> CrossingOver[SequentialCytogenticIndex]:
    def xover(
            left: Sequence[Gene[SequentialCytogenticIndex]],
            right: Sequence[Gene[SequentialCytogenticIndex]]
    ) -> Iterable[XoverResult[SequentialCytogenticIndex]]:
        overlap_at: set[XoverRegion] = overlap_sections(len(left), len(right))

        def _in_overlap_region(index: SequentialCytogenticIndex) -> bool:
            return any(map(partial(flip(contains), index.index), overlap_at))

        def _predicate(origin: ChromosomeOrigin, index: SequentialCytogenticIndex) -> ChromosomeAssignment:
            return origin.assign(_in_overlap_region(index))

        return index_predicate_xover(_predicate, left, right)

    return xover
