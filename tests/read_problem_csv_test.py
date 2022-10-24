import csv
import re

f = open('practice/project/problem_list.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
problems = dict()
problem_category = set()
for line in rdr:
    if line[0] == "PROBLEM_ID":
        continue
    problems[int(line[0])] = [line[1], line[2], line[3], line[4]]
    problem_tag = line[4].lstrip("[").rstrip("]")
    problem_tag = re.sub("'", "", problem_tag)
    problem_tag = re.sub('"', "", problem_tag)
    problem_tag = re.sub(", ", "/", problem_tag).split('/')
    # print(problem_tag)
    for tag in problem_tag:
        problem_category.add(tag)
        # print("tag: " + tag)
problem_category.discard("")
# print(problems)
for p in problem_category:
    print(p)
# 190개 태그 존재
print(len(problem_category))

f.close()
