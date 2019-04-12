# coding: utf-8
from flask import session
from flask_wtf import FlaskForm
from wtforms import (
    widgets,
    StringField,
    PasswordField,
    TextAreaField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    URL,
    Email,
    Required
)
from .models import User, Post, Comment, PostCategory


class LoginForm(FlaskForm):
    username = StringField('用户名', [
        DataRequired("用户名必填")
    ])
    password = PasswordField('密码', [DataRequired("密码必填")])
    errors_msgs = []

    def validate(self):
        self.errors_msgs.clear()
        # 先调用父类的校验器 validators
        check_validate = super(LoginForm, self).validate()

        # 如果验证没有通过
        if not check_validate:
            return False

        # 检查用户是否存在
        user = User.query.filter_by(
            username=self.username.data
        ).first()

        if not user:
            self.username.errors.append('用户不存在')
            self.errors_msgs.append('用户不存在')
            return False

        if not user.check_password(self.password.data):
            self.username.errors.append('用户名或密码不正确')
            self.errors_msgs.append('用户名或密码不正确')
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField('用户名', [
        DataRequired(),
        Length(max=255)
    ])
    email = StringField('电子邮箱', [
        DataRequired(),
        Email()
    ])
    password = PasswordField('密码', [
        DataRequired(),
        Length(min=8)
    ])
    confirm = PasswordField('确认密码', [
        DataRequired(),
        EqualTo('password')
    ])
    verification_code = StringField('验证码', [
        DataRequired()
    ])
    errors_msgs = []

    def validate(self):
        self.errors_msgs.clear()
        # 先调用父类的校验器 validators
        check_validate = super(RegisterForm, self).validate()

        # 如果验证没有通过
        if not check_validate:
            return False

        if self.verification_code.data.lower() != session['image'].lower():
            self.errors_msgs.append('验证码有误,请重新输入')
            return False

        user = User.query.filter_by(
            email=self.email.data
        ).first()

        # 用户已存在
        if user and user.activated:
            self.errors_msgs.append('对应邮箱用户已存在, 请选择登陆')
            return False

        if user and not user.activated:
            self.errors_msgs.append('对应邮箱用户已存在尚未激活, 清先激活登陆')
            return False

        username = User.query.filter_by(
            username=self.username.data
        ).first()

        if username:
            self.errors_msgs.append('该用户名已被使用，请更换用户名')
            return False

        return True


select_choice_names = ['综合', '问答求助', '三次元', '技术讨论', '意见反馈']
select_field_choice = list(
    zip([x.value for x in PostCategory], select_choice_names))


class PostForm(FlaskForm):
    title = StringField('标题', [
        DataRequired(),
        Length(max=255)
    ])
    content = TextAreaField('内容', [DataRequired()])
    category = SelectField('分类', choices=select_field_choice, validators=[
                           DataRequired()], coerce=int)

    def validate(self):
        check_validate = super(PostForm, self).validate()
        return check_validate


class CommentForm(FlaskForm):
    text = TextAreaField('评论', [DataRequired()])

    def validate(self):
        check_validate = super(CommentForm, self).validate()
        return check_validate
