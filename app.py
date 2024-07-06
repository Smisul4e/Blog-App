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


@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    posts = load_posts()
    for post in posts:
        if post['id'] == id:
            post['likes'] = post.get('likes', 0) + 1
            break

    save_posts(posts)
    return redirect(url_for('index'))


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run()
