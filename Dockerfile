FROM dtcooper/raspberrypi-os:python3.9

RUN apt update
RUN apt install -y ttf-wqy-zenhei python3-pip python3-smbus python3-serial

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "agent"]
