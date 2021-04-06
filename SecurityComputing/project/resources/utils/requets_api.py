import requests
import os
import json
from project.configuration_manager import ConfigurationManger

class RequestApi():

    @staticmethod 
    def get_key(key):
        """ Get configuration map """
        return ConfigurationManger.get_config(key)

    @staticmethod 
    def get_region(code_iso="ARG"):
        """ Get configuration map """
        url = RequestApi.get_key('KEY_REGION')+code_iso
        response = requests.request("GET", url)
        return response.text

    @staticmethod 
    def get_ip_aws():
        """ Get configuration map """
        url = RequestApi.get_key('KEY_IP_AWS')
        response = requests.request("GET", url)
        return response.text

    @staticmethod 
    def get_ip(ip):
        """ Get configuration map """
        url = RequestApi.get_key('KEY_INFO_IP') + ip
        response = requests.request("GET", url)
        return json.loads(response.text) if response.status_code != 400 else None