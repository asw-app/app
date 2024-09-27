from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract,func
from sqlalchemy.dialects.mysql import INTEGER as Integer
from authlib.integrations.flask_client import OAuth

import functools
import datetime
import os


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
    client_kwargs={'scope': 'openid email'},
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
    date                      = db.Column('date',db.Date,unique=True,default=datetime.date.today(),nullable=True)
    created_at                = db.Column('created', db.DateTime, default=datetime.date.today(), nullable=True)
    updated_at                = db.Column('modified', db.DateTime, default=datetime.date.today(), nullable=True)

    def to_dict(self):
        return {
            'cleaning_ink_press_1'      : self.cleaning_ink_press_1,
            'cleaning_ink_press_2'      : self.cleaning_ink_press_2,
            'plate_processing'          : self.plate_processing,
            'fountain_solution_press_1' : self.fountain_solution_press_1,
            'fountain_solution_press_2' : self.fountain_solution_press_2,
            'water_sum'                 : self.water_sum,
            'flaky_waste_paper'         : self.flaky_waste_paper,
            'cutting_machine_1'         : self.cutting_machine_1,
            'cutting_machine_2'         : self.cutting_machine_2,
            'three_sided_trimmer'       : self.three_sided_trimmer,
            'sheet_waste_paper_1'       : self.sheet_waste_paper_1,
            'sheet_waste_paper_2'       : self.sheet_waste_paper_2,
            'sheet_waste_paper_3'       : self.sheet_waste_paper_3,
            'sheet_waste_paper_4'       : self.sheet_waste_paper_4,
            'paper_sum'                 : self.paper_sum,
            'date'                      : self.date.strftime("%m/%d"),
            'created_at'                : self.date.strftime("%Y-%m-%d"),
            'updated_at'                : self.date.strftime("%Y-%m-%d")
        }

#####
db.create_all()

id_to_culum = {
    'Cleaning ink Press1':                         'cleaning_ink_press_1',
    'Cleaning ink Press2':                         'cleaning_ink_press_2',
    'Plate Processing':                            'plate_processing',
    'Fountain Solution Press1':                    'fountain_solution_press_1',
    'Fountain Solution Press2':                    'fountain_solution_press_2',
    'Flaky Waste Paper':                           'flaky_waste_paper',
    'Pieces Waste Paper Cutting Machine 1':        'cutting_machine_1',
    'Pieces Waste Paper Cutting Machine 2':        'cutting_machine_2',
    'Pieces Waste Paper Cutting 3-sided trimmer': 'three_sided_trimmer',
    'Sheet Waste Paper Press 1':                   'sheet_waste_paper_1',
    'Sheet Waste Paper Press 2':                   'sheet_waste_paper_2',
    'Sheet Waste Paper Press 3':                   'sheet_waste_paper_3',
    'Sheet Waste Paper Press 4':                   'sheet_waste_paper_4',
    'date':                                        'date'
}

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user") is None:
            return redirect(url_for("top"))
        else:
            return func(*args, **kwargs)
    return wrapper

@app.route("/top", methods=["GET"])
def top():
    return render_template('top.html')

@app.route("/", methods=["GET"])
@login_required
def home():
    data_set = db.session.query(WasteData).filter(WasteData.date == datetime.date.today()).first()
    if data_set != None:
        return render_template('home.html',id_to_culum=id_to_culum,data=data_set.__dict__,keys=list(id_to_culum.keys()))
    else:
        return render_template('home.html',id_to_culum=id_to_culum,data=None,keys=list(id_to_culum.keys()))

@app.route('/login', methods=["GET"])
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/top')

@app.route('/auth/callback')
def auth_callback():
    try:
        token = oauth.google.authorize_access_token()
        print(token['userinfo'])
        session['user'] = token['userinfo']
        return redirect('/')
    except:
        return redirect('/top')
        

#####
# Index View
#
@app.route("/index", methods=["GET"])
@login_required
def index():
    # Get all data from db
    this_year = datetime.datetime.now().year
    this_month = datetime.datetime.now().month
    start_date = datetime.datetime(this_year, this_month, 1)
    end_date = datetime.datetime(this_year + 1, this_month + 1, 1)
    buf = db.session.query(WasteData).order_by(WasteData.date).filter(WasteData.date >= start_date,WasteData.date < end_date)
    data_set = buf.all()
    sum = db.session.query(func.sum(WasteData.water_sum),func.sum(WasteData.paper_sum)).filter(WasteData.date >= start_date,WasteData.date < end_date)
    
    year_list = db.session.query(WasteData).group_by(extract('year', WasteData.date)).all()
    if len(data_set) == 0:
        return render_template('index.html', data_set=None,sum_data=None,year=[this_year])
    else:
        return render_template('index.html', data_set=data_set,sum_data=sum[0],year=[year.date.strftime('%Y') for year in year_list])

@app.route("/get-data", methods=["GET"])
@login_required
def getData():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    print(month)
    start_date = datetime.datetime(year, month, 1)
    if month == 1:
        end_date = datetime.datetime(year - 1, 12, 1)
    elif month == 12:
        end_date = datetime.datetime(year + 1, 1, 1)
    else:
        end_date = datetime.datetime(year, month + 1, 1)
    data_set = db.session.query(WasteData).order_by(WasteData.date).filter(WasteData.date >= start_date,WasteData.date < end_date).all()
    print(month)
    print([data.to_dict() for data in data_set])
    return jsonify({'data':[data.to_dict() for data in data_set]})

#####
# Report View
#
@app.route("/report", methods=["GET","POST"])
@login_required
def report():
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
                setattr(wasate_data,'date',datetime.datetime.strptime(data_set.get('date'), '%Y-%m-%d'))
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

        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
