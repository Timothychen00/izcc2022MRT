from flask_wtf import FlaskForm
from wtforms.fields import TextField,PasswordField,SubmitField
from wtforms.validators import InputRequired

class CreateGame(FlaskForm):
    name=TextField('名稱',validators=[InputRequired()])
    password=PasswordField('密碼',validators=[InputRequired()])
    submit=SubmitField('送出')