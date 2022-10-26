import time
import pandas as pd
from BOJPSR import get_recommended_problem


if __name__ == "__main__":
    target_user_name = 'gnaroshi'
    similar_boundary = 10
    similar_user_list, final_frequent_problems_list, final_problem_top5_list, excute_time = get_recommended_problem(
        target_user_name, similar_boundary)
    sul = pd.DataFrame(similar_user_list)
    ffpl = pd.DataFrame(final_frequent_problems_list, columns=[
                        'PID', 'PTITLE', 'PTIER', 'PTAG'])
    fptl = pd.DataFrame(final_problem_top5_list,
                        columns=['PID', 'PTITLE', 'PTIER', 'PTAG'])

    print(sul.to_html(index=False))
    print(ffpl.to_html(index=False))
    print(fptl.to_html(index=False))
