from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template('home.html')


@app.route("/profile", methods=["GET"])
def profile():
    return render_template('profile.html')

# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         # フォームからのデータを処理
#         return render_template('contact.html', message=True)
#     else:
#         return render_template('contact.html', message=False)


@app.route("/calc", methods=["GET", "POST"])
def calc():
    water_sum = None
    paper_sum = None
    
    if request.method == "POST":
        # ユーザーが入力した数値を取得し、合計を計算
        water_num1 = request.form.get("cleaning-ink-press1", type=int) or 0
        water_num2 = request.form.get("cleaning-ink-press2", type=int) or 0
        water_num3 = request.form.get("plate-processing", type=int) or 0
        water_num4 = request.form.get("fountain-solution-press1", type=int) or 0
        water_num5 = request.form.get("fountain-solution-press2", type=int) or 0

        # None がないかを確認しながら合計を計算
        water_sum = (water_num1 or 0) + (water_num2 or 0) + (water_num3 or 0) + (water_num4 or 0) + (water_num5 or 0)
        
        paper_num1 = request.form.get("flaky-waste-paper1", type=int) or 0
        paper_num2 = request.form.get("cutting-machine-1", type=int) or 0
        paper_num3 = request.form.get("cutting-machine-2", type=int) or 0
        paper_num4 = request.form.get("3-sided-trimmer", type=int) or 0
        paper_num5 = request.form.get("sheet-waste-paper1", type=int) or 0
        paper_num6 = request.form.get("sheet-waste-paper2", type=int) or 0
        paper_num7 = request.form.get("sheet-waste-paper3", type=int) or 0
        paper_num8 = request.form.get("sheet-waste-paper4", type=int) or 0

        # None がないかを確認しながら合計を計算
        paper_sum = (paper_num1 or 0) + (paper_num2 or 0) + (paper_num3 or 0) + (paper_num4 or 0) + (paper_num5 or 0) + (paper_num6 or 0) + (paper_num7 or 0) + (paper_num8 or 0)

    return render_template('calc.html', water_sum=water_sum, paper_sum=paper_sum)



if __name__ == "__main__":
    app.run(debug=True)
