# https://www.kaggle.com/ikonnikovirina

# ABOUT PROJECT

The project implements the creation of a machine learning model designed to identify anomalies in the operation of equipment.
The project demonstrates the ability to automatically deploy web-service using Docker.

# START

Install Docker on your computer (https://www.docker.com/).

Clone the repository and go to it on the command line:
```
git clone git@github.com:irinaexzellent/ikonnikovirina.git
```
# Description of commands for running an application in container

Dockerfile — this is a file with instructions for creating an image.
'docker-compose.yaml' provides instructions for deploying a project to container.

Go to the directory where docker-compose.yml is saved and run:
```
docker compose up -d --build
```
You can view information about deployed containers using the command:
```
$ docker container ls
```

## Functionality check

API project:

* http://localhost:8004/docs#

After sending a POST request in string format, you will receive information about the presence or absence of an anomaly in the operation of the equipment.
Example string:
```
"2020-03-09 14:09:56,0.0278083,0.0399288,1.21178,0.054711,68.7436,24.7123,235.085,27.977"
```
Value in string:
```
datetime,Accelerometer1RMS,Accelerometer2RMS,Current,Pressure,Temperature,Thermocouple,Voltage,Volume Flow RateRMS
```
The request requires at least 110 lines.

## Author

* **Irina Ikonnikova** -  [[IrinaIkonnikova](https://github.com/irinaexzellent)]
