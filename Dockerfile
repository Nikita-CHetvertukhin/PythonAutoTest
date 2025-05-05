# Базовый образ Debian
FROM debian:bullseye-slim

# Установка базовых пакетов, локалей, Python, Java, а также инструментов для виртуального дисплея, VNC и noVNC
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
    xvfb \
    x11vnc \
    fluxbox \
    git && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean

# Установка переменных окружения для локалей
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Установка Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && apt-get clean

# Установка Chromedriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver_linux64.zip

# Установка Firefox
RUN apt-get update && apt-get install -y firefox-esr && apt-get clean

# Установка Geckodriver для Firefox
RUN GECKO_DRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | \
    grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/') && \
    wget -q "https://github.com/mozilla/geckodriver/releases/download/v$GECKO_DRIVER_VERSION/geckodriver-v$GECKO_DRIVER_VERSION-linux64.tar.gz" && \
    tar -xzf geckodriver-v$GECKO_DRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-v$GECKO_DRIVER_VERSION-linux64.tar.gz

# Установка Allure CLI для генерации отчётов
RUN curl -sSL https://github.com/allure-framework/allure2/releases/download/2.22.0/allure-2.22.0.tgz | tar -xz -C /opt/ && \
    ln -s /opt/allure-2.22.0/bin/allure /usr/bin/allure

# Клонирование noVNC и websockify (без них noVNC работать не будет)
RUN git clone --depth=1 https://github.com/novnc/noVNC.git /opt/novnc && \
    git clone --depth=1 https://github.com/novnc/websockify.git /opt/novnc/utils/websockify

# Рабочая директория и переменная PYTHONPATH
WORKDIR /app
ENV PYTHONPATH="/app"

# Копирование зависимостей для уменьшения пересборки слоев
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Копирование всех остальных файлов проекта
COPY . .

# Копирование скрипта-стартапа
COPY entrypoint.sh /app/entrypoint.sh
RUN apt-get update && apt-get install -y dos2unix && dos2unix /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Проброс порта для доступа к noVNC (HTML5-интерфейсу)
EXPOSE 6080

# Точка входа
ENTRYPOINT ["/app/entrypoint.sh"]
