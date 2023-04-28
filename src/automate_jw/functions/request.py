"""
Fetch a file with requests
https://requests.readthedocs.io/en/latest/
"""

import requests

def get_content(url: string) -> str:
    resp = requests.get(url)
    return resp.text
