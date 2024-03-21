# blueprint/routes/user_routes
from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash
from models.models import db, user_list
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

bp_user = Blueprint('user', __name__, url_prefix='/user')



# 用户登录
@bp_user.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 在数据库中查找用户是否存在
        user = user_list.query.filter_by(username=username).first()
        # 检查账号密码是否存在
        if user and user.check_password(password):
            # 使用Flask——login的login——user方法登录用户
            login_user(user)
            # # 创建JWT访问令牌
            # access_token = create_access_token(identity=user.username)
            return jsonify(
                {"message": "登录成功",
                 "user_info": {"username": user.username, "user_type": user.user_type}})
        else:
            return jsonify({"message": "登录失败", "error": "用户名或密码无效"}), 401
    except Exception as e:
        print(f"登录过程中错误: {e}")
        return jsonify({"message": "登录失败，发生错误.", "error": str(e)}), 500


# 注册
@bp_user.route('/register', methods=['POST'])
def register():
    try:
        form_data = request.get_json()
        username = form_data.get('username', '')
        password = form_data.get('password', '')
        cell = form_data.get('cell', '')

        # 检索用户名是否存在
        existing_user = user_list.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'state': -1, 'msg': '用户名已存在'})

        # 检查哈希密码
        hashed_password = generate_password_hash(password)

        # 保存信息
        new_user = user_list(
            username=username,
            password=hashed_password,
            cell=cell,
        )

        # 添加到数据库
        db.session.add(new_user)
        db.session.commit()

        return {'state': 0, 'msg': '注册成功'}
    except Exception as e:
        print(f"Error: {str(e)}")
        db.session.rollback()
        error_message = str(e) if str(e) else '未知错误'
        return {'state': -1, 'msg': f'Operation failed: {error_message}'}


# 加载数据
@bp_user.route('/info', methods=['GET'])
def get_info():
    try:
        # 获取请求中的分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 11, type=int)
        user_type = request.args.get('user_type', '')

        # 查询用户列表并分页
        if user_type == '100':
            users = user_list.query.paginate(page=page, per_page=per_page)
        else:
            users = user_list.query.filter_by(user_type=user_type).paginate(page=page, per_page=per_page)
        # 构建用户数据列表
        user_data = [
            {
                'id': user.id,
                'username': user.username,
                'cell': user.cell,
                'sex': user.sex,
                'address': user.address,
                'user_type': user.user_type_text(),
                'balance': user.balance
            }
            for user in users.items
        ]
        # 返回JSON格式的响应
        return jsonify({
            'total': users.total,
            'current_page': users.page,
            'page_size': users.per_page,
            'user_data': user_data
        })
    except Exception as e:
        # 打印异常信息
        print(f"Exception: {str(e)}")
        return jsonify({'error': 'Failed to fetch user data'}), 500


# 编辑用户数据
@bp_user.route('/edit/<id>', methods=['POST'])
def edit_user(id):
    # 从数据库中查找指定id的用户
    user = user_list.query.filter_by(id=id).first()

    if user:
        # 从请求中获取json数据
        data = request.get_json()

        # 更新数据
        user.username = data['username']
        user.cell = data['cell']
        user.sex = data['sex']
        user.address = data['address']
        user.user_type = data['user_type']
        user.balance = data['balance']

        # 提交数据
        db.session.commit()

        return jsonify({'message': '修改成功'})
    else:
        return jsonify({'message': '错误'}), 404


@bp_user.route('/get_user_data', methods=['GET'])
@jwt_required()  # 使用 JWT 验证装饰器，确保需要认证才能访问
def get_user_data():
    try:
        # 获取当前用户的用户名（从 JWT 负载中获取）
        current_username = get_jwt_identity()

        # 从数据库中查找当前用户名对应的用户信息
        user = user_list.query.filter_by(username=current_username).first()

        # 如果找到了用户
        if user:
            # 构建包含用户信息的字典
            user_data = {
                'username': user.username,
                'cell': user.cell,
                'sex': user.sex,
                'address': user.address,
                'user_type': user.user_type,
                'balance': user.balance
            }
            # 返回 JSON 响应，包含用户信息
            return jsonify({'user_data': user_data})
        else:
            # 如果未找到用户，返回 404 错误
            return jsonify({'message': '用户不存在'}), 404

    except Exception as e:
        # 捕获异常，并返回 500 错误
        print(f"Exception: {str(e)}")
        return jsonify({"message": "发生错误，无法获取用户数据.", "error": str(e)}), 500
