from collections.abc import Sequence
from typing import Protocol

from pyploid.types.individual import Population, IndividualType


class SelectParents(Protocol[IndividualType]):
    def __call__(
            self,
            candidates: Sequence[IndividualType]
    ) -> Sequence[IndividualType]:
        ...


class DetermineOffspringCount(Protocol[IndividualType]):
    def __call__(
        self,
        population: Population[IndividualType],
        survivors: Sequence[IndividualType]
    ) -> int:
        ...