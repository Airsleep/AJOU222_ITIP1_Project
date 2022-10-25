import requests
import time
import json
import pandas as pd

problem_ids = []
problem_hashes = []
problem_titles = []
problem_levels = []
problem_tags = []
# problem_tags_set = set()


def appending(pid, ph, pt, pl, ptg):
    problem_ids.append(pid)
    problem_hashes.append(ph)
    problem_titles.append(pt)
    problem_levels.append(pl)
    problem_tags.append(ptg)


def crawl(page):
    url = "https://solved.ac/api/v3/search/problem"
    querystring = {"query": " ", "page": f"{page}"}

    headers = {"Content-Type": "application/json"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    one_page = dict()
    one_page["item"] = json.loads(response.text).get("items")
    for item in one_page["item"]:
        problem_id = int(item.get("problemId"))
        problem_hash = problem_id * 100
        problem_title = item.get("titleKo")
        problem_level = int(item.get("level"))
        problem_tag = []

        problem_tag_info = item.get("tags")
        problem_tag_info_len = len(problem_tag_info)
        for i, tag in enumerate(problem_tag_info):
            temp = tag.get("displayNames")
            problem_tag.append(temp[1].get("name"))
            # problem_tags_set.add(temp[1].get("name"))
            if i == problem_tag_info_len - 1:
                continue
        appending(problem_id, problem_hash, problem_title,
                  problem_level, problem_tag)


def make_csv():
    df = pd.DataFrame({"PROBLEM_ID": problem_ids, "PROBLEM_HASH": problem_hashes,
                      "PROBLEM_TITLE": problem_titles, "PROBLEM_LEVEL": problem_levels, "PROBLEM_TAGS": problem_tags})
    df.to_csv("problem_list.csv", index=False, encoding="utf8")


def main():
    for i in range(1, 495):
        print(f"crawling {i} page now still {495 - i} to go")
        crawl(i)

        time.sleep(12)

    make_csv()
    # print(problem_tags_set)


if __name__ == "__main__":
    main()
