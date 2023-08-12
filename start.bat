@echo off

start cmd /k ^
    "cd server/src" ^
    "& python server.py"
start cmd /k ^
    "cd real-estate-predictor" ^
    "& npm start"