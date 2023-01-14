from flask import Flask
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

app=Flask(__name__)
scheduler = APScheduler(BackgroundScheduler({'apscheduler.timezone': 'Asia/Taipei'}))

class Config(object):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = "Asia/Taipei"


    
@scheduler.task('cron', id='崩塌開始', day='*', hour='11', minute='23', second='20')
def job3():
    @scheduler.task('interval', id='do_job_4', seconds=2)
    def job4():
        print(str(datetime.datetime.now()) + ' fuck')
        print(scheduler.get_jobs())
    print(str(datetime.datetime.now()) + 'set  Job 4 executed')
    
@scheduler.task('cron', id='第二階段', day='*', hour='11', minute='24', second='40')
def job3():
    scheduler.delete_job('do_job_4')
    print(scheduler.get_jobs())

def checking_points():
    print(str(datetime.datetime.now())+"hello" )

@app.route('/')
def home():
    return '11'

if __name__=='__main__':
    app.config.from_object(Config())
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False)