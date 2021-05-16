from flask import request
from app import app, db
from app.models import Posts, Users


@app.route('/posts')
def get_posts():
    output = []
    posts = Posts.query.all()
    if len(posts) == 0:
        return {
            'status_code': 204, 'error': 'No Content',
            'description': "No any posts found."
        }

    for post in posts:
        data = {'title': post.title, 'description': post.description}
        output.append(data)

    return {
        'status_code': 200,
        "content": {'posts': output},
        "total_items": len(output)
    }


@app.route('/posts/<post_id>', methods=['GET'])
@app.route('/posts/', methods=['GET'])
def get_post(post_id=None):
    user = None
    if post_id is None:
        return {
            'status_code': 400, 'Error': 'Bad Request',
            'Error Description': "Post id is required."
        }
    post = Posts.query.filter_by(id=post_id).first()
    if post.publisher is not None:
        user = Users.query.filter_by(id=post.publisher).first()
    if post is None:
        return {
            'status_code': 200,
            'Error': "NO VALID POST ID."
        }

    return {
        'status_code': 200,
        'content': {
            'id': post.id,
            'description': post.description,
            'publisher': f"{user.name}"}
    }


@app.route('/posts', methods=['POST'])
def create_post():
    post = Posts(title=request.json['title'], description=request.json['description'],
                 published=request.json['published'], publisher=request.json['publisher'])
    db.session.add(post)
    db.session.commit()

    if post.id is None:
        return {
            'status_code': 408, 'error': 'Request Timeout',
            'description': "Something going wrong . Please try again."
        }

    return {
        'id': post.id,
        'status_code': 201,
        'status': 'created',
        "description": f"Post with id {post.id} successfully created."
    }


@app.route('/post/<post_id>', methods=['PUT'])
@app.route('/post/', methods=['PUT'])
def update_post(post_id=None):
    if not request.json:
        return {
            'status_code': 204, 'Error': 'No Content',
            'Error Description': "No Content."
        }
    elif post_id is None:
        return {
            'status_code': 400, 'Error': 'Bad Request',
            'Error Description': "Post id is required."
        }
    else:
        post = Posts.query.filter_by(id=post_id).first()
        if post is None:
            return {
                'status_code': 400, 'Error': 'Bad Request',
                'Error Description': f"Unable to find post with id {post_id}"
            }
        for item in request.json:
            if item == 'id':
                continue
            post.item = request.json[item]
            db.session.commit()
        return {
            'id': post.id,
            'status_code': 200,
            "description": f"Post id : {post.id} successfully updated."
        }


@app.route('/users', methods=['POST'])
def create_user():
    user = Users(username=request.json['username'], email=request.json['email'], name=request.json['name'])

    db.session.add(user)
    db.session.commit()

    if user.id is None:
        return {
            'status_code': 408,
            'error': 'Request Timeout',
            'description': "Something going wrong .Unable to create new user. Please try again."
        }

    return {
        'id': user.id,
        'status_code': 201,
        'status': 'created',
        "description": f"User created successfully."
    }
