FROM dtcooper/raspberrypi-os:python3.9

ENV DEBIAN_FRONTEND=noninteractive

ENV DEBIAN_FRONTEND=noninteractive

# Prioriser les paquets Raspberry Pi
RUN echo 'Package: *\nPin: origin "archive.raspberrypi.org"\nPin-Priority: 1001' > /etc/apt/preferences.d/raspi.pref
# Dépendances système
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
    meson \
    ninja-build \
    python3-pybind11 \
    python3-jinja2 \
    python3-yaml \
    python3-ply \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer libcamera depuis la source

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install


COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]