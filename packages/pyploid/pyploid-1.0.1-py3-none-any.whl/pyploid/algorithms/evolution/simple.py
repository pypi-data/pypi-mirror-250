from random import Random, SystemRandom

from toolz import identity

from pyploid.algorithms.meiosis.even import create_even_meiosis
from pyploid.algorithms.population.constant import constant_population
from pyploid.algorithms.selection.tournament import create_tournament_selection
from pyploid.algorithms.survival.ratio import create_ratio_survival
from pyploid.individual.trivial import create_trivial_population
from pyploid.types.algorithms.evolution import create_basic_evolution, Evolution
from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.algorithms.mutation import Mutation
from pyploid.types.algorithms.reproduce import create_reproduction, IndividualFactory
from pyploid.types.cytogenetic_index import ComplexPolyploidIndexType
from pyploid.types.gene import Gene
from pyploid.types.individual import Individual


def create_simple_evolution(
        fitness: Fitness[Individual[Gene[ComplexPolyploidIndexType]]],
        create_individual: IndividualFactory[ComplexPolyploidIndexType],
        survivor_ratio: float = 0.5,
        mutation: Mutation[Gene[ComplexPolyploidIndexType]] = identity,
        random: Random = SystemRandom()
) -> Evolution[Individual[Gene[ComplexPolyploidIndexType]]]:
    return create_basic_evolution(
        create_ratio_survival(survivor_ratio),
        constant_population,
        create_tournament_selection(fitness, random=random),
        create_reproduction(create_even_meiosis(random), create_individual, mutation),
        fitness,
        create_trivial_population
    )
