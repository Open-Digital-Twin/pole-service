import os
import requests
from cloudevents.http import CloudEvent, to_structured, from_http, to_binary

EVENT_REAL_TO_VIRTUAL = "ktwin.real.%s"
EVENT_VIRTUAL_TO_REAL = "ktwin.virtual.%s"
EVENT_TO_EVENT_STORE = "ktwin.event.store"

def get_event_store_url():
    return os.getenv("KTWIN_EVENT_STORE")

# Decode Request to Cloud Event
# Send Request

# Get Value from Event Store
# TwinEvent
# Send event to parent

class KTwinEvent:
    def __init__(self, cloud_event: CloudEvent):
        self.cloud_event = cloud_event
        ce_type_split = cloud_event["type"].split(".")
        if len(ce_type_split) > 2:
            self.twin_interface = ce_type_split[2]
        self.twin_instance = cloud_event["source"]

def build_attributes(type, source):
    attributes = {
        "type" : type,
        "source" : source
    }
    return attributes

def send_message(target_address, source_address, message_type, data):
    attributes = build_attributes(message_type, source_address)

    event = CloudEvent(attributes, data)
    headers, body = to_structured(event)

    requests.post(target_address, headers=headers, data=body)
    print(f"Sent {event['id']} from {event['source']} with " f"{event.data}")

def handle_event(request: requests.Request, twinInterface: str, callback):
    ktwin_event = handle_request(request)
    if ktwin_event.twin_interface == twinInterface:
        callback(ktwin_event)

def handle_request(request) -> KTwinEvent:
    cloud_event = from_http(request.headers, request.get_data())
    return KTwinEvent(cloud_event)

def get_latest_twin_event(twin_interface, twin_instance):
    url = get_event_store_url() + "/api/v1/twin-events/%s/%s/latest" % (twin_interface, twin_instance)
    response = requests.get(url)

    if response.status_code == 404:
        return None

    cloud_event = from_http(response.headers, response.content)
    return KTwinEvent(cloud_event)

def update_twin_event(ktwin_event: KTwinEvent):
    url = get_event_store_url() + "/api/v1/twin-events"
    headers, body = to_binary(ktwin_event.cloud_event)
    response = requests.post(url, data=body, headers=headers)

    if response.status_code != 202:
        raise Exception("Error while updating twin event", response)

    return response

