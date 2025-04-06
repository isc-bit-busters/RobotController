# Hardware Setup
⚠️ https://www.waveshare.com/wiki/AlphaBot2-Pi#Hardware_setup ⚠️

# AlphaPi Zero Agent

A SPADE-based XMPP agent for controlling an AlphaBot2 robot using the Raspberry Pi Zero.

## Overview

This project implements a SPADE (Smart Python Agent Development Environment) agent that controls an AlphaBot2 robot. The agent uses XMPP (Extensible Messaging and Presence Protocol) for communication, allowing remote control of the robot through messaging.

## Features

- Remote control of AlphaBot2 robot via XMPP messages
- Movement commands: forward, backward, left, right, stop
- Direct motor control with specified speed values
- Containerized deployment with Docker

## Requirements

### Hardware
- Raspberry Pi Zero (or compatible)
- AlphaBot2 robot kit
- GPIO access

### Software
- Python 3.9+
- SPADE 3.3.3
- RPi.GPIO
- spidev
- rpi_ws281x

## Installation

### Using Docker (Recommended)

0. Install Docker:
   ```
   curl -sSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   restart terminal
   ```
   
2. Clone this repository:
   ```
   git clone <repository-url>
   cd AlphaPiZeroAgent
   ```

3. Configure the XMPP settings in `docker-compose.yml`: (Leave as it is unless configured)
   ```yaml
   environment:
     XMPP_SERVER: "prosody"
     XMPP_PORT: 5222
     XMPP_DOMAIN: "prosody"
     XMPP_USERNAME: "alpha-pi-zero-agent"
     XMPP_PASSWORD: "top_secret"
   ```

4. Build and run with Docker Compose:
   ```
   docker-compose up -d
   ```

### Manual Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set the required environment variables:
   ```
   export XMPP_SERVER="prosody"
   export XMPP_PORT=5222
   export XMPP_DOMAIN="prosody"
   export XMPP_USERNAME="alpha-pi-zero-agent"
   export XMPP_PASSWORD="top_secret"
   ```

3. Run the agent:
   ```
   python -m agent
   ```

## Usage

Send XMPP messages to the agent with the following commands:

- `forward` - Move the robot forward for 2 seconds
- `backward` - Move the robot backward for 2 seconds
- `left` - Turn the robot left for 2 seconds
- `right` - Turn the robot right for 2 seconds
- `stop` - Stop all motors
- `motor <left_speed> <right_speed>` - Set specific motor speeds (range: -100 to 100)

## Project Structure

- `agent/__main__.py` - Main agent implementation
- `agent/alphabotlib/` - Library for controlling the AlphaBot2 hardware
  - `AlphaBot2.py` - Core motor control functions
  - Additional sensor and control modules

## Configuration

The agent uses environment variables for configuration:

- `XMPP_SERVER` - XMPP server hostname
- `XMPP_PORT` - XMPP server port (default: 5222)
- `XMPP_DOMAIN` - XMPP domain
- `XMPP_USERNAME` - XMPP username for the agent
- `XMPP_PASSWORD` - XMPP password for the agent

## License

[Add your license information here]

## Acknowledgments

- This project uses the [SPADE](https://github.com/javipalanca/spade) framework for agent development
- AlphaBot2 is a product of Waveshare 
