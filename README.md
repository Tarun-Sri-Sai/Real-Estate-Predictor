# Real Estate Price Predictor

## Description

A web application that takes in details about the property you're looking for, and provides an estimation of the price according to the data provided to train the model. The data provided with this project contains 9000 listings of properties from the cities Hyderabad and Mumbai.

## Requirements

This project requires the following software:

- docker: 28.0 or above
- 7z: 24 or above

## Usage

1. Extract `server/data.7z` into `server`.

   ```bash
   7z x "server/data.7z" -o"server"
   ```

2. Open Docker Desktop and run the following command in the terminal at the root of this repository:

   ```bash
   docker compose up --build
   ```

   To stop the container, run the following command:

   ```bash
   docker compose down
   ```
