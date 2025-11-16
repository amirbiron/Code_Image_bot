FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies and base fonts available via apt
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        fonts-firacode \
        fonts-hack \
        fonts-dejavu \
        fontconfig \
        wget \
        unzip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install JetBrains Mono, Victor Mono, Cascadia Code, and Ubuntu fonts manually (not in apt repos)
RUN set -eux; \
    mkdir -p /usr/share/fonts/truetype/jetbrains /usr/share/fonts/truetype/victor-mono /usr/share/fonts/truetype/cascadia /usr/share/fonts/truetype/ubuntu; \
    cd /tmp; \
    wget -O JetBrainsMono.zip https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip; \
    unzip JetBrainsMono.zip -d JetBrainsMono; \
    find JetBrainsMono -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/jetbrains/ \;; \
    rm -rf JetBrainsMono JetBrainsMono.zip; \
    wget -O VictorMono.zip https://rubjo.github.io/victor-mono/VictorMonoAll.zip; \
    unzip VictorMono.zip -d VictorMono; \
    find VictorMono -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/victor-mono/ \;; \
    rm -rf VictorMono VictorMono.zip; \
    wget -O CascadiaCode.zip https://github.com/microsoft/cascadia-code/releases/download/v2111.01/CascadiaCode-2111.01.zip; \
    unzip CascadiaCode.zip -d CascadiaCode; \
    find CascadiaCode -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/cascadia/ \;; \
    rm -rf CascadiaCode CascadiaCode.zip; \
    wget -O UbuntuFonts.zip https://assets.ubuntu.com/v1/fad7939b-ubuntu-font-family-0.83.zip; \
    unzip UbuntuFonts.zip -d UbuntuFonts; \
    find UbuntuFonts -name "*.ttf" -exec install -m 644 {} /usr/share/fonts/truetype/ubuntu/ \;; \
    rm -rf UbuntuFonts UbuntuFonts.zip; \
    fc-cache -f -v

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "code_image_bot_macos.py"]
