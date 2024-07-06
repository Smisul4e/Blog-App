from flask import Flask, jsonify, request, render_template, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/post', methods=['POST'])
def add_post():
    new_post = request.json
    posts = load_posts()
    new_post['id'] = max(post['id'] for post in posts) + 1 if posts else 1
    posts.append(new_post)
    save_posts(posts)
    return jsonify(new_post), 201


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        posts = load_posts()
        new_post = {
            'id': max(post['id'] for post in posts) + 1 if posts else 1,
            'author': author,
            'title': title,
            'content': content
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        posts = load_posts()
        for i, p in enumerate(posts):
            if p['id'] == post_id:
                posts[i] = post
                break
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()
