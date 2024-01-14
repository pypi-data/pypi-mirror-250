from collections.abc import Sequence, Iterable
from dataclasses import dataclass
from typing import Generic, Self

from pyploid.types.gene import GeneType
from pyploid.types.individual import IndividualType, Population


@dataclass(frozen=True)
class TrivialIndividual(Generic[GeneType]):
    genes: Sequence[GeneType]

@dataclass(frozen=True)
class TrivialPopulation(Generic[IndividualType], Population[IndividualType]):
    members: Sequence[IndividualType]


def create_trivial_individual(
        genes: Iterable[GeneType],
        _: Iterable[TrivialIndividual[GeneType]]
) -> TrivialIndividual[GeneType]:
    return TrivialIndividual(tuple(genes))


def create_trivial_population(members: Iterable[IndividualType]) -> TrivialPopulation[IndividualType]:
    return TrivialPopulation(tuple(members))
