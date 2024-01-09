import requests


def get_random_user():
    """
    Fetches a random user from the randomuser.me API.

    :return: A dictionary containing the user details.
    """
    api_url = "https://randomuser.me/api"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        user_data = response.json()["results"][0]

        del user_data["dob"]
        del user_data["registered"]
        del user_data["id"]

        return user_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching random user: {e}")
        return None




