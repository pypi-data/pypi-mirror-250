import requests


class InvalidAmountError(Exception):
    def __init__(self, amount):
        super().__init__(
            f"Invalid amount of jokes requested: {amount}. Maximum allowed is 10. Minimum allowed is 1."
        )


def get_random_joke(type="single", amount=1, aboutProgramming=False):
    if amount > 10 or amount < 1:
        raise InvalidAmountError(amount)

    api_url = "https://v2.jokeapi.dev/joke/"
    api_url += "Programming" if aboutProgramming else "Any"
    api_url += f"?type={type}" if type == "twopart" else "?type=single"
    api_url += f"&amount={amount}" if amount > 1 else ""

    response = requests.get(api_url)
    data = response.json()

    if amount == 1:
        if type == "twopart":
            return {
                "error": data["error"],
                "category": data["category"],
                "type": data["type"],
                "setup": data["setup"],
                "delivery": data["delivery"],
            }
        else:
            return {
                "error": data["error"],
                "category": data["category"],
                "type": data["type"],
                "joke": data["joke"],
            }
    else:
        jokes = []
        for joke in data["jokes"]:
            if type == "twopart":
                jokes.append(
                    {
                        "category": joke["category"],
                        "type": joke["type"],
                        "setup": joke["setup"],
                        "delivery": joke["delivery"],
                    }
                )
            else:
                jokes.append(
                    {
                        "category": joke["category"],
                        "type": joke["type"],
                        "joke": joke["joke"],
                    }
                )

        return {"error": data["error"], "amount": data["amount"], "jokes": jokes}


def print_jokes(jokes):
    if "error" in jokes and not jokes["error"]:
        if "amount" in jokes:
            print(f"Amount: {jokes['amount']}")
            for idx, joke in enumerate(jokes["jokes"], start=1):
                if joke["type"] == "twopart":
                    print(f"Joke {idx} - {joke['setup']} {joke['delivery']}")
                else:
                    print(f"Joke {idx} - {joke['joke']}")
        else:
            print(f"Category: {jokes['category']}")
            if jokes["type"] == "twopart":
                print(f"Jackson: {jokes['setup']}")
                print(f"Olivia: {jokes['delivery']}")
            else:
                print(f"Joke: {jokes['joke']}")
    else:
        print(f"Error: {jokes['error']}")

