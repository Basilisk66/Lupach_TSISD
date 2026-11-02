import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Film {
    public String title;
    public int year;
    public String genre;
    public double rating;

    public Film(String title, int year, String genre, double rating) {
        this.title = title;
        this.year = year;
        this.genre = genre;
        this.rating = rating;
    }

    @Override
    public String toString() {
        return title + " (" + year + ", " + genre + ", рейтинг " + rating + ")";
    }
}

class FilmLibraryStruct {

    public static void add(List<Film> lib, Film f) {
        lib.add(f);
    }

    public static List<Film> findByGenre(List<Film> lib, String genre) {
        List<Film> result = new ArrayList<>();
        for (Film f : lib) {
            if (f.genre.equalsIgnoreCase(genre)) {
                result.add(f);
            }
        }
        return result;
    }

    public static List<Film> findByMinRating(List<Film> lib, double threshold) {
        List<Film> result = new ArrayList<>();
        for (Film f : lib) {
            if (f.rating >= threshold) {
                result.add(f);
            }
        }
        return result;
    }

    public static double averageRatingByGenre(List<Film> lib, String genre) {
        int count = 0;
        double sum = 0;
        for (Film f : lib) {
            if (f.genre.equalsIgnoreCase(genre)) {
                sum += f.rating;
                count++;
            }
        }
        if (count == 0) return 0;
        return sum / count;
    }

    public static Film findOldest(List<Film> lib) {
        if (lib.isEmpty()) return null;
        Film oldest = lib.get(0);
        for (Film f : lib) {
            if (f.year < oldest.year) {
                oldest = f;
            }
        }
        return oldest;
    }
}

public class structural {

    // Один Scanner на всю программу, чтобы не терять ввод
    private static final Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        List<Film> library = new ArrayList<>();

        // Немного фильмов "из коробки"
        FilmLibraryStruct.add(library, new Film("Области тьмы", 2011, "триллер", 7.4));
        FilmLibraryStruct.add(library, new Film("Властелин колец: Две башни", 2002, "фэнтези", 8.8));
        FilmLibraryStruct.add(library, new Film("Джентльмены", 2019, "криминал", 8.2));
        FilmLibraryStruct.add(library, new Film("Назад в будущее", 1985, "фантастика", 7.8));
        FilmLibraryStruct.add(library, new Film("Третий лишний", 2012, "комедия", 6.9));
        FilmLibraryStruct.add(library, new Film("Зелёный слоник", 1999, "драма", 5.3));
        FilmLibraryStruct.add(library, new Film("Семь", 1995, "триллер", 7.6));
        FilmLibraryStruct.add(library, new Film("Хатико", 2008, "драма", 7.5));

        boolean running = true;
        while (running) {
            printMenu();
            int choice = readInt("Ваш выбор: ");

            switch (choice) {
                case 1:
                    showAll(library);
                    break;
                case 2:
                    addMovieDialog(library);
                    break;
                case 3:
                    searchByGenreDialog(library);
                    break;
                case 4:
                    searchByRatingDialog(library);
                    break;
                case 5:
                    averageRatingDialog(library);
                    break;
                case 6:
                    showOldest(library);
                    break;
                case 0:
                    running = false;
                    System.out.println("Конец");
                    break;
                default:
                    System.out.println("Нет такого пункта. Попробуйте снова.");
            }
        }
        sc.close();
    }

    // ---------- Меню и вспомогательные методы ввода ----------

    private static void printMenu() {
        System.out.println("\n       ФИЛЬМОТЕКА");
        System.out.println("1. Показать все фильмы");
        System.out.println("2. Добавить фильм");
        System.out.println("3. Найти фильмы по жанру");
        System.out.println("4. Фильмы с рейтингом >= порога");
        System.out.println("5. Средний рейтинг по жанру");
        System.out.println("6. Самый старый фильм");
        System.out.println("0. Выход");
    }

    private static int readInt(String prompt) {
        while (true) {
            System.out.print(prompt);
            String line = sc.nextLine().trim();
            try {
                return Integer.parseInt(line);
            } catch (NumberFormatException e) {
                System.out.println("Нужно ввести целое число");
            }
        }
    }

    private static double readDouble(String prompt) {
        while (true) {
            System.out.print(prompt);
            String line = sc.nextLine().trim().replace(',', '.');
            try {
                return Double.parseDouble(line);
            } catch (NumberFormatException e) {
                System.out.println("Нужно ввести число. Попробуй ещё раз.");
            }
        }
    }

    private static String readLine(String prompt) {
        System.out.print(prompt);
        return sc.nextLine().trim();
    }

    private static void showAll(List<Film> library) {
        System.out.println("\nВсе фильмы (" + library.size() + " шт.):");
        if (library.isEmpty()) {
            System.out.println("  (пусто)");
            return;
        }
        for (Film f : library) {
            System.out.println("  " + f);
        }
    }

    private static void addMovieDialog(List<Film> library) {
        System.out.println("\nДобавление фильма");
        String title = readLine("Название: ");
        if (title.isEmpty()) {
            System.out.println("Название не может быть пустым. Отмена.");
            return;
        }
        int year = readInt("Год выпуска: ");
        String genre = readLine("Жанр: ");
        double rating = readDouble("Рейтинг (от 0 до 10): ");

        FilmLibraryStruct.add(library, new Film(title, year, genre, rating));
        System.out.println("Фильм добавлен: " + title);
    }

    private static void searchByGenreDialog(List<Film> library) {
        System.out.println("\nПоиск по жанру");
        String genre = readLine("Введите жанр: ");
        if (genre.isEmpty()) {
            System.out.println("Жанр не введён. Отмена.");
            return;
        }

        List<Film> found = FilmLibraryStruct.findByGenre(library, genre);
        if (found.isEmpty()) {
            System.out.println("Фильмов жанра \"" + genre + "\" не найдено.");
        } else {
            System.out.println("Найдено (" + found.size() + "):");
            for (Film f : found) {
                System.out.println("  " + f);
            }
        }
    }

    private static void searchByRatingDialog(List<Film> library) {
        System.out.println("\nФильмы с рейтингом >= порога");
        double threshold = readDouble("Введите порог рейтинга: ");

        List<Film> found = FilmLibraryStruct.findByMinRating(library, threshold);
        if (found.isEmpty()) {
            System.out.println("Нет фильмов с рейтингом >= " + threshold);
        } else {
            System.out.println("Найдено (" + found.size() + "):");
            for (Film f : found) {
                System.out.println("  " + f);
            }
        }
    }

    private static void averageRatingDialog(List<Film> library) {
        System.out.println("\nСредний рейтинг по жанру");
        String genre = readLine("Введите жанр: ");
        if (genre.isEmpty()) {
            System.out.println("Жанр не введён. Отмена.");
            return;
        }

        double avg = FilmLibraryStruct.averageRatingByGenre(library, genre);
        if (avg == 0) {
            System.out.println("Фильмов жанра \"" + genre + "\" нет — средний рейтинг не определён.");
        } else {
            System.out.printf("Средний рейтинг жанра \"%s\": %.2f%n", genre, avg);
        }
    }

    private static void showOldest(List<Film> library) {
        System.out.println("\nСамый старый фильм");
        Film oldest = FilmLibraryStruct.findOldest(library);
        if (oldest == null) {
            System.out.println("Библиотека пуста.");
        } else {
            System.out.println("  " + oldest);
        }
    }
}