from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Blog Post Class/Model
class BlogPost(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), unique=True)
  content = db.Column(db.String(200))

  def __init__(self, title, content):
    self.title = title
    self.content = content

# Blog Post Schema
class BlogPostSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'content')

# Init schema
blog_post_schema = BlogPostSchema()
blog_posts_schema = BlogPostSchema(many=True)

# Create a Blog Post
@app.route('/blog_post', methods=['POST'])
def add_blog_post():
  title = request.json['title']
  content = request.json['content']

  new_blog_post = BlogPost(title, content)

  db.session.add(new_blog_post)
  db.session.commit()

  return blog_post_schema.jsonify(new_blog_post)

# Get All Blog Posts
@app.route('/blog_post', methods=['GET'])
def get_blog_posts():
  all_blog_posts = BlogPost.query.all()
  result = blog_posts_schema.dump(all_blog_posts)
  return jsonify(result)

# Run Server
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True)

