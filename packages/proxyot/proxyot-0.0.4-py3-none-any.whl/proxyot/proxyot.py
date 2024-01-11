import requests
import json


class Client():
    """Creates a client for ProxyOT to access the values of your points and lists."""

    def __init__(self, sk):
        self.server = 'https://api.proxyot.com/'
        self.sk = sk
    def write_point(self, path, value):
        """Write a value to an existing point"""
        p = requests.post(
            f'{self.server}write_point', data={'path': path, 'sk': self.sk, 'value':value})
        j = json.loads(p.text)
        if j['error']:
            raise Exception(j['error'])
        else:
            return value
    def get_point(self, path):
        """Return the current value of a point."""
        p = requests.post(
            f'{self.server}get_point', data={'path': path, 'sk': self.sk})
        j = json.loads(p.text)
        if j['error']:
            raise Exception(j['error'])
        else:
            return j['value']

    def get_list(self, list_name):
        """Returns a list of strings that represent the values of the points in the list."""
        r = requests.post(
            f'{self.server}get_list', data={'name': list_name, 'sk': self.sk})
        j = json.loads(r.text)
        if j['error']:
            raise Exception(j['error'])
        else:
            return j['points']
