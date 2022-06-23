"""
filename: utilities.py
last-updated: *in development
authors: Josh Schmitz

description:
    Basic utility functions used by api, cli, controller, etc.
"""

import pyqrcode
from PIL import Image

def get_api_key(name):
    api_keys = {}
    with open('api_keys.txt', 'r') as f:
        for line in f:
            k, v = line.strip().split('=')
            api_keys[k.strip()] = v.strip()
    return api_keys[name]

def generate_qr_code(link):
    url = pyqrcode.create(link)
    url.png('qr.png', scale=6)
