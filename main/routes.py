from flask import Blueprint, redirect, render_template, request,session,flash
from main.model import db_model
from main.forms import CreateGame,JoinGame
from main.decorators import login_required
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
    form1=JoinGame()
    games=[]
    
    if request.method=='POST':
        print('post')
        if form.validate_on_submit():
            print(db_model.create_game(form.name.data,form.password.data,form.teamnumber.data))
        else:
            print(form.name.errors,form.password.errors,form.teamnumber.errors)

        if form1.validate_on_submit():
            permission=db_model.join_game(form1.name.data,form1.pin.data)
            print(permission)
            if permission!='not allowed':
                session['games']={}
                session['games']['permission']=permission#寫入權限pin
                session['games']['name']=form1.name.data
                return redirect('/games/'+form1.name.data)
            else:
                flash('pin碼錯誤')
        return redirect('/games')
    else:
        if 'games' in session:
            if 'permission' in session['games']:
                return redirect('/games/'+session['games']['name'])#前往現在已經加入的遊戲
        print('get')
        games=db_model.find_game()
        print(games)
    return render_template('games.html',form=form,games=games,page='games',form1=form1)


@app_route.route('/games/<name>')
@login_required
def each_game(name):
    data=db_model.load_data()
    return render_template('each_game.html',page='map',data=data,total=13)

@app_route.route('/quit')
def quit():
    session.clear()
    return redirect('/')