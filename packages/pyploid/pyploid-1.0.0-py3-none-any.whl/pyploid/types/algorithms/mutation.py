from typing import Protocol, Sequence, Iterable

from pyploid.types.gene import GeneType


class Mutation(Protocol[GeneType]):
    def __call__(self, genes: Sequence[GeneType]) -> Iterable[GeneType]: ...
