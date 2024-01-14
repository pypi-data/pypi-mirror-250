from collections.abc import Iterable
from typing import Sequence, Protocol, TypeVar

from pyploid.types.gene import GeneType


class Individual(Protocol[GeneType]):
    genes: Sequence[GeneType]


class NamedIndividual(Individual[GeneType], Protocol):
    uuid: str

    def __hash__(self) -> int: ...


class EvaluatedIndividual(Individual[GeneType], Protocol):
    fitness: float | None



IndividualType = TypeVar('IndividualType', bound=Individual)
ResultIndividualType = TypeVar('ResultIndividualType', bound=Individual)
ContravariantIndividualType = TypeVar('ContravariantIndividualType', bound=Individual, contravariant=True)


class Population(Protocol[IndividualType]):
    members: Sequence[IndividualType]


class PopulationFactory(Protocol[IndividualType]):
    def __call__(self, members: Iterable[IndividualType]) -> Population[IndividualType]: ...


