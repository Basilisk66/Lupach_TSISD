import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

class Film {
    private final String title;
    private final int year;
    private final String genre;
    private final double rating;
    private final String directorName;

    public Film(String title, int year, String genre, double rating, String directorName) {
        this.title = title;
        this.year = year;
        this.genre = genre;
        this.rating = rating;
        this.directorName = directorName;
    }

    public String getTitle()        { return title; }
    public int getYear()            { return year; }
    public String getGenre()        { return genre; }
    public double getRating()       { return rating; }
    public String getDirectorName() { return directorName; }

    public boolean hasGenre(String genre) {
        return this.genre.equalsIgnoreCase(genre);
    }

    public boolean hasRatingAtLeast(double threshold) {
        return this.rating >= threshold;
    }

    @Override
    public String toString() {
        return title + " (" + year + ", " + genre
                + ", рейтинг " + rating
                + ", реж. " + directorName + ")";
    }
}

class FilmLibrary {
    private final List<Film> films = new ArrayList<>();

    public void add(Film film) {
        films.add(film);
    }

    public int size() {
        return films.size();
    }

    public boolean isEmpty() {
        return films.isEmpty();
    }
    public List<Film> getAll() {
        return Collections.unmodifiableList(films);
    }

    public List<Film> findByGenre(String genre) {
        List<Film> result = new ArrayList<>();
        for (Film f : films) {
            if (f.hasGenre(genre)) {
                result.add(f);
            }
        }
        return result;
    }

    public List<Film> withRatingAtLeast(double threshold) {
        List<Film> result = new ArrayList<>();
        for (Film f : films) {
            if (f.hasRatingAtLeast(threshold)) {
                result.add(f);
            }
        }
        return result;
    }

    public double averageRatingByGenre(String genre) {
        double sum = 0;
        int count = 0;
        for (Film f : films) {
            if (f.hasGenre(genre)) {
                sum += f.getRating();
                count++;
            }
        }
        return count == 0 ? 0.0 : sum / count;
    }

    public Film findOldest() {
        if (films.isEmpty()) return null;
        Film oldest = films.get(0);
        for (Film f : films) {
            if (f.getYear() < oldest.getYear()) {
                oldest = f;
            }
        }
        return oldest;
    }
}

class ConsoleUI {
    private final FilmLibrary library;
    private final Scanner scanner;

    public ConsoleUI(FilmLibrary library, Scanner scanner) {
        this.library = library;
        this.scanner = scanner;
    }

    public void run() {
        boolean running = true;
        while (running) {
            printMenu();
            int choice = readInt("Ваш выбор: ");
            switch (choice) {
                case 1: showAll(); break;
                case 2: addMovieDialog(); break;
                case 3: searchByGenreDialog(); break;
                case 4: searchByRatingDialog(); break;
                case 5: averageRatingDialog(); break;
                case 6: showOldest(); break;
                case 0:
                    running = false;
                    System.out.println("До свидания!");
                    break;
                default:
                    System.out.println("Нет такого пункта. Попробуйте снова.");
            }
        }
    }

    private void printMenu() {
        System.out.println("\n     ФИЛЬМОТЕКА");
        System.out.println("1. Показать все фильмы");
        System.out.println("2. Добавить фильм");
        System.out.println("3. Найти фильмы по жанру");
        System.out.println("4. Фильмы с рейтингом >= порога");
        System.out.println("5. Средний рейтинг по жанру");
        System.out.println("6. Самый старый фильм");
        System.out.println("0. Выход");
    }
    private int readInt(String prompt) {
        while (true) {
            System.out.print(prompt);
            String line = scanner.nextLine().trim();
            try {
                return Integer.parseInt(line);
            } catch (NumberFormatException e) {
                System.out.println("Нужно ввести целое число");
            }
        }
    }

    private double readDouble(String prompt) {
        while (true) {
            System.out.print(prompt);
            String line = scanner.nextLine().trim().replace(',', '.');
            try {
                return Double.parseDouble(line);
            } catch (NumberFormatException e) {
                System.out.println("Нужно ввести число. Попробуй ещё раз.");
            }
        }
    }

