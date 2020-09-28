#! /usr/bin/bash

python tests/pusher.py

queuemo --runtime 20 --verbose
