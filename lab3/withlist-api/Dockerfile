# --- Stage 1: Builder (збираємо залежності) ---
FROM python:3.12-slim as builder

# Встановлюємо змінні середовища
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Встановлюємо системні залежності (gcc та libpq потрібні для збірки)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Створюємо віртуальне середовище
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
# Оновлюємо pip і встановлюємо бібліотеки
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# --- Stage 2: Runtime (фінальний легкий образ) ---
FROM python:3.12-slim

WORKDIR /app

# Встановлюємо runtime-бібліотеки для Postgres та curl для healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

# Копіюємо віртуальне середовище з етапу Builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Створюємо користувача без прав root
RUN useradd -m appuser
USER appuser

# Копіюємо код програми
COPY . .

# Healthcheck: перевіряємо сервер кожні 30 секунд
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Запускаємо сервер
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]