    private String readLine(String prompt) {
        System.out.print(prompt);
        return scanner.nextLine().trim();
    }

    private void showAll() {
        System.out.println("\nВсе фильмы (" + library.size() + " шт.):");
        printList(library.getAll());
    }

    private void addMovieDialog() {
        System.out.println("\nДобавление фильма");
        String title = readLine("Название: ");
        if (title.isEmpty()) {
            System.out.println("Название не может быть пустым");
            return;
        }
        int year = readInt("Год выпуска: ");
        String genre = readLine("Жанр: ");
        double rating = readDouble("Рейтинг (от 0 до 10): ");
        String directorName = readLine("Режиссёр: ");
        if (directorName.isEmpty()) {
            directorName = "неизвестен";
        }

        library.add(new Film(title, year, genre, rating, directorName));
        System.out.println("Фильм добавлен: " + title);
    }

    private void searchByGenreDialog() {
        System.out.println("\nПоиск по жанру");
        String genre = readLine("Введите жанр: ");
        if (genre.isEmpty()) {
            System.out.println("Жанр не введён");
            return;
        }
        List<Film> found = library.findByGenre(genre);
        if (found.isEmpty()) {
            System.out.println("Фильмов жанра \"" + genre + "\" не найдено.");
        } else {
            System.out.println("Найдено (" + found.size() + "):");
            printList(found);
        }
    }

    private void searchByRatingDialog() {
        System.out.println("\nФильмы с рейтингом >= порога");
        double threshold = readDouble("Введите порог рейтинга: ");
        List<Film> found = library.withRatingAtLeast(threshold);
        if (found.isEmpty()) {
            System.out.println("Нет фильмов с рейтингом >= " + threshold);
        } else {
            System.out.println("Найдено (" + found.size() + "):");
            printList(found);
        }
    }

    private void averageRatingDialog() {
        System.out.println("\nСредний рейтинг по жанру");
        String genre = readLine("Введите жанр: ");
        if (genre.isEmpty()) {
            System.out.println("Жанр не введён. Отмена.");
            return;
        }
        double avg = library.averageRatingByGenre(genre);
        if (avg == 0.0) {
            System.out.println("Фильмов жанра \"" + genre + "\" нет — средний рейтинг не определён.");
        } else {
            System.out.printf("Средний рейтинг жанра \"%s\": %.2f%n", genre, avg);
        }
    }

    private void showOldest() {
        System.out.println("\nСамый старый фильм");
        Film oldest = library.findOldest();
        if (oldest == null) {
            System.out.println("Библиотека пуста");
        } else {
            System.out.println("  " + oldest);
        }
    }

    private void printList(List<Film> films) {
        if (films.isEmpty()) {
            System.out.println("  (пусто)");
            return;
        }
        for (Film f : films) {
            System.out.println("  " + f);
        }
    }
}


public class oop {
    public static void main(String[] args) {
        FilmLibrary library = new FilmLibrary();

        library.add(new Film("Области тьмы", 2011, "триллер", 7.4, "Нил Бёргер"));
        library.add(new Film("Властелин колец: Две башни", 2002, "фэнтези", 8.8, "Питер Джексон"));
        library.add(new Film("Джентльмены", 2019, "криминал", 8.2, "Гай Ричи"));
        library.add(new Film("Назад в будущее", 1985, "фантастика", 7.8, "Роберт Земекис"));
        library.add(new Film("Третий лишний", 2012, "комедия", 6.9, "Сет МакФарлейн"));
        library.add(new Film("Зелёный слоник", 1999, "драма", 5.3, "Светлана Баскова"));
        library.add(new Film("Семь", 1995, "триллер", 7.6, "Дэвид Финчер"));
        library.add(new Film("Хатико", 2008, "драма", 7.5, "Лассе Халльстрём"));

        ConsoleUI ui = new ConsoleUI(library, new Scanner(System.in));
        ui.run();
    }
}