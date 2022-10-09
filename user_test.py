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

url = '가져올 웹사이트 주소'

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)

else:
    print(response.status_code)
