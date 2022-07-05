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
    return render_template('control.html',page='control')

@app_route.route('/games',methods=['GET','POST'])
def games():
    form=CreateGame()
    games=[]
    if request.method=='POST':
        print('post')
        if form.validate_on_submit():
            print(db_model.create_game(form.name.data,form.password.data))
        else:
            print(form.name.errors,form.password.errors)
        return redirect('/games')
    else:
        print('get')
        games=db_model.find_game()
        print(games)
    return render_template('games.html',form=form,games=games,page='games')

@app_route.route('/games/<name>')
def each_game(name):
    
    return render_template('base.html',page='map')
