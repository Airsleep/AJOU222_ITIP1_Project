# solved.ac에서 직접 사용자의 정보에 대하여 crawling 불가능
from xml.dom.minidom import TypeInfo
import requests
import time
import json
import numpy as np
import pandas as pd
from xmlrpc.client import MAXINT
from bs4 import BeautifulSoup

MX_RANKING_PAGE = MAXINT

ranking_page_cnt = 0
ranking_base_url = "https://solved.ac/ranking/tier?page="

user_list = dict()
error_page = []

user_profile_base_url = "https://solved.ac/profile/"
user_name = "koosaga"
user_profile_url = user_profile_base_url + user_name

print(user_profile_url)
user_profile_response = requests.get(user_profile_url)
html_user_profile = user_profile_response.text
soup_user_profile = BeautifulSoup(html_user_profile, "html.parser")
user_profile_container = soup_user_profile.find("body")
print(user_profile_container)
top_problem_container = user_profile_container.select(
    "div.css-1948bce")
# print(top_problem_container)
# isEnd = False
# while isEnd != True:
#     print("current page: " + str(ranking_page_cnt))
#     response = requests.get(ranking_base_url + str(ranking_page_cnt))
#     if response.ok == False:
#         error_page.append(ranking_page_cnt)
#         ranking_page_cnt += 1
#     else:
#         try:
#             ranking_page_cnt += 1
#             response = requests.get(ranking_base_url + str(ranking_page_cnt))
#             html = response.text
#             soup = BeautifulSoup(html, "html.parser")
#             ranking_tbody = soup.find("tbody")

#             # user ranking numbers: int
#             # user name : str
#             # user rating : int
#             user_rankings = []
#             user_names = []
#             user_ratings = []
#             ranking_trs_table = ranking_tbody.select("tr > td b")

#             # to split info
#             block_size = 3
#             ranking_table_container_temp = []
#             for t in ranking_trs_table:
#                 ranking_table_container_temp.append(t.get_text())

#             ranking_table_container_len = len(ranking_table_container_temp)
#             for i in range(0, ranking_table_container_len, block_size):
#                 one_user_container = list(
#                     ranking_table_container_temp[i:i+block_size])
#                 user_rankings.append(one_user_container[0])
#                 user_names.append(one_user_container[1])
#                 user_ratings.append(one_user_container[2])

#             # print(ranking_table_container_temp)

#             # get user's solved problem list
#             for i in range(0, ranking_table_container_len):
#                 user_base_url = "https://www.acmicpc.net/user/"
#                 user_url = user_base_url + user_names[i]

#                 # print(user_url)

#                 user_response = requests.get(user_url)

#                 # print(user_response.ok)

#                 html_user = user_response.text
#                 soup_user = BeautifulSoup(html_user, "html.parser")
#                 problem_container = soup_user.find(
#                     "div", {"class": "problem-list"})

#                 # print(problem_container)

#                 problems = problem_container.find_all("a")
#                 problem_list = []
#                 for p in problems:
#                     problem_list.append(p.text)
#                 user_list[user_rankings[i]] = [user_rankings[i],
#                                                user_names[i], user_ratings[i], problem_list]
#                 print(user_rankings[i])
#         except:
#             error_page.append(ranking_page_cnt)

#     if ranking_page_cnt == 1:
#         break


# def make_csv():
#     # df = pd.DataFrame({"USER_RANK": idx,
#     #                    "USER_NAME": user_list[1],
#     #                    "USER_SOLVED_PROBLEM": user_list[2]})
#     df = pd.DataFrame.from_dict(user_list, orient="index").rename(
#         columns={0: "USER_RANK", 1: "USER_NAME",
#                  2: "ACRATING", 3: "USER_TOP_100_SOLVED_PROBLEM", 4: "USER_SOLVED_PROBLEM"}
#     )
#     df.to_csv("user_top_100_problems.csv", index=False, encoding="utf8")


# make_csv()
# print(error_page)
