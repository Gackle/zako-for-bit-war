# coding: utf-8
import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

from .extensions import bcrypt

db = SQLAlchemy()

roles = db.Table('role_users',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                 db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                 )


class PostCategory(Enum):
    General = 1             # 综合
    QA = 2                  # 问答求助
    Reality = 3             # 三次元
    TechTalk = 4            # 技术讨论
    Feedback = 99           # 意见反馈


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column('user_name', db.String(255), nullable=False)
    password = db.Column(db.String(255))
    email = db.Column(db.String(30), nullable=False, unique=True)
    nickname = db.Column('nick_name', db.String(255), default="TestUser")
    createtime = db.Column('create_time', db.DateTime())
    activated = db.Column(db.Boolean(), default=False)
    scripts = db.relationship(
        'Script',
        backref='user',
        lazy='dynamic'
    )
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )
    comments = db.relationship(
        'Comment',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username):
        self.username = username
        self.nickname = username
        self.createtime = datetime.datetime.now()

    def __repr__(self):
        return '[User {} - {}]'.format(self.id, self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '[Role {} - {}]'.format(self.id, self.title)


class Script(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    createtime = db.Column('create_time', db.DateTime(), nullable=False)
    content = db.Column(db.Text())
    description = db.Column(db.Text())
    usable = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    is_private = db.Column(db.Boolean(), default=True)

    def __init__(self, name):
        self.name = name
        self.createtime = datetime.datetime.now()

    def __repr__(self):
        return '[Script {}-{} by {}]'.format(self.id, self.name, self.user.username)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    publish_date = db.Column('publish_date', db.DateTime(), nullable=False)
    content = db.Column(db.Text())
    category = db.Column(db.Enum(PostCategory),
                         nullable=False, default=PostCategory.General)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )

    def __init__(self, title, content):
        self.publish_date = datetime.datetime.now()
        self.title = title
        self.content = content

    def __repr__(self):
        return "<Post {}: `{} - {}`>".format(self.id, self.title, self.user)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __init__(self, text):
        self.date = datetime.datetime.now()
        self.text = text

    def __repr__(self):
        return "<Comment `{}`>".format(self.text[:15])
