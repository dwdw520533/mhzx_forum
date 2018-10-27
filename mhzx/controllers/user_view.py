from flask import Blueprint, render_template, request, jsonify, url_for, redirect, abort
from flask_login import login_user, logout_user, login_required, current_user
from mhzx import forms, models, code_msg
from mhzx.util import db_utils, utils
from mhzx.extensions import mongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from random import randint
from datetime import datetime
from mhzx.config import IS_MOCK
from mhzx.constant import SMS_TYPE_REGISTER
from mhzx.ops.user import register_zx_user, update_zx_user_password
from mhzx.ops.phone import (send_sms_phone_code, filter_phone,
                            generate_verify_code, verify_phone_code)
from mhzx.mongo import Product

user_view = Blueprint("user", __name__, url_prefix="", template_folder="templates")


@user_view.route('/<ObjectId:user_id>')
def user_home(user_id):
    user = mongo.db.users.find_one_or_404({'_id': user_id})
    return render_template('user/home.html', user=user)


@user_view.route('/posts')
@login_required
def user_posts():
    return render_template('user/index.html', user_page='posts', page_name='user')


@user_view.route('/message')
@user_view.route('/message/page/<int:pn>')
@login_required
def user_message(pn=1):
    user = current_user.user
    if user.get('unread', 0) > 0:
        mongo.db.users.update({'_id': user['_id']}, {'$set': {'unread': 0}})
    message_page = db_utils.get_page('messages', pn, filter1={'user_id': user['_id']}, sort_by=('_id', -1))
    return render_template('user/message.html', user_page='message', page_name='user', page=message_page)


@user_view.route('/order')
@user_view.route('/order/page/<int:pn>')
@login_required
def user_order(pn=1):
    user = current_user.user
    order_page = db_utils.get_page('order', pn, filter1={'user_id': str(user['_id'])}, sort_by=('_id', -1))
    for order in order_page.result:
        order["product"] = Product.objects(id=str(order["product"])).first().dict_data
    return render_template('user/order.html', user_page='order', page_name='user', page=order_page)


@user_view.route('/message/remove', methods=['POST'])
@login_required
def remove_message():
    user = current_user.user
    if request.values.get('all') == 'true':
        mongo.db.messages.delete_many({'user_id': user['_id']})
    elif request.values.get('id'):
        msg_id = ObjectId(request.values.get('id'))
        mongo.db.messages.delete_one({'_id': msg_id})
    return jsonify(models.BaseResult())


@user_view.route('/set', methods=['GET', 'POST'])
@login_required
def user_set():
    if request.method == 'POST':
        include_keys = ['username', 'avatar', 'desc', 'city', 'sex']
        data = request.values
        update_data = {}
        for key in data.keys():
            if key in include_keys:
                update_data[key] = data.get(key)
        # print(update_data)
        mongo.db.users.update({'_id': current_user.user['_id']}, {'$set': data})
        return jsonify(models.BaseResult())
    return render_template('user/set.html', user_page='set', page_name='user', title='基本设置')


@user_view.route('/repass', methods=['POST'])
def user_repass():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    pwd_form = forms.ChangePassWordForm()
    if not pwd_form.validate():
        return jsonify(models.R.fail(code_msg.PARAM_ERROR.get_msg(), str(pwd_form.errors)))
    nowpassword = pwd_form.nowpassword.data
    password = pwd_form.password.data
    user = current_user.user
    if not models.User.validate_login(user['password'], nowpassword):
        raise models.GlobalApiException(code_msg.PASSWORD_ERROR)
    mongo.db.users.update({'_id': user['_id']}, {'$set': {'password': generate_password_hash(password)}})
    update_zx_user_password(user["loginname"], password)
    return jsonify(models.R.ok())


@user_view.route('/forget', methods=['POST', 'GET'])
def user_pass_forget():
    if request.method == 'POST':
        forget_form = forms.ForgetPasswordForm()
        if not forget_form.validate():
            return jsonify(models.R.fail(code_msg.PARAM_ERROR.get_msg(), str(forget_form.errors)))
        loginname = forget_form.loginname.data
        password = forget_form.password.data
        question = forget_form.question.data
        answer = forget_form.answer.data
        ver_code = forget_form.vercode.data
        utils.verify_num(ver_code)
        user = mongo.db.users.find_one({'loginname': loginname})
        if not user:
            return jsonify(code_msg.USER_ID_NOT_EXIST)
        if user["question"] != question:
            return jsonify(code_msg.QUESTION_ERROR)
        if user["answer"] != answer:
            return jsonify(code_msg.ANSWER_ERROR)
        mongo.db.users.update({'_id': user['_id']}, {'$set': {
            'password': generate_password_hash(password)}})
        update_zx_user_password(loginname, password)
        return jsonify(code_msg.CHANGE_PWD_SUCCESS.put('action', url_for('user.login')))
    else:
        ver_code = utils.gen_verify_num()
        return render_template('user/forget.html', user=None,
                               ver_code=ver_code['question'])


