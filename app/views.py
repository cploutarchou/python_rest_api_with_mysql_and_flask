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

    return {'posts': output}


@app.route('/posts/<id>')
def get_post(post_id: str):
    post = Posts.query.get_or_404(id)
    return jsonify({'id': post.id, 'description': post.description})


# insert_drinks()
@app.route('/posts', methods=['POST'])
def create_drink():
    post = Posts(title=request.json['name'], description=request.json['description'],
                 published=request.json['published'])
    db.session.add(post)
    db.session.commit()
    return {'id': post.id}
