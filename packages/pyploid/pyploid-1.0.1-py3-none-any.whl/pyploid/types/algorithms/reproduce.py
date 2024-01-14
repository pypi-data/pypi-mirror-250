from collections.abc import Iterable, Sequence
from collections.abc import Iterable, Sequence
from itertools import chain
from typing import Protocol

from toolz import identity

from pyploid.types.algorithms.meiosis import Meiosis
from pyploid.types.algorithms.mutation import Mutation
from pyploid.types.cytogenetic_index import IndexType, ComplexPolyploidIndexType
from pyploid.types.gene import Gene, reindex_chromosome_sets
from pyploid.types.individual import IndividualType, Individual


class Reproduce(Protocol[IndividualType]):
    def __call__(self, parents: Sequence[IndividualType]) -> IndividualType:
        ...


class IndividualFactory(Protocol[IndexType]):
    def __call__(
            self,
            genes: Iterable[Gene[IndexType]],
            parents: Iterable[Individual[Gene[IndexType]]]
    ) -> Individual[Gene[IndexType]]:
        ...


def create_reproduction(
        meiosis: Meiosis[Gene[ComplexPolyploidIndexType]],
        create_individual: IndividualFactory[ComplexPolyploidIndexType],
        mutation: Mutation[Gene[ComplexPolyploidIndexType]] = identity
) -> Reproduce[Individual[Gene[ComplexPolyploidIndexType]]]:
    def reproduce(parents: Sequence[IndividualType]) -> Individual[Gene[ComplexPolyploidIndexType]]:
        if not parents:
            raise AttributeError('Reproduction without parents is not supported')

        child_genes: Sequence[Gene[ComplexPolyploidIndexType]] = tuple(
            reindex_chromosome_sets(chain(*map(meiosis, parents)))
        )
        if not child_genes:
            raise AttributeError(f'Meiosis did not yield genes for child')
        return create_individual(mutation(child_genes), parents)

    return reproduce
