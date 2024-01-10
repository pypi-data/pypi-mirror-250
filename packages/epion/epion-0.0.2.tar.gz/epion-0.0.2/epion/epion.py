import requests
import datetime as dt
from functools import wraps
import pytz
import numbers

__title__ = "epion"
__version__ = "0.0.2"
__author__ = "Leendert Gravendeel"
__license__ = "MIT"

BASEURL = 'https://api.epion.nl'

class Epion(object):
    """
    Object containing Epion API-methods.
    """
    def __init__(self, api_token):
        """
        To communicate with the Epion API, you need to have an API token for your account.
        Log in to your Epion account and request an API token from the Integrations page.

        Parameters
        ----------
        api_token : str
        """
        self.token = api_token

    def get_current(self):
        """
        Request current measurements from all devices in the linked account

        Returns
        -------
        dict
        """

        url = urljoin(BASEURL, "api", "current")

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'User-Agent': 'EpionPython/' + __version__
        }

        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        return r.json()


def urljoin(*parts):
    """
    Join terms together with forward slashes

    Parameters
    ----------
    parts

    Returns
    -------
    str
    """
    # first strip extra forward slashes (except http:// and the likes) and
    # create list
    part_list = []
    for part in parts:
        p = str(part)
        if p.endswith('//'):
            p = p[0:-1]
        else:
            p = p.strip('/')
        part_list.append(p)
    # join everything together
    url = '/'.join(part_list)
    return url