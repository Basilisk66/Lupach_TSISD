def create_movie(title, year, genre, rating):
    return {
        "title": title,
        "year": year,
        "genre": genre,
        "rating": rating,
    }


def add_movie(library, movie):
    library.append(movie)


def find_by_genre(library, genre):
    return [m for m in library if m["genre"].lower() == genre.lower()]


def filter_by_rating(library, threshold):
    return [m for m in library if m["rating"] >= threshold]


def average_rating_by_genre(library, genre):
    """Считает средний рейтинг по жанру. None, если фильмов нет."""
    movies = find_by_genre(library, genre)
    if not movies:
        return None
    return sum(m["rating"] for m in movies) / len(movies)


def oldest_movie(library):
    """Возвращает самый старый фильм. None, если в библиотеке фильмов пусто."""
    if not library:
        return None
    oldest = library[0]
    for movie in library:
        if movie["year"] < oldest["year"]:
            oldest = movie
    return oldest


def format_movie(m):
    return f"{m['title']} ({m['year']}) — {m['genre']}, рейтинг {m['rating']}"


def print_list(title, items, formatter=format_movie):
    print(f"\n{title}:")
    if not items:
        print("  (пусто)")
        return
    for item in items:
        print(" -", formatter(item))


def main():
    library = []

    for data in [
        ("Области тьмы", 2011, "триллер", 7.4),
        ("Властелин колец: Две башни", 2002, "фэнтези", 8.8),
        ("Джентльмены", 2019, "криминал", 8.2),
        ("Назад в будущее", 1985, "фантастика", 7.8),
        ("Третий лишний", 2012, "комедия", 6.9),
        ("Зеленый слоник", 1999, "драма", 5.3),
        ("Семь", 1995, "триллер", 7.6),
        ("Хатико", 2008, "драма", 7.5),
    ]:
        add_movie(library, create_movie(*data))

    # Демонстрация обычных операций
    print_list("Все фильмы в фильмотеке", library)
    print_list("Жанр триллер", find_by_genre(library, "триллер"))
    print_list("Рейтинг >= 6.9", filter_by_rating(library, 6.9))

    avg = average_rating_by_genre(library, "триллер")
    print(f"\nСредний рейтинг триллер: {avg:.2f}" if avg else "\nтриллер: нет фильмов")

    old = oldest_movie(library)
    print("Самый старый фильм:", format_movie(old) if old else "—")


if __name__ == "__main__":
    main()
