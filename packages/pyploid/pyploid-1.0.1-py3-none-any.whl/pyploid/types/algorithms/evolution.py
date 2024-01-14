from collections.abc import Sequence
from itertools import chain
from typing import Protocol

from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.algorithms.reproduce import Reproduce
from pyploid.types.algorithms.selection import SelectParents, DetermineOffspringCount
from pyploid.types.algorithms.survival import Survival
from pyploid.types.individual import IndividualType, Population, PopulationFactory


class Evolution(Protocol[IndividualType]):
    def __call__(
            self,
            population: Population[IndividualType]
    ) -> Population[IndividualType]:
        ...


def create_basic_evolution(
        survive: Survival[IndividualType],
        determine_offspring_count: DetermineOffspringCount[IndividualType],
        select_parents: SelectParents[IndividualType],
        reproduce: Reproduce[IndividualType],
        fitness: Fitness[IndividualType],
        create_population: PopulationFactory[IndividualType]
) -> Evolution[IndividualType]:
    def evolution(population: Population[IndividualType]) -> Population[IndividualType]:
        survivors: Sequence[IndividualType] = survive(fitness, population)
        offspring_count: int = determine_offspring_count(population, survivors)
        return create_population(
            chain(survivors, (reproduce(select_parents(survivors)) for _ in range(offspring_count)))
        )

    return evolution
