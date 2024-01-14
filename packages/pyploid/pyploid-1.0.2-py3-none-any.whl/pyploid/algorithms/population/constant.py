from collections.abc import Sequence

from pyploid.types.individual import IndividualType, Population


def constant_population(population: Population[IndividualType], survivors: Sequence[IndividualType]) -> int:
    return len(population.members) - len(survivors)