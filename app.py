from flask import Flask,session
from main.routes import app_route
import datetime
from main.model import db_model
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os
load_dotenv()
scheduler=BackgroundScheduler(daemon=True)
class Config(object):
    SCHEDULER_API_ENABLED = True

app=Flask(__name__,static_folder='main/static',template_folder='main/templates')

app.secret_key=os.urandom(16).hex()
app.register_blueprint(app_route)

def auto_decrease(collaspe_settings,stage):
    games=db_model.find_game()
    for i in games:
        teams=db_model.load_data(i['name'])
        for k in range(len(teams)):
            if teams[k]['now'] in collaspe_settings['stage']:
                db_model.edit_scores(i['name'],k,collaspe_settings['decrease_score'])
                
                
    

@scheduler.task('cron', id='崩塌開始_stage1', day='*', hour='10', minute='35', second='00')
def job3():
    @scheduler.task('interval', id='do_job_4', seconds=2)
    def job4():
        print(str(datetime.datetime.now()) + ' fuck')
    print(str(datetime.datetime.now()) + 'set  Job 4 executed')
    
@scheduler.task('cron', id='崩塌開始_stage2', day='*', hour='10', minute='35', second='00')
def job3():
    @scheduler.task('interval', id='do_job_4', seconds=2)
    def job4():
        print(str(datetime.datetime.now()) + ' fuck')
    print(str(datetime.datetime.now()) + 'set  Job 4 executed')

@scheduler.task('cron', id='崩塌開始_stage3', day='*', hour='10', minute='35', second='00')
def job3():
    @scheduler.task('interval', id='do_job_4', seconds=2)
    def job4():
        print(str(datetime.datetime.now()) + ' fuck')
    print(str(datetime.datetime.now()) + 'set  Job 4 executed')

@scheduler.task('cron', id='崩塌開始_stage4', day='*', hour='10', minute='35', second='00')
def job3():
    @scheduler.task('interval', id='do_job_4', seconds=2)
    def job4():
        print(str(datetime.datetime.now()) + ' fuck')
    print(str(datetime.datetime.now()) + 'set  Job 4 executed')




if __name__=='__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True,port=8080)
