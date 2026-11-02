# Задача 20: Фильмотека

**Студент:** Лупач Д.А.

## Постановка задачи
Написать юнит-тесты и измерить покрытие для модуля фильмотеки.
юнит-тесты должны проверить работоспособность функций:
- add_film()
- by_genre()
- rating_at_least()
- average_rating_by_genre()
- oldest_film()

## Как запустить тесты
python -m unittest -v               --запуск unit-тестов

## Как получить отчёт о покрытии
python -m venv .venv                --создаем виртуальное окружение
.\.venv\Scripts\Activate.ps1        --активируем виртуальное окружение
pip install coverage                --Ставит пакет coverage (инструмент измерения покрытия кода)
coverage run -m unittest            --Запускает unittest под наблюдением coverage
coverage report -m                  --Читает файл .coverage и печатает текстовый отчёт с процентом покрытия.