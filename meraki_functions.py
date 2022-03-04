#!/usr/bin/env python3
"""Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied."""
import requests
import json


def getOrgID(base_url, headers, org_name):
    orgs_endpoint = "organizations"
    response = json.loads(requests.get(base_url+orgs_endpoint, headers=headers).text)

    for org in response:
        if org["name"] == org_name:
            return org["id"]

    return None


def getNetworkID(base_url, headers, org_id, net_name):
    org_nets_endpoint = "organizations/{}/networks".format(org_id)
    response = json.loads(requests.get(base_url+org_nets_endpoint, headers=headers).text)

    for network in response:
        if network["name"] == net_name:
            return network["id"]

    return None


def getDeviceSerial(base_url, headers, net_id, device_name):
    net_device_endpoint = "networks/{}/devices".format(net_id)
    response = json.loads(requests.get(base_url+net_device_endpoint, headers=headers).text)

    for device in response:
        if device["name"] == device_name:
            return device["serial"]

    return None


def getNetworkDetails(base_url, headers, net_id):
    net_endpoint = "networks/{}".format(net_id)
    response = requests.get(base_url+net_endpoint, headers=headers)

    network = json.loads(response)

    return network


def claimDevicesToNetwork(base_url, headers, net_id, devices):
    net_claim_endpoint = "networks/{}/devices/claim".format(net_id)
    body = {"serials": devices}
    response = requests.post(base_url+net_claim_endpoint, headers=headers, data=json.dumps(body))

    print(response.status_code)

    return response.status_code


def getDeviceDetails(base_url, headers, serial):
    device_endpoint = "devices/{}".format(serial)
    response = requests.get(base_url+device_endpoint, headers=headers)

    device = json.loads(response.text)

    return device


def editDeviceDetails(base_url, headers, serial, data):
    device_endpoint = "devices/{}".format(serial)
    response = requests.put(base_url+device_endpoint, headers=headers, data=json.dumps(data))

    updated_device = json.loads(response.text)

    return updated_device


def createAlertProfile(base_url, headers, net_id, data):
    alert_profile_endpoint = "networks/{}/sensor/alerts/profiles".format(net_id)
    response = requests.post(base_url+alert_profile_endpoint, headers=headers, data=json.dumps(data))

    print(response)
    print(response.status_code)

    alert_profile = json.loads(response.text)

    return alert_profile


def getSensors(base_url, headers, net_id):
    sensors_endpoint = "networks/{}/sensors".format(net_id)
    response = requests.get(base_url+sensors_endpoint, headers=headers)

    sensors = json.loads(response.text)

    return sensors
