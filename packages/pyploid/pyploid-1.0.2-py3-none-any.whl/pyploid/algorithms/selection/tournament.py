from math import log, floor
from random import Random, SystemRandom
from typing import Sequence

from toolz import take, partition

from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.algorithms.selection import SelectParents
from pyploid.types.individual import IndividualType


def create_tournament_selection(
        fitness: Fitness[IndividualType],
        max_rounds: int = 4,
        keep_top: int = 2,
        blur: float | None = None,
        random: Random = SystemRandom()
) -> SelectParents[IndividualType]:
    def tournament_fitness(individual: IndividualType) -> float:
        value: float = fitness(individual)
        if blur:
            value *= random.uniform(blur, 1.0)
        return value

    def select_by_tournament(candidates: Sequence[IndividualType]) -> Sequence[IndividualType]:
        rounds: int = min(max_rounds, floor(log(len(candidates), 2)))
        start_numbers: list[int] = list(range(len(candidates)))
        random.shuffle(start_numbers)
        participants: list[IndividualType] = [
            candidates[start_number] for start_number in take(rounds ** 2, start_numbers)
        ]
        while len(participants) > keep_top:
            participants = [
                min(white, black, key=tournament_fitness)
                for white, black in partition(2, participants)
            ]
        return participants

    return select_by_tournament
