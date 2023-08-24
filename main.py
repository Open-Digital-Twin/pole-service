import sys
import logging
from dotenv import load_dotenv
from flask import Flask, request
from modules.ktwin import handle_request, handle_event, KTwinEvent, get_latest_twin_event, update_twin_event

app = Flask(__name__)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

load_dotenv('local.env')

@app.route("/", methods=["POST"])
def home():
    event = handle_request(request)

    app.logger.info(
        f"Event Content: {event.getCloudEvent()}"
        f"Event TwinInstance: {event.getTwinInstance()}"
        f"Event TwinInterface: {event.getTwinInterface()}"
    )

    handle_event(request, 'air-quality-observed', handle_air_quality_observed_event)
        
    # Return 204 - No-content
    return "", 204

def handle_air_quality_observed_event(event: KTwinEvent):
    latest_event = get_latest_twin_event(event.getTwinInterface(), event.getTwinInstance())
    if latest_event is None:
        latest_event = KTwinEvent(event.getCloudEvent())

    air_quality_observed = event.getCloudEvent().data
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

def air_quality_level():
    return {
        "level": "good"
    }

if __name__ == "__main__":
    app.logger.info("Starting up server...")
    app.run(host='0.0.0.0', port=8081)