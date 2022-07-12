from flask import Flask
from main.routes import app_route
from dotenv import load_dotenv
import os
load_dotenv()
app=Flask(__name__,static_folder='main/static',template_folder='main/templates')

app.secret_key='os.urandom(16).hex()'
app.register_blueprint(app_route)

if __name__=='__main__':
    app.run(debug=True,port=8080)
