from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


# Функция за зареждане на блог постовете от JSON файл
def load_posts():
    with open('posts.json', 'r') as file:
        return json.load(file)


# Функция за запис на блог постовете в JSON файл
def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file, indent=4)


# Маршрут за увеличаване на броя лайкове на блог пост
@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    posts = load_posts()
    for post in posts:
        if post['id'] == id:
            post['likes'] = post.get('likes', 0) + 1
            break

    save_posts(posts)
    return redirect(url_for('index'))


# Маршрут за добавяне на нов блог пост
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            'id': len(posts) + 1,  # Генериране на уникален ID за новия блог пост
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content'],
            'likes': 0  # Нулиране на броя лайкове за новия блог пост
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')


# Маршрут за показване на всички блог постове
@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


# Маршрут за изтриване на блог пост
@app.route('/delete/<int:id>')
def delete(id):
    posts = load_posts()
    for post in posts:
        if post['id'] == id:
            posts.remove(post)
            save_posts(posts)
            break

    return redirect(url_for('index'))


# Маршрут за показване на формата за обновяване на блог пост
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    posts = load_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
