from sqlalchemy.exc import InternalError
from flask import request
from app import app, db
from app.models import Posts, Users


@app.route('/posts')
def get_posts():
    try:
        output = []
        posts = Posts.query.all()
        if len(posts) == 0:
            return {
                'status_code': 204,
                'status_msg': 'No Content',
                'description': "No any posts found."
            }

        for post in posts:
            data = {'title': post.title, 'description': post.description}
            output.append(data)

        return {
            'status_code': 200,
            'status_msg': "200",
            "content": {'posts': output},
            "total_items": len(output)
        }
    except InternalError:
        db.session.rollback()
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            "description": f"Something going wrong. Error: {InternalError}",
        }


@app.route('/posts/<post_id>', methods=['GET'])
@app.route('/posts/', methods=['GET'])
def get_post(post_id=None):
    full_name = ""
    if post_id is None:
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            'description': "Post id is required."
        }
    try:
        post = Posts.query.filter_by(id=post_id).first()
        if post.publisher is not None:
            user = Users.query.filter_by(id=post.publisher).first()
            if user is not None:
                full_name = user.name
        if post is None:
            return {
                'status_code': 200,
                'status_msg': "NO VALID POST ID.",
                'description': "NO VALID POST ID."
            }

        return {
            'status_code': 200,
            'status_msg': "",
            'content': {
                'id': post.id,
                'description': post.description,
                'publisher': f"{full_name}"}
        }
    except InternalError:
        db.session.rollback()
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            "description": f"Something going wrong. Error: {InternalError}",
        }


@app.route('/posts', methods=['POST'])
def create_post():
    try:
        post = Posts(title=request.json['title'], description=request.json['description'],
                     published=request.json['published'], publisher=request.json['publisher'])
        db.session.add(post)
        db.session.commit()

        if post.id is None:
            return {
                'status_code': 408,
                'status_msg': 'Request Timeout',
                'description': "Something going wrong . Please try again."
            }

        return {
            'id': post.id,
            'status_code': 201,
            'status_msg': 'created',
            "description": f"Post with id {post.id} successfully created."
        }
    except InternalError:
        db.session.rollback()
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            "description": f"Something going wrong. Error: {InternalError}",
        }


@app.route('/posts/<post_id>', methods=['PUT'])
@app.route('/posts/', methods=['PUT'])
def update_post(post_id=None):
    if not request.json:
        return {
            'status_code': 204,
            'status_msg': 'No Content',
            'description': "No Content."
        }
    elif post_id is None:
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            'description': "Post id is required."
        }
    else:
        try:
            post = Posts.query.filter_by(id=post_id).first()
            if post is None:
                return {
                    'status_code': 400,
                    'status_msg': 'Bad Request',
                    'description': f"Unable to find post with id {post_id}"
                }
            for item in request.json:
                if item == 'id':
                    continue
                post.item = request.json[item]
                db.session.commit()
            return {
                'id': post.id,
                'status_code': 200,
                'status_msg': "200",
                "description": f"Post id : {post.id} successfully updated."
            }
        except InternalError:
            db.session.rollback()
            return {
                'status_code': 400,
                'status_msg': 'Bad Request',
                "description": f"Something going wrong. Error: {InternalError}",
            }


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = Users(username=request.json['username'], email=request.json['email'], name=request.json['name'])
        db.session.add(user)
        db.session.commit()

        if user.id is None:
            return {
                'status_code': 408,
                'status_msg': 'Request Timeout',
                'description': "Something going wrong .Unable to create new user. Please try again."
            }

        return {
            'id': user.id,
            'status_code': 201,
            'status_msg': 'created',
            "description": f"User created successfully."
        }
    except InternalError:
        db.session.rollback()
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            "description": f"Something going wrong. Error: {InternalError}",
        }


@app.route('/posts/delete/<post_id>', methods=['DELETE'])
def delete_post(post_id=None):
    if post_id is None:
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            'description': "Post id is required."
        }

    if post_id:
        try:
            post = Posts.query.filter_by(id=post_id).first()
            if post is None:
                return {
                    'status_code': 400,
                    'status_msg': 'Bad Request',
                    'description': "Not valid post id."
                }
            db.session.delete(post)
            db.session.commit()
            return {
                'id': post.id,
                'status_code': 200,
                'status_msg': 'delete',
                "description": f"Post id {post.id} successfully deleted."
            }
        except InternalError:
            db.session.rollback()
            return {
                'status_code': 400,
                'status_msg': 'Bad Request',
                "description": f"Something going wrong. Error: {InternalError}",
            }


@app.route('/posts/delete_all', methods=['DELETE'])
def delete_all_posts():
    try:
        num_rows_deleted = db.session.query(Posts).delete()
        db.session.commit()
        return {
            'status_code': 200,
            'status_msg': 'delete',
            "description": f"All posts successfully deleted.",
            "Num of deleted rows": num_rows_deleted
        }
    except InternalError:
        db.session.rollback()
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            "description": f"Something going wrong. Error: {InternalError}",
        }


@app.route('/posts/published')
def get_published_posts():
    try:
        output = []
        posts = Posts.query.filter(Posts.published == True).all()
        if len(posts) == 0:
            return {
                'status_code': 204,
                'status_msg': 'No Content',
                'description': "No any posts found."
            }

        for post in posts:
            data = {'title': post.title, 'description': post.description}
            output.append(data)

        return {
            'status_code': 200,
            'status_msg': "OK",
            "content": {'posts': output},
            "total_items": len(output)
        }
    except InternalError:
        db.session.rollback()
        return {
            'status_code': 400,
            'status_msg': 'Bad Request',
            "description": f"Something going wrong. Error: {InternalError}",
        }
