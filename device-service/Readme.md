# Device Service

This service implements the Device business logic for Smart Grids DTDL use case.

1. It sends a message to the Neighborhood entity in case Devices are with low battery.

## Setup Virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Update dependencies

```bash
pip freeze > requirements.txt
```

## Build Docker Container

```bash
docker build -t ktwin/device-service:0.1 .
docker compose up -d
```

## Load Docker into Kind

```bash
kind load docker-image ktwin/device-service:0.1
```

## Example of cloud payload

### Battery Level event

Expected behavior: it process the event and in case of low battery level, it sends a notification to the neighborhood entity.

```sh
curl --request POST \
  --url http://localhost:8081/ \
  --header 'Content-Type: application/json' \
  --header 'ce-id: 123' \
  --header 'ce-source: device-001' \
  --header 'ce-specversion: 1.0' \
  --header 'ce-time: 2021-10-16T18:54:04.924Z' \
  --header 'ce-type: ktwin.real.device' \
  --data '{
	"batteryLevel": 10,
	"dateObserved": "2023-07-01T01:11:34.39Z"
}'
```

The following object is stored in event store:

```json
```
