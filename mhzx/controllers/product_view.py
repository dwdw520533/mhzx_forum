from flask import Blueprint, render_template, request, jsonify, url_for, redirect, abort
from flask_login import login_user, logout_user, login_required, current_user
from mhzx import models, code_msg
from mhzx.util import db_utils, utils
from mhzx.mongo import Product, Order
from mhzx.constant import *
from mhzx.ops import coin
from mhzx.util import cache_lock

product_view = Blueprint("prod", __name__, url_prefix="", template_folder="templates")


@product_view.route('/')
@product_view.route('/page/<int:pn>')
def show_product(pn=1):
    sort_key = request.values.get('sort_key', '_id')
    product_page = db_utils.get_page('product', pn, filter1={'status': PRODUCT_STATUS_NORMAL}, sort_by=(sort_key, -1))
    return render_template('product/index.html', user_page='product', page_name='user', page=product_page,
                           sort_key=sort_key)


@product_view.route('/detail/<ObjectId:product_id>')
@product_view.route('/detail/<ObjectId:product_id>/page/<int:pn>/')
def product_detail(product_id, pn=1):
    product = Product.objects(id=product_id).first()
    if not product:
        abort(404)
    product.view_count = (product.view_count or 0) + 1
    product.save()
    post = product.dict_data
    # page = db_utils.get_page('comments', pn=pn, size=10,
    #                          filter1={'product_code': product_code},
    #                          sort_by=('is_adopted', -1))
    return render_template('product/detail.html', user_page='product_detail',
                           order=post, page_name='user')


@product_view.route('/order', methods=['POST'])
@product_view.route('/order/<ObjectId:order_id>', methods=['GET'])
def get_create_order(order_id=None):
    if not current_user.is_authenticated:
        raise models.GlobalApiException(code_msg.USER_NO_LOGIN)
    if request.method == 'GET':
        order = Order.objects(id=order_id).first()
        if not order:
            return jsonify(code_msg.ORDER_NOT_EXIST)
        return jsonify(models.R.ok(data=order.dict_data))
    else:
        user = current_user.user
        user_id = str(user['_id'])
        with cache_lock("user_create_order_%s" % user_id):
            product_code = request.values.get('product_code')
            product = Product.objects(product_code=product_code).first()
            history_orders = Order.objects(user_id=user_id, product=product,
                                           status__in=ORDER_STATUS_VALID)
            if product.limit and len(history_orders) >= product.limit:
                return jsonify(code_msg.ORDER_SURPASS_LIMIT)
            if product.require_perm and product.require_perm not in user.perms:
                raise models.GlobalApiException(code_msg.PERM_ERROR)
            if product.price_type == PRICE_TYPE_COIN:
                recharge_handler = coin.recharge_coin
                not_enough_msg = code_msg.COIN_BALANCE_NOT_ENOUGH
            else:
                recharge_handler = coin.recharge_credit
                not_enough_msg = code_msg.CREDIT_BALANCE_NOT_ENOUGH
            result = recharge_handler(user, product.price)
            if not result:
                return jsonify(not_enough_msg)
            order = Order(user_id=user_id, product=product,
                          cd_key=utils.generate_cd_key(),
                          price=product.price)
            order.save()
            product.sale_num += 1
            product.inventory -= 1
            product.save()
            return jsonify(models.R.ok(data=order.dict_data).put('action', url_for('user.user_order')))
