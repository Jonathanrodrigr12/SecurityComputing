import requests
import os
import json

class RequestApi():

    @staticmethod 
    def get_region(code_iso="ARG"):
        """ Get configuration map """
        url = "https://restcountries.eu/rest/v2/alpha/"+code_iso
        response = requests.request("GET", url)
        return response.text

    @staticmethod 
    def get_ip_aws():
        """ Get configuration map """
        url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
        response = requests.request("GET", url)
        return response.text

    @staticmethod 
    def get_ip(ip):
        """ Get configuration map """
        url = "https://api.ip2country.info/ip?" + ip
        response = requests.request("GET", url)
        return json.loads(response.text) if response.status_code != 400 else None