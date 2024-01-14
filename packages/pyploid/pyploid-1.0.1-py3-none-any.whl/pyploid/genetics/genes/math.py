from collections.abc import Iterable
from dataclasses import dataclass, replace
from inspect import signature
from operator import attrgetter
from typing import Generic, Protocol, Sequence, Callable

from toolz import groupby, valmap

from pyploid.types.algorithms.fitness import Fitness
from pyploid.types.algorithms.mutation import Mutation
from pyploid.types.cytogenetic_index import IndexType
from pyploid.types.individual import Individual


class MathFunction(Protocol):
    parameter_count: int
    name: str

    def __call__(self, parameter: Sequence[float]) -> float: ...


class _WrappedMathFunction:
    def __init__(self, func: Callable[..., float]):
        self.name = func.__name__
        self.parameter_count: int = len(signature(func).parameters)
        self._func: Callable[..., float] = func

    def __call__(self, parameter: Sequence[float]) -> float: return self._func(*parameter)


def as_math_function(
        func: Callable[..., float]
) -> MathFunction:
    return _WrappedMathFunction(func)


@dataclass(frozen=True)
class FunctionParameterGene(Generic[IndexType]):
    function: MathFunction
    value: float
    parameter_index: int
    position: IndexType

    def get_function(self) -> MathFunction: return self.function

    def get_parameter_index(self) -> int: return self.parameter_index


def average(values: Sequence[float]) -> float: return sum(values) / len(values)


def _calculate_value(
        function: MathFunction,
        parameter: Sequence[FunctionParameterGene[IndexType]],
        default_for_missing: float,
        aggregate: Callable[[Sequence[float]], float]
) -> float:
    values: dict[int, float] = valmap(
        lambda p: aggregate(tuple(map(attrgetter('value'), p))),
        groupby(attrgetter('parameter_index'), parameter)
    )
    return function(
        [values.get(i, default_for_missing) for i in range(function.parameter_count)]
    )


def create_function_parameter_fitness(
        aggregate: Callable[[Sequence[float]], float] = average,
        default_for_missing: float = float('inf')
) -> Fitness[Individual[FunctionParameterGene[IndexType]]]:
    def fitness(individual: Individual[FunctionParameterGene[IndexType]]) -> float:
        evaluations: dict[MathFunction, Sequence[FunctionParameterGene[IndexType]]] = groupby(
            attrgetter('function'),
            individual.genes
        )
        return sum(
            _calculate_value(func, genes, default_for_missing, aggregate)
            for func, genes in evaluations.items()
        )

    return fitness


def create_value_mutation(
        mutate_value: Callable[[float], float],
) -> Mutation[FunctionParameterGene[IndexType]]:
    def mutate_values(genes: Sequence[FunctionParameterGene[IndexType]]) -> Iterable[FunctionParameterGene[IndexType]]:
        for gene in genes:
            yield replace(gene, value=mutate_value(gene.value))

    return mutate_values
