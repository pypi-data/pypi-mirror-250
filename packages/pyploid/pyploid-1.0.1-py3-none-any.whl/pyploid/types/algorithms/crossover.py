from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from itertools import repeat, chain
from typing import Protocol, Sequence, Callable, Generic, Self

from pyploid.types.cytogenetic_index import CytogeneticIndex
from pyploid.types.gene import Gene, IndexType


class ChromosomeAssignment(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    DROP = 'drop'
    BOTH = 'BOTH'


class ChromosomeOrigin(Enum):
    LEFT = 'left'
    RIGHT = 'right'

    def assign(self, complement: bool) -> ChromosomeAssignment:
        match self:
            case ChromosomeOrigin.LEFT: return ChromosomeAssignment.RIGHT if complement else ChromosomeAssignment.LEFT
            case ChromosomeOrigin.RIGHT: return ChromosomeAssignment.LEFT if complement else ChromosomeAssignment.RIGHT


@dataclass(frozen=True)
class XoverResult(Generic[IndexType]):
    gene: Gene[IndexType]
    assignment: ChromosomeAssignment


class CrossingOver(Protocol[IndexType]):
    def __call__(
            self,
            left: Sequence[Gene[IndexType]],
            right: Sequence[Gene[IndexType]]
    ) -> Iterable[XoverResult[IndexType]]:
        ...


def _tag_genes(
        origin: ChromosomeOrigin,
        genes: Sequence[Gene[IndexType]]
) -> Iterable[tuple[ChromosomeOrigin, Gene[IndexType]]]:
    return zip(repeat(origin), genes)


def index_predicate_xover(
        predicate: Callable[[ChromosomeOrigin, IndexType], ChromosomeAssignment],
        left: Sequence[Gene[IndexType]],
        right: Sequence[Gene[IndexType]]
) -> Iterable[XoverResult[IndexType]]:
    for origin, gene in chain(_tag_genes(ChromosomeOrigin.LEFT, left), _tag_genes(ChromosomeOrigin.RIGHT, right)):
        yield XoverResult(gene, predicate(origin, gene.position))
