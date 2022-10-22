import requests
import time
import json
import pandas as pd

user = 'gnaroshi'


def crawl(user):
    user_url = "https://solved.ac/api/v3/user/show"
    query_string = {"query": " ", "handle": f"{user}"}

    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "GET", user_url, headers=headers, params=query_string)

    user_json = json.loads(response.text)
    user_rating = user_json.get("rating")
    print(user_rating)


def main():
    crawl(user)


if __name__ == '__main__':
    main()
