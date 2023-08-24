import os
import json
import requests
from cloudevents.http import CloudEvent, to_structured, from_http, to_binary

EVENT_REAL_TO_VIRTUAL = "ktwin.real.%s"
EVENT_VIRTUAL_TO_REAL = "ktwin.virtual.%s"
EVENT_TO_EVENT_STORE = "ktwin.event.store"

def get_event_store_url():
    return os.getenv("KTWIN_EVENT_STORE")

def get_broker_url():
    return os.getenv("KTWIN_BROKER")

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

def build_cloud_event(ce_type, ce_source, data):
    attributes = {
        "type" : ce_type,
        "source" : ce_source
    }
    return CloudEvent(attributes, data)

def push_to_real_twin(twin_interface, twin_instance, data):
    ce_type = EVENT_VIRTUAL_TO_REAL.format(twin_interface)
    ce_source = twin_instance
    cloud_event = build_cloud_event(ce_type, ce_source, data)
    headers, body = to_structured(cloud_event)

    response = requests.post(get_broker_url(), headers=headers, data=body)

    if response.status_code != 202:
        raise Exception("Error when pushing to event broker", response)


def push_to_virtual_twin(twin_interface, twin_instance, data):
    ce_type = EVENT_REAL_TO_VIRTUAL.format(twin_interface)
    ce_source = twin_instance
    cloud_event = build_cloud_event(ce_type, ce_source, data)
    headers, body = to_structured(cloud_event)

    response = requests.post(get_broker_url(), headers=headers, data=body)

    if response.status_code != 202:
        raise Exception("Error when pushing to event broker", response)
    

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

class Twin:
    def __init__(self, twin_interface, twin_instance) -> None:
        self.twin_interface = twin_interface
        self.twin_instance = twin_instance

def get_parent_twins() -> list[Twin]:
    parent_twins = os.getenv("PARENT_TWINS")
    if parent_twins is None:
        return parent_twins
    j = json.loads(parent_twins)

    twin_list = list()
    for twin_json in j:
        twin = Twin(**twin_json)
        twin_list.append(twin)

    return twin_list
