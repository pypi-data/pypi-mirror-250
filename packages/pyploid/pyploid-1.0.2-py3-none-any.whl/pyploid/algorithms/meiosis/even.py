from collections.abc import Sequence
from itertools import groupby
from operator import itemgetter
from random import Random, SystemRandom
from typing import Callable, TypeAlias, TypeVar

from pyploid.types.algorithms.meiosis import Meiosis, predicate_meiosis
from pyploid.types.cytogenetic_index import Qualifier, PolyploidIndexType
from pyploid.types.gene import Gene
from pyploid.types.individual import Individual

Size: TypeAlias = int
T = TypeVar('T')


def _choose_half(choose: Callable[[Sequence[int]], int], items: Sequence[T]) -> Sequence[T]:
    chosen_items: list[T] = list()
    available_indices: list[int] = list(range(len(items)))
    items_to_pick: int = len(items) // 2
    for _ in range(items_to_pick):
        index: int = choose(available_indices)
        chosen_items.append(items[index])
        available_indices.remove(index)
    return chosen_items


def create_even_meiosis(
        random: Random = SystemRandom()
) -> Meiosis[Gene[PolyploidIndexType]]:
    choose: Callable[[Sequence[T]], T] = random.choice

    def homogenous_meiosis(
            individual: Individual[Gene[PolyploidIndexType]]
    ) -> Sequence[Gene[PolyploidIndexType]]:
        available_sets: set[tuple[Qualifier, int]] = {
            (gene.position.qualifier(), gene.position.set_index) for gene in individual.genes
        }
        choices: dict[Qualifier, set[int]] = dict(
            (qualifier, set(_choose_half(choose, tuple(set(map(itemgetter(1), indices))))))
            for qualifier, indices in
            groupby(sorted(available_sets), key=itemgetter(0))
        )

        def _predicate(index: PolyploidIndexType) -> bool:
            return index.set_index in choices[index.qualifier()]

        return predicate_meiosis(_predicate, individual)

    return homogenous_meiosis
