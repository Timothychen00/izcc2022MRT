from flask import Blueprint, render_template, request
app_route=Blueprint('捷大',__name__,static_folder='static',template_folder='templates')

@app_route.route('/')
def home():
    return render_template('base.html')

@app_route.route('/eachstation')
def eachstation():
    station=request.args.get('station',None)
    return render_template('eachstation.html',station=station)

@app_route.route('/dashboard')
def dashboard():
    count=int(request.args.get('c',0))
    return render_template('dashboard.html',total=13,counts=count)