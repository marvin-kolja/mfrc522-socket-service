# mfrc522-socket-service

This repo is for installing a MFRC522 scanner on a RaspberyPi and let you access the UID through socket communcation.

# Installation

The scanner.service file should be copied into "/etc/systemd/system". For more information, follow this documentary (https://www.raspberrypi.org/documentation/linux/usage/systemd.md).

The created service is using the server.py file as script. The other files are for testing purpose, e.g with the client.py script you can interact with the service.

Most importantly here is what you else need:

- python3 or higher
- pip3
  - sudo pip3 install mfrc522
  - sudo pip3 install spidev
  - pip install RPi.GPIO
  

