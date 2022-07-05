from flask import Blueprint, redirect, render_template, request,session
from main.model import db_model
from main.forms import CreateGame
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
    data=db_model.load_data()
    return render_template('dashboard.html',total=13,data=data,page='dashboard')

@app_route.route('/control')
def control_center():
    return render_template('control.html',map='control')

@app_route.route('/games',methods=['GET','POST'])
def games():
    form=CreateGame()
    if form.validate_on_submit():
        print(db_model.create_game(form.name.data,form.password.data))
    return render_template('games.html',form=form)

# @app_route.route('/games/create',methods=['GET','POST'])
# def create_game():
#     form=CreateGame()
#     if form.validate_on_submit():
#         print(db_model.create_game(form.name.data,form.password.data))
#     return redirect('/games')