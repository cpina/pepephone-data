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


def main():
    if 'REQUEST_METHOD' in os.environ:
        print("Content-Type: text/plain\n")

    authorization_code = get_authorization_code()
    consumption_json = get_consumption(authorization_code)

    print()
    dataConsumeAllGb = consumption_json["dataConsumeAll"] / 1024
    dataTotalGb = consumption_json["dataFlat"] / 1024
    print("GB total    : {:.2f} GB".format(dataTotalGb))
    print("GB used     : {:.2f} GB".format(dataConsumeAllGb))
    print("GB remaining: {:.2f} GB".format(dataTotalGb-dataConsumeAllGb))
    print()

    percentage_used = (dataConsumeAllGb / 23) * 100
    print("% Used      : {:.2f}%".format(percentage_used))

    now = datetime.datetime.now()
    number_of_days_month = calendar.monthrange(now.year, now.month)[1]

    percentage_month = ((now.day-1) / number_of_days_month) * 100
    print("% Month     : {:.2f}%".format(percentage_month))


if __name__ == "__main__":
    main()
