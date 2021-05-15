from flask import render_template, request, jsonify

from app import app, db
from app.models import Posts


@app.route('/')
def index():
    return 'Hello!'


@app.route('/posts')
def get_posts():
    output = []
    for post in Posts.query.all():
        data = {'title': post.title, 'description': post.description}
        output.append(data)

    return {'status_code': 200, "content": {'posts': output}, "items": len(output)}


@app.route('/post/<post_id>', methods=['GET'])
@app.route('/post/', methods=['GET'])
def get_post(post_id=None):
    if request.json is None:
        return jsonify({
            'status_code': 400, 'Error': 'Bad Request',
            'Error Description': "Post id is required."})
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        return jsonify({'status_code': 200, 'Error': "NO VALID POST ID."})
    return jsonify({
        'status_code': 200,
        'content': {'id': post.id, 'description': post.description},
        "message": f""
    })


@app.route('/posts', methods=['POST'])
def create_post():
    post = Posts(title=request.json['title'], description=request.json['description'],
                 published=request.json['published'])
    db.session.add(post)
    db.session.commit()
    return {'id': post.id, 'status_code': 200, "message": f"Post id : {post.id} successfully created."}


@app.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id=None):
    if post_id is None:
        return "Unable to update post. Post id is required."
    else:
        post = Posts.query.filter_by(id=request.json['id']).first()
        for item in request.json:
            if item == 'id':
                continue
            post.item = request.json[item]
            db.session.commit()
    return {'id': post.id, 'status_code': 200, "message": f"Post id : {post.id} successfully updated."}
