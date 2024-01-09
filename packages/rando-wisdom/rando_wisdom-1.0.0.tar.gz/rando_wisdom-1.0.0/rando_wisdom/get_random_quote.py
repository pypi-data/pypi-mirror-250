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


# Example usage:
# tags = ["inspirational"]
# max_length = 100

# random_quote = get_random_quote(tags=tags, max_length=max_length)

# if random_quote:
#     print("Random Quote:")
#     print(f"Author: {random_quote['author']}")
#     print(f"Content: {random_quote['content']}")
#     print(f"Tags: {random_quote['tags']}")
#     print(f"Length: {random_quote['length']}")
#     print(f"Date Added: {random_quote['dateAdded']}")
#     print(f"Date Modified: {random_quote['dateModified']}")
# else:
#     print("Failed to retrieve a quote.")
