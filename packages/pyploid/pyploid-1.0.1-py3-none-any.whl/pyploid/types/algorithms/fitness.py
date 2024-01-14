from functools import lru_cache, wraps
from typing import Protocol

from pyploid.types.cytogenetic_index import IndexType
from pyploid.types.individual import Individual, NamedIndividual, EvaluatedIndividual, ContravariantIndividualType


class Fitness(Protocol[ContravariantIndividualType]):
    def __call__(self, individual: ContravariantIndividualType) -> float: ...


def create_caching_fitness(
        fitness: Fitness[NamedIndividual[IndexType]],
        max_size: int = 128
) -> Fitness[NamedIndividual[IndexType]]:
    @wraps(fitness)
    @lru_cache(max_size)
    def cached_fitness(individual: NamedIndividual) -> float:
        return fitness(individual)

    return cached_fitness


def make_evaluation_aware(
        fitness: Fitness[Individual[IndexType]],
        asign: bool = False
) -> Fitness[EvaluatedIndividual[IndexType]]:
    def use_prior_evaluation(individual: EvaluatedIndividual[IndexType]) -> float:
        if individual.fitness is None:
            evaluation: float = fitness(individual)
            if asign:
                individual.fitness = evaluation
            return evaluation
        else:
            return individual.fitness

    return use_prior_evaluation
