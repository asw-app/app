# from flask import Flask, request, render_template_string

# app = Flask(__name__)

# # HTMLテンプレート
# html_template = """
# <!doctype html>
# <html lang="ja">
#   <head>
#     <meta charset="utf-8">
#     <title>Sum Calculator</title>
#   </head>
#   <body>
#     <h1>数値の合計を計算する</h1>
#     <form method="post">
#       <label for="num1">数値1:</label>
#       <input type="number" name="num1" id="num1" required><br><br>
#       <label for="num2">数値2:</label>
#       <input type="number" name="num2" id="num2" required><br><br>
#       <label for="num3">数値3:</label>
#       <input type="number" name="num3" id="num3" required><br><br>
#       <input type="submit" value="計算する">
#     </form>
#     {% if sum is not none %}
#       <h2>合計: {{ sum }}</h2>
#     {% endif %}
#   </body>
# </html>
# """

# @app.route("/", methods=["GET", "POST"])  # アプリのルートパス
# # HTTPメソッド
# # GET: サーバーからデータを取得するリクエストです。通常、Webページを表示する際に使用されます。
# # POST: サーバーにデータを送信するリクエストです。例えば、フォームに入力したデータを送信する場合に使われます。
# # 初めてページを開くとき、ブラウザはGETリクエストを送信します。このとき、サーバーはフォームが含まれたHTMLページを返します。
# # ユーザーがフォームに数値を入力して「計算する」ボタンを押すと、ブラウザはPOSTリクエストをサーバーに送信します。このリクエストには、ユーザーが入力した数値が含まれます。

# def index():
#     sum_result = None
#     if request.method == "POST":
#         # フォームからの入力値を取得し、合計を計算
#         num1 = request.form.get("num1", type=int)
#         num2 = request.form.get("num2", type=int)
#         num3 = request.form.get("num3", type=int)
#         sum_result = num1 + num2 + num3

#     # HTMLテンプレートに合計結果を渡してレンダリング
#     return render_template_string(html_template, sum=sum_result)

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, render_template_string

app = Flask(__name__)

# ホームページのHTMLテンプレート
home_html = """

<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>ホームページ</title>
  </head>
  <body>
    <h1>ホームページ</h1>
    <p>こちらはホームページです。</p>
    <p><a href="/profile">プロフィールページへ</a></p>
    <p><a href="/contact">お問い合わせページへ</a></p>
  </body>
</html>
"""

# プロフィールページのHTMLテンプレート
profile_html = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>プロフィールページ</title>
  </head>
  <body>
    <h1>プロフィールページ</h1>
    <p>こちらはプロフィールページです。</p>
    <p><a href="/">ホームページへ戻る</a></p>
  </body>
</html>
"""

# お問い合わせページのHTMLテンプレート
contact_html = """
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <title>お問い合わせページ</title>
  </head>
  <body>
    <h1>お問い合わせページ</h1>
    <form method="post">
      名前: <input type="text" name="name"><br>
      メッセージ: <textarea name="message"></textarea><br>
      <input type="submit" value="送信">
    </form>
    {% if message %}
      <p>送信ありがとうございます。</p>
    {% endif %}
    <p><a href="/">ホームページへ戻る</a></p>
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(home_html)

@app.route("/profile", methods=["GET"])
def profile():
    return render_template_string(profile_html)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # フォームからのデータを処理
        return render_template_string(contact_html, message=True)
    else:
        return render_template_string(contact_html, message=False)

if __name__ == "__main__":
    app.run(debug=True)
