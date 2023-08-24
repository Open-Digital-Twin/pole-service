# Pole Service

This service implements the Pole business logic for Smart Grids DTDL use case.

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
docker build -t ktwin/pole-service:0.1 .
docker compose up -d
```

## Load Docker into Kind

```bash
kind load docker-image ktwin/pole-service:0.1
```

## Example of cloud payload

### Air Quality Observed

Expected behavior: the City Pole will process the event, calculate the air quality levels based on the provided values and update the record in Event Store.

```sh
curl --request POST \
  --url http://localhost:8081/ \
  --header 'Content-Type: application/json' \
  --header 'ce-id: 123' \
  --header 'ce-source: air-quality-observed-001' \
  --header 'ce-specversion: 1.0' \
  --header 'ce-time: 2021-10-16T18:54:04.924Z' \
  --header 'ce-type: ktwin.real.air-quality-observed' \
  --data '{
    "reliability": 8,
    "volatileOrganicCompoundsTotal": 10,
    "CO2Density": 8,
    "CODensity": 8,
    "PM1Density": 8,
    "PM10Density": 8,
    "PM25Density": 8,
    "SO2Density": 8,
    "C6H6Density": 8,
    "NIDensity": 8,
    "ASDensity": 8,
    "CDDensity": 8,
    "NO2Density": 8,
    "O3Density": 8,
    "PBDensity": 8,
    "SH2Density": 8,
    "precipitation": 8,
    "temperature": 8,
    "WindDirection": 8,
    "WindSpeed": 8,
    "relativeHumidity": 8
}'
```

The following object is stored in event store:

```json
{
    "reliability": 8,
    "volatileOrganicCompoundsTotal": 10,
    "CO2Density": 8,
    "CODensity": 8,
    "PM1Density": 8,
    "PM10Density": 8,
    "PM25Density": 8,
    "SO2Density": 8,
    "C6H6Density": 8,
    "NIDensity": 8,
    "ASDensity": 8,
    "CDDensity": 8,
    "NO2Density": 8,
    "O3Density": 8,
    "PBDensity": 8,
    "SH2Density": 8,
    "precipitation": 8,
    "temperature": 8,
    "WindDirection": 8,
    "WindSpeed": 8,
    "relativeHumidity": 8,
    "CO2_level": {
        "level": "good"
    },
    "CO_level": {
        "level": "good"
    },
    "PM10_level": {
        "level": "good"
    },
    "PM25_level": {
        "level": "good"
    },
    "NO_level": {
        "level": "good"
    },
    "SO2_level": {
        "level": "good"
    },
    "C6H6level": {
        "level": "good"
    },
    "CD_level": {
        "level": "good"
    },
    "O3_level": {
        "level": "good"
    },
    "PB_level": {
        "level": "good"
    },
    "SH2_level": {
        "level": "good"
    }
}
```
