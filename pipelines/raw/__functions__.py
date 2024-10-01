import requests
from time import sleep

def req_data(url, timer=1, recursive=False, verbose=False):
  
    response = requests.get(url)

    if response.status_code == 200:
        sleep(timer)
        if verbose:
            print(url)
            print(response.status_code)
        return response
    else:
        print("'" * 5)
        print(response.status_code, url)
        print('Error response: Check URL or internet availability, and Try again.')
        if recursive:
            return req_data(url, timer=5, recursive=True)
        else:
            return None