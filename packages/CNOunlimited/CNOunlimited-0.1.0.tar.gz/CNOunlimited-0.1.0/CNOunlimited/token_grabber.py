# CNOunlimited/token_grabber.py

import requests

def get_access_token(username, password, content_type, post_url, verify=True):
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
