import time
import pandas as pd
from BOJPSR import get_recommended_problem
from flask import Flask, render_template, request, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/result', methods=['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        target_user_name = request.args.get('targetUserName')
        similar_boundary = int(request.args.get('similarBoundary'))
        print(target_user_name)
        print(similar_boundary)
        similar_user_list, final_frequent_problems_list, final_problem_top5_list, excute_time = get_recommended_problem(
            target_user_name, similar_boundary)
        sul = similar_user_list
        ffpl = final_frequent_problems_list
        fptl = final_problem_top5_list
        return render_template("result.html", target_user_name=target_user_name, similar_boundary=similar_boundary, sul=sul, ffpl=ffpl, et=excute_time, fptl=fptl)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
