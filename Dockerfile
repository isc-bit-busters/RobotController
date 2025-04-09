FROM dtcooper/raspberrypi-os:python3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
ENV DEBIAN_FRONTEND=noninteractive
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# Prioritize Raspberry Pi packages
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
RUN echo 'Package: *\nPin: origin "archive.raspberrypi.org"\nPin-Priority: 1001' > /etc/apt/preferences.d/raspi.pref
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# System dependencies - avoid python3-pip which can cause conflicts
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
RUN apt-get update && apt-get install -y \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-smbus \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-serial \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    build-essential \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libgl1-mesa-glx \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libglib2.0-0 \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libcap-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    cmake \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    git \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    pkg-config \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libjpeg-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libtiff5-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libavcodec-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libavformat-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libswscale-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libv4l-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libxvidcore-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libx264-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libfontconfig1-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    libfreetype6-dev \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    ffmpeg \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    meson \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    ninja-build \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-venv \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-pybind11 \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-jinja2 \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-yaml \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    python3-ply \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    && apt-get clean \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    && rm -rf /var/lib/apt/lists/*
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# Create and activate a virtual environment to avoid Python module conflicts
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
RUN python3 -m venv /opt/venv
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
ENV PATH="/opt/venv/bin:$PATH"
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
ENV VIRTUAL_ENV="/opt/venv"
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# Install pip inside the virtual environment
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
RUN python -m pip install --upgrade pip
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# Build and install libcamera
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
WORKDIR /opt
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
RUN git clone https://github.com/raspberrypi/libcamera.git && \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    cd libcamera && \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    meson setup build && \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    ninja -C build -j2 install
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# Make sure Python can find the libraries
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
ENV LD_LIBRARY_PATH="/usr/local/lib"
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/opt/venv/lib/python3.9/site-packages"
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# Now install picamera2 and other requirements
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
RUN pip install --no-cache-dir picamera2 RPi.GPIO spidev rpi_ws281x spade==3.3.3 aiofiles \
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
    opencv-python==4.11.0.86 slixmpp pyyaml jinja2 ply
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
# App setup
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
WORKDIR /app
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
COPY agent/ ./agent/
FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]

FROM raspbian/python:3.9

ENV DEBIAN_FRONTEND=noninteractive

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
WORKDIR /opt
RUN git clone https://git.libcamera.org/libcamera/libcamera.git && \
    cd libcamera && \
    meson setup build && \
    ninja -C build install

# Corriger le lien pour Python (libcamera bindings)
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.9/dist-packages:/usr/local/lib/python3.9"

# Installer picamera2 via pip (qui utilise libcamera compilé)
RUN pip3 install --no-cache-dir picamera2

# Appli
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY agent/ ./agent/

CMD ["python3", "-m", "agent.camera_streamer"]
CMD ["python", "-m", "agent.camera_streamer"]