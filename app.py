from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
data_file = os.path.join(os.path.dirname(__file__), 'data.json')


def json_file(mode,var=None):
    """Reads and writes data from/to json"""
    with open('data.json', mode , encoding='utf-8') as fileobj:
        if mode == 'w':
            json.dump(var, fileobj, indent=4)
        elif mode == 'r':
            return json.load(fileobj)


# check if json file exists
if not os.path.exists(data_file):
    blog_posts = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post.", "likes": 0},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post.", "likes": 0}
    ]
    json_file('w',blog_posts)
else:
    blog_posts = json_file('r')


def find_post_by_id(post_id):
    """Find a post by its id"""
    return next((post for post in blog_posts if post["id"] == post_id), None)


@app.route('/')
def index():
    """Renders the homepage"""
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Adds new post to the blog list"""
    post = {}
    if request.method == 'POST':

        # Generate a new id for the post
        new_id = max((blog_post['id'] for blog_post in blog_posts), default=0) + 1
        post['id'] = new_id

        # Fill the post with new data
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        post['likes'] = 0

        # Add the post to the list
        blog_posts.append(post)

        # Save to file
        json_file('w',blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes post"""
    post = find_post_by_id(post_id) # Find the post by id
    blog_posts.remove(post) # remove post
    json_file('w',blog_posts) # Save to file

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Updates post"""
    # Find the post by id
    post = find_post_by_id(post_id)
    if not post:
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with new data
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save to file
        json_file('w',blog_posts)

        return redirect(url_for('index'))

    # GET request → render the form with current values
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def likes(post_id):
    """Counts likes"""
    post = find_post_by_id(post_id) # Find the post by id
    post['likes'] += 1 # update likes
    json_file('w',blog_posts) # Save to file

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)