import unittest

from main import (
    add_film,
    average_rating_by_genre,
    by_genre,
    oldest_film,
    rating_at_least,
)


class TestAddFilm(unittest.TestCase):
    def setUp(self):
        self.films = {}

    def test_add_record(self):
        add_film(self.films, "The Hobbit", 2012, "fantasy", 8.1)
        self.assertEqual(
            self.films,
            {"The Hobbit": {"year": 2012, "genre": "fantasy", "rating": 8.1}},
        )

    def test_rejects_rating_below_zero(self):
        for bad in (-0.3, -6, -100):
            with self.subTest(rating=bad):
                with self.assertRaisesRegex(ValueError, r"rating must be in \[0, 10\]"):
                    add_film(self.films, "Green mile", 2000, "Drama", bad)
                self.assertEqual(self.films, {})

    def test_rejects_rating_above_ten(self):
        for bad in (10.1, 11, 100):
            with self.subTest(rating=bad):
                with self.assertRaisesRegex(ValueError, r"rating must be in \[0, 10\]"):
                    add_film(self.films, "Green mile", 2000, "Drama", bad)
                self.assertEqual(self.films, {})

    def test_boundary_ratings(self):
        for ok in (0, 0.0, 10, 10.0, 5.5):
            with self.subTest(rating=ok):
                films = {}
                add_film(films, "Murder", 2001, "Drama", ok)
                self.assertEqual(films["Murder"]["rating"], ok)


class TestByGenre(unittest.TestCase):
    def setUp(self):
        self.films = make_sample_films()

    def test_basic(self):
        self.assertEqual(by_genre(self.films, "Drama"), ["C", "D"])

    def test_case_insensitive(self):
        expected = ["A", "B", "E"]
        self.assertEqual(by_genre(self.films, "sci-fi"), expected)
        self.assertEqual(by_genre(self.films, "SCI-FI"), expected)

    def test_empty_result(self):
        self.assertEqual(by_genre(self.films, "Horror"), [])


class TestRatingAtLeast(unittest.TestCase):
    def setUp(self):
        self.films = make_sample_films()

    def test_basic(self):
        self.assertEqual(rating_at_least(self.films, 8.8), ["A", "D"])

    def test_threshold_is_inclusive(self):
        result = rating_at_least(self.films, 8.8)
        self.assertIn("A", result)
        self.assertNotIn("B", result)
        self.assertIn("D", result)

    def test_no_matches(self):
        self.assertEqual(rating_at_least(self.films, 10), [])


class TestAverageRatingByGenre(unittest.TestCase):
    def setUp(self):
        self.films = make_sample_films()

    def test_basic(self):
        self.assertAlmostEqual(average_rating_by_genre(self.films, "Drama"), 8.35)

    def test_case_insensitive(self):
        self.assertAlmostEqual(average_rating_by_genre(self.films, "Fantasy"), 2.05)

    def test_empty_dict_raises(self):
        with self.assertRaisesRegex(ValueError, "no films in genre"):
            average_rating_by_genre({}, "Drama")


class TestOldestFilm(unittest.TestCase):
    def test_basic(self):
        films = make_sample_films()
        self.assertEqual(oldest_film(films), "H")

    def test_empty_returns_none(self):
        self.assertIsNone(oldest_film({}))

    def test_tie_break_by_title(self):
        films = {
            "Havoc": {"year": 2000, "genre": "Drama", "rating": 7.0},
            "Solace": {"year": 2000, "genre": "Drama", "rating": 7.0},
            "Harvey": {"year": 2001, "genre": "Drama", "rating": 7.0},
        }
        self.assertEqual(oldest_film(films), "Havoc")

    def test_single(self):
        films = {"Solo": {"year": 1990, "genre": "Drama", "rating": 6.0}}
        self.assertEqual(oldest_film(films), "Solo")


def make_sample_films():
    return {
        "A": {"year": 2010, "genre": "Sci-Fi", "rating": 8.8},
        "B": {"year": 1999, "genre": "Sci-Fi", "rating": 8.7},
        "C": {"year": 1997, "genre": "Drama", "rating": 7.9},
        "D": {"year": 1994, "genre": "Drama", "rating": 8.8},
        "E": {"year": 2014, "genre": "sci-fi", "rating": 8.6},
        "F": {"year": 2013, "genre": "fantasy", "rating": 2.5},
        "G": {"year": 2027, "genre": "FaNTaSY", "rating": 1.6},
        "H": {"year": 1984, "genre": "thriller", "rating": 4.0},
    }
