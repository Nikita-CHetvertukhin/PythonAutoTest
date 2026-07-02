# Легковесный образ Debian
FROM debian:bullseye-slim

# Установка базовых пакетов, Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    gnupg \
    curl \
    tar \
    wget \
    git && \
    apt-get clean

# Установка Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && apt-get clean

# Установка Firefox
RUN apt-get update && apt-get install -y firefox-esr && apt-get clean

# Установка Microsoft Edge
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - && \
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list && \
    apt-get update && apt-get install -y microsoft-edge-stable && apt-get clean

# Рабочая директория и переменная PYTHONPATH
WORKDIR /app
ENV PYTHONPATH="/app"

# Копирование зависимостей для уменьшения пересборки слоев
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Копирование всех остальных файлов проекта
COPY . .

# Подготовка entrypoint
RUN apt-get update && apt-get install -y dos2unix && dos2unix /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Точка входа
ENTRYPOINT ["/app/entrypoint.sh"]
