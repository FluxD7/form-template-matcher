# Form Template Matcher

## Описание

`Form Template Matcher` — это Python-приложение для сопоставления входных аргументов с шаблонами форм, хранящимися в базе данных `forms.json`. Программа принимает аргументы командной строки, определяет типы полей (дата, телефон, email, текст) и возвращает имя подходящего шаблона или словарь с типами полей, если шаблон не найден. Проект включает тесты с 100% покрытием кода и оптимизирован для быстрого выполнения (~0.4 секунды).

## Требования

- Python 3.11+
- Зависимости (указаны в `requirements.txt`):
  - pytest>=8.4.1
  - pytest-cov>=6.2.1
  - tinydb>=4.8.0

## Установка

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/form-template-matcher.git
   cd form-template-matcher
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # для Windows
   # или
   source .venv/bin/activate  # для Linux/Mac
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Инициализируйте базу данных:
   ```bash
   python init_db.py
   ```

## Использование

Запустите приложение с командой `get_tpl` и аргументами в формате `--field=value`:

```bash
python app.py get_tpl --customer="John Smith" --дата_заказа=27.05.2025 --order_id=12345 --contact="+7 903 123 45 78"
```

**Пример вывода**:
```
Форма заказа
```

Если шаблон не найден, возвращается словарь с типами полей:

```bash
python app.py get_tpl --email=user@example.com --name="Anna Petrova"
```

**Вывод**:
```json
{
  "email": "email",
  "name": "text"
}
```

## Запуск тестов

Проект содержит 23 теста, обеспечивающих 100% покрытие кода. Для запуска тестов с отчётом покрытия выполните:

```bash
python -m pytest test_app.py test_init_db.py --cov=. --cov-config=.coveragerc --cov-report=term-missing --cov-report=html -vv
```

**Ожидаемый результат**:
```
---------- coverage: platform win32, python 3.11.9-final-0 -----------
Name                Stmts   Miss  Cover   Missing
-----------------------------------------------
app.py                 78      0   100%
init_db.py             22      0   100%
-----------------------------------------------
TOTAL                 100      0   100%
Coverage HTML written to dir htmlcov
================= 23 passed in 0.40s ==================
```

HTML-отчёт покрытия доступен в папке `htmlcov`.

## Структура проекта

- `app.py`: Основной скрипт для обработки аргументов и сопоставления шаблонов.
- `init_db.py`: Инициализация базы данных `forms.json` с тремя шаблонами.
- `test_app.py`: Тесты для `app.py` (21 тест).
- `test_init_db.py`: Тесты для `init_db.py` (2 теста).
- `.coveragerc`: Конфигурация для `pytest-cov`.
- `requirements.txt`: Зависимости проекта.
- `.gitignore`: Исключение временных файлов и виртуального окружения.
- `README.md`: Документация проекта.

## Настройка GitHub Actions

Проект включает GitHub Action для автоматического запуска тестов при каждом `push` или `pull request`. Конфигурация находится в `.github/workflows/pytest.yml`. Для проверки статуса тестов перейдите в раздел **Actions** на странице репозитория.

## Оптимизация производительности

- Время выполнения тестов оптимизировано до ~0.4 секунды.
- Для ускорения тестов добавьте папку `C:\form-template-matcher` в исключения антивируса:
  - "Безопасность Windows" → "Защита от вирусов и угроз" → "Параметры" → "Добавить исключение".

## Контакты

Если у вас есть вопросы или предложения, создайте issue в репозитории: [[https://github.com/your-username/form-template-matcher](https://github.com/FluxD7/form-template-matcher)]
