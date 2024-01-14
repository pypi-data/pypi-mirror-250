from collections.abc import Sequence
from functools import partial
from math import floor
from operator import itemgetter
from typing import cast

from toolz import take_nth, take

from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.algorithms.survival import Survival
from pyploid.types.individual import IndividualType, Population


def top_n_percent_survive(
        ratio: float,
        fitness: Fitness[IndividualType],
        population: Population[IndividualType]
) -> Sequence[IndividualType]:
    survivor_count: int = floor(len(population.members) * ratio)
    fitness_values: dict[int, float] = dict(
        sorted(
            ((i, fitness(member)) for i, member in enumerate(population.members)),
            key=itemgetter(1)
        )
    )
    return list(
        take(survivor_count, (population.members[i] for i in fitness_values))
    )


def create_ratio_survival(ratio: float) -> Survival[IndividualType]:
    return cast(Survival[IndividualType], partial(top_n_percent_survive, ratio))