# CNOunlimited/token_grabber.py

import requests
from datetime import datetime
import json

def simple_token(username, password, content_type, post_url, verify=True):
    """
    Get an access token using provided credentials.

    Parameters:
    - username (str): The username for authentication.
    - password (str): The password for authentication.
    - content_type (str): The content type for the request headers.
    - post_url (str): The URL for the token endpoint.
    - verify (bool): Optional. Whether to verify SSL/TLS certificates. Defaults to True.

    Returns:
    - str: The access token.
    """
    client_id = f'grant_type=password&username={username}&password={password}&client_id=custom'

    try:
        response = requests.post(post_url, headers={'Content-Type': content_type}, data=client_id, verify=verify)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx status codes)
        return response.json()['access_token']
    except requests.RequestException as e:
        # Handle exceptions (network errors, bad responses, etc.)
        print(f"Error during token retrieval: {e}")
        return None


def complex_token(token_url, client_id, client_secret, verify=True):
    """
    Perform a more complex API call, including obtaining the access token using client credentials.

    Parameters:
    - api_url (str): The URL for the more complex API call.
    - client_id (str): The client ID for obtaining the access token.
    - client_secret (str): The client secret for obtaining the access token.
    - verify (bool): Optional. Whether to verify SSL/TLS certificates. Defaults to True.

    Returns:
    - dict: The JSON response from the API call.
    """
    # Obtain access token using client credentials
    token_headers = {'accept': 'application/json', 'content-type': 'application/json'}
    token_data = {
        'grant_type': 'client_credentials',
        'scope': 'read',
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        token_response = requests.post(token_url, headers=token_headers, data=json.dumps(token_data), verify=verify)
        token_response.raise_for_status()
        access_token = token_response.json()['access_token']
        return access_token
    except requests.RequestException as e:
        print(f"Error obtaining access token: {e}")
        return None

