from flask import Blueprint, render_template, request
from main.model import db_model
app_route=Blueprint('捷大',__name__,static_folder='static',template_folder='templates')

@app_route.route('/')
def home():
    return render_template('base.html',page='map')

@app_route.route('/eachstation')
def eachstation():
    station=request.args.get('station',None)
    return render_template('eachstation.html',station=station,page='map')

@app_route.route('/dashboard')
def dashboard():
    count=int(request.args.get('c',0))
    data=db_model.load_data()
    return render_template('dashboard.html',total=13,data=data,page='dashboard')

@app_route.route('/control')
def control_center():
    return render_template('control.html',map='control')