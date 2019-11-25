from flask import Blueprint, render_template
from mhzx.util.date import strftime
from datetime import datetime
from mhzx import forms
from mhzx.extensions import mongo
from flask import Blueprint, render_template, request, jsonify
from mhzx import models, code_msg


page_index = Blueprint("index", __name__, url_prefix="", template_folder="templates")


@page_index.route('/api/data', methods=['POST'])
def data_api():
    exchange_form = forms.DataForm()
    date = exchange_form.date.data
    order = exchange_form.order.data
    data = dict(
        jin=exchange_form.jin.data,
        mu=exchange_form.mu.data,
        shui=exchange_form.shui.data,
        huo=exchange_form.huo.data,
        tu=exchange_form.tu.data
    )
    record = mongo.db.hx.find_one({'date': date, 'order': order})
    if record:
        mongo.db.hx.update({'_id': record['_id']}, data)
    else:
        mongo.db.hx.insert_one(dict(data, date=date, order=order))
    return jsonify(models.R.ok())


@page_index.route('/data')
def data_page():
    return render_template(
        "form.html",
        options=[
            '真身', '假身', '空图'
        ],
        order_options=[
            '1', '2', '3', '4'
        ],
        default_date=strftime(datetime.now(), '%Y-%m-%d')
    )
