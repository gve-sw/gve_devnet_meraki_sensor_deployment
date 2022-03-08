# Meraki Sensor Deployment
An application using the Meraki APIs to deploy MT sensors in an organization, create alert profiles, and assign the alert profiles, a name, and a location to the sensors.

## Contacts
* Danielle Stacy

## Solution Components
* Python 3.9
* Meraki MT
* Meraki APIs

## Prerequisites
- **API Key**: In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:
1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.
> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization). 

> Note: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).

- **CSV files**: Prior to running this program, determine the sensors that need to be deployed, which networks they will be in, what alert profiles will be needed, who will be alerted for which alert profiles, and which sensors will need which alert profiles.
    - In the sensors.csv file, each line will give the information needed for each sensor. Provide the serial number of the sensor, the name you want to give the sensor, the organization where you are deploying the sensor, the network where you are deploying the sensor, and the address of the building where the sensor is located on each line, separated by commas and no spaces.
    - In the alert_profiles.csv file, each line will give the information needed for each alert profile. Provide the name of the alert profile, the temperature threshold (in Fahrenheit) at which you want to send an alert once the temperature goes about that threshold, the duration of time (in seconds) that the sensor should register above the threshold temperature before it sends an alert, and the network where you want the alert profile associated, separated by commas and no spaces. If you want the same alert profile in different networks, it will require two lines in the file where the only difference between the lines is the network name.
    - In the alert_recipients.csv file, each line will give the name of the alert profile, the name of the network that the alert profile is associated with, and the email address of someone who should receive an alert notification email. The alert profile name, network name, and email should all be separated by commas and no spaces. If an alert profile should have multiple alert recipients, each recipient needs their own line. In this case, the lines will have the same values except the email value.
    - In the sensors_to_profiles.csv file, each line will provide the name of the sensor, the serial name of the sensor, and the alert profile that should be associated with that sensor. Each sensor can be associated with multiple alert profiles. In this case, each alert profile association that the sensor has requires its own line where the lines will have the same values except for the alert_profile value.

## Installation/Configuration
1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_meraki_sensor_deployment` and open the directory.
2. Add Meraki environment variables to the env.py files
```python
API_KEY = "enter API key here"
org_name = "enter organization name here"
```
3. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
4. Install the requirements with `pip install -r requirements.txt`.
5. Before you run the program, make sure you add the information necessary to the CSV files listed in the Prerequisites section: sensors.csv, alert_profiles.csv, alert_recipients.csv, and sensors_to_profiles.csv.

## Usage
The functions that this program uses to interact with the Meraki APIs are located in meraki_functions.py.

To run the program, use the command:
```
$ python3 add_sensors.py
```

The code will print out messages when it successfully adds sensors and alert profiles to networks.

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

Output from running the code
![/IMAGES/output.png](/IMAGES/output.png)

Meraki sensors in dashboard after running the code
![/IMAGES/sensors.png](/IMAGES/sensors.png)

Meraki alert profiles in dashboard after running the code
![/IMAGES/alert_profiles.png](/IMAGES/alert_profiles.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
