from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER as Integer
from authlib.integrations.flask_client import OAuth

import functools
from datetime import datetime
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")

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
# db settings
#
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)
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
    water_sum                 = db.Column('water_sum',Integer(unsigned=True),nullable=True)
    flaky_waste_paper         = db.Column('flaky_waste_paper',Integer(unsigned=True),nullable=True)
    cutting_machine_1         = db.Column('cutting_machine_1',Integer(unsigned=True),nullable=True)
    cutting_machine_2         = db.Column('cutting_machine_2',Integer(unsigned=True),nullable=True)
    three_sided_trimmer       = db.Column('three_sided_trimmer',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_1       = db.Column('sheet_waste_paper_1',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_2       = db.Column('sheet_waste_paper_2',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_3       = db.Column('sheet_waste_paper_3',Integer(unsigned=True),nullable=True)
    sheet_waste_paper_4       = db.Column('sheet_waste_paper_4',Integer(unsigned=True),nullable=True)
    paper_sum                 = db.Column('paper_sum',Integer(unsigned=True),nullable=True)
    date                      = db.Column('date',db.Date,unique=True,default=datetime.now,nullable=True)
    created_at                = db.Column('created', db.DateTime, default=datetime.now, nullable=True)
    updated_at                = db.Column('modified', db.DateTime, default=datetime.now, nullable=True)
#####
db.create_all()

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

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for("login"))
        else:
            return func(*args, **kwargs)
    return wrapper

@app.route("/", methods=["GET"])
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET"])
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/auth/callback')
def auth_callback():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/')

#####
# Index View
#
@app.route("/index", methods=["GET"])
@login_required
def index():
    # Get all data from db
    data_set = db.session.query(WasteData).order_by(WasteData.date).all()
    return render_template('index.html', data_set=data_set)

#####
# Report View
#
@app.route("/report", methods=["GET","POST"])
@login_required
def calc():
    water_sum = None
    paper_sum = None

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
            
            water_waste_sum = 0
            paper_waste_sum = 0

            for index,key in enumerate(id_to_culum.keys()):

                if index < 5 and key != 'date' and getattr(wasate_data,id_to_culum[key]) != None:
                    print('----------')
                    print(getattr(wasate_data,id_to_culum[key]))
                    water_waste_sum += int(getattr(wasate_data,id_to_culum[key]))
                elif key != 'date' and getattr(wasate_data,id_to_culum[key]) != None:
                    paper_waste_sum += int(getattr(wasate_data,id_to_culum[key]))

            setattr(wasate_data,'water_sum',water_waste_sum)
            setattr(wasate_data,'paper_sum',paper_waste_sum)
            # Add a data to DB
            db.session.add(wasate_data)
            db.session.commit()
        else:
            # Exist date data
            if data_set.get('selector') != None and data_set.get('selector') != '' and data_set.get('quantity') != None and data_set.get('quantity') != '':
                setattr(query,id_to_culum[data_set.get('selector')],data_set.get('quantity'))

            water_waste_sum = 0
            paper_waste_sum = 0
            for index,key in enumerate(id_to_culum.keys()):
                if index < 5 and key != 'date' and getattr(query,id_to_culum[key]) != None:
                    water_waste_sum += int(getattr(query,id_to_culum[key]))
                elif key != 'date' and getattr(query,id_to_culum[key]) != None:
                    paper_waste_sum += int(getattr(query,id_to_culum[key]))
            
            setattr(query,'water_sum',water_waste_sum)
            setattr(query,'paper_sum',paper_waste_sum)
            # Update value
            db.session.commit()

        return render_template('result.html', water_sum=water_sum, paper_sum=paper_sum)

if __name__ == "__main__":
    app.run(debug=True)
