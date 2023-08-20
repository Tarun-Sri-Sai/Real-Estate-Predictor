@echo off

start cmd /k ^
    "pip install pandas scikit-learn flask flask-cors" ^
    "& exit"

start cmd /k ^
    "cd frontend" ^
    "& npm install" ^
    "& npm install @angular/cli" ^
    "& npm audit fix" ^
    "& exit"