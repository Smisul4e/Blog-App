from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)

def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)

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

@app.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    posts = load_posts()
    posts = [post for post in posts if post['id'] != post_id]
    save_posts(posts)
    return '', 204

if __name__ == '__main__':
    app.run()
