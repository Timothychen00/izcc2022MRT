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
    join_form=JoinForm()
    delete_form=DeleteForm()
    games=[]
    
    if request.method=='POST':
        print('post')
        print(create_form.validate_on_submit(),join_form.validate_on_submit(),delete_form.validate_on_submit())
        if create_form.validate_on_submit():#新增遊戲
            print(db_model.create_game(create_form.name.data,create_form.teamnumber.data))
        else:
            print(create_form.name.errors,create_form.teamnumber.errors)

        if join_form.validate_on_submit():#加入遊戲
            permission=db_model.check_permission(join_form.name.data,join_form.pin.data)
            print(permission)
            if permission!='not allowed':
                session['games']={}
                session['games']['permission']=permission#寫入權限pin
                session['games']['name']=join_form.name.data
                return redirect('/games/'+join_form.name.data)
            else:
                flash('pin碼錯誤')
        if delete_form.validate_on_submit():
            db_model.delete_games(delete_form.name.data)
        
        return redirect('/games')
    else:
        if 'games' in session:
            if 'permission' in session['games']:
                return redirect('/games/'+session['games']['name'])#前往現在已經加入的遊戲
        print('get')
        games=db_model.find_game()
        print(games)
    return render_template('games.html',create_form=create_form,games=games,page='games',join_form=join_form,delete_form=delete_form)


@app_route.route('/games/<name>')
@login_required
def each_game(name):
    data=db_model.load_data()
    return render_template('each_game.html',page='map',data=data,total=13)

@app_route.route('/quit')
def quit():
    session.clear()
    return redirect('/')
