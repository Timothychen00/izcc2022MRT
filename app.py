from flask import Flask,session
from main.routes import app_route
import datetime
from main.model import db_model
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
from flask_cors import CORS
import os
load_dotenv()
scheduler=APScheduler(BackgroundScheduler({'apscheduler.timezone': 'Asia/Taipei','daemon':False}))
class Config(object):
    SCHEDULER_API_ENABLED = True



app=Flask(__name__,static_folder='main/static',template_folder='main/templates')
CORS(app,resources={r"*": {"origins": "*"}})

app.secret_key='os.urandom(16).hex()'
app.register_blueprint(app_route)

def staged_auto_decrease(collapse_settings,stage):
    @scheduler.task('interval', id='自動扣分', seconds=2)
    def decrease():
        games=db_model.find_game()
        for i in games:
            teams=db_model.load_data(i['name'])
            for k in range(len(teams)):
                if '0' not in stage:
                    stage_tuple=['stage0','stage1','stage2','stage3','stage4']
                    if teams[k]['now'] !='' and teams[k]['now'] !='' and teams[k]['now'] in collapse_settings['map'][stage_tuple[stage_tuple.index(stage)-1]]['warn']:#在上一個階段的警告區進行扣分
                        db_model.edit_scores(i['name'],k,collapse_settings['decrease_score']*-1)
                        print(i['name'],k,'\b小扣分 now(before):',teams[k]['counts'],' ['+str(datetime.datetime.now()),']')

def stage1():
    print('stage1')
    collapse_settings=db_model.load_settings('collapse')
    staged_auto_decrease(collapse_settings,'stage1')

def stage2():
    print('stage2')
    try:
        scheduler.delete_job('自動扣分')
    except:
        pass
    collapse_settings=db_model.load_settings('collapse')
    staged_auto_decrease(collapse_settings,'stage2')

def stage3():
    print('stage3')
    try:
        scheduler.delete_job('自動扣分')
    except:
        pass
    collapse_settings=db_model.load_settings('collapse')
    staged_auto_decrease(collapse_settings,'stage3')

def stage4():
    print('stage4')
    try:
        scheduler.delete_job('自動扣分')
    except:
        pass
    print('結束')

if __name__=='__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    
    collapse=db_model.load_settings('collapse')
    stages={'stage1':stage1,'stage2':stage2,'stage3':stage3,'stage4':stage4}
    
    for l in stages:#jobs info
        time=collapse['time'][l].split(':')
        scheduler.add_job(id='崩塌開始_'+l,func=stages[l],trigger='cron',day='*', hour=time[0], minute=time[1], second=time[2],misfire_grace_time=900)
    for k in scheduler.get_jobs():
        print(k)
    app.run(debug=False,port=8080)
