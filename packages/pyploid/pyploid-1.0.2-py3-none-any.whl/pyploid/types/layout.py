from collections.abc import Sequence
from typing import Protocol, Iterable

from pyploid.types.cytogenetic_index import IndexType, SecondaryIndexType
from pyploid.types.gene import Gene


class GeneLayout(Protocol[SecondaryIndexType, IndexType]):
    def __call__(self, genes: Sequence[Gene[IndexType]]) -> Iterable[Gene[SecondaryIndexType]]: ...