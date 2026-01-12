# Dockerfile pour Whisper STT Global avec Faster-Whisper
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Bigmoletos"
LABEL description="Service Whisper STT Global pour transcription vocale en temps réel"
LABEL version="1.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV WHISPER_CACHE_DIR=/app/.cache/whisper

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    portaudio19-dev \
    alsa-utils \
    pulseaudio \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer Rust (nécessaire pour Faster-Whisper)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    . "$HOME/.cargo/env" && \
    rustc --version

# Ajouter Rust au PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python (avec Faster-Whisper)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir faster-whisper

# Copier le code source
COPY src/ ./src/
COPY config.json .

# Créer le répertoire pour le cache Whisper
RUN mkdir -p /app/.cache/whisper && \
    mkdir -p /app/logs

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 whisperuser && \
    chown -R whisperuser:whisperuser /app

USER whisperuser

# Exposer le port (si nécessaire pour une API future)
# EXPOSE 8000

# Commande par défaut
CMD ["python", "-m", "src.main"]
