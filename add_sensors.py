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
import csv
import sys
from meraki_functions import *
from env import *


sensors_file = open("sensors.csv", "r")
csv_reader = csv.DictReader(sensors_file)

networks = {} #dictionary will map network names to network ids
networks_to_organizations = {} #dictionary will map networks to their organizations

for row in csv_reader:
    org_id = getOrgID(base_url, headers, row["organization"])
    if org_id is None:
        print("No organization exists with the name".format(row["organization"]))
        sys.exit(1)

    net_id = getNetworkID(base_url, headers, org_id, row["network"])
    if net_id is None:
        print("No network exists in the organization with ID {} with the name {}".format(org_id, row["network"]))
        sys.exit(1)

    networks[row["network"]] = net_id #the key row["network"] is the network name
    networks_to_organizations[net_id] = org_id

    serial = row["serial"]

    status_code = claimDevicesToNetwork(base_url, headers, net_id, [serial])
    if status_code != 200:
        print("{} Error".format(status_code))
        print("There was an error adding the device: {} to the network with ID {}.".format(serial, net_id))
        sys.exit(1)

    sensor_details = {
        "name": row["name"],
        "address": row["location"]
    }

    status_code = editDeviceDetails(base_url, headers, serial, sensor_details)
    if status_code != 200:
        print("{} Error".format(status_code))
        print("There was an error editing the device {} with these details: {}".format(serial, sensor_details))
        sys.exit(1)

    print("Sensor {} was added to network {}".format(serial, row["network"]))

sensors_file.close()

sensor_profile_file = open("sensors_to_profiles.csv", "r")
csv_reader = csv.DictReader(sensor_profile_file)

sensors_to_profiles = {} #dictionary will map the sensors to the alert profiles they need
for row in csv_reader:
    alert_profile = row["alert_profile"]
    serial = row["sensor_serial"]

    if alert_profile in sensors_to_profiles.keys(): #we've already added this alert profile to the dictionary, so we just add another sensor the list
        sensors_to_profiles[alert_profile].append(serial)
    else: #we haven't yet added this alert profile to the dictionary, so we create a new alert profile key and assign it a value of a new list with this serial number as the first value
        sensors_to_profiles[alert_profile] = [serial]

sensor_profile_file.close()

alert_recipients_file = open("alert_recipients.csv", "r")
csv_reader = csv.DictReader(alert_recipients_file)

profiles_to_recipients = {} #dictionary will map the alert profiles to the alert recipients for that profile - this will be a nested dictionary
'''
Data structure example
profiles_to_recipients = {
    "network name": {
        "alert profile": ["email", "email", "email"],
        "alert profile": ["email", "email", "email"]
    }
}
'''

for row in csv_reader:
    profile_name = row["alert_profile"]
    net_name = row["network"]
    recipient = row["email"] #the recipient is defined by an email address

    if net_name in profiles_to_recipients.keys(): #we've already added this network to the dictionary, so we need to check if the alert profile has also already been seen
        if profile_name in profiles_to_recipients[net_name].keys(): #we've already added this alert profile to the dictionary, so we just need to add the recipient to the list
            profiles_to_recipients[net_name][profile_name].append(recipient)
        else: #we haven't yet seen this alert profile, so we need to add a new key to the dictionary that is the profile name and assign it a value of a new list with this recipient as the first value
            profiles_to_recipients[net_name][profile_name] = [recipient]
    else: #we haven't yet added this network to the dictionary, so we need to add a new key to the dictionary that is the network name and assign it a value of a dictionary with a key of the alert profile name with the value of a new list with this recipient as the first value
        profiles_to_recipients[net_name] = {
            profile_name: [recipient]
        }

alert_recipients_file.close()

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
            "emails": profiles_to_recipients[net_name][profile_name],
            "snmp": False,
            "allAdmins": False,
            "smsNumbers": [],
            "httpServerIds": [],
            "pushUserIds": []
        },
        "serials": serials
    }

    status_code = createAlertProfile(base_url, headers, net_id, alert_profile_details)
    if status_code != 201:
        print("Error {}".format(status_code))
        print("There was an issue creating the alert profile: {} to the network with ID {}".format(alert_profile_details, net_id))

    print("Alert profile {} was added to the network {}".format(profile_name, net_name))

alert_profile_file.close()
