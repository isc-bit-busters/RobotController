FROM dtcooper/raspberrypi-os:python3.9

RUN apt update
RUN apt install -y ttf-wqy-zenhei python3-pip python3-smbus python3-serial

RUN pip install --no-cache-dir RPi.GPIO spidev rpi_ws281x spade

CMD ["python", "-m", "agent"]
