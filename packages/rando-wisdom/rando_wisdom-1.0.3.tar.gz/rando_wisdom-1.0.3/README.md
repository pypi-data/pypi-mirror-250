# Rando-wisdom (Creative library)

`Rando-wisdom` is a versatile Python library designed to inject a dose of variety and entertainment into your projects. This all-in-one library offers functionalities to generate random content, ensuring a delightful and engaging experience for users.
**Table of Contents:**

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
   - [1. Generates random advice](#1-generating-advice)
   - [2. Generates jokes](#2-generates-joke-or-jokes)
   - [3. Produces a quote](#3-produce-quote)
   - [4. Generates a useless fact](#4-generating-useless-fact)
   - [5. Generates full user info](#5-full-user-info-generating)
3. [License](#license)
4. [Author](#author)
5. [Links](#links)

## Installation

You can easily install `Rando-wisdom` using `pip`:

```shell
pip install rando-wisdom
```

## Basic Usage

### 1. Generating advice

Access a curated collection of inspiring and thought-provoking quotes to add wisdom and motivation to your applications.


#### Example:

```python
from rando_wisdom import get_advice

advice = get_advice()
print(advice['advice'])
#Example output: Once you find a really good friend don't do anything that could mess up your friendship.
```

### 2. Generates joke or jokes

Bring humor to your projects with a vast array of jokes covering various categories, guaranteed to bring a smile to users' faces.

#### Example:

```python
result = get_random_joke(type="twopart", amount=1, aboutProgramming=False)
print_jokes(result)

#Example output:
#Category: Pun
#Jackson: Why does the size of the snack not matter to a giraffe?
#Olivia: Because even a little bit goes a long way.


#or


result = get_random_joke(type="single", amount=2, aboutProgramming=True)
print_jokes(result)

#Example output:
#Amount: 2
#Joke 1 - Eight bytes walk into a bar.
#The bartender asks, "Can I get you anything?"
#"Yeah," reply the bytes.
#"Make us a double."
#Joke 2 - A byte walks into a bar looking miserable.
#The bartender asks it: "What's wrong buddy?"
#"Parity error." it replies. 
#"Ah that makes sense, I thought you looked a bit off."

```

### 3. Produce quote

`Rando-wisdom` can produce quote, here is example how to do it.

#### Example:

```python
from rando_wisdom import get_random_quote

tags = ["inspirational"]
max_length = 100

random_quote = get_random_quote(tags=tags, max_length=max_length)

if random_quote:
    print("Random Quote:")
    print(f"Author: {random_quote['author']}")
    print(f"Content: {random_quote['content']}")
    print(f"Tags: {random_quote['tags']}")
    print(f"Length: {random_quote['length']}")
    print(f"Date Added: {random_quote['dateAdded']}")
    print(f"Date Modified: {random_quote['dateModified']}")
else:
    print("Failed to retrieve a quote.")

#Example output:
#Random Quote:
#Author: Johann Wolfgang von Goethe
#Content: Knowing is not enough; we must apply!
#Tags: ['Famous Quotes', 'Inspirational']
#Length: 37
#Date Added: 2019-11-16
#Date Modified: 2023-04-14
```

### 4. Generating useless fact

Infuse curiosity with useless yet fascinating facts that spark interest and trivia enthusiasts.

#### Example:

```python
from rando_wisdom import get_random_useless_fact


random_fact = get_random_useless_fact()
if random_fact:
    print(random_fact)

#Example output: The most common name in world is Mohammed.
```

### 5. Full user info generating

Generate random user profiles with diverse attributes, ideal for testing or creating realistic mock scenarios in your applications.

#### Example:

```python
from rando_wisdom import get_random_user


random_user = get_random_user()

if random_user:
    print("Random User:")
    print(
        f"Name: {random_user['name']['title']} {random_user['name']['first']} {random_user['name']['last']}"
    )
    print(f"Gender: {random_user['gender']}")
    print(
        f"Location: {random_user['location']['city']}, {random_user['location']['state']}, {random_user['location']['country']}"
    )
    print(f"Email: {random_user['email']}")
    print(f"Username: {random_user['login']['username']}")
    print(f"Phone: {random_user['phone']}")
    print(f"Cell: {random_user['cell']}")
    print(f"Nationality: {random_user['nat']}")
    print(f"Profile Picture: {random_user['picture']['large']}")

else:
    print("Failed to retrieve a random user.")

#Example output:
#Random User:
# Name: Mr Dorian Fabre
# Gender: male
# Location: Brest, Deux-Sèvres, France
# Email: dorian.fabre@example.com
# Username: silverbutterfly775
# Phone: 01-30-10-45-31
# Cell: 06-48-58-91-52
# Nationality: FR
# Profile Picture: https://randomuser.me/api/portraits/men/21.jpg

```


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- [Imranqsl212](https://github.com/Imranqsl212)

## Links

- [GitHub repository](https://github.com/Imranqsl212/rando_wisdom)
- [Telegram](https://t.me/wh0s1mran)

Feel free and creative to explore and utilize the various features of `Random-wisdom` for your project needs.