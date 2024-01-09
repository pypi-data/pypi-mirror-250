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


# Example usage:
# random_user = get_random_user()

# if random_user:
#     print("Random User:")
#     print(
#         f"Name: {random_user['name']['title']} {random_user['name']['first']} {random_user['name']['last']}"
#     )
#     print(f"Gender: {random_user['gender']}")
#     print(
#         f"Location: {random_user['location']['city']}, {random_user['location']['state']}, {random_user['location']['country']}"
#     )
#     print(f"Email: {random_user['email']}")
#     print(f"Username: {random_user['login']['username']}")
#     print(f"Phone: {random_user['phone']}")
#     print(f"Cell: {random_user['cell']}")
#     print(f"Nationality: {random_user['nat']}")
#     print(f"Profile Picture: {random_user['picture']['large']}")

# else:
#     print("Failed to retrieve a random user.")
