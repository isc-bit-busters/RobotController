FROM dtcooper/raspberrypi-os:python3.9

# Install basic build and runtime dependencies
RUN apt update && apt install -y \
    git \
    python3-pip \
    python3-dev \
    libcamera-dev \
    libcamera-apps \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-smbus \
    python3-serial \
    libatlas-base-dev \
    libcap-dev \
    libboost-dev \
    libgnutls28-dev \
    qtbase5-dev \
    qttools5-dev-tools \
    libevent-dev \
    libjpeg-dev \
    libtiff-dev \
    libpng-dev \
    libexif-dev \
    libyaml-dev \
    python3-pyudev \
    pybind11-dev \
    libudev-dev \
    libssl-dev \
    cmake \
    pkg-config \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev \
    libglib2.0-dev \
    python3-kms++



COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install Python packages required by libcamera's build system
RUN pip install meson ninja jinja2 pyyaml ply


# Install dependencies for pykms
RUN apt install -y libkms++-dev libfmt-dev libdrm-dev

# Clone and install pykms
RUN git clone https://github.com/raspberrypi/pykms.git /opt/pykms
WORKDIR /opt/pykms
RUN pip install .



# Clone and build libcamera from Raspberry Pi fork
RUN git clone --branch v0.4.0+rpt20250213 https://github.com/raspberrypi/libcamera.git /opt/libcamera
WORKDIR /opt/libcamera

# Build and install libcamera
RUN meson setup build --buildtype=release \
    -Dpipelines=rpi/vc4,rpi/pisp \
    -Dipas=rpi/vc4,rpi/pisp \
    -Dv4l2=true \
    -Dgstreamer=enabled \
    -Dtest=false \
    -Dlc-compliance=disabled \
    -Dcam=disabled \
    -Dqcam=disabled \
    -Ddocumentation=disabled \
    -Dpycamera=enabled && \
    ninja -C build install

# Clone and install Picamera2
RUN git clone https://github.com/raspberrypi/picamera2.git /opt/picamera2
WORKDIR /opt/picamera2
RUN pip install .

RUN pip install opencv-python mmcv-full timm onnx onnx-simplifier onnx-tf tensorflow torch torchvision torchaudio

ENV PYTHONPATH=/usr/local/lib/aarch64-linux-gnu/python3.9/site-packages:$PYTHONPATH

# App code
WORKDIR /agent
COPY . .

WORKDIR ..

CMD ["python3","-m", "agent"]
