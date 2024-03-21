# blueprint/routes/redis.py
from flask import Blueprint, jsonify, request
import redis

bp_redis = Blueprint('redis', __name__, url_prefix='/redis')

redis_client = redis.Redis(host='8.140.118.229', port=6379, db=15, password='sg@123456')


@bp_redis.route('/set_data', methods=['POST'])
def set_data():
    try:
        data = request.json
        key = data.get('key')
        value = data.get('value')

        # 在Redis中存储数据
        redis_client.set(key, value)

        return jsonify({'message': '数据存储成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_redis.route('/get_data/<key>', methods=['GET'])
def get_data(key):
    try:
        # 从Redis中检索数据
        value = redis_client.get(key)

        if value is not None:
            return jsonify({'key': key, 'value': value.decode('utf-8')})
        else:
            return jsonify({'message': '未找到键'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_redis.route('/get_all', methods=['GET'])
def get_redis_data():
    try:
        # 获取所有的 keys
        keys = redis_client.keys('*')

        # 遍历 keys 并获取对应的 values
        data = {}
        for key in keys:
            value = redis_client.get(key)
            # 将字节转换为字符串
            value_str = value.decode('utf-8') if value else None
            data[key.decode('utf-8')] = value_str

        return jsonify({'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_redis.route('/set_data_with_expiry', methods=['POST'])
def set_data_with_expiry():
    try:
        data = request.get_json()
        # 设置过期时间为 30 秒
        redis_client.setex('hello123', 30, data['data'])
        return jsonify({'message': '带过期时间的数据设置成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_redis.route('/get_hash_data', methods=['GET'])
def get_hash_data():
    try:
        # 获取 Redis 哈希表中的数据
        hash_data = redis_client.hgetall('your_hash_key')
        decoded_hash_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data.items()}
        return jsonify({'data': decoded_hash_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_redis.route('/set_hash_data', methods=['POST'])
def set_hash_data():
    try:
        data = request.get_json()
        # 设置 Redis 哈希表中的数据
        redis_client.hmset('325325', data['data'])
        return jsonify({'message': '哈希表数据设置成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_redis.route('/hello', methods=['GET', 'POST'])
def hello():
    try:
        # 增加数据
        a = redis_client.incr('counter')
        print(a)
        #
        # # 获取数据
        # data_value = redis_client.get('key')
        #
        # # 设置数据
        # redis_client.set('key', 'value')
        #
        # # 删除数据
        # redis_client.delete('5')
        #
        # # 存储列表
        # redis_client.lpush('list', 'value1')
        #
        # # 获取列表
        # list_data = redis_client.lrange('list', 0, -1)
        #
        # # 存储字典
        # redis_client.hmset("dict", {"key1": "value1", "key2": "value2"})
        #
        # # 获取字典
        # dict_data = redis_client.hgetall('dict')

        return jsonify({
            'message': 'Redis Hello 操作成功',
            # 'data_value': data_value.decode('utf-8') if data_value else None,
            # 'list_data': [item.decode('utf-8') for item in list_data],
            # 'dict_data': {key.decode('utf-8'): value.decode('utf-8') for key, value in dict_data.items()}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
