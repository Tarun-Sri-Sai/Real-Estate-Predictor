# Real Estate Predictor

## About

Real Estate Predictor is an application that can predict the price of a plot based on its type, BHK, Location, Area and Construction status. The data the model has been trained on maybe outdated.

## Getting Started

### Prerequisites

- Requires an installation of [Python 3](https://python.org/downloads).
- Requires an installation of [Node.js](https://nodejs.org/en/download/current) package that includes NPM package manager.

### Setup

- [Repository](https://github.com/Tarun-Sri-Sai/Real-Estate-Predictor.git) can be forked using `git fork`.
- For Windows, navigating to the repository in Command Prompt and running the following command will finish setup:

    ```bash
    setup
    ```

## Usage

- For Windows, navigating to the repository in Command Prompt and running the following command will launch a test version of the application at <localhost:4200>:

    ```bash
    launch
    ```

- The application automatically detects when all the fields have been selected.

## Inside the application

- The application uses Angular.JS, Bootstrap CSS, Python Flask, Pandas and Scikit-learn libraries.
- The price prediction is done using a linear regression model from `scikit-learn` trained on data that whose features have been encoded using target mean ranking.
- The `data.csv` contains around `10,000` records of previous plots and their prices from two cities: Hyderabad and Mumbai.
