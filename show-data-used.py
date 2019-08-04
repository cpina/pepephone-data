#!/usr/bin/env python3

import requests
import datetime
import calendar
import os
import configparser
import pathlib


def read_configuration_authentication():
    config_home = os.path.join(str(pathlib.Path.home()), ".pepephone")
    config_system = os.path.join("/etc", "pepephone")

    config = configparser.ConfigParser()
    if os.path.isfile(config_home):
        config.read(config_home)
    else:
        config.read(config_system)

    return config["authentication"]


def get_authorization_code():
    """
    POST to https://services.pepephone.com/v1/auth with parameters:
    JSON with email, password and source: ECARE_WEB.
    Returns authorization code
    """

    authentication_data = read_configuration_authentication()
    print("Getting authorization code...")
    payload = {"email": authentication_data["email"], "password": authentication_data["password"], "source": "ECARE_WEB"}
    json_request = requests.post("https://services.pepephone.com/v1/auth", json=payload).json()
    return json_request["jwt"]


def get_consumption(authorization_code):
    """
    GET https://services.pepephone.com/v1/consumption/623040167, pass
    Authorization: Bearer and the Authorization code
    """
    print("Getting consumption...")
    headers = {"Authorization": "Bearer {}".format(authorization_code)}
    authentication = read_configuration_authentication()
    consumption = requests.get("https://services.pepephone.com/v1/consumption/{}".format(authentication["phone"])   , headers=headers)
    return consumption.json()


def calculate_total_data_gb(consumption_json):
    total = consumption_json["dataFlat"]

    if "bundles" in consumption_json:
        for bundle in consumption_json["bundles"]:
            total += bundle["data"]

    return total / 1024

def main():
    if 'REQUEST_METHOD' in os.environ:
        print("Content-Type: text/plain\n")

    authorization_code = get_authorization_code()
    consumption_json = get_consumption(authorization_code)

    print()
    dataConsumeAllGb = (consumption_json["dataConsumeAll"] + consumption_json["dataConsumeRoamingRlah"]) / 1024
    dataConsumeEuGb = consumption_json["dataConsumeRoamingRlah"] / 1024
    dataTotalAvailableGb = calculate_total_data_gb(consumption_json)

    print("Time         : {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("GB total     : {:.2f} GB".format(dataTotalAvailableGb))
    print("GB used total: {:.2f} GB (EU roaming: {:.2f} GB)".format(dataConsumeAllGb, dataConsumeEuGb))
    print("GB remaining : {:.2f} GB".format(dataTotalAvailableGb-dataConsumeAllGb))
    print()

    percentage_used = (dataConsumeAllGb / dataTotalAvailableGb) * 100
    print("% Used       : {:.2f}%".format(percentage_used))

    now = datetime.datetime.now()
    number_of_days_month = calendar.monthrange(now.year, now.month)[1]

    percentage_month = (now.day / number_of_days_month) * 100
    print("% Month      : {:.2f}%".format(percentage_month))


if __name__ == "__main__":
    main()
