import requests

def get_random_useless_fact():
    api_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    response = requests.get(api_url)
    data = response.json()
    
    return data["text"] if "text" in data else None

# Example usage:
# random_fact = get_random_useless_fact()
# if random_fact:
#     print(random_fact)
# else:
#     print("Failed to fetch a random useless fact.")
