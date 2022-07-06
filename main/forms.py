from flask_wtf import FlaskForm
from wtforms.fields import TextField,PasswordField,SubmitField,IntegerField
from wtforms.validators import InputRequired,NumberRange

class CreateForm(FlaskForm):
    name=TextField('名稱',validators=[InputRequired()])
    # password=PasswordField('密碼',validators=[InputRequired()])
    teamnumber=IntegerField('隊伍數量',validators=[InputRequired(),NumberRange(min=3,max=10)])
    submit=SubmitField('送出')
    
class JoinForm(FlaskForm):
    name=TextField('名稱',validators=[InputRequired()])
    pin=TextField('pin',validators=[InputRequired()])
    submit=SubmitField('送出')
    
class DeleteForm(FlaskForm):
    name=TextField('名稱',validators=[InputRequired()])
    pin=TextField('pin',validators=[InputRequired()])
    submit=SubmitField('送出')