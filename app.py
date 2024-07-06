from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


# Assuming you have functions to load and save blog posts
def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = next((post for post in posts if post['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run()
