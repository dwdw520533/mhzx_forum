import json
import pymongo
import itertools
import logging
from datetime import datetime
from operator import itemgetter
from flask import Blueprint, render_template, redirect
from mhzx.util.date import strftime, increase_day
from datetime import datetime
from mhzx import forms
from mhzx.extensions import mongo
from flask import Blueprint, render_template, request, jsonify
from mhzx import models, code_msg

logger = logging.getLogger(__name__)
page_index = Blueprint("index", __name__, url_prefix="", template_folder="templates")


@page_index.route('/')
def index():
    return redirect('/report')


@page_index.route('/api/data', methods=['POST'])
def data_api():
    exchange_form = forms.DataForm()
    date = exchange_form.date.data
    order = exchange_form.order.data
    data = dict(
        date=date,
        order=order,
        jin=exchange_form.jin.data,
        mu=exchange_form.mu.data,
        shui=exchange_form.shui.data,
        huo=exchange_form.huo.data,
        tu=exchange_form.tu.data,
        created=datetime.now()
    )
    record = mongo.db.hx.find_one({'date': date, 'order': order})
    if record:
        mongo.db.hx.update({'_id': record['_id']}, data)
        logger.info('#Update record: %s', data)
    else:
        mongo.db.hx.insert_one(data)
        logger.info('#Create record: %s', data)
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
    begin_date = strftime(increase_day(-7, datetime.now()))
    begin3_date = increase_day(-3, datetime.now())
    x_axis, series, source_dict = [], [], {}
    max_idx, max_value = 0, 0
    pie_data = {i: 0 for i in category_enum.values()}
    for date, items in itertools.groupby(mongo.db.hx.find({
        '$and': [
            {'date': {'$gte': begin_date}},
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
    number = 0
    for ct, desc in category_enum.items():
        ct_data, x = [], []
        for i in range(-7, 1):
            _date = increase_day(i, datetime.now())
            data = source_dict.get(strftime(_date, '%Y-%m-%d')) or {}
            count = data.get(ct) or 0
            ct_data.append(count)
            x.append(strftime(_date, '%m-%d'))

            if _date < begin3_date:
                continue
            pie_data[desc] += count

        series.append({
            'name': desc,
            'type': 'line',
            'smooth': True,
            'stack': '次数%s' % number,
            'data': ct_data
        })
        x_axis = x

        if sum(ct_data) > max_value:
            max_value = sum(ct_data)
            max_idx = number
        number += 1
    series[max_idx]['label'] = {
        'normal': {
            'show': True,
            'position': 'top'
        }
    }
    return jsonify(models.R.ok(data=dict(
        data1=dict(
            x_axis=x_axis,
            series=series,
            legend=list(category_enum.values())
        ),
        data2=dict(
            selected={},
            series=[{
                'name': k,
                'value': v
            }for k, v in pie_data.items()],
            legend=list(category_enum.values())
        ),
    )))
