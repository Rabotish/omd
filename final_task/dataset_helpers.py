from collections import defaultdict
from typing import Any, Callable


def filter_records(
    data: list[dict[str, Any]],
    condition: Callable[[dict[str, Any]], bool]
) -> list[dict[str, Any]]:
    """
    Фильтрует записи по заданному условию.
    """
    return [record for record in data if condition(record)]


def group_by_attributes(
    data: list[dict[str, Any]],
    attributes: list[str],
) -> dict[tuple[Any, ...], list[dict[str, Any]]]:
    """
    Группирует записи по одному или нескольким атрибутам.
    """
    groups = defaultdict(list)

    for record in data:
        key = tuple(
            record.get(attribute)
            for attribute in attributes
        )
        groups[key].append(record)

    return dict(groups)


def aggregate_groups(
    groups: dict[tuple[Any, ...], list[dict[str, Any]]],
    aggregation: Callable[[list[dict[str, Any]]], Any],
) -> dict[tuple[Any, ...], Any]:
    """
    Применяет функцию агрегации к каждой группе.
    """
    return {key: aggregation(records) for key, records in groups.items()}


def missing_value_counts(
    data: list[dict[str, Any]],
    attributes: list[str] | None = None,
) -> dict[str, int]:
    """
    Подсчитывает количество пропусков по каждому атрибуту.
    Если attributes не указан, подсчитывает для всех атрибутов.
    """
    if not data:
        return {}

    if attributes is None:
        attributes = sorted({key for record in data for key in record})

    return {
        attribute: sum(
            record.get(attribute) is None or record.get(attribute) == ""
            for record in data
        )
        for attribute in attributes
    }


def find_id_gaps(
    data: list[dict[str, Any]],
    attribute: str = "id",
) -> list[tuple[int, int]]:
    """Находит промежутки с пропущенными ID."""
    ids = sorted({
        int(record[attribute])
        for record in data
        if record.get(attribute) is not None
    })

    return [
        (left, right)
        for left, right in zip(ids, ids[1:])
        if right - left > 1
    ]


def calculate_group_shares(
    data: list[dict[str, Any]],
    subset: list[dict[str, Any]],
    attributes: list[str],
    aggregation: Callable[[list[dict[str, Any]]], int | float],
) -> dict[tuple[Any, ...], float]:
    """
    Рассчитывает процентную долю подвыборки в каждой группе.
    Агрегация должна подсчитывать количество объектов.
    """
    total_counts = aggregate_groups(
        group_by_attributes(data, attributes),
        aggregation
    )

    subset_counts = aggregate_groups(
        group_by_attributes(subset, attributes),
        aggregation
    )

    return {
        key: round(subset_counts.get(key, 0) / total * 100, 2)
        for key, total in total_counts.items()
        if total > 0 and None not in key
    }
