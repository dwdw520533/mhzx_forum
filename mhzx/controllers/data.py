import json
import pymongo
import itertools
from operator import itemgetter
from flask import Blueprint, render_template
from mhzx.util.date import strftime, increase_day
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


@page_index.route('/report')
def report_page():
    return render_template("report.html")


@page_index.route('/api/report')
def report_data():
    category = request.args['category']
    category_enum = {
        'jin': '金',
        'mu': '木',
        'shui': '水',
        'huo': '火',
        'tu': '土'
    }
    begin_date = increase_day(-7, datetime.now())
    x_axis, series, source_dict = [], [], {}
    for date, items in itertools.groupby(mongo.db.hx.find({
        '$and': [
            {'date': {'$gte': strftime(begin_date, '%Y-%m-%d')}},
            {'$or': [
                {'jin': category},
                {'mu': category},
                {'shui': category},
                {'huo': category},
                {'tu': category},
            ]}
        ]
    }).sort('date', pymongo.ASCENDING), key=itemgetter('date')):
        temp = {}
        for i in items:
            def accumulate(ct):
                if i.get(ct) == category:
                    temp.setdefault(ct, 0)
                    temp[ct] += 1

            list(map(accumulate, category_enum))
        source_dict.setdefault(date, temp)

    for ct, desc in category_enum.items():
        ct_data, x = [], []
        for i in range(-7, 1):
            _date = increase_day(i, datetime.now())
            data = source_dict.get(strftime(_date, '%Y-%m-%d')) or {}
            ct_data.append(data.get(ct) or 0)
            x.append(strftime(_date, '%m%d'))
        series.append({
            'name': desc,
            'type': 'line',
            'stack': '次数',
            'data': ct_data
        })
        x_axis = x

    return jsonify(models.R.ok(data=dict(
            x_axis=x_axis,
            series=series,
            legend=list(category_enum.values())
        )))
