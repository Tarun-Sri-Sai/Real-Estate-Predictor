@echo off

start cmd /k ^
    "cd server & python server.py"

start cmd /k ^
    "cd frontend & npm start"
