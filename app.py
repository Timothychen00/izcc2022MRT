from flask import Flask,session
from main.routes import app_route
import datetime
from main.model import db_model
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
import os
load_dotenv()
scheduler=APScheduler(BackgroundScheduler({'apscheduler.timezone': 'Asia/Taipei','daemon':False}))
class Config(object):
    SCHEDULER_API_ENABLED = True

app=Flask(__name__,static_folder='main/static',template_folder='main/templates')

app.secret_key=os.urandom(16).hex()
app.register_blueprint(app_route)

def staged_auto_decrease(collapse_settings,stage):
    @scheduler.task('interval', id='自動扣分', seconds=2)
    def decrease():
        games=db_model.find_game()
        for i in games:
            teams=db_model.load_data(i['name'])
            for k in range(len(teams)):
                if teams[k]['now'] in collapse_settings[stage]:
                    db_model.edit_scores(i['name'],k,collapse_settings['decrease_score']*-1)
                    print(i['name'],k,'\b小扣分 now(before):',teams[k]['counts'],' ['+str(datetime.datetime.now()),']')
    

@scheduler.task('cron', id='崩塌開始_stage1', day='*', hour='12', minute='17', second='30')
def stage1():
    print('stage1')
    collapse_settings=db_model.load_settings('collapse')
    staged_auto_decrease(collapse_settings,'stage1')
    
    
@scheduler.task('cron', id='崩塌開始_stage2', day='*', hour='12', minute='18', second='00')
def stage2():
    print('stage2')
    scheduler.delete_job('自動扣分')
    collapse_settings=db_model.load_settings('collapse')
    staged_auto_decrease(collapse_settings,'stage2')

@scheduler.task('cron', id='崩塌開始_stage3', day='*', hour='12', minute='18', second='30')
def stage3():
    print('stage3')
    scheduler.delete_job('自動扣分')
    collapse_settings=db_model.load_settings('collapse')
    staged_auto_decrease(collapse_settings,'stage3')

@scheduler.task('cron', id='崩塌開始_stage4', day='*', hour='12', minute='19', second='00')
def stage4():
    print('stage4')
    scheduler.delete_job('自動扣分')
    print('結束')




if __name__=='__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False,port=8080)
