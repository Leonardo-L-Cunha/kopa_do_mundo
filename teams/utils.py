from datetime import datetime
from .exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError


def data_processing(args: dict):
    fisrt_cup: str = args["first_cup"]
    get_year = fisrt_cup.split("-")
    year = datetime(int(get_year[0]), 1, 1)
    date = int(year.strftime("%Y"))

    current_year = int(datetime.now().today().year)
    max_titles = (current_year - date) // 4

    if args["titles"] <= 0:
        raise NegativeTitlesError("titles cannot be negative")

    if date < 1930 or (date - 1930) % 4 != 0:
        raise InvalidYearCupError("there was no world cup this year")

    if args["titles"] > max_titles:
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
