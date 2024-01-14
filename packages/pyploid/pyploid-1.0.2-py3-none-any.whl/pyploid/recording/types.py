from collections.abc import Callable
from functools import wraps
from typing import Protocol, Iterable, TypedDict

from pyploid.types.algorithms.evolution import Evolution
from pyploid.types.individual import IndividualType, Population
from pyploid.types.primitive import JSONType


class DataExtractor(Protocol):
    def __call__(self, individual: IndividualType) -> dict[str, JSONType]: ...


class PopulationSampleSelector(Protocol[IndividualType]):
    def __call__(self, population: Population[IndividualType]) -> Iterable[IndividualType]: ...


def complete_population(population: Population[IndividualType]) -> Iterable[IndividualType]:
    return (member for member in population.members)


class RecordRow(TypedDict):
    step: int
    selected_individuals: list[dict[str, JSONType]]


def create_evolution_recorder(
        evolution: Evolution[IndividualType],
        handle_record: Callable[[RecordRow], None],
        extract_data: DataExtractor,
        select_sample: PopulationSampleSelector[IndividualType] = complete_population
) -> Evolution[IndividualType]:
    step: int = 0

    def _handle_population(population: Population[IndividualType]) -> None:
        handle_record(dict(step=step, selected_individuals=list(map(extract_data, select_sample(population)))))

    @wraps(evolution)
    def recorded_evolution(population: Population[IndividualType]) -> Population[IndividualType]:
        nonlocal step
        if step == 0:
            _handle_population(population)
        step += 1
        next_population: Population[IndividualType] = evolution(population)
        _handle_population(next_population)
        return next_population

    return recorded_evolution
