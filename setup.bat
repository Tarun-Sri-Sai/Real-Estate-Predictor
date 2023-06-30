@echo off

start cmd /k "cd server/src & pip install pickle-mixin & pip install pandas & pip install scikit-learn & pip install flask & pip install -U flask-cors & pip install requests & exit"
start cmd /k "cd real-estate-predictor & npm install & exit"