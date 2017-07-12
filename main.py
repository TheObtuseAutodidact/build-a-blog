from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import os

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:{}@localhost:8889/build-a-blog'.format(os.environ['RDS_PASSWORD2']) #user:password
app.config['SQLALCHEMY_ECHO'] = True # show sql generated by sqlalchemy

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    # owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        # self.owner = owner


@app.route("/", methods=["POST", "GET"])
def blog_post():
    if request.method == "POST":
        title = request.form['blog_title']
        body = request.form['blog_post']

        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()

        return redirect("/")
    posts = Blog.query.order_by(desc(Blog.id))
    return render_template("index.html", posts=posts)

if __name__ == '__main__':
    app.run()