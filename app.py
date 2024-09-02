from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER as Integer

from datetime import datetime
import os

app = Flask(__name__)

##### 
# db settings
#
base_dir = os.path.dirname(__file__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "sample.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)
app.app_context().push()
#####

#####
# db class
#
class WasteData(db.Model):
    id                        = db.Column('id',Integer(unsigned=True), primary_key=True ,autoincrement=True)
    cleaning_ink_press_1      = db.Column('cleaning_ink_press_1',Integer(unsigned=True),nullable=False)
    cleaning_ink_press_2      = db.Column('cleaning_ink_press_2',Integer(unsigned=True),nullable=False)
    plate_processing          = db.Column('plate_processing',Integer(unsigned=True),nullable=False)
    fountain_solution_press_1 = db.Column('fountain_solution_press_1',Integer(unsigned=True),nullable=False)
    fountain_solution_press_2 = db.Column('fountain_solution_press_2',Integer(unsigned=True),nullable=False)
    water_sum                 = db.Column('water_sum',Integer(unsigned=True),nullable=False)
    flaky_waste_paper         = db.Column('flaky_waste_paper',Integer(unsigned=True),nullable=False)
    cutting_machine_1         = db.Column('cutting_machine_1',Integer(unsigned=True),nullable=False)
    cutting_machine_2         = db.Column('cutting_machine_2',Integer(unsigned=True),nullable=False)
    three_sided_trimmer       = db.Column('three_sided_trimmer',Integer(unsigned=True),nullable=False)
    sheet_waste_paper_1       = db.Column('sheet_waste_paper_1',Integer(unsigned=True),nullable=False)
    sheet_waste_paper_2       = db.Column('sheet_waste_paper_2',Integer(unsigned=True),nullable=False)
    sheet_waste_paper_3       = db.Column('sheet_waste_paper_3',Integer(unsigned=True),nullable=False)
    sheet_waste_paper_4       = db.Column('sheet_waste_paper_4',Integer(unsigned=True),nullable=False)
    paper_sum                 = db.Column('paper_sum',Integer(unsigned=True),nullable=False)
    date                      = db.Column('date',db.Date,unique=True,default=datetime.now,nullable=False)
    created_at                   = db.Column('created', db.DateTime, default=datetime.now, nullable=False)
    updated_at                  = db.Column('modified', db.DateTime, default=datetime.now, nullable=False)
#####

db.create_all()

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

#####
# Index View
#
@app.route("/index", methods=["GET"])
def index():
    # Get all data from db
    data_set = db.session.query(WasteData).all()
    return render_template('index.html', data_set=data_set)

#####
# Report View
#
@app.route("/report", methods=["GET","POST"])
def calc():
    data = request.form
    water_sum = None
    paper_sum = None

    if request.method == "GET":
        # Show Report Form HTML
        return render_template('report_form.html')
    elif request.method == "POST":
        # ユーザーが入力した数値を取得し、合計を計算
        water_num1 = data.get("cleaning-ink-press-1", type=int) or 0
        water_num2 = data.get("cleaning-ink-press-2", type=int) or 0
        water_num3 = data.get("plate-processing", type=int) or 0
        water_num4 = data.get("fountain-solution-press-1", type=int) or 0
        water_num5 = data.get("fountain-solution-press-2", type=int) or 0

        # None がないかを確認しながら合計を計算
        water_sum = (water_num1 or 0) + (water_num2 or 0) + (water_num3 or 0) + (water_num4 or 0) + (water_num5 or 0)
        
        paper_num1 = data.get("flaky-waste-paper", type=int) or 0
        paper_num2 = data.get("cutting-machine-1", type=int) or 0
        paper_num3 = data.get("cutting-machine-2", type=int) or 0
        paper_num4 = data.get("3-sided-trimmer", type=int) or 0
        paper_num5 = data.get("sheet-waste-paper-1", type=int) or 0
        paper_num6 = data.get("sheet-waste-paper-2", type=int) or 0
        paper_num7 = data.get("sheet-waste-paper-3", type=int) or 0
        paper_num8 = data.get("sheet-waste-paper-4", type=int) or 0

        # None がないかを確認しながら合計を計算
        paper_sum = (paper_num1 or 0) + (paper_num2 or 0) + (paper_num3 or 0) + (paper_num4 or 0) + (paper_num5 or 0) + (paper_num6 or 0) + (paper_num7 or 0) + (paper_num8 or 0)

        # date time
        date = data.get("date") or 0

        # Create Instance
        wasate_data = WasteData(
                            cleaning_ink_press_1 = water_num1,
                            cleaning_ink_press_2 = water_num2,
                            plate_processing = water_num3,
                            fountain_solution_press_1 = water_num4,
                            fountain_solution_press_2 = water_num5,
                            water_sum = water_sum,
                            flaky_waste_paper = paper_num1,
                            cutting_machine_1 = paper_num2,
                            cutting_machine_2 = paper_num3,
                            three_sided_trimmer = paper_num4,
                            sheet_waste_paper_1 = paper_num5,
                            sheet_waste_paper_2 = paper_num6,
                            sheet_waste_paper_3 = paper_num7,
                            sheet_waste_paper_4 = paper_num8,
                            paper_sum = paper_sum,
                            date = datetime.strptime(date, '%Y-%m-%d'))
        
        # Add a data to DB
        db.session.add(wasate_data)
        db.session.commit()

        return render_template('result.html', water_sum=water_sum, paper_sum=paper_sum)

if __name__ == "__main__":
    app.run(debug=True)