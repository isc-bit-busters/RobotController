FROM dtcooper/raspberrypi-os:python3.9

# 1. MàJ et installation des dépendances système
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
    libcamera-dev \
    libcamera-apps \
    python3-picamera2 \
    python3-libcamera \
    && rm -rf /var/lib/apt/lists/*

# 2. Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Lancer ton code
CMD ["python", "-m", "agent"]
