from typing import Any, Callable

from json_dict_processing import create_processor
from prizes_configs import prize_processor


def process_year(year_string: str | None) -> int | None:
    """
    Извлекает год из строки даты в формате "YYYY-MM-DD".
    """
    if not year_string:
        return None
    try:
        return int(year_string.split("-")[0])
    except (ValueError, AttributeError):
        return None


CONFIG_PERSON: dict[
    str,
    list[str] | tuple[list[str], Callable[[Any], Any]]
] = {
    "id": ["id"],
    "name": ["knownName", "en"],
    "gender": ["gender"],
    "birth_year": (["birth", "date"], process_year),
    "country_birth": ["birth", "place", "country", "en"],
    "country_now": ["birth", "place", "countryNow", "en"],
    "prizes_relevant": (["nobelPrizes"], prize_processor())
}


CONFIG_ORG: dict[
    str,
    list[str] | tuple[list[str], Callable[[Any], Any]]
] = {
    "id": ["id"],
    "name": ["orgName", "en"],
    "founded_year": (["founded", "date"], process_year),
    "country_founded": ["founded", "place", "country", "en"],
    "country_now": ["founded", "place", "countryNow", "en"],
    "prizes_relevant": (["nobelPrizes"], prize_processor())
}


def person_processor() -> Callable[[dict[str, Any]], dict[str, Any]]:
    """
    Процессор для данных о людях-лауреатах
    """
    return create_processor(CONFIG_PERSON)


def org_processor() -> Callable[[dict[str, Any]], dict[str, Any]]:
    """
    Процессор для данных об организациях-лауреатах
    """
    return create_processor(CONFIG_ORG)


process_orgs = org_processor()
process_persons = person_processor()
