# Базовый образ Debian
FROM debian:bullseye-slim

# Установка базовых пакетов, локалей, Python, Java, а также инструментов для виртуального дисплея, VNC и noVNC
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    xclip \
    xsel \
    git && \
    apt-get clean

# Установка Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && apt-get clean

# Установка Firefox
RUN apt-get update && apt-get install -y firefox-esr && apt-get clean

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
