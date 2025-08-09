from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Naming convention to avoid migration issues
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Article(db.Model, SerializerMixin):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    preview = db.Column(db.String)
    minutes_to_read = db.Column(db.Integer)
    date = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Prevent recursion in relationships
    serialize_rules = ('-user.articles',)

    def __repr__(self):
        return f'Article {self.id} by {self.author}'

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    articles = db.relationship('Article', backref='user')

    # Prevent recursion
    serialize_rules = ('-articles.user',)

    def __repr__(self):
        return f'User {self.name}, ID {self.id}'
