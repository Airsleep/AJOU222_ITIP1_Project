from collections import UserList
import requests
import time
import json
import pandas as pd
from xmlrpc.client import MAXINT
from bs4 import BeautifulSoup

MX_RANKING_PAGE = MAXINT

ranking_page_cnt = 1
ranking_base_url = 'https://www.acmicpc.net/ranklist/'

user_list = dict()

isEnd = False
while isEnd != True:
    response = requests.get(ranking_base_url + str(ranking_page_cnt))
    # if ranking_page_cnt == 2:
    #     break
    if response.ok == False:
        isEnd = True
        MX_RANKING_PAGE = ranking_page_cnt
    else:
        ranking_page_cnt += 1
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ranking_div = soup.find("div", {"class": "table-responsive"})
        ranking_table = ranking_div.find("table", {"id": "ranklist"})
        ranking_tbody = ranking_table.find("tbody")
        ranking_tr = ranking_tbody.find_all("tr")
        for tr in ranking_tr:
            # get user rank
            one_user = tr.find_all("td")
            user_rank = one_user[0].text
            user_name = one_user[1].find("a").attrs["href"].split("/")
            # user_list.append({user_rank: user_name[2]})

            # get user's solved problem list
            user_base_url = 'https://www.acmicpc.net/user/'
            user_url = user_base_url + user_name[2]
            # print(user_url)
            user_response = requests.get(user_url)
            # print(user_response.ok)
            html_user = user_response.text
            soup_user = BeautifulSoup(html_user, 'html.parser')
            problem_container = soup_user.find(
                "div", {"class": "problem-list"})
            # print(problem_container)
            problems = problem_container.find_all("a")
            problem_list = []
            for p in problems:
                problem_list.append(p.text)

            user_list[user_rank] = [user_rank, user_name[2], problem_list]
            print(user_rank)
idx = range(1, 6800)


def make_csv():
    # df = pd.DataFrame({"USER_RANK": idx,
    #                    "USER_NAME": user_list[1],
    #                    "USER_SOLVED_PROBLEM": user_list[2]})
    df = pd.DataFrame.from_dict(user_list, orient='index').rename(
        columns={0: 'USER_RANK', 1: 'USER_NAME', 2: 'USER_SOLVED_PROBLEM'})
    df.to_csv("user_rank_name_problem.csv", index=False, encoding="utf8")
    # break


make_csv()
# print(user_list)
# print(url+str(MX_RANKING_PAGE))
# print(response.ok)
