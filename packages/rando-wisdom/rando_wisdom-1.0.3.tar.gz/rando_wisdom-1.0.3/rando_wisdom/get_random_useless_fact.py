import requests

def get_random_useless_fact():
    api_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    response = requests.get(api_url)
    data = response.json()
    
    return data["text"] if "text" in data else None

