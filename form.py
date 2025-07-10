from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    task = StringField(
        render_kw={'placeholder':'Enter your task'},
        validators=[DataRequired()]
    )
    submit = SubmitField('Add', render_kw={"class": "btn btn-info"})