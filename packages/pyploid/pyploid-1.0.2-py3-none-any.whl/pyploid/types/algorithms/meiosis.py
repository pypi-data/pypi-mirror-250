from collections.abc import Iterable
from operator import attrgetter
from typing import Protocol, Sequence, Callable

from toolz import compose

from pyploid.types.cytogenetic_index import PolyploidIndexType, IndexType
from pyploid.types.gene import Gene, GeneType
from pyploid.types.individual import Individual


class Meiosis(Protocol[GeneType]):
    def __call__(self, individual: Individual[GeneType]) -> Sequence[GeneType]:
        ...


def predicate_meiosis(
    predicate: Callable[[PolyploidIndexType], bool],
    individual: Individual[Gene[PolyploidIndexType]],
    *,
    seq_factory: Callable[[Iterable[Gene[PolyploidIndexType]]], Sequence[Gene[PolyploidIndexType]]] = tuple
) -> Sequence[Gene[PolyploidIndexType]]:
    return seq_factory(filter(compose(predicate, attrgetter('position')), individual.genes))


