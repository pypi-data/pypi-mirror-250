from collections.abc import Sequence
from typing import Protocol

from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.individual import Population, IndividualType


class Survival(Protocol[IndividualType]):
    def __call__(
            self,
            fitness: Fitness[IndividualType],
            population: Population[IndividualType]
    ) -> Sequence[IndividualType]:
        ...
