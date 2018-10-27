import re
from flask_wtf import FlaskForm
from wtforms import fields
from wtforms.validators import DataRequired, Regexp, EqualTo, Length, InputRequired
from mhzx import code_msg


class RegisterForm(FlaskForm):
    loginname = fields.StringField(validators=[DataRequired(code_msg.USER_ID_EMPTY.get_msg()),
                                               Regexp(re.compile(r"^[a-z0-9]+$"), code_msg.USER_ID_ERROR.get_msg())])
    username = fields.StringField()
    vercode = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])
    password = fields.PasswordField(validators=[Length(min=6, max=16, message=code_msg.PASSWORD_LENGTH_ERROR.get_msg())])
    re_password = fields.PasswordField(validators=[EqualTo('password', code_msg.PASSWORD_REPEAT_ERROR.get_msg())])
    phone = fields.StringField(validators=[DataRequired(code_msg.QUESTION_EMPTY.get_msg())])


class LoginForm(FlaskForm):
    loginname = fields.StringField(validators=[DataRequired(code_msg.USER_ID_EMPTY.get_msg())])
    vercode = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])
    password = fields.PasswordField(validators=[DataRequired(code_msg.PASSWORD_LENGTH_ERROR.get_msg())])


class PostsForm(FlaskForm):
    id = fields.StringField()
    title = fields.StringField(validators=[DataRequired(code_msg.POST_TITLE_EMPTY.get_msg())])
    content = fields.StringField(validators=[DataRequired(code_msg.POST_CONTENT_EMPTY.get_msg())])
    catalog_id = fields.StringField(validators=[DataRequired(code_msg.POST_CATALOG_EMPTY.get_msg())])
    #reward = fields.IntegerField(validators=[InputRequired(code_msg.POST_COIN_EMPTY.get_msg())])
    vercode = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])


class ForgetPasswordForm(FlaskForm):
    loginname = fields.StringField(validators=[DataRequired(code_msg.USER_ID_EMPTY.get_msg()),
                                               Regexp(re.compile(r"^[a-z0-9]+$"), code_msg.USER_ID_ERROR.get_msg())])
    vercode = fields.StringField(validators=[InputRequired(code_msg.VERIFY_CODE_ERROR.get_msg())])
    password = fields.PasswordField(
        validators=[Length(min=6, max=16, message=code_msg.PASSWORD_LENGTH_ERROR.get_msg())])
    repassword = fields.PasswordField(validators=[EqualTo('password', code_msg.PASSWORD_REPEAT_ERROR.get_msg())])
    phone = fields.StringField(validators=[DataRequired(code_msg.QUESTION_EMPTY.get_msg())])


class ChangePassWordForm(FlaskForm):
    nowpassword = fields.StringField(validators=[DataRequired(code_msg.NOW_PASSWORD_EMPTY.get_msg())])
    password = fields.PasswordField(
        validators=[Length(min=6, max=16, message=code_msg.PASSWORD_LENGTH_ERROR.get_msg())])
    repassword = fields.PasswordField(validators=[EqualTo('password', code_msg.PASSWORD_REPEAT_ERROR.get_msg())])


class ExchangeForm(FlaskForm):
    zone_id = fields.StringField(validators=[InputRequired(code_msg.ZONE_EMPTY.get_msg())])
    login_name = fields.StringField(validators=[DataRequired(code_msg.USER_ID_EMPTY.get_msg())])
    cd_key = fields.StringField(validators=[InputRequired(code_msg.CD_KEY_EMPTY.get_msg())])
    role_id = fields.IntegerField(validators=[InputRequired(code_msg.ROLE_EMPTY.get_msg())])
