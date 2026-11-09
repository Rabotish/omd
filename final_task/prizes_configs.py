from typing import Any, Callable

from json_dict_processing import create_processor


CONFIG_PRIZE: dict[
    str,
    list[str] | tuple[list[str], Callable[[Any], Any]]
] = {
    "prize_amount": ["prizeAmount"],
    "prize_amount_adjusted": ["prizeAmountAdjusted"],
    "award_year": (["awardYear"], int),
    "category_en": ["category", "en"],
    "prize_status": ["prizeStatus"]
}


def prize_processor() -> Callable[
    [list[dict[str, Any]]],
    list[dict[str, Any]]
]:
    """
    Процессор для данных о призах
    """
    return create_processor(CONFIG_PRIZE, list_processor=True)
