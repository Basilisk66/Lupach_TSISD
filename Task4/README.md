# Задача 20: Проверка скобочной последовательности

**Студент:** Лупач Д.А.

Реализовать проверку сбалансированности только круглых скобок '()':

## Запуск юнит-тестов
python -m unittest -v 

## Запуск BDD
pip install pytest pytest-bdd
pytest features -v

**Ожидаемый результат**
features/steps/test_brackets_steps.py::test_balanced_string PASSED
features/steps/test_brackets_steps.py::test_extra_closing_bracket PASSED
features/steps/test_brackets_steps.py::test_not_enough_closing_bracket PASSED
features/steps/test_brackets_steps.py::test_string_without_brackets_is_balanced PASSED

## Red–Green–Refactor (кратко)

**Red**
Сначала написал unittests в test_main.py пару методов: пустая
строка, сбалансированные, лишняя ')', нехватка ')', индексы
BDD-сценарии в features/brackets.feature + шаги в
features/steps/test_brackets_steps.py. Запуск падал


**Green**
Добавил main.py с минимальной реализацией через счётчик


**Refactor**
Дописал еще несколько тестов в test_main.py. Дополнительно добавил пустой conftest.py в
корень, чтобы pytest видел main при сборе BDD-шагов/