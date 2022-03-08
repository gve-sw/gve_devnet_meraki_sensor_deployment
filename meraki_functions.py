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


#this function takes an organization name and finds its corresponding ID and returns the ID
def getOrgID(base_url, headers, org_name):
    orgs_endpoint = "organizations"
    response = requests.get(base_url+orgs_endpoint, headers=headers)

    if response.status_code != 200:
        return None

    organizations = json.loads(response.text)
    for org in organizations:
        if org["name"] == org_name:
            return org["id"]

    return None


#this function takes an organization ID and network name and finds its corresponding ID and returns the ID
def getNetworkID(base_url, headers, org_id, net_name):
    org_nets_endpoint = "organizations/{}/networks".format(org_id)
    response = requests.get(base_url+org_nets_endpoint, headers=headers)

    if response.status_code != 200:
        return None

    networks = json.loads(response.text)
    for network in networks:
        if network["name"] == net_name:
            return network["id"]

    return None


#this function takes a network ID and a list of device serial numbers and claims those devices into the specified network
def claimDevicesToNetwork(base_url, headers, net_id, devices):
    net_claim_endpoint = "networks/{}/devices/claim".format(net_id)
    body = {"serials": devices}
    response = requests.post(base_url+net_claim_endpoint, headers=headers, data=json.dumps(body))

    return response.status_code


#this function takes a device serial number and a dictionary that contains the
def editDeviceDetails(base_url, headers, serial, data):
    device_endpoint = "devices/{}".format(serial)
    response = requests.put(base_url+device_endpoint, headers=headers, data=json.dumps(data))

    return response.status_code


#this function takes a network ID and a dictionary that defines the alert profile
def createAlertProfile(base_url, headers, net_id, data):
    alert_profile_endpoint = "networks/{}/sensor/alerts/profiles".format(net_id)
    response = requests.post(base_url+alert_profile_endpoint, headers=headers, data=json.dumps(data))

    return response.status_code
