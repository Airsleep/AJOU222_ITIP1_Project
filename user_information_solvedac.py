from xml.dom.minidom import TypeInfo
import requests
import time
import json
import numpy as np
import pandas as pd
from xmlrpc.client import MAXINT
from bs4 import BeautifulSoup

MX_RANKING_PAGE = MAXINT

ranking_page_cnt = 2
ranking_base_url = "https://solved.ac/ranking/tier?page="

user_list = dict()
error_page = []

isEnd = False
while isEnd != True:
    response = requests.get(ranking_base_url + str(ranking_page_cnt))
    if ranking_page_cnt == 1550:
        break
    else:
        print("current page: " + str(ranking_page_cnt))

    if response.ok == False:
        error_page.append(ranking_page_cnt)
        ranking_page_cnt += 1
    else:
        # try:
        #     ranking_page_cnt += 1
        #     response = requests.get(ranking_base_url + str(ranking_page_cnt))
        #     html = response.text
        #     # html_file = open('html_file.html', 'w')
        #     # html_file.write(html)
        #     # html_file.close()
        #     soup = BeautifulSoup(html, "html.parser")
        #     ranking_tbody = soup.find("tbody")

        #     # user ranking numbers: int
        #     # user name : str
        #     # user rating : int
        #     user_rankings = []
        #     user_names = []
        #     user_ratings = []
        #     ranking_trs_table = ranking_tbody.select("tr > td b")

        #     # to split info
        #     block_size = 3
        #     ranking_table_container_temp = []
        #     for t in ranking_trs_table:
        #         ranking_table_container_temp.append(t.get_text())

        #     ranking_table_container_len = len(ranking_table_container_temp)
        #     for i in range(0, ranking_table_container_len, block_size):
        #         one_user_container = list(
        #             ranking_table_container_temp[i:i+block_size])
        #         user_rankings.append(one_user_container[0])
        #         user_names.append(one_user_container[1])
        #         user_ratings.append(one_user_container[2])

        #     # print(ranking_table_container_temp)
        #     # print("len", str(ranking_table_container_len))

        #     # get user's solved problem list
        #     iter_problem = int(ranking_table_container_len/block_size)
        #     # print(iter_problem)
        #     for i in range(0, iter_problem):
        #         user_base_url = "https://www.acmicpc.net/user/"
        #         user_url = user_base_url + user_names[i]

        #         # print(user_url)

        #         user_response = requests.get(user_url)

        #         # print(user_response.ok)

        #         html_user = user_response.text
        #         soup_user = BeautifulSoup(html_user, "html.parser")
        #         problem_container = soup_user.find(
        #             "div", {"class": "problem-list"})

        #         # print(problem_container)

        #         problems = problem_container.find_all("a")
        #         problem_list = []
        #         for p in problems:
        #             problem_list.append(p.text)
        #         user_list[user_rankings[i]] = [user_rankings[i],
        #                                        user_names[i], user_ratings[i], problem_list]
        #         # print(user_rankings[i])
        #         print(i)
        # except Exception as e:
        #     print(e.with_traceback)
        #     error_page.append(ranking_page_cnt)

        ranking_page_cnt += 1
        response = requests.get(ranking_base_url + str(ranking_page_cnt))
        html = response.text
        # html_file = open('html_file.html', 'w')
        # html_file.write(html)
        # html_file.close()
        soup = BeautifulSoup(html, "html.parser")
        ranking_tbody = soup.find("tbody")

        # user ranking numbers: int
        # user name : str
        # user rating : int
        user_rankings = []
        user_names = []
        user_ratings = []
        ranking_trs_table = ranking_tbody.select("tr > td")

        # to split info
        block_size = 3
        ranking_table_container_temp = []
        for t in ranking_trs_table:
            ranking_table_container_temp.append(t.get_text())
        print(ranking_table_container_temp)
        ranking_table_container_len = len(ranking_table_container_temp)
        print(ranking_table_container_len)
        for i in range(0, ranking_table_container_len, block_size):
            one_user_container = list(
                ranking_table_container_temp[i:i+block_size])
            user_rankings.append(one_user_container[0])
            user_names.append(one_user_container[1])
            user_ratings.append(one_user_container[2])

        # print(ranking_table_container_temp)
        # print("len", str(ranking_table_container_len))

        # get user's solved problem list
        iter_problem = int(ranking_table_container_len/block_size)
        # print(iter_problem)
        for i in range(0, iter_problem):
            user_base_url = "https://www.acmicpc.net/user/"
            user_url = user_base_url + user_names[i]

            # print(user_url)

            user_response = requests.get(user_url)

            # print(user_response.ok)

            html_user = user_response.text
            soup_user = BeautifulSoup(html_user, "html.parser")
            problem_container = soup_user.find(
                "div", {"class": "problem-list"})

            # print(problem_container)

            problems = problem_container.find_all("a")
            problem_list = []
            for p in problems:
                problem_list.append(p.text)
            user_list[user_rankings[i]] = [user_rankings[i],
                                           user_names[i], user_ratings[i], problem_list]
            print(user_rankings[i])

    # if ranking_page_cnt == 1:
    #     break


def make_csv():
    # df = pd.DataFrame({"USER_RANK": idx,
    #                    "USER_NAME": user_list[1],
    #                    "USER_SOLVED_PROBLEM": user_list[2]})
    df = pd.DataFrame.from_dict(user_list, orient="index").rename(
        columns={0: "USER_RANK", 1: "USER_NAME",
                 2: "ACRATING", 3: "USER_SOLVED_PROBLEM"}
    )
    df.to_csv("user_info_solvedac.csv", index=False, encoding="utf8")


make_csv()
print(error_page)
