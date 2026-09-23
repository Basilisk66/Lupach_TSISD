class Movie:
    def __init__(self, title, year, genre, rating):
        self.title = title
        self.year = year
        self.genre = genre
        self.rating = rating

    def __str__(self):
        return f"{self.title} ({self.year}) — {self.genre}, рейтинг {self.rating}"

    def matches_genre(self, genre):
        return self.genre.lower() == genre.lower()

    def is_rated_at_least(self, threshold):
        return self.rating >= threshold


class FilmLibrary:
    # Инкапсулирует список _movies
    def __init__(self):
        self._movies = []

    def add(self, movie):
        self._movies.append(movie)

    def find_by_genre(self, genre):
        return [m for m in self._movies if m.matches_genre(genre)]

    def filter_by_rating(self, threshold):
        return [m for m in self._movies if m.is_rated_at_least(threshold)]

    def average_rating_by_genre(self, genre):
        movies = self.find_by_genre(genre)
        if not movies:
            return None
        return sum(m.rating for m in movies) / len(movies)

    def oldest_movie(self):
        if not self._movies:
            return None
        return min(self._movies, key=lambda m: m.year)

    def all(self):
        return list(self._movies)


def print_list(title, items):
    print(f"\n{title}:")
    if not items:
        print("  (пусто)")
        return
    for item in items:
        print(" -", item)


def main():
    library = FilmLibrary()

    for data in [
        ("Хоббит: неожиданное путешествие", 2012, "фэнтези", 7.3),
        ("Великий Гэтсби", 2013, "драма", 7.2),
        ("Три мушкетера", 1979, "приключения", 8.2),
        ("Граф Монте-Кристо", 2002, "триллер", 7.6),
        ("Дети капитана Гранта", 1985, "приключения", 8.3),
        ("Дон Кихот", 1957, "драма", 7.5),
        ("1984", 2023, "фантастика", 4.0),
    ]:
        library.add(Movie(*data))

    print_list("Все фильмы", library.all())
    print_list("Жанр приключения", library.find_by_genre("драма"))
    print_list("Рейтинг >= 8.8", library.filter_by_rating(8.8))

    avg = library.average_rating_by_genre("приключения")
    print(
        f"\nСредний рейтинг приключения: {avg:.2f}"
        if avg
        else "\nприключения: нет фильмов"
    )

    old = library.oldest_movie()
    print("Самый старый фильм:", old if old else "—")


if __name__ == "__main__":
    main()
