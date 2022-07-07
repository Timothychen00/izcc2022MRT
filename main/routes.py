from flask import Blueprint, redirect, render_template, request,session,flash
from main.model import db_model
from main.forms import CreateForm,JoinForm,DeleteForm
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
    create_form=CreateForm()
    games=[]
    
    if request.method=='POST':
        print('post')
        print(create_form.validate_on_submit())
        if create_form.validate_on_submit():#新增遊戲
            msg=db_model.create_game(create_form.name.data,create_form.teamnumber.data)
            if msg:
                flash(msg)
        else:
            print(create_form.name.errors,create_form.teamnumber.errors)
            return redirect('/games')
    else:
        if 'games' in session:
            if 'permission' in session['games']:
                return redirect('/games/'+session['games']['name'])#前往現在已經加入的遊戲
            
        name=request.args.get('name',None)
        pin=request.args.get('pin',None)
        method=request.args.get('method',None)
        print(method,name,pin)
        if method:
            if method=='delete':
                print('delete')
                db_model.delete_games(name,pin)
            elif method=='join':
                print('join')
                permission=db_model.check_permission(name,pin)
                print(permission)
                if permission!='not allowed':
                    session['games']={}
                    session['games']['permission']=permission#寫入權限pin
                    session['games']['name']=name
                    return redirect('/games/'+name)
                else:
                    flash('pin碼錯誤')
            return redirect('/games')
        print('get')
    games=db_model.find_game()
    print(games)
    return render_template('games.html',create_form=create_form,games=games,page='games')


@app_route.route('/games/<name>')
@login_required
def each_game(name):
    data=db_model.load_data(name)
    return render_template('each_game.html',page='map',data=data,total=13)

@app_route.route('/quit')
def quit():
    session.clear()
    return redirect('/')
