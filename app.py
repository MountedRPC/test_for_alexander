import vk_api
from flask import Flask, request, jsonify
import time
import re
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1 per day"],
)


def auth():
    r = requests.get('https://oauth.vk.com/access_token',
                     params={'client_id': 51730448, 'client_secret': 'lEmf9dCJwtCGq0yksOFS',
                             'grant_type': 'client_credentials', 'v': '5.131'})
    return r.json()
    # vk_session = vk_api.VkApi(app_id=51730448, client_secret='lEmf9dCJwtCGq0yksOFS')
    # vk_session.server_auth()
    # return vk_session.token


@app.route('/api/v1', methods=['GET'])
def get_data():
    method_name = request.args.get('method')
    if method_name == 'profile':
        return get_vk_profile(vk=auth())
    elif method_name == 'likes':
        return get_likes_profile(vk=auth())
    elif method_name == 'posts':
        return get_posts_profile(vk=auth())
    else:
        return jsonify({'error': 'Invalid method'}), 400


# <your_domain>/api/v1?method=profile&profile=<username>
def get_vk_profile(vk):
    profile_name = request.args.get('profile')
    r = requests.get('https://api.vk.com/method/users.get',
                     params={'access_token': vk['access_token'], 'user_ids': profile_name,
                             'fields': 'counters,photo_max_orig', 'v': '5.131'})

    vk_data = r.json()

    if 'response' in vk_data:
        user_info = vk_data['response'][0]
        formatted_data = {
            "status": "success",
            "code": 200,
            "data": {
                "profile_id": user_info["id"],
                "avatar_url": user_info.get("photo_max_orig", ""),
                "followers": user_info["counters"]["followers"],
                "following": user_info["counters"].get("subscriptions", 0),
            }
        }
        return jsonify(formatted_data)
    else:
        return jsonify({'status': 'error', 'code': 403, 'message': "Invalid account name:"}), 403

# FIXME
# <your_domain>/api/v1?method=likes&link=<post_link>
def get_likes_profile(vk):
    link = request.args.get('link')
    post_id = re.sub(r"[^\d_]", "", link)
    r = requests.get('https://api.vk.com/method/wall.getById',
                     params={'access_token': vk['access_token'], 'posts': post_id, 'v': '5.131'})
    response_data = r.json()
    if 'response' in response_data:
        post_info = response_data['response'][0]
        formatted_data = {
            "status": "success",
            "code": 200,
            "data": {
                "post_id": f"{post_info['from_id']}_{post_info['id']}",
                "url": f"https://vk.com/wall{post_info['from_id']}_{post_info['id']}",
                "likes": post_info['likes']['count'],
                "share": post_info['reposts']['count'],
                "views": post_info['views']['count']
            }
        }
        return jsonify(formatted_data)
    else:
        error_message = response_data.get('error', {}).get('error_msg', 'Unknown error')
        error_data = {
            "status": "error",
            "code": 403,
            "message": error_message
        }
        return jsonify(error_data), 403


# <your_domain>/api/v1?method=posts&profile=<username>
def get_posts_profile(vk):
    profile_name = request.args.get('profile')
    r = requests.get('https://api.vk.com/method/wall.get',
                     params={'access_token': vk['access_token'], 'domain': profile_name, 'v': '5.131', 'count': 10})
    response_data = r.json()

    if 'response' in response_data:
        items = response_data['response']['items']
        posts_data = []
        for post_info in items:
            post_data = {
                "post_id": f"{profile_name}_{post_info['id']}",
                "url": f"https://vk.com/wall{profile_name}_{post_info['id']}",
                "likes": str(post_info['likes']['count']),
                "share": str(post_info['reposts']['count']),
                "views": str(post_info['views']['count'])
            }
            posts_data.append(post_data)

        formatted_data = {
            "status": "success",
            "code": 200,
            "data": {
                "posts": posts_data
            }
        }
        return jsonify(formatted_data)
    else:
        error_message = response_data.get('error', {}).get('error_msg', 'Unknown error')
        error_data = {
            "status": "error",
            "code": 403,
            "message": error_message
        }
        return jsonify(error_data), 403


if __name__ == '__main__':
    app.run(debug=True)
