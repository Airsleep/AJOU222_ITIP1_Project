from util.BOJPSR import get_recommended_problem

if __name__ == "__main__":
    print("Input the target user and similar boundary. e.g.: gnaroshi 10")
    input_string = input().split(' ')
    input_user_name = str(input_string[0])
    similar_boundary = int(input_string[1])
    similar_user_list, final_frequent_problems_dict, final_problem_dict_top5, excute_time = get_recommended_problem(
        input_user_name, similar_boundary)

    print("-"*10 + "MAIN" + "-"*10)
    print(final_frequent_problems_dict)
    print(final_problem_dict_top5)
    print("Excuted time: {t}s".format(t=excute_time))
