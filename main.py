from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'yzXK27&&Fyr76sLLwD8'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')   

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')
    if (blog_id):
        post = Blog.query.get(blog_id)
        return render_template('post.html', title="Blog Entry", post=post)
    post = Blog.query.all()
    return render_template('blogs.html', title="Blogosphere", posts=post)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title =='' or body=='':
            flash('Title and body cannot be blank')
            return render_template('newpost.html', titleb=title, bodyb=body)
        else:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            post = {
                    'title': title,
                    'body': body
                    }
            return render_template('post.html', post=post)
    return render_template('newpost.html')



if __name__ == '__main__':
    app.run()
