FROM docker.io/python:3.9-bullseye AS build

# Укажем рабочий каталог
WORKDIR "/app"

# Установим зависимости
# hadolint ignore=DL3008,DL3013
RUN set -eux && \
    apt-get update; \
    apt-get install --no-install-recommends -y \
        # python3-dev и build-essential - понадобится для pyinstaller \
        # UPX - уменьшит размер итоговых файлов \
        # build-essential и patchelf - нужен staticx \
        python3-dev build-essential patchelf upx; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    # обновим pip и установим wheel, staticx и pyinstaller \
    python -m pip install --no-cache-dir --upgrade --force --ignore-installed pip; \
    python -m pip install --no-cache-dir --upgrade wheel staticx pyinstaller

# Установим зависимости
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --requirement requirements.txt

# Скопируем приложение
COPY load_from_csv.py ./

# Создадим бинарный файл приложения
RUN set -eux && \
    # Создадим и упаковываем единый бинарный файл приложения \
    pyinstaller \
      --name app-compiled \
      --onefile app.py \
      --paths "$(python -m site --user-site)"; \
    # Создаем статически линкованный бинарный файл \
    staticx --strip dist/app-compiled dist/app; \
    # Выиграем дополнительно несколько сотен байт, обрезав лишние метаданные \
    strip -s -R .comment -R .gnu.version --strip-unneeded dist/app-compiled; \
    # Создадим каталог tmp, он понадобится для последующей работы приложения \
    mkdir -p dist/tmp; \
    # Убедимся что права выставлены верно \
    chmod -c 755 ./app; \
    chown -c 0:0 ./app


FROM scratch
# Копируем готовый дистрибутив приложения
COPY --from=build /app/dist/app /app

ENTRYPOINT ["/app"]