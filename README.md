# Washing Machines - IoT Project

Project to allow students at UNISA Residences to not have to be physically in the washing machines room to know if a given machine is occupied or not.

Also provide a way to make reservation for a given machine, authorize the person that reserved a given machine through QR Codes and a platform management so building manager can support how is currently working.

# Branches

1. `main` -> Using firebase.
2. `mongodb` -> Using a mongodb database with fake init data.

# Docker Image - Instructions 
1. Build Image: `docker build -t washing_machines_iot_server_64 . --platform linux/amd64`
2. Export it to a given folder: `docker save -o washing_machines_64.tar washing_machines_iot_server_64`

# Run the server
1. `poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000`
2. If [behind a proxy server](https://fastapi.tiangolo.com/deployment/docker/) as in Portainer: `poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000 --proxy-headers`


# App to test it
1. App to consume this API -> https://github.com/y3rbiadit0/washing-machine-iot-app


