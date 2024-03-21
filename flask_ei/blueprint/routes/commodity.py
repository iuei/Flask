# blueprint/routes/commodity_routes
import logging
from flask import Blueprint, jsonify, request
from sqlalchemy.sql.functions import current_time
from models.models import db, commodity
import pytz

bp_commodity = Blueprint('commodity', __name__, url_prefix='/commodity')

china_tz = pytz.timezone('Asia/Shanghai')


# 添加数据
@bp_commodity.route('/add', methods=['POST'])
def add_commodity():
    try:
        form_data = request.get_json()
        commodity_name = commodity.query.filter_by(name=form_data.get('name', '')).first()
        commodity_serial = commodity.query.filter_by(serial=form_data.get('serial', '')).first()
        if commodity_name:
            return {'status': 1, 'msg': '添加失败，商品已存在'}
        if commodity_serial:
            return {'status': 1, 'msg': '添加失败，编号不能重复'}

        new_commodity = commodity(
            name=form_data.get('name', ''),
            price=form_data.get('price', ''),
            type=form_data.get('type', ''),
            serial=form_data.get('serial', ''),
            inventory=form_data.get('inventory', ''),
            status=form_data.get('status', ''),
            create_time=current_time()
        )

        db.session.add(new_commodity)
        db.session.commit()

        return {'status': 200, 'msg': '添加成功'}
    except Exception as e:
        print(f"Error: {str(e)}")
        db.session.rollback()
        return {'state': 1, 'msg': '添加失败'}


# 编辑数据
@bp_commodity.route('/edit', methods=['POST'])
def edit_commodity():
    data = request.json

    edit_commodity = db.session.query(commodity).filter_by(id=data.get('id')).first()

    if edit_commodity:
        edit_commodity.name = data.get('name')
        edit_commodity.price = data.get('price')
        edit_commodity.type = data.get('type')
        edit_commodity.serial = data.get('serial')
        edit_commodity.inventory = data.get('inventory')
        edit_commodity.status = data.get('status')

        db.session.commit()

        return {'state': 0, 'msg': '编辑成功'}
    else:
        return {'state': 1, 'msg': '编辑失败'}


# 查询/加载数据
@bp_commodity.route('/search', methods=['POST'])
def search_commodity():
    try:
        form_data = request.get_json()
        serial = form_data.get('serial', '')
        name = form_data.get('name', '')
        status = form_data.get('status', '')
        page = form_data.get('page', 1)  # 默认为第一页
        per_page = form_data.get('per_page', 11)  # 默认每页11条记录

        # 计算偏移量
        offset = (page - 1) * per_page

        # 查询分页结果
        if status == 100:  # 如果status值为100，则查询全部的商品
            query = commodity.query.filter(
                commodity.serial.ilike(f'%{serial}%'),
                commodity.name.ilike(f'%{name}%')
            )
        else:
            query = commodity.query.filter(
                commodity.serial.ilike(f'%{serial}%'),
                commodity.status.ilike(f'%{status}%'),
                commodity.name.ilike(f'%{name}%')
            )

        # 查询总记录数（用于分页）
        total_count = query.count()

        search_results = query.offset(offset).limit(per_page).all()

        commodity_data = [
            {
                'id': result.id,
                'name': result.name,
                'price': result.price,
                'type': result.type,
                'serial': result.serial,
                'inventory': result.inventory,
                'status': result.status_text(),
                'create_time': result.create_time.astimezone(china_tz).strftime('%Y-%m-%d %H:%M:%S'),
            }
            for result in search_results
        ]

        return jsonify({'total': total_count, 'data': commodity_data, 'current_page': page, 'page_size': per_page})
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        return jsonify({'error': 'Failed to fetch commodity data'}), 500


# 打印excel
@bp_commodity.route('/print', methods=['POST'])
def print():
    try:
        form_data = request.get_json()
        serial = form_data.get('serial', '')
        name = form_data.get('name', '')
        status = form_data.get('status', '')
        page = form_data.get('page', 1)  # 默认为第一页
        per_page = form_data.get('per_page', 11)  # 默认每页11条记录

        # 计算分页的偏移量
        offset = (page - 1) * per_page

        # 查询总记录数（用于分页）
        total_count = commodity.query.filter(
            commodity.serial.ilike(f'%{serial}%'),
            commodity.status.ilike(f'%{status}%'),
            commodity.name.ilike(f'%{name}%')
        ).count()

        # 查询分页结果
        if status == 100:  # 如果status值为100 则查询全部的商品
            search_results = commodity.query.filter(
                commodity.serial.ilike(f'%{serial}%'),
                commodity.name.ilike(f'%{name}%')
            ).offset(offset).limit(per_page).all()
        else:
            search_results = commodity.query.filter(
                commodity.serial.ilike(f'%{serial}%'),
                commodity.status.ilike(f'%{status}%'),
                commodity.name.ilike(f'%{name}%')
            ).offset(offset).limit(per_page).all()

        commodity_data = [
            {
                'id': result.id,
                'name': result.name,
                'price': result.price,
                'type': result.type,
                'serial': result.serial,
                'inventory': result.inventory,
                'status': result.status_text(),
                'create_time': result.create_time.astimezone(china_tz).strftime('%Y-%m-%d %H:%M:%S'),
            }
            for result in search_results
        ]

        return jsonify({'total': total_count, 'data': commodity_data})
    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({'error': 'Failed to fetch commodity data'}), 500


# 删除数据
@bp_commodity.route('/delete', methods=['POST'])
def delete():
    try:
        form_data = request.get_json()
        id = form_data.get('id', '')

        if not id:
            return {'state': 1, 'msg': '参数错误'}

        commodity_to_delete = db.session.query(commodity).filter(commodity.id == id).first()

        if not commodity_to_delete:
            return {'state': 1, 'msg': '商品不存在'}

        # 删除
        db.session.delete(commodity_to_delete)
        db.session.commit()

        return {'state': 0, 'msg': '操作成功'}

    except Exception as e:
        return {'state': 1, 'msg': '操作失败，服务器异常'}
