FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-smbus \
    python3-serial \
    build-essential \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libcap-dev \
    cmake \
    git \
    pkg-config \
    libjpeg-dev \
    libtiff5-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libcamera0 \
    libcamera-dev \
    python3-libcamera \
    python3-picamera2 \
    libcamera-apps \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances Python
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copier ton code
COPY agent/ ./agent/

# Lancer le programme
CMD ["python3", "-m", "agent.camera_streamer"]
