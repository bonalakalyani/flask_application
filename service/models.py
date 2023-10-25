from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

ma = Marshmallow()
db = SQLAlchemy()
#narsimha

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def is_correct_password(self, password):
        return check_password_hash(self.password, password)


class BlacklistedToken(db.Model):
    __tablename__ = 'BlacklistedToken'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)


class UserSchema(ma.Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


# Other models for reference
# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True)
#     comment = db.Column(db.String(256), nullable=False)
#     creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
#     category = db.relationship('Category', backref=db.backref('comments', lazy='dynamic'))
#     type = db.Column(db.String(24), nullable=True)
#
#     def __init__(self, comment, category_id):
#         self.comment = comment
#         self.category_id = category_id
#
#
# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), unique=True, nullable=False)
#
#     def __init__(self, name):
#         self.name = name
#
#
# class CategorySchema(ma.Schema):
#     id = fields.Integer()
#     name = fields.String(required=True)
#
#
# class CommentSchema(ma.Schema):
#     id = fields.Integer(dump_only=True)
#     category_id = fields.Integer(required=True)
#     comment = fields.String(required=True, validate=validate.Length(1))
#     creation_date = fields.DateTime()
