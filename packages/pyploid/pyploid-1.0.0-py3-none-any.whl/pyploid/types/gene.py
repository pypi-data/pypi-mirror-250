from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field, is_dataclass, replace
from typing import TypeVar, NewType, Protocol, runtime_checkable

from pyploid.types.cytogenetic_index import IndexType, ComplexPolyploidIndexType

T = TypeVar('T')

GeneID = NewType('GeneID', str)


@dataclass(frozen=True)
class GeneDescription:
    uuid: GeneID
    allele_type: type
    description: str | None = field(default=None)


class Gene(Protocol[IndexType]):
    position: IndexType


@runtime_checkable
@dataclass
class DataclassGene(Protocol[IndexType]):
    position: IndexType


GeneType = TypeVar('GeneType')


def update_position(gene: Gene[IndexType] | DataclassGene[IndexType], position: IndexType) -> Gene[IndexType]:
    if isinstance(gene, DataclassGene):
        return replace(gene, position=position)
    else:
        gene.position = position
        return gene


def reindex_chromosome_sets(
    genes: Iterable[Gene[ComplexPolyploidIndexType]]
) -> Iterable[Gene[ComplexPolyploidIndexType]]:
    indices: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for gene in genes:
        position: ComplexPolyploidIndexType = gene.position
        new_set_index: int = indices[position.chromosome_number][position.index]
        yield update_position(gene, position.reindex(position.chromosome_number, new_set_index, position.index))
        indices[position.chromosome_number][position.index] += 1
