FROM dtcooper/raspberrypi-os:python3.9

ENV DEBIAN_FRONTEND=noninteractive

ENV DEBIAN_FRONTEND=noninteractive

# Prioriser les paquets Raspberry Pi
RUN echo 'Package: *\nPin: origin "archive.raspberrypi.org"\nPin-Priority: 1001' > /etc/apt/preferences.d/raspi.pref

# Mettez à jour et installez les dépendances nécessaires
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
    ffmpeg \
    libcamera-dev \
    libcamera-apps \
    python3-libcamera \
    python3-picamera2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers Python
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]