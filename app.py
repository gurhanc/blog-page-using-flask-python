from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    title = db.Column(db.String(120))
    subtitle = db.Column(db.String(200))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()
db.session.commit()

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/',methods=['GET'])
def index():
    posts = Blogpost.query.all()
    return render_template('index.html',posts=posts)

@app.route('/add', methods=['GET'])
def post():
    return render_template('add.html')

@app.route('/addPost', methods=['POST'])
def add_post():
    title = request.form['title']
    subtitle = request.form['subtitle']
    content = request.form['content']
    author = request.form['author']
    post = Blogpost(author=author, title=title, subtitle=subtitle, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=['GET'])
def delete():
    posts = Blogpost.query.all()
    return render_template('delete.html',posts=posts)

@app.route('/deletePost', methods=['POST'])
def delete_post():
    Blogpost.query.filter_by(id=request.form["id"]).delete()
    db.session.commit()
    return redirect(url_for('delete'))

@app.route('/posts/<id>', methods=['GET'])
def read_post(id):
    post = Blogpost.query.filter_by(id=id).first()
    return render_template('read.html',post=post)


@app.route('/view/<id>', methods=['GET'])
def view_post(id):
    post = Blogpost.query.filter_by(id=id).first()
    return render_template('read.html',post=post)

@app.route('/update/<id>', methods=['GET'])
def update_post(id):
    post = Blogpost.query.filter_by(id=id).first()
    return render_template('update.html',post=post)

@app.route('/do_update/<id>', methods=['POST'])
def do_update_post(id):
    post = Blogpost.query.filter_by(id=id).first()
    post.title = request.form['title']
    post.subtitle = request.form['subtitle']
    post.content = request.form['content']
    post.author = request.form['author']
    post = Blogpost(title=post.title, subtitle=post.subtitle, content=post.content, author=post.author, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
    
    
    