
from flask import Blueprint, redirect, render_template, request,session,flash,jsonify
from main.model import db_model
from main.forms import CreateForm
from main.decorators import login_required,admin_required
import datetime

app_route=Blueprint('捷大',__name__,static_folder='static',template_folder='templates')

@app_route.before_request
def print_session():
    print(session)

@app_route.route('/')
def home():
    return render_template('base.html',page='map')


@app_route.route('/games/<name>/places')
def places(name):
    print(request.args)
    data=db_model.load_data(name)
    return render_template('places.html',data=data,page='map')

@app_route.route('/games/<name>/random')
def random(name):
    print(request.args)
    data=db_model.load_data(name)
    return render_template('random.html',data=data,page='map')

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
                if session['games']['permission']!='not allowed':
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
                if permission[1]!='not allowed':
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
    stages=stages_check()
    print('eachgame')
    data=db_model.load_data(name)
    # print(data)
    move=request.args.get('move',None)
    station=request.args.get('station',None)
    have=request.args.get('have',None)
    settings=db_model.load_settings('map')
    # print(settings)
    # print(station)
    # print(session)
    if station:
        if move:
            db_model.move(name,session['games']['team'],station)
            session['now']=station
            # flash('移動成功')
            return redirect('/games/'+name)
        if have:
            db_model.have(name,session['games']['team'],station)
            flash('佔領成功')
            return redirect('/games/'+name)
        return render_template('eachstation.html',station=station,settings=settings,data=data)
    return render_template('each_game.html',page='map',data=data,total=13,settings=settings,stages=stages)

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

@app_route.route('/games/<name>/cards')
def cards(name):
    get=request.args.get('get',None)
    delete=request.args.get('delete',None)
    if get:
        db_model.get_card(name,session['games']['team'],get)
        return redirect('/games/'+name+"/cards")
    if delete:
        delete=int(delete)
        db_model.delete_card(name,session['games']['team'],delete)
        return redirect('/games/'+name+"/cards")
    data=db_model.load_data(name)
    cards=data[session['games']['team']]['cards']
    return render_template('cards.html',cards=cards)

@app_route.before_request
def session_out():
    global session
    print(session)
    
@app_route.route('/task')
def upload_task():
    db_model.upload_tasks()
    return "1"


# api
@app_route.route('/games/<name>/api/teams')
def api_teams(name):
    print(1)
    teams=db_model.load_data(name)
    print(teams)
    print(len(teams))
    return jsonify(teams)

@app_route.route('/games/<name>/api/stages_check')
def stages_check(name):
    date=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+8)))
    stages=0
    if date.hour==14:
        if date.minute>=50:
            stages=1
    elif date.hour==15:
       stages=2
    elif date.hour==16:
        stages=3
    elif date.hour==17:
       stages=4
# stage1 => 14:50
# stage2 => 15:00
# stage3 => 16:00
# stage4 => 17:00
    return stages