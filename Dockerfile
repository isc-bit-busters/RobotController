FROM dtcooper/raspberrypi-os:python3.9

# Installer dépendances système
RUN apt update && apt install -y \
    python3-pip \
    python3-smbus \
    python3-serial \
    ttf-wqy-zenhei \
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
    libcamera-dev \
    libcamera-apps \
    python3-picamera2 \
    python3-libcamera \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt
COPY requirements.txt .

# Installer dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Lancer le programme principal
CMD ["python", "-m", "agent"]
