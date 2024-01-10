import requests


def get_random_quote(tags=None, max_length=None):
    """
    Fetches a random quote from quotable.io API.

    :param tags: List of tags to filter quotes (optional).
    :param max_length: Maximum length of the quote (optional).
    :return: A dictionary containing the quote details.
    """
    base_url = "https://api.quotable.io/random"

    params = {}
    if tags:
        params["tags"] = ",".join(tags)
    if max_length:
        params["maxLength"] = max_length

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        quote_data = response.json()

        return quote_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote: {e}")
        return None



