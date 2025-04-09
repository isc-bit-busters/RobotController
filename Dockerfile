FROM dtcooper/raspberrypi-os:python3.9

ENV DEBIAN_FRONTEND=noninteractive

# Prioritize Raspberry Pi packages
RUN echo 'Package: *\nPin: origin "archive.raspberrypi.org"\nPin-Priority: 1001' > /etc/apt/preferences.d/raspi.pref

# System dependencies - avoid python3-pip which can cause conflicts
RUN apt-get update && apt-get install -y \
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
    python3-venv \
    python3-pybind11 \
    python3-jinja2 \
    python3-yaml \
    python3-ply \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment to avoid Python module conflicts
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

# Install pip inside the virtual environment
RUN python -m pip install --upgrade pip

# Build and install libcamera
WORKDIR /opt
RUN git clone https://github.com/raspberrypi/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build -j2 install

# Make sure Python can find the libraries
ENV LD_LIBRARY_PATH="/usr/local/lib"
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/opt/venv/lib/python3.9/site-packages"

# Now install picamera2 and other requirements
RUN pip install --no-cache-dir picamera2 RPi.GPIO spidev rpi_ws281x spade==3.3.3 aiofiles \
    opencv-python==4.11.0.86 slixmpp pyyaml jinja2 ply

# App setup
WORKDIR /app
COPY agent/ ./agent/

CMD ["python", "-m", "agent.camera_streamer"]