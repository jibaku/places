# -*- coding: utf-8 -*-
""" Utils functions for places app """

import base64
import hashlib
import hmac
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def sign_googleapi_url(input_url, secret):
    """ Sign a request URL with a URL signing secret.
    Usage:
    from places.utils import sign_googleapi_url
    signed_url = sign_googleapi_url(input_url=my_url, secret=SECRET)
    Args:
    input_url - The URL to sign
    secret    - Your URL signing secret
    Returns:
    The signed request URL
    """
    input_url = input_url.encode('utf-8')
    url = urlparse(input_url)

    # We only need to sign the path+query part of the string
    url_to_sign = url.path + b"?" + url.query

    # Decode the private key into its binary format
    # We need to decode the URL-encoded private key
    decoded_key = base64.urlsafe_b64decode(secret)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decoded_key, url_to_sign, hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encoded_signature = base64.urlsafe_b64encode(signature.digest())

    original_url = url.scheme + b"://" + url.netloc + url.path + b"?" + url.query

    # Return signed URL
    return original_url + b"&signature=" + encoded_signature
