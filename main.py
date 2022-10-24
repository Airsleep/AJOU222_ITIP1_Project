from binhex import REASONABLY_LARGE
from cmath import sqrt
from email import header
from random import betavariate
from tkinter.simpledialog import SimpleDialog
from unicodedata import name
import requests
import time
import json
import numpy as np
import pandas as pd
import csv
import re
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth
from zss import simple_distance, Node
from bs4 import BeautifulSoup


def get_recommended_problem(input_target_user):
    target_user = dict()
    target_user_name = input_target_user
    error_users = list()

    SIMILAR_BOUNDARY = 20
    similar_users = dict()
    similar_user_list = list()
    ranking_page_cnt = 0
    ranking_base_url = "https://www.acmicpc.net/ranklist/"
    user_base_url = "https://www.acmicpc.net/user/"
    user_profile_base_url = "https://www.acmicpc.net/user/"

    # f_problem_list = open('practice/project/problem_list2.csv')

    '''
    -------------------------------------------------------------------------------
    make_boj_problems_info:
    백준에 존재하는 문제들의 정보를 구함
    전체 문제: boj_problems, dict(문제번호: 문제해시, 문제제목, 문제레벨, 문제태그)
    전체 문제 태그: boj_problem_tag, set(strings), 190개 존재
    '''
    boj_problems = dict()
    boj_problem_tag = set()
    similar_user_problem_tag = set()
    similar_user_problem_tag_list = list()
    user_solved_tag_cnts = dict()
    similar_user_solved_tag_cnts = dict()

    def make_boj_problems_info():
        boj_problem_list_f = open(
            'practice/project/problem_list.csv', 'r', encoding='utf-8')
        boj_problem_list_reader = csv.reader(boj_problem_list_f)
        for line in boj_problem_list_reader:
            if line[0] == "PROBLEM_ID":
                continue
            # 리스트 형태의 문자열을 리스트로 변환
            problem_tags = line[4].lstrip("[").rstrip("]")
            problem_tags = re.sub("'", "", problem_tags)
            problem_tags = re.sub('"', "", problem_tags)
            problem_tags = re.sub(", ", "/", problem_tags).split('/')
            for tag in problem_tags:
                boj_problem_tag.add(tag)
            boj_problems[int(line[0])] = [
                line[1], line[2], line[3], problem_tags]

        # 공백 제거
        boj_problem_tag.discard("")
        boj_problem_list_f.close()

    # 유저가 해결한 문제들의 tag별 cnt 반환
    # 유저가 해결한 문제 총 수의 10%보다 작은 문제들은 제외
    # input: user(str)
    # return: dict(tag(str):cnt(int))

    def crawl_user_solved_problems(user, cnt_threshold):
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
        # tag key 값 초기화
        for tag in boj_problem_tag:
            one_user_tags_cnt[tag] = 0

        return_solved_problem_list = []
        for p in one_problem_list:
            # 사라진 문제나 25880 이후의 문제가 있는 경우 예외처리
            try:
                pt = boj_problems[p][3]
                for t in pt:
                    one_user_tags_cnt[t] += 1
                if int(target_user["tier"]) - 3 < int(boj_problems[p][2]) and int(target_user["tier"]) + 3 > int(boj_problems[p][2]):
                    return_solved_problem_list.append(p)
            except:
                pass
        return_tags_cnt = dict()
        for k, v in one_user_tags_cnt.items():
            if v >= cnt_threshold:
                return_tags_cnt[k] = v

        if user == target_user_name:
            target_user["solved"] = return_solved_problem_list
        else:
            similar_users[user]["solved"] = return_solved_problem_list
        return return_tags_cnt

    # 원하는 사용자의 해결한 문제 수에 따른 비슷한 사용자 구하기. 위 아래로 10명
    # input: input_user_name(str)
    # list(name(strs),)

    def get_similar_user_list(input_user_name):
        similar_user_names = []
        # 해결한 문제 수에 따른 유저의 랭킹 : user_solved_count
        user_solved_count = int(input_user_name["ratingBySolvedCount"]) - 1
        input_user_ranking_page = str((user_solved_count)//100 + 1)
        input_user_ranking_url = ranking_base_url + input_user_ranking_page
        input_user_ranking_page_back = str(int(input_user_ranking_page) - 1)
        input_user_ranking_page_front = str(int(input_user_ranking_page) + 1)
        input_user_ranking_page_less_cnt = (
            user_solved_count % 100) - SIMILAR_BOUNDARY
        input_user_ranking_page_over_cnt = (
            user_solved_count % 100) + SIMILAR_BOUNDARY
        input_user_page_bound_lower = (
            user_solved_count % 100) - SIMILAR_BOUNDARY
        input_user_page_bound_upper = (
            user_solved_count % 100) + SIMILAR_BOUNDARY

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
            before_page_table = before_page_soup.find(
                "table", {"id": "ranklist"})
            before_page_tbody = before_page_table.find("tbody")
            before_page_tr = before_page_tbody.find_all("tr")
            before_page_users = []
            for t in range(99, iter_for_less - 1, -1):
                one_user = before_page_tr[t].find_all("td")
                before_page_users.append(
                    one_user[1].find("a").attrs["href"].split("/")[2])
            for t in before_page_users:
                similar_user_names.append(t)

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
            next_page_users = []
            for t in range(0, iter_for_more):
                one_user = next_page_tr[t].find_all("td")
                next_page_users.append(
                    one_user[1].find("a").attrs["href"].split("/")[2])
            for t in next_page_users:
                similar_user_names.append(t)

        # 현재 보고 있는 page의 유저 가져오기
        current_page_url = input_user_ranking_url
        current_page_response = requests.get(current_page_url)
        current_page_html = current_page_response.text
        current_page_soup = BeautifulSoup(current_page_html, "html.parser")
        current_page_table = current_page_soup.find(
            "table", {"id": "ranklist"})
        current_page_tbody = current_page_table.find("tbody")
        current_page_tr = current_page_tbody.find_all("tr")

        for i in range(input_user_page_bound_lower, input_user_page_bound_upper + 1):
            if i == user_solved_count % 100:
                continue
            one_user = current_page_tr[i].find_all("td")
            similar_user_names.append(one_user[1].find(
                "a").attrs["href"].split("/")[2])

        if target_user_name in similar_user_names:
            similar_user_names.remove(target_user_name)
            print("deleted")
        print(similar_user_names)

        return similar_user_names

    # 원하는 사용자의 해결한 문제 수에 따른 백준 순위 구하기
    # input: temp_user_name
    # return: ranking_by_solved_problem(int)

    def get_user_ranking_by_solved_problem(temp_user_name):
        temp_user_values = []
        temp_user_url = user_profile_base_url + str(temp_user_name)
        temp_user_response = requests.get(temp_user_url)
        temp_user_html = temp_user_response.text
        temp_user_soup = BeautifulSoup(temp_user_html, "html.parser")
        temp_user_statics_container = temp_user_soup.find(
            "table", {"id": "statics"})
        temp_user_statics = temp_user_statics_container.find_all("td")
        temp_user_statics_solved = temp_user_soup.find(
            "span", {"id": "u-solved"})
        temp_user_values.append(int(temp_user_statics[0].text))
        temp_user_values.append(int(temp_user_statics_solved.text))
        return temp_user_values

    # 원하는 사용자의 정보 구하기
    # input: temp_user_name(str)
    # return: dict(rating:int, tier:int, ratingBySolvedCount:int)

    def get_user_info(temp_user_name):
        return_info = dict()
        temp_user_url = "https://solved.ac/api/v3/user/show"
        query_string = {"query": " ", "handle": f"{temp_user_name}"}
        headers = {"Content-Type": "application/json"}
        response = requests.request(
            "GET", temp_user_url, headers=headers, params=query_string)
        if response.ok:
            temp_user_statics = get_user_ranking_by_solved_problem(
                temp_user_name)
            temp_user_json = json.loads(response.text)
            # return_info["solvedCount"] = int(temp_user_json.get("solvedCount"))
            return_info["solvedCount"] = temp_user_statics[1]
            return_info["rating"] = int(temp_user_json.get("rating"))
            return_info["tier"] = int(temp_user_json.get("tier"))
            return_info["ratingBySolvedCount"] = temp_user_statics[0]
        else:
            print(temp_user_name + " is not subscribed to solvedac..")
            error_users.append(temp_user_name)
        return return_info

    # similar_user의 tag set 구하기
    # similar_user_problem_tag에 tag들이 들어감

    def get_similar_user_tag_set():
        for su in similar_users:
            for t in similar_users[su]["tagscnt"]:
                similar_user_problem_tag.add(t)

    # column: tag, row: user
    # 1st row: target user, nth row: similar user

    def make_tag_table():
        tag_table = []
        tag_table.append(similar_user_problem_tag_list)
        target_user_solved_cnts = target_user["tagscnt"]
        tag_table.append([])
        for i in range(len(similar_user_problem_tag_list)):
            tag_table[1].append(0)

        for k, v in target_user_solved_cnts.items():
            try:
                tag_table[1][tag_table[0].index(k)] = v
            except:
                pass

        similar_user_idx = 2
        for su in similar_users:
            tag_table.append([])
            for i in range(len(similar_user_problem_tag_list)):
                tag_table[similar_user_idx].append(0)
            for k, v in similar_users[su]["tagscnt"].items():
                tag_table[similar_user_idx][tag_table[0].index(k)] = v
            similar_user_idx += 1
        # for u in tag_table:
        #     print(u)
        return tag_table

    def get_cos_sim(tag_table):
        cos_sim = []
        cos_sim_normalized = []
        target_user_row = tag_table[1]
        target_user_sum = 0
        for tc in target_user_row:
            target_user_sum += (tc**2)
        target_user_sum = sqrt(target_user_sum)
        for sr in tag_table[2:]:
            temp_similar_user_numerator = 0
            temp_similar_user_sum = 0
            for stc in sr:
                temp_similar_user_sum += (stc**2)
            for tc, stc in zip(target_user_row, sr):
                temp_similar_user_numerator += tc*stc
            temp_similar_user_sum = sqrt(temp_similar_user_sum)
            temp_cos_sim = temp_similar_user_numerator / \
                (target_user_sum + temp_similar_user_sum).real
            cos_sim.append(temp_cos_sim)

        # z-score normalization
        cos_sim_sum = 0
        cos_sim_avg = 0
        cos_sim_var = 0
        cos_sim_std = 0
        for cs in cos_sim:
            cos_sim_sum += cs
        cos_sim_avg = cos_sim_sum / len(cos_sim)
        for cs in cos_sim:
            cos_sim_var += (cs - cos_sim_avg)**2
        cos_sim_var = cos_sim_var / len(cos_sim)
        cos_sim_std = sqrt(cos_sim_var).real

        for cs in cos_sim:
            cos_sim_normalized.append(
                abs(round((cs - cos_sim_avg) / cos_sim_std, 2)))

        print("-"*20 + "COSINE SIMILILARITY" + "-" * 20)
        print(cos_sim_normalized)
        return cos_sim_normalized

    def get_tree_sim(tag_col, tag_table):
        tags_len = len(tag_col)
        tree_sim = []
        mat_with_tags = []
        mat_with_tags_idx = 0
        for row in tag_table:
            # row init
            mat_with_tags.append([])
            for i in range(tags_len):
                mat_with_tags[mat_with_tags_idx].append(0)
            row_idx = 0
            for row_elem in row:
                mat_with_tags[mat_with_tags_idx][row_idx] = [
                    row_elem, tag_col[row_idx]]
                row_idx += 1
            mat_with_tags[mat_with_tags_idx].sort(key=lambda x: (-x[0], x[1]))
            mat_with_tags_idx += 1

        def make_node(parent_node, child_cnt, mat) -> Node:
            nonlocal node_cnt
            nonlocal mat_with_tags
            if node_cnt >= tags_len:
                return parent_node
            else:
                for i in range(child_cnt):
                    if node_cnt >= tags_len:
                        break
                    temp_child_node = Node(mat[node_cnt][1], [])
                    node_cnt += 1
                    next_child_cnt = child_cnt * 2
                    parent_node.addkid(
                        make_node(temp_child_node, next_child_cnt, mat))
            return parent_node

        node_cnt = 0
        temp_target_user_top_node = Node('top', [])
        # node_iter += 1
        target_user_top_node = make_node(
            temp_target_user_top_node, 2, mat_with_tags[0])

        similar_user_get_node_iter = len(tag_table)
        for i in range(1, similar_user_get_node_iter):
            node_cnt = 0
            temp_top_node = Node('top', [])
            temp_ret_node = make_node(temp_top_node, 2, mat_with_tags[i])
            tree_sim.append(simple_distance(
                target_user_top_node, temp_ret_node))

        print("-"*20 + "TREE EDIT DISTANCE" + "-" * 20)
        print(tree_sim)
        return tree_sim

    def make_table_of_weighted_problem_score():
        shared_problem_ids_by_su = set()
        for su in similar_users:
            for p in similar_users[su]["solved"]:
                shared_problem_ids_by_su.add(p)
        for p in target_user["solved"]:
            try:
                shared_problem_ids_by_su.remove(p)
            except:
                pass

        # shared_problem_ids_by_su = list(shared_problem_ids_by_su).sort()
        # print(shared_problem_ids_by_su)

        shared_problem_dict_cnt = dict()
        shared_problem_dict_just_cnts = dict()
        for sp in shared_problem_ids_by_su:
            temp_cnt = 0
            temp_cnt_weighted = 0
            for su in similar_users:
                for p in similar_users[su]["solved"]:
                    if p == sp:
                        temp_rating_dif = abs(similar_users[su]["rating"] -
                                              target_user["rating"])
                        if temp_rating_dif == 0:
                            temp_rating_factor = 1
                        else:
                            temp_rating_factor = target_user["rating"] / \
                                temp_rating_dif
                        temp_cnt_weighted += 1 * \
                            similar_users[su]["cos_sim"] / 10 / \
                            similar_users[su]["tree_sim"] * temp_rating_factor
                        temp_cnt += 1
                        break
            shared_problem_dict_cnt[str(sp)] = round(temp_cnt_weighted, 2)
            shared_problem_dict_just_cnts[str(sp)] = temp_cnt
        shared_problem_weighted_cnt_list = [[int(k), v]
                                            for k, v in shared_problem_dict_cnt.items()]
        shared_problem_just_cnt_list = [[int(k), v]
                                        for k, v in shared_problem_dict_just_cnts.items()]
        shared_problem_weighted_cnt_list.sort(key=lambda x: (-x[1], x[0]))
        shared_problem_just_cnt_list.sort(key=lambda x: (-x[1], x[0]))
        # print(shared_problem_weighted_cnt_list)
        # print(shared_problem_just_cnt_list)
        # print("-"*40)
        # print(shared_problem_weighted_cnt_list[:5])
        # print("-"*40)
        final_weighted_problem_dict = dict()
        for p in shared_problem_weighted_cnt_list[:5]:
            final_weighted_problem_dict[p[0]] = [
                boj_problems[p[0]][1], boj_problems[p[0]][2], boj_problems[p[0]][3]]
        final_problem_dict_top5_list = []
        for fr in final_weighted_problem_dict:
            final_problem_dict_top5_list.append(
                [fr, final_weighted_problem_dict[fr]])

        return shared_problem_dict_cnt, shared_problem_just_cnt_list, final_problem_dict_top5_list

    def get_frequent_items(shared_problem_dict_cnt):
        similar_user_problem_table = list()
        similar_user_len = len(similar_user_list)
        for su in similar_users:
            similar_user_problem_table.append(
                list(set(similar_users[su]["solved"]) - set(target_user["solved"])))

        # print("-"*40)
        # for t in similar_user_problem_table:
        #     print(t)
        # print("-"*40)

        te = TransactionEncoder()
        te_ary = te.fit(similar_user_problem_table).transform(
            similar_user_problem_table)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        mn_support = 0.4
        # mn_support = 0.1
        frequent_itemsets = fpgrowth(
            df, min_support=mn_support, use_colnames=True)

        # print("-"*40)
        # print(frequent_itemsets)
        # print("-"*40)
        frequent_itemsets_list = frequent_itemsets.values.tolist()
        # print(frequent_itemsets_list)
        frequent_itemsets_list_weighted = list()
        for itemset in frequent_itemsets_list:
            itemset_list = list()
            itemset_weighted_value = 0
            for i in itemset[1]:
                itemset_list.append(i)
                itemset_weighted_value += shared_problem_dict_cnt[str(i)]
            frequent_itemsets_list_weighted.append(
                [itemset_weighted_value, itemset_list])
        # for f in frequent_itemsets_list_weighted:
        #     print(f)
        frequent_itemsets_list_weighted.sort(key=lambda x: -x[0])
        return frequent_itemsets_list_weighted[0][1]

    s_time = time.time()
    # 백준 문제 정보 만들기
    make_boj_problems_info()
    # target user init
    target_user = get_user_info(target_user_name)
    print(target_user)
    # similar user init, target user 기준
    similar_user_list = get_similar_user_list(target_user)

    # 사용자들이 해결한 문제의 tag들을 가져옴.
    # 만약 전체 해결한 문제의 10%가 안되는 문제들은 제외
    # (threshold가 전체 해결한 문제의 10%)
    # target user가 해결한 문제들의 tag들 가져오기
    target_user["tagscnt"] = crawl_user_solved_problems(
        target_user_name, int(target_user["solvedCount"] / 10))
    for su in similar_user_list:
        similar_users[su] = get_user_info(su)
        # solvedac과 연동이 안 된 사용자들은 제외
        if su in error_users:
            del similar_users[su]
            continue

        similar_users[su]["tagscnt"] = crawl_user_solved_problems(
            su, int(similar_users[su]["solvedCount"] / 10))

    # tag들을 alphabet 순으로 정렬
    get_similar_user_tag_set()
    for t in similar_user_problem_tag:
        similar_user_problem_tag_list.append(t)
    similar_user_problem_tag_list.sort()

    # tag_table 생성
    tag_table = make_tag_table()

    # cosine similarity, tree edit distance 구함
    similar_user_cos_sim = get_cos_sim(tag_table)
    similar_user_tree_sim = get_tree_sim(tag_table[0], tag_table[1:])
    similarity_idx = 0
    for su in similar_users:
        similar_users[su]["cos_sim"] = similar_user_cos_sim[similarity_idx]
        similar_users[su]["tree_sim"] = similar_user_tree_sim[similarity_idx]

    # print(target_user)
    shared_problem_dict_cnt, shared_problem_just_cnts, final_problem_dict_top5 = make_table_of_weighted_problem_score()

    print("-"*10+" FREQUENT PROBLEMS "+"-"*10)
    final_recommend_problems = get_frequent_items(shared_problem_dict_cnt)
    final_recommend_problems_dict = dict()
    for p in final_recommend_problems:
        final_recommend_problems_dict[p] = [
            boj_problems[p][1], boj_problems[p][2], boj_problems[p][3]]
    for fr in final_recommend_problems_dict:
        print(fr, final_recommend_problems_dict[fr])

    print("-"*10+" TOP5 RECOMMENDED PROBLEMS "+"-"*10)
    for t in final_problem_dict_top5:
        print(t)

    '''
    PROGRAM END
    '''
    print("-"*10+" PROGRAM ENDS "+"-"*10)
    print("Failed users:")
    print(error_users)

    e_time = time.time()
    excute_time = round(e_time - s_time, 3)
    print(f"{e_time - s_time:.5f} sec")
    return final_recommend_problems_dict, final_problem_dict_top5, excute_time


if __name__ == "__main__":
    input_user_name = str(input())
    final_recommend_problems_dict, final_problem_dict_top5, excute_time = get_recommended_problem(
        input_user_name)

    print("-"*10 + "MAIN" + "-"*10)
    print(final_recommend_problems_dict)
    print(final_problem_dict_top5)
    print(excute_time)
