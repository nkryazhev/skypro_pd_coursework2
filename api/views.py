from flask import Blueprint, send_file, jsonify
from utils import read_json
import config
import os

api_bp = Blueprint('api_blueprint', __name__)


@api_bp.route('/posts')
def api_endpoint_posts():
    return send_file(os.path.join(config.SITE_ROOT, 'data', config.POSTS_FILE))


@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def api_endpoint_single_post(post_id):
    posts = read_json(config.POSTS_FILE)
    for post in posts:
        if post['pk'] == post_id:
            return jsonify(post)
