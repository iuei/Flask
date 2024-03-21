from flask import Blueprint, jsonify
from models.models import employees
from datetime import datetime
import pytz

bp_employees = Blueprint('employees', __name__, url_prefix='/employees')

china_tz = pytz.timezone('Asia/Shanghai')


# 加载数据
@bp_employees.route('/load', methods=['POST'])
def load_data():
    try:
        employees_data = employees.query.all()

        employees_list = [
            {
                'id': data.id,
                'name': data.name,
                'number': data.number,
                'title': data.title,
                'salary': data.salary,
                'date': datetime.combine(data.date, datetime.min.time()).astimezone(china_tz).strftime('%Y-%m-%d %H:%M:%S'),
            }
            for data in employees_data
        ]
        return jsonify(employees_list)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch commodity data'}), 500
