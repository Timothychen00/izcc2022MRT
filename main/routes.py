from flask import Blueprint, redirect, render_template, request,session,flash,jsonify
from main.model import db_model
from main.forms import CreateForm
from main.decorators import login_required,admin_required
app_route=Blueprint('捷大',__name__,static_folder='static',template_folder='templates')

@app_route.route('/')
def home():
    return render_template('base.html',page='map')

@app_route.route('/games/<name>/eachstation')
def eachstation(name):
    print(request.args)
    station=request.args.get('station',None)
    move=int(request.args.get('move',0))
    if move:
        move(name,session['games']['team'],station)
        return redirect('/games/'+name)
    return render_template('eachstation.html',station=station,page='map')


@app_route.route('/games/<name>/places')
def places(name):
    print(request.args)
    data=db_model.load_data(name)
    return render_template('places.html',data=data,page='map')

@app_route.route('/games/<name>/cards')
def cards(name):
    print(request.args)
    data=db_model.load_data(name)
    return render_template('places.html',data=data,page='map')

@app_route.route('/games/<name>/random')
def random(name):
    print(request.args)
    data=db_model.load_data(name)
    return render_template('random.html',data=data,page='map')


@app_route.route('/control')
def control_center():
    return render_template('control.html',page='control')

@app_route.route('/games',methods=['GET','POST'])
def games():
    print(str(request.url_rule).split('/')[1])
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
                    session['games']['permission']=permission[1]#寫入權限pin
                    session['games']['name']=name
                    session['games']['team']=permission[0]
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
    print(data)
    move=request.args.get('move',None)
    station=request.args.get('station',None)
    have=request.args.get('have',None)
    if station:
        if move:
            db_model.move(name,session['games']['team'],station)
            return redirect('/games/'+name)
        if have:
            db_model.have(name,session['games']['team'],station)
            return redirect('/games/'+name)
        return render_template('eachstation.html',station=station)
    return render_template('each_game.html',page='map',data=data,total=13)

@app_route.route('/games/<name>/scores')
@login_required
@admin_required
def edit_scores(name):
    types=request.args.get('type',None)
    value=int(request.args.get('value',0))
    team=int(request.args.get('team',0))
    if types and value:
        if types=='decrease':
            value*=-1
        db_model.edit_scores(name,team,value)
    print(types,team,value)
    data=db_model.load_data(name)
    
    max=1
    for i in data:
        if i['counts']>max:
            max=i['counts']
    return render_template('dashboard.html',data=data,total=max)


@app_route.route('/quit')
def quit():
    session.clear()
    return redirect('/')

@app_route.route('/dice')
def dice():
    return render_template('dice.html')