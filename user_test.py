# import requests
# import time
# import json
# import pandas as pd

# url = "https://solved.ac/api/v3/search/user/show"
# querystring = {"query": " ", "page": f"{page}"}
# headers = {"Content-Type": "application/json"}
# response = requests.request(
#     "GET", url, headers=headers, params=querystring)
# print(response.ok)

import requests
from bs4 import BeautifulSoup

url = 'https://www.acmicpc.net/user/koosaga'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    problem_container = soup.find("div", {"class": "problem-list"})
    problems = problem_container.find_all("a")
    problem_list = []
    for p in problems:
        problem_list.append(p.text)
    print(problem_list)

else:
    print(response.status_code)
