from collections.abc import Sequence
from functools import reduce
from random import Random, SystemRandom

from toolz import update_in, valmap, compose

from pyploid.types.algorithms.meiosis import Meiosis
from pyploid.types.cytogenetic_index import ComplexPolyploidCytogeneticIndex
from pyploid.types.gene import Gene
from pyploid.types.individual import Individual


def _add_choice(
    possible_choices: dict[int, set[int]],
        gene: Gene[ComplexPolyploidCytogeneticIndex]
) -> dict[int, set[int]]:
    return update_in(
        possible_choices,
        [gene.position.chromosome_number],
        lambda c: c.union((gene.position.set_index, )),
        set()
    )


def create_random_pick_from_set_meiosis(
    random: Random = SystemRandom()
) -> Meiosis[Gene[ComplexPolyploidCytogeneticIndex]]:
    def pick_from_set(
        individual: Individual[Gene[ComplexPolyploidCytogeneticIndex]]
    ) -> Sequence[Gene[ComplexPolyploidCytogeneticIndex]]:
        choices: dict[int, set[int]] = reduce(_add_choice, individual.genes, dict())
        picks: dict[int, set[int]] = valmap(compose(random.choice, tuple), choices)
        return tuple(
            gene
            for gene in individual.genes
            if gene.position.set_index == picks.get(gene.position.chromosome_number)
        )
    return pick_from_set