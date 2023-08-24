import os
import math
import sys
import logging
from dotenv import load_dotenv
from flask import Flask, request
from modules.ktwin import handle_request, handle_event, KTwinEvent, Twin, get_latest_twin_event, update_twin_event, get_parent_twins, push_to_virtual_twin

if os.getenv("ENV") == "local":
    load_dotenv('local.env')

app = Flask(__name__)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route("/", methods=["POST"])
def home():
    event = handle_request(request)

    app.logger.info(
        f"Event TwinInstance: {event.twin_instance} - Event TwinInterface: {event.twin_interface}"
    )

    handle_event(request, 'air-quality-observed', handle_air_quality_observed_event)
    handle_event(request, 'weather-observed', handle_weather_observed_event)

    # Return 204 - No-content
    return "", 204

def handle_air_quality_observed_event(event: KTwinEvent):
    air_quality_observed = event.cloud_event.data
    air_quality_observed["CO2_level"] = air_quality_level()
    air_quality_observed["CO_level"] = air_quality_level()
    air_quality_observed["PM10_level"] = air_quality_level()
    air_quality_observed["PM25_level"] = air_quality_level()
    air_quality_observed["NO_level"] = air_quality_level()
    air_quality_observed["SO2_level"] = air_quality_level()
    air_quality_observed["C6H6level"] = air_quality_level()
    air_quality_observed["CD_level"] = air_quality_level()
    air_quality_observed["O3_level"] = air_quality_level()
    air_quality_observed["PB_level"] = air_quality_level()
    air_quality_observed["SH2_level"] = air_quality_level()

    update_twin_event(event)

    if air_quality_observed["SO2_level"] > 10:
        parent_twins = get_parent_twins()

        if (parent_twins) > 0:
            send_air_quality_to_neighborhood(air_quality_observed, parent_twins[0])

def send_air_quality_to_neighborhood(air_quality_observed, parent_twin: Twin):
    data = {
        "SO2_level": air_quality_observed["SO2_level"]
    }
    push_to_virtual_twin(parent_twin.twin_interface, parent_twin.twin_instance, data=data)

def air_quality_level():
    return {
        "level": "good"
    }

def handle_weather_observed_event(event: KTwinEvent):
    latest_event = get_latest_twin_event(event.twin_interface, event.twin_instance)
    if latest_event is None:
        latest_event = KTwinEvent(event.cloud_event)

    weather_observed = event.cloud_event.data
    weather_observed["pressureTendency"] = calculate_pressure_tendency(latest_event, event)
    weather_observed["FeelsLikeTemperature"] = calculate_feel_like_temperature(weather_observed["temperature"], weather_observed["WindSpeed"])
    weather_observed["dewpoint"] = calculate_dewpoint(weather_observed["temperature"], weather_observed["relativeHumidity"])

    update_twin_event(event)

def calculate_pressure_tendency(latest_event: KTwinEvent, current_event: KTwinEvent):
    latest_cloud_event = latest_event.cloud_event.data
    current_cloud_event = current_event.cloud_event.data

    if latest_cloud_event["atmosphericPressure"] is not None and current_cloud_event["atmosphericPressure"] is not None:
        difference = current_cloud_event["atmosphericPressure"] - latest_cloud_event["atmosphericPressure"]
        if abs(difference) < 0.1:
            return "steady"
        if difference < 0:
            return "falling"
        return "raising"
    else:
        "steady"

def calculate_feel_like_temperature(temperature: float, wind_speed: float):
    return 33 + (10 * math.sqrt(wind_speed) + 10.45 - wind_speed) * (temperature - 33)/22

def calculate_dewpoint(temperature: float, relative_humidity: float):
    return temperature - ((100-relative_humidity/5))

if __name__ == "__main__":
    app.logger.info("Starting up server...")
    app.run(host='0.0.0.0', port=8081)