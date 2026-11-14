from typing import Any, Callable


def extract_nested_value(obj: dict[str, Any], keys: list[str]) -> Any:
    """
    Извлекает значение из вложенных структур данных по цепочке ключей.
    """
    value: Any = obj

    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)

    return value


def process_dictionary_with_config(
    dictionary: dict[str, Any],
    config: dict[str, list[str] | tuple[list[str], Callable[[Any], Any]]]
) -> dict[str, Any]:
    """
    Обрабатывает один словарь согласно словарю-конфигу.
    """
    processed_dict = {}
    for attribute, processing_rule in config.items():
        if isinstance(processing_rule, tuple):
            keys, processing_function = processing_rule
            value = extract_nested_value(dictionary, keys)
            processed_dict[attribute] = (
                processing_function(value)
                if value is not None
                else None
            )
        else:
            value = extract_nested_value(dictionary, processing_rule)
            processed_dict[attribute] = value
    return processed_dict


def process_list_of_dicts_with_config(
    list_of_dicts: list[dict[str, Any]],
    config: dict[str, list[str] | tuple[list[str], Callable[[Any], Any]]]
) -> list[dict[str, Any]]:
    """
    Обрабатывает список словарей согласно словарю-конфигу.
    """
    return [
        process_dictionary_with_config(item, config)
        for item in list_of_dicts
    ]


def create_processor(
    config: dict[str, list[str] | tuple[list[str], Callable[[Any], Any]]],
    list_processor: bool = False
) -> Callable[[Any], Any]:
    """
    Создает готовый процессор с предзагруженной конфигурацией.
    В случае, если list_processor == True,
    внутрь процессора подается process_list_of_dicts_with_config,
    иначе process_dictionary_with_config.
    """
    if list_processor:
        return lambda data: process_list_of_dicts_with_config(data, config)
    else:
        return lambda data: process_dictionary_with_config(data, config)
