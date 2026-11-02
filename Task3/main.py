from typing import Dict, List, Optional


def add_film(films: Dict[str, dict], title: str, year: int, genre: str, rating: float) -> None:
    if rating < 0 or rating > 10:
        raise ValueError("rating must be in [0, 10]")
    films[title] = {"year": year, "genre": genre, "rating": rating}


def by_genre(films: Dict[str, dict], genre: str) -> List[str]:
    return sorted(t for t, f in films.items() if f["genre"].lower() == genre.lower())


def rating_at_least(films: Dict[str, dict], threshold: float) -> List[str]:
    return sorted(t for t, f in films.items() if f["rating"] >= threshold)


def average_rating_by_genre(films: Dict[str, dict], genre: str) -> float:
    selected = [f["rating"] for f in films.values() if f["genre"].lower() == genre.lower()]
    if not selected:
        raise ValueError("no films in genre")
    return sum(selected) / len(selected)


def oldest_film(films: Dict[str, dict]) -> Optional[str]:
    if not films:
        return None
    return min(films.items(), key=lambda x: (x[1]["year"], x[0]))[0]