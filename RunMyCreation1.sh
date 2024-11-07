#!/bin/bash
echo "cd to My Discord Creation Bot"
cd /home/darkie2305/Desktop/My-Discord-Creation-Bot
echo "Pulling latest update from git repo"
git pull
echo "Activate source venv"
source venv/bin/activate
cd /home/darkie2305/Desktop/My-Discord-Creation-Bot
echo "Starting up My Creation 1"
python3 MyCreation1.py
