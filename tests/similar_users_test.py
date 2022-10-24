from binhex import REASONABLY_LARGE
from email import header
from random import betavariate
from unicodedata import name
import requests
import time
import json
import numpy as np
import pandas as pd
import csv
from bs4 import BeautifulSoup

input_user = dict()
# 1등
# input_user["name"] = "koosaga"
# 2201등
# input_user["name"] = "idiot"
# 2400등
# input_user["name"] = "kangjoseph90"
# 2399등
input_user["name"] = "ksw888"
# 2395등
# input_user["name"] = "hoyyang22"


SIMILAR_BOUNDARY = 5
similar_users = dict()
ranking_page_cnt = 0
ranking_base_url = "https://www.acmicpc.net/ranklist/"
user_profile_base_url = "https://www.acmicpc.net/user/"

f_problem_list = open('')


# 원하는 사용자의 해결한 문제 수에 따른 비슷한 사용자 구하기. 위 아래로 10명
def get_similar_user_list(input_user_name):
    is_less_or_more = [False, False]
    similar_user_names = []
    # 해결한 문제 수에 따른 유저의 랭킹 : user_solved_count
    user_solved_count = int(input_user["ratingBySolvedCount"]) - 1
    input_user_ranking_page = str((user_solved_count)//100 + 1)
    input_user_ranking_url = ranking_base_url + input_user_ranking_page
    input_user_ranking_page_back = str(int(input_user_ranking_page) - 1)
    input_user_ranking_page_front = str(int(input_user_ranking_page) + 1)
    input_user_ranking_page_less_cnt = (
        user_solved_count % 100) - SIMILAR_BOUNDARY
    input_user_ranking_page_over_cnt = (
        user_solved_count % 100) + SIMILAR_BOUNDARY
    input_user_page_bound_lower = (user_solved_count % 100) - SIMILAR_BOUNDARY
    input_user_page_bound_upper = (user_solved_count % 100) + SIMILAR_BOUNDARY

    # 만약 유저가 전체 해결한 문제 수에 따른 사용자 랭킹의 10위 이내의 경우
    # if user_solved_count < 10:
    #     print("You are in top 10, there is no recommendation.")

    # 만약 유저의 page에 유저보다 랭킹이 높은 사용자가 5명보다 작을 경우, 이전 페이지에서 사용자들의 이름을 가져와야 함
    if input_user_ranking_page_less_cnt < 0:
        input_user_page_bound_lower = user_solved_count % 100
        iter_for_less = 99 - abs(input_user_ranking_page_less_cnt)
        before_page_url = ranking_base_url + input_user_ranking_page_back
        before_page_response = requests.get(before_page_url)
        before_page_html = before_page_response.text
        before_page_soup = BeautifulSoup(before_page_html, "html.parser")
        before_page_table = before_page_soup.find("table", {"id": "ranklist"})
        before_page_tbody = before_page_table.find("tbody")
        before_page_tr = before_page_tbody.find_all("tr")
        # before_page_tr.reverse()
        before_page_users = []
        for t in range(99, iter_for_less - 1, -1):
            one_user = before_page_tr[t].find_all("td")
            before_page_users.append(
                one_user[1].find("a").attrs["href"].split("/")[2])
        for t in before_page_users:
            similar_user_names.append(t)
        # print(before_page_users)

    # 89 90 91 92 93 /94/ 95 96 97 98 99
    # 만약 유저의 page에 유저보다 랭킹이 낮은 사용자가 5명보다 작을 경우, 다음 페이지에서 사용자들의 이름을 가져와야 함
    if input_user_ranking_page_over_cnt > 99:
        input_user_page_bound_upper = user_solved_count % 100
        iter_for_more = input_user_ranking_page_over_cnt - 99
        next_page_url = ranking_base_url + input_user_ranking_page_front
        next_page_response = requests.get(next_page_url)
        next_page_html = next_page_response.text
        next_page_soup = BeautifulSoup(next_page_html, "html.parser")
        next_page_table = next_page_soup.find("table", {"id": "ranklist"})
        next_page_tbody = next_page_table.find("tbody")
        next_page_tr = next_page_tbody.find_all("tr")
        # before_page_tr.reverse()
        next_page_users = []
        for t in range(0, iter_for_more):
            one_user = next_page_tr[t].find_all("td")
            next_page_users.append(
                one_user[1].find("a").attrs["href"].split("/")[2])
        for t in next_page_users:
            similar_user_names.append(t)
        # print(next_page_users)

    current_page_url = input_user_ranking_url
    current_page_response = requests.get(current_page_url)
    current_page_html = current_page_response.text
    current_page_soup = BeautifulSoup(current_page_html, "html.parser")
    current_page_table = current_page_soup.find("table", {"id": "ranklist"})
    current_page_tbody = current_page_table.find("tbody")
    current_page_tr = current_page_tbody.find_all("tr")

    print(input_user_page_bound_lower)
    print(input_user_page_bound_upper)
    for i in range(input_user_page_bound_lower, input_user_page_bound_upper + 1):
        if i == user_solved_count % 100:
            continue
        one_user = current_page_tr[i].find_all("td")
        similar_user_names.append(one_user[1].find(
            "a").attrs["href"].split("/")[2])

    print(similar_user_names)

    print("*"*20)
    print(user_solved_count)
    print(input_user_ranking_page)
    print(input_user_ranking_page_less_cnt)
    print(input_user_ranking_page_over_cnt)


# 원하는 사용자의 해결한 문제 수에 따른 백준 순위 구하기
def get_user_ranking_by_solved_problem(temp_user_name) -> int:
    temp_user_url = user_profile_base_url + str(temp_user_name)
    temp_user_response = requests.get(temp_user_url)
    temp_user_html = temp_user_response.text
    temp_user_soup = BeautifulSoup(temp_user_html, "html.parser")
    temp_user_statics_container = temp_user_soup.find(
        "table", {"id": "statics"})
    temp_user_statics = temp_user_statics_container.find_all("td")
    return int(temp_user_statics[0].text)


# 원하는 사용자의 정보 구하기
def get_input_user_info(input_user_name):
    input_user_url = "https://solved.ac/api/v3/user/show"
    query_string = {"query": " ", "handle": f"{input_user_name}"}
    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "GET", input_user_url, headers=headers, params=query_string)

    input_user_json = json.loads(response.text)
    input_user["rating"] = input_user_json.get("rating")
    # input_user["ratingBySolvedCount"] = input_user_json.get(
    #     "ratingBySolvedCount")
    input_user["ratingBySolvedCount"] = get_user_ranking_by_solved_problem(
        input_user_name)
    # print(input_user["rating"])
    # print(input_user["solvedCount"])


def main():
    get_input_user_info(input_user["name"])
    get_similar_user_list(input_user["name"])
    return


if __name__ == '__main__':
    main()
