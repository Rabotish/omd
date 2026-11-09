from typing import Any, Callable


def add_attribute(
    data: list[dict[str, Any]],
    attribute: str,
    calculation: Callable[[dict[str, Any]], Any],
) -> list[dict[str, Any]]:
    """
    Добавляет новый, вычисляемый через calculation атрибут в каждую запись.
    data: Список словарей (записей).
    attribute: Имя нового атрибута.
    calculation: Функция, которая принимает запись и возвращает значение
    нового атрибута.
    """
    return [
        {
            **record,
            attribute: calculation(record)
        }
        for record in data
    ]


def expand_list_attribute(
    data: list[dict[str, Any]],
    attribute: str,
    list_attributes: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Разворачивает вложенный список словарей в плоские записи."""
    expanded = []

    for record in data:
        parent = {
            key: value
            for key, value in record.items()
            if key != attribute
        }

        for item in record.get(attribute) or []:
            values = (
                item
                if list_attributes is None
                else {
                    key: item.get(key)
                    for key in list_attributes
                }
            )

            overlap = parent.keys() & values.keys()

            if overlap:
                raise ValueError(
                    f"Атрибут уже существует: {sorted(overlap)}"
                )

            expanded.append({**parent, **values})

    return expanded
