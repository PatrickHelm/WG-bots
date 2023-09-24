#!/bin/bash

nohup xvfb-run -a python wochenanzeigerbot.py >> nohup.out 2>&1 &