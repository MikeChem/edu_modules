# Stage 1: Сборка зависимостей через Poetry
FROM python:3.13-slim as builder

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем pyproject.toml и README.md для установки зависимостей
COPY pyproject.toml README.md ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --with dev

# Stage 2: Финальный образ
FROM python:3.13-slim

WORKDIR /app

# Установка Poetry и подготовка кэша
RUN pip install --no-cache-dir poetry && \
    mkdir -p /root/cache

# Копируем зависимости из первого этапа
COPY --from=builder /root/.cache/pypoetry /root/.cache/pypoetry
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# ЯВНО УСТАНОВИМ GUNICORN (на случай, если он не попал в образ)
RUN pip install gunicorn

# Копируем исходный код приложения
COPY . .

# Команда запуска
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]