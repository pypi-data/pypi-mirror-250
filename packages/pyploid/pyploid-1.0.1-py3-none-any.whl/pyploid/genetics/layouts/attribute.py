from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import replace
from typing import Callable, TypeVar, cast

from pyploid.types.cytogenetic_index import ComplexPolyploidIndexType, IndexType
from pyploid.types.gene import Gene, DataclassGene
from pyploid.types.layout import GeneLayout

_AttributeType1 = TypeVar('_AttributeType1')
_AttributeType2 = TypeVar('_AttributeType2')


def _get_attribute_map(
        get_attr: Callable[[Gene[IndexType]], _AttributeType1],
        genes: Sequence[Gene[IndexType]]
) -> dict[_AttributeType1, int]:
    return dict(
        (attribute, i)
        for i, attribute in enumerate(set(map(get_attr, genes)))
    )


def dataclass_reindex(
        gene: DataclassGene[IndexType | ComplexPolyploidIndexType],
        new_index: ComplexPolyploidIndexType
) -> DataclassGene[ComplexPolyploidIndexType]:
    return cast(DataclassGene[ComplexPolyploidIndexType], replace(gene, position=new_index))


def create_attribute_based_layout(
        get_chromosome_attribute: Callable[[Gene[IndexType]], _AttributeType1],
        get_index_attribute: Callable[[Gene[IndexType]], _AttributeType2],
        index_factory: Callable[[int, int, int], ComplexPolyploidIndexType],
        reindex: Callable[[Gene[IndexType], ComplexPolyploidIndexType], Gene[ComplexPolyploidIndexType]]
) -> GeneLayout[ComplexPolyploidIndexType, IndexType]:
    def layout_by_attributes(genes: Sequence[Gene[IndexType]]) -> Iterable[Gene[ComplexPolyploidIndexType]]:
        chromosome_map: dict[_AttributeType1, int] = _get_attribute_map(get_chromosome_attribute, genes)
        index_map: dict[_AttributeType2, int] = _get_attribute_map(get_index_attribute, genes)
        set_indices: dict[tuple[int, int], int] = defaultdict(int)
        for gene in genes:
            index: int = index_map[get_index_attribute(gene)]
            new_index: ComplexPolyploidIndexType = index_factory(
                (chromosome := chromosome_map[get_chromosome_attribute(gene)]),
                set_indices[(chromosome, index)],
                index
            )
            set_indices[(new_index.chromosome_number, new_index.index)] += 1
            yield reindex(gene, new_index)

    return layout_by_attributes
