from statistics import mean, median
from typing import Any


def count_records(records: list[dict[str, Any]]) -> int:
    """
    Возвращает количество записей.
    """
    return len(records)


def count_unique(
    records: list[dict[str, Any]],
    attribute: str,
) -> int:
    """
    Подсчитывает уникальные непустые значения атрибута.
    """
    return len({
        record[attribute]
        for record in records
        if record.get(attribute) is not None
    })


def mean_value(
    records: list[dict[str, Any]],
    attribute: str,
) -> int | float | None:
    """
    Рассчитывает среднее значение атрибута.
    """
    values = [
        record[attribute]
        for record in records
        if record.get(attribute) is not None
    ]

    return mean(values) if values else None


def median_value(
    records: list[dict[str, Any]],
    attribute: str,
) -> int | float | None:
    """
    Рассчитывает медиану атрибута.
    """
    values = [
        record[attribute]
        for record in records
        if record.get(attribute) is not None
    ]

    return median(values) if values else None


def max_value(
    records: list[dict[str, Any]],
    attribute: str,
) -> int | float | None:
    """
    Возвращает максимальное значение атрибута.
    """
    values = [
        record[attribute]
        for record in records
        if record.get(attribute) is not None
    ]

    return max(values) if values else None


def min_value(
    records: list[dict[str, Any]],
    attribute: str,
) -> int | float | None:
    """
    Возвращает минимальное значение атрибута.
    """
    values = [
        record[attribute]
        for record in records
        if record.get(attribute) is not None
    ]

    return min(values) if values else None


def top_n(counts: dict, n: int = 5) -> str:
    """
    Возвращает топ-N объектов по убыванию значения метрики.
    """
    lines = []
    sorted_counts = sorted(
        counts.items(),
        key=lambda item: (-item[1], str(item[0]))
    )[:n]
    for key, count in sorted_counts:
        label = (
            ", ".join(map(str, key))
            if isinstance(key, tuple)
            else str(key)
        )

        lines.append(f"{label}: {count}")

    return "\n".join(lines)