@user_view.route('/active', methods=['GET', 'POST'])
def user_active():
    if request.method == 'GET':
        code = request.values.get('code')
        if code:
            user_id = mongo.db.active_codes.find_one({'_id': ObjectId(code)})['user_id']
            if user_id:
                mongo.db.active_codes.delete_many({'user_id': ObjectId(user_id)})
                mongo.db.users.update({'_id': user_id}, {"$set": {'is_active': True}})
                user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
                login_user(models.User(user))
                return render_template('user/activate.html')
        if not current_user.is_authenticated:
            abort(403)
        return render_template('user/activate.html')
    if not current_user.is_authenticated:
        abort(403)
    user = current_user.user
    mongo.db.active_codes.delete_many({'user_id': ObjectId(user['_id'])})
    send_active_email(user['username'], user['_id'], user['email'])
    return jsonify(code_msg.RE_ACTIVATE_MAIL_SEND.put('action', url_for('user.active')))


@user_view.route('/reg', methods=['GET', 'POST'])
def register():
    if db_utils.get_option('open_user', {}).get('val') != '1':
        abort(404)
    user_form = forms.RegisterForm()
    if user_form.is_submitted():
        if not user_form.validate():
            return jsonify(models.R.fail(code_msg.PARAM_ERROR.get_msg(), str(user_form.errors)))
        phone = user_form.phone.data
        if not filter_phone(phone):
            return jsonify(code_msg.SMS_PHONE_ERROR)
        user_count = mongo.db.users.find({'phone': phone}).count()
        reg_limit = int(db_utils.get_option_val('phone_register_limit', 0))
        if user_count >= reg_limit:
            return jsonify(code_msg.SMS_PHONE_LIMIT)
        if not verify_phone_code(phone, user_form.vercode.data):
            raise models.GlobalApiException(code_msg.VERIFY_CODE_ERROR)
        loginname = user_form.loginname.data
        password = user_form.password.data
        user = mongo.db.users.find_one({'loginname': loginname})
        if user:
            return jsonify(code_msg.USER_ID_EXIST)
        if not filter_phone(phone):
            return jsonify(code_msg.SMS_PHONE_ERROR)
        flag, game_user = register_zx_user(loginname, password, "123", "123", "123")
        if not flag:
            return jsonify(code_msg.USER_GAME_CREATE_ERROR)
        user = dict({
            'is_active': True,
            'coin': 0,
            'credit': 0,
            'credit_used': 0,
            'game_user_id': game_user["ID"],
            'phone': phone,
            'loginname': loginname,
            'username': user_form.username.data or loginname,
            'vip': 0,
            'reply_count': 0,
            'avatar': url_for('static', filename='images/avatar/' + str(randint(0, 12)) + '.jpg'),
            'password': generate_password_hash(password),
            'create_at': datetime.utcnow(),
            'perms': []
        })
        mongo.db.users.insert_one(user)
        return jsonify(code_msg.REGISTER_SUCCESS.put('action', url_for('user.login')))
    ver_code = utils.gen_verify_num()
    # session['ver_code'] = ver_code['answer']
    return render_template('user/reg.html', ver_code=ver_code['question'], form=user_form)


@user_view.route('/login', methods=['GET','POST'])
def login():
    user_form = forms.LoginForm()
    if user_form.is_submitted():
        if not user_form.validate():
            return jsonify(models.R.fail(code_msg.PARAM_ERROR.get_msg(), str(user_form.errors)))
        utils.verify_num(user_form.vercode.data)
        user = mongo.db.users.find_one({'loginname': user_form.loginname.data})
        if not user:
            return jsonify(code_msg.USER_NOT_EXIST)
        if not models.User.validate_login(user['password'], user_form.password.data):
            raise models.GlobalApiException(code_msg.PASSWORD_ERROR)
        if not user.get('is_active', False):
            return jsonify(code_msg.USER_UN_ACTIVE)
        if user.get('is_disabled', False):
            return jsonify(code_msg.USER_DISABLED)
        login_user(models.User(user))
        action = request.values.get('next')
        if not action:
            action = url_for('index.index')
        return jsonify(code_msg.LOGIN_SUCCESS.put('action', action))
    logout_user()
    ver_code = utils.gen_verify_num()
    # session['ver_code'] = ver_code['answer']
    return render_template('user/login.html', ver_code=ver_code['question'], form=user_form, title='登录')


@user_view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@user_view.route('/sms', methods=['GET'])
def send_verify_sms():
    phone = request.values.get('phone')
    sms_type = int(request.values.get('sms_type', SMS_TYPE_REGISTER))
    if not filter_phone(phone):
        return jsonify(code_msg.SMS_PHONE_ERROR)
    user_count = mongo.db.users.find({'phone': phone}).count()
    reg_limit = int(db_utils.get_option_val('phone_register_limit', 0))
    if user_count >= reg_limit:
        return jsonify(code_msg.SMS_PHONE_LIMIT)
    phone_code = generate_verify_code(phone, sms_type, IS_MOCK)
    if not phone_code:
        return jsonify(code_msg.SMS_SEND_REPEAT)
    if not IS_MOCK:
        send_sms_phone_code(phone_code)
    return jsonify(code_msg.SMS_SEND_SUCCESS)
