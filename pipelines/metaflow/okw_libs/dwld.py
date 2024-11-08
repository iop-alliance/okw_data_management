#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 03:55:14 2024

@author: kny5
"""

import requests
from time import sleep
import logging
import functools



def retry_on_exception(max_retries=3, backoff_factor=1):
    """
    Decorator to retry a function on exception.

    Args:
        max_retries:
        backoff_factor:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)  # Execute and return the function result
                except requests.exceptions.RequestException as e:
                    if retries < max_retries:
                        sleep(backoff_factor * (retries + 1))
                        retries += 1
                    else:
                        raise e

        return wrapper

    return decorator


def req_data(url, timer=1, verbose=False, head={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'}):
    """
    Sends a GET request to the specified URL and returns the response.

    Args:
        url:
        timer:
        recursive:
        verbose:
    """
    @retry_on_exception(max_retries=5, backoff_factor=2)  # Increase max retries and backoff factor
    def inner():
        response = requests.get(url, headers=head)
        if response.status_code == 200:
            sleep(timer)
            if verbose:
                logging.info(f"URL: {url}")
                logging.info(f"Status Code: {response.status_code}")
            return response
        else:
            logging.error(f"Error Response: {response.status_code} ({url})")
            raise Exception("Request failed")

    return inner()  # Directly return the response



def iter_request(url):
    data = []
    x = 0
    
    while True:
        response = requests.get(url.format(n=x))
        json_data = response.json()
        if not json_data:
            break
        data += json_data
        x += 1
        print('Pages: {p}'.format(p=x))
        print('Entries: {e}'.format(e=len(data)))
    return data