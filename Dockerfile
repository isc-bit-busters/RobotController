FROM dtcooper/raspberrypi-os:python3.9

ENV DEBIAN_FRONTEND=noninteractive

# Prioritize Raspberry Pi packages
RUN echo 'Package: *\nPin: origin "archive.raspberrypi.org"\nPin-Priority: 1001' > /etc/apt/preferences.d/raspi.pref

# System dependencies
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies needed for libcamera build
RUN pip3 install --no-cache-dir Jinja2 PyYAML ply

# Set up Python path
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Build and install libcamera
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build -j2 install

# Now install picamera2 after libcamera is built
RUN pip3 install --no-cache-dir picamera2

# App setup
WORKDIR /app
COPY requirements.txt .

# Fix requirements.txt - make sure it uses pyyaml instead of yaml
RUN sed -i 's/yaml/pyyaml/g' requirements.txt && \
    pip3 install --no-cache-dir -r requirements.txt

COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]