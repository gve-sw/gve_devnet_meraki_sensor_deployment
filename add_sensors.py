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
from pprint import pprint
import csv
import sys
from meraki_functions import *
from env import *


sensors_file = open("sensors.csv", "r")
csv_reader = csv.DictReader(sensors_file)

networks = {}
networks_to_organizations = {}

for row in csv_reader:
    org_id = getOrgID(base_url, headers, row["organization"])
    if org_id is None:
        print("No organization exists with the name".format(row["organization"]))
        sys.exit(1)

    net_id = getNetworkID(base_url, headers, org_id, row["network"])
    if net_id is None:
        print("No network exists in the organization with ID {} with the name {}".format(org_id, row["network"]))
    networks[row["network"]] = net_id
    networks_to_organizations[net_id] = org_id

    serial = row["serial"]

    status_code = claimDevicesToNetwork(base_url, headers, net_id, [serial])
    if status_code != 200:
        print("{} Error".format(status_code))
        print("There was an error adding the device: {} to the network with ID.".format(serial, net_id))
        sys.exit(1)

    sensor_details = {
        "name": row["name"],
        "address": row["location"]
    }

    editDeviceDetails(base_url, headers, serial, sensor_details)

sensors_file.close()

sensor_profile_file = open("sensors_to_profiles.csv", "r")
csv_reader = csv.DictReader(sensor_profile_file)

sensors_to_profiles = {}
for row in csv_reader:
    alert_profile = row["alert_profile"]
    serial = row["sensor_serial"]

    if alert_profile in sensors_to_profiles.keys():
        sensors_to_profiles[alert_profile].append(serial)
    else:
        sensors_to_profiles[alert_profile] = [serial]

sensor_profile_file.close()

alert_profile_file = open("alert_profiles.csv", "r")
csv_reader = csv.DictReader(alert_profile_file)

for row in csv_reader:
    temp_threshold = row["temp_threshold"]
    temp_duration = row["temp_duration"]
    profile_name = row["name"]
    net_name = row["network"]

    net_id = networks[net_name]
    org_id = networks_to_organizations[net_id]
    serials = sensors_to_profiles[profile_name]


    alert_profile_details = {
        "name": profile_name,
        "scheduleId": "",
        "conditions": [
            {
                "type": "temperature",
                "unit": "fahrenheit",
                "direction": "+",
                "threshold": temp_threshold,
                "duration": temp_duration
            }
        ],
        "recipients": {
            "emails": [],
            "snmp": False,
            "allAdmins": False,
            "smsNumbers": [],
            "httpServerIds": [],
            "pushUserIds": []
        },
        "serials": serials
    }

    new_profile = createAlertProfile(base_url, headers, net_id, alert_profile_details)

alert_profile_file.close()
