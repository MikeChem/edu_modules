# Stage 1: builder
FROM python:3.13-slim as builder

WORKDIR /app

RUN pip install --no-cache-dir poetry
COPY pyproject.toml README.md ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --with dev


# Stage 2: final
FROM python:3.13-slim

WORKDIR /app

# Установим pip + gunicorn явно
RUN pip install --no-cache-dir gunicorn

# Копируем зависимости из первого этапа
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

# Копируем исходный код проекта
COPY . .

# Команда запуска
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]