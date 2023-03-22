"""
Functions for processing URLs
"""

from urllib.parse import urlsplit


def url_details(url: str):
    details = urlsplit(url)
    out = {"url": details.geturl()}
    if details.scheme != "":
        out["scheme"] = details.scheme
    if details.netloc != "":
        out["netloc"] = details.netloc
    if details.path != "":
        out["path"] = details.path
    if details.query != "":
        out["query"] = details.query
    if details.fragment != "":
        out["fragment"] = details.fragment
    if details.username is not None:
        out["username"] = details.username
    if details.password is not None:
        out["password"] = details.password
    if details.hostname is not None:
        out["hostname"] = details.hostname
    if details.port is not None:
        out["port"] = details.port
    return out
