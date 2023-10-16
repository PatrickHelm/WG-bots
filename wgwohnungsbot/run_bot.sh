#!/bin/bash
export EMAIL='you@gmail.com'
export EMAIL_PW='your gmail password for third-party apps' 
# see https://www.youtube.com/watch?v=lSURGX0JHbA for how to get this
export WG_EMAIL='your WG-Gesucht.de email'
export WG_PW='your WG-Gesucht.de password'
nohup xvfb-run -a python wg-gesucht.py >> nohup.out 2>&1 &