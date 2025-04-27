#Базовый образ Debian
FROM debian:bullseye-slim

# Установка базовых пакетов, локализаций, Python, Java и необходимых инструментов
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    openjdk-11-jre-headless \
    python3 \
    python3-pip \
    curl \
    tar \
    gnupg \
    wget \
    software-properties-common \
    unzip \
    firefox-esr && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean

# Установка переменных окружения для локализаций
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Установка Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && apt-get clean

# Установка Firefox
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && apt-get clean

# Установка Yandex Browser
RUN apt-get update && apt-get install -y wget && \
    wget -q https://browser.yandex.ru/download/?os=linux -O yandex-browser-beta.deb && \
    apt-get update && apt-get install -y ./yandex-browser-beta.deb && \
    rm yandex-browser-beta.deb

# Установка Allure CLI
RUN curl -sSL https://github.com/allure-framework/allure2/releases/download/2.22.0/allure-2.22.0.tgz | tar -xz -C /opt/ && \
    ln -s /opt/allure-2.22.0/bin/allure /usr/bin/allure

# Рабочая директория
WORKDIR /app

# Копируем зависимости отдельно для уменьшения пересборки слоев
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем все остальные файлы проекта
COPY newFrameworks /app

# Команда по умолчанию
CMD ["pytest", "--alluredir=allure-results"]
