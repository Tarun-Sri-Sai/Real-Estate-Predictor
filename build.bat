@echo off

start cmd /k "pip install pandas scikit-learn flask flask-cors & exit"
start cmd /k "cd real-estate-predictor & npm install & npm install @angular/cli & npm audit fix --force & exit"