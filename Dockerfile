FROM dtcooper/raspberrypi-os:python3.9

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages"
ENV LD_LIBRARY_PATH="/usr/local/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH"

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python deps
RUN pip3 install jinja2 PyYAML ply redis opencv-python-headless

# Compile libcamera
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build -Dpycamera=enabled && \
    ninja -C build install

# Fix bindings
RUN cp /opt/libcamera/build/src/py/libcamera/_libcamera.so /usr/local/lib/python3.9/site-packages/ && \
    echo "from _libcamera import *" > /usr/local/lib/python3.9/site-packages/libcamera.py

# Install picamera2
RUN pip3 install --no-cache-dir picamera2

# Application
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
