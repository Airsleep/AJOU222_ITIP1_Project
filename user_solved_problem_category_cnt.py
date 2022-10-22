from cgitb import html
from random import betavariate
import requests
import time
import json
import pandas as pd
import csv
import re
from bs4 import BeautifulSoup

user = 'gnaroshi'
user_base_url = "https://www.acmicpc.net/user/"

'''
make_boj_problems_info:
백준에 존재하는 문제들의 정보를 구함
전체 문제: boj_problems, dict(문제번호: 문제해시, 문제제목, 문제레벨, 문제태그)
전체 문제 태그: boj_problem_category, set(strings), 190개 존재
'''
boj_problems = dict()
boj_problem_category = set()
user_solved_category_cnts = dict()


def make_boj_problems_info():
    boj_problem_list_f = open(
        'practice/project/problem_list.csv', 'r', encoding='utf-8')
    boj_problem_list_reader = csv.reader(boj_problem_list_f)
    for line in boj_problem_list_reader:
        if line[0] == "PROBLEM_ID":
            continue
        boj_problems[int(line[0])] = [line[1], line[2], line[3], line[4]]
        # 리스트 형태의 문자열을 리스트로 변환
        problem_tags = line[4].lstrip("[").rstrip("]")
        problem_tags = re.sub("'", "", problem_tags)
        problem_tags = re.sub('"', "", problem_tags)
        problem_tags = re.sub(", ", "/", problem_tags).split('/')
        for tag in problem_tags:
            boj_problem_category.add(tag)
    # 공백 제거
    boj_problem_category.discard("")
    # for p in boj_problem_category:
    #     print(p)
    # print(len(boj_problem_category))
    boj_problem_list_f.close()


def crawl_user_solved_problems(user):
    one_user_url = user_base_url + str(user)
    one_user_response = requests.get(one_user_url)
    one_html_user = one_user_response.text
    one_soup_user = BeautifulSoup(one_html_user, "html.parser")
    one_problem_container = one_soup_user.find(
        "div", {"class": "problem-list"})
    one_problems = one_problem_container.find_all("a")
    one_problem_list = []
    for op in one_problems:
        one_problem_list.append(int(op.text))
    one_user_tags_cnt = dict()
    for tag in boj_problem_category:
        one_user_tags_cnt[tag] = 0
    # print(boj_problems)
    for p in one_problem_list:
        # print(p)
        try:
            pt = boj_problems[p][3]
            # print(pt)
        #     for t in boj_problems[p][3]:
        #         one_user_tags_cnt[t] += 1
        except:
            pass

    # print(one_user_tags_cnt)


def crawl(user):
    user_url = "https://solved.ac/api/v3/user/show"
    query_string = {"query": " ", "handle": f"{user}"}

    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "GET", user_url, headers=headers, params=query_string)

    user_json = json.loads(response.text)
    user_rating = user_json.get("rating")
    # print(user_rating)


def main():
    make_boj_problems_info()
    crawl(user)
    crawl_user_solved_problems(user)


if __name__ == '__main__':
    main()
