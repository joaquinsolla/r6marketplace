#!/bin/bash

/usr/bin/python /home/raspy/Desktop/r6marketplace/main.py

origen="/home/raspy/Desktop/r6marketplace/website"

destino="/var/www/html"

sudo cp -r "$origen"/* "$destino"

echo "[ Website files copied to Apache2 ]"

/home/raspy/Desktop/status/status.sh
