import requests

def get_advice():
    """
    Fetches random advice from the adviceslip.com API.

    :return: A dictionary containing the advice details.
    """
    api_url = "https://api.adviceslip.com/advice"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        advice_data = response.json()

        return advice_data['slip']

    except requests.exceptions.RequestException as e:
        print(f"Error fetching advice: {e}")
        return None

# random_advice = get_advice()

# if random_advice:
#     print("Random Advice:")
#     print(f"ID: {random_advice['id']}")
#     print(f"Advice: {random_advice['advice']}")
# else:
#     print("Failed to retrieve advice.")
