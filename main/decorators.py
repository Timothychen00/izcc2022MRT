from flask import session,flash,redirect,request
from functools import wraps
def login_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if 'games' in session:
            if 'permission' in session['games']:
                return a(*args,**kwargs)
        else:
            flash('請先加入遊戲')
            return redirect('/games')
    return wrap

def admin_required(a):
    @wraps(a)
    def wrap(*args,**kwargs):
        if 'games' in session:
            if 'permission' in session['games']:
                if session['games']['permission']=='admin':
                    return a(*args,**kwargs)
        flash('請先加入遊戲')
        return redirect('/games')
    return wrap