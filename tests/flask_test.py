from flask import Flask, render_template, request, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/result', methods=['POST', 'GET'])
def recommend():
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_platform = request.form['game_platform']
        user_platform = request.form['user_platform']
        a = find_sim_game(data, cosine_sim, game_name,
                          game_platform, user_platform)
        a = a.drop(['platform', 'totalscore', 'genre',
                   'developer', 'feature'], axis=1)
        return render_template("result.html", tables=[a.to_html(index=False)])


if __name__ == "__main__":
    app.run()
