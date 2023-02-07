from  flask import Flask,render_template,redirect,flash,request,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
app.app_context().push()
app.secret_key = 'oasis'


# Creating database
class blogpost(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),nullable = False)
    author = db.Column(db.String(50),nullable = False,default = 'Tech Watt')
    content = db.Column(db.Text,nullable = False)
    dateposted = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
    def __repr__(self) -> str:
        return 'blogpost '+ str(self.id)


@app.route('/')
def home():
    return render_template('base.html')

# Post blog route
@app.route('/posts',methods =['POST','GET'])
def posts():
    if request.method == 'POST':
        post_title = request.form.get('title')
        post_author =request.form.get('author')
        post_content =request.form.get('content')
        posts = blogpost(title=post_title,author = post_author,content = post_content)
        db.session.add(posts)
        db.session.commit()
        return redirect('/posts')
    else:
        posts = blogpost.query.order_by(blogpost.dateposted).all()
        return render_template('posts.html',posts = posts)

# Deleting post
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

# For viewers
@app.route('/blogs',methods=(['POST','GET']))
def blogs():
    posts = blogpost.query.order_by(blogpost.dateposted).all()
    return render_template('blogs.html',posts = posts)

# Editing Posts
@app.route('/posts/edit/<int:id>',methods=(['POST','GET']))
def edit(id):
    posts = blogpost.query.get_or_404(id)
    if request.method == 'POST':
        posts.title = request.form.get('title')
        posts.author = request.form.get('author')
        posts.content = request.form.get('content')
        db.session.commit()
        return redirect('/posts')
    else: 
        return render_template('edit.html',posts = posts)


# About Page
@app.route('/about')
def about():
    return render_template('about.html')



if __name__=="main":
    app.run(debug=True)