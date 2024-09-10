from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER as Integer

from datetime import datetimegit 
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
    cleaning_ink_press_1      = db.Column('cleaning_ink_press_1',Integer(unsigned=True),nullable=True)
    cleaning_ink_press_2      = db.Column('cleaning_ink_press_2',Integer(unsigned=True),nullable=True)
    plate_processing          = db.Column('plate_processing',Integer(unsigned=True),nullable=True)
    fountain_solution_press_1 = db.Column('fountain_solution_press_1',Integer(unsigned=True),nullable=True)
    fountain_solution_press_2 = db.Column('fountain_solution_press_2',Integer(unsigned=True),nullable=True)
    flaky_waste_paper         = db.Column('flaky_waste_paper',Integer(unsigned=True),nullable=True)
    cutting_machine_1         = db.Column('cutting_machine_1',Integer(unsigned=True),nullable=True)
    cutting_machine_2         = db.Column('cutting_machine_2',Integer(unsigned=True),nullable=True)
    three_sided_trimmer       = db.Column('three_sided_trimmer',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_1       = db.Column('sheet_waste_paper_1',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_2       = db.Column('sheet_waste_paper_2',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_3       = db.Column('sheet_waste_paper_3',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_4       = db.Column('sheet_waste_paper_4',Integer(unsigned=True),nullable=True)
    date                      = db.Column('date',db.Date,unique=True,default=datetime.now,nullable=True)
    created_at                = db.Column('created', db.DateTime, default=datetime.now, nullable=True)
    updated_at                = db.Column('modified', db.DateTime, default=datetime.now, nullable=True)
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
    data_set = db.session.query(WasteData).order_by(WasteData.date).all()    
    return render_template('index.html', data_set=data_set)

#####
# Report View
#
@app.route("/report", methods=["GET","POST"])
def calc():
    water_sum = None
    paper_sum = None
    id_to_culum = {
        'cleaning-ink-press-1':      'cleaning_ink_press_1',
        'cleaning-ink-press-2':      'cleaning_ink_press_2',
        'plate-processing':          'plate_processing',
        'fountain-solution-press-1': 'fountain_solution_press_1',
        'fountain-solution-press-2': 'fountain_solution_press_2',
        'flaky-waste-paper':         'flaky_waste_paper',
        'cutting-machine-1':         'cutting_machine_1',
        'cutting-machine-2':         'cutting_machine_2',
        '3-sided-trimmer':           'three_sided_trimmer',
        'sheet-waste-paper-1':       'sheet_waste_paper_1',
        'sheet-waste-paper-2':       'sheet_waste_paper_2',
        'sheet-waste-paper-3':       'sheet_waste_paper_3',
        'sheet-waste-paper-4':       'sheet_waste_paper_4',
        'date':                      'date'
    }

    if request.method == "GET":
        # Show Report Form HTML
        return render_template('report_form.html')
    elif request.method == "POST":
        data_set = request.form

        # Search by date
        query = db.session.query(WasteData).filter(WasteData.date == data_set.get("date")).first()

        if query == None:
            # Not Exist date data
            wasate_data = WasteData()
            if data_set.get('date') != None:
                setattr(wasate_data,'date',datetime.strptime(data_set.get('date'), '%Y-%m-%d'))
            if data_set.get('selector') != None and data_set.get('selector') != '' and data_set.get('quantity') != None and data_set.get('quantity') != '':
                setattr(wasate_data,id_to_culum[data_set.get('selector')],data_set.get('quantity'))

            # Add a data to DB
            db.session.add(wasate_data)
            db.session.commit()
        else:
            # Exist date data
            if data_set.get('selector') != None and data_set.get('selector') != '' and data_set.get('quantity') != None and data_set.get('quantity') != '':
                setattr(query,id_to_culum[data_set.get('selector')],data_set.get('quantity'))

            # Update value
            db.session.commit()

        return render_template('result.html', water_sum=water_sum, paper_sum=paper_sum)

if __name__ == "__main__":
    app.run(debug=True)