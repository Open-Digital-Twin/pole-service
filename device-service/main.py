import os
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

    handle_event(request, 'device', handle_device_event)

    # Return 204 - No-content
    return "", 204

def handle_device_event(event: KTwinEvent):
    device_event = event.cloud_event.data
    
    if device_event["batteryLevel"] < 15:
        # Must get something that is not the parent
        parent_twins = get_parent_twins()

        if (parent_twins) > 0:
            send_battery_level_to_neighborhood(device_event, parent_twins[0])

def send_battery_level_to_neighborhood(batteryLevel, target_twin: Twin):
    data = {
        "batteryLevel": batteryLevel
    }
    push_to_virtual_twin(target_twin.twin_interface, target_twin.twin_instance, data=data)

def air_quality_level():
    return {
        "level": "good"
    }

if __name__ == "__main__":
    app.logger.info("Starting up server...")
    app.run(host='0.0.0.0', port=8081)