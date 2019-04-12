# coding: utf-8
''' main.py 主控制器蓝图
'''
import os
import time
import random
from io import BytesIO
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from flask import render_template, Blueprint, redirect, url_for, flash, session, request, make_response, g
from webapp.models import db, User, Role, PostCategory
from webapp.forms import LoginForm, RegisterForm
from webapp.identicon import render_identicon

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)


@main_blueprint.before_request
def check_user():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session["username"]
        ).one()
    else:
        g.current_user = None


def validate_picture():
    ''' 生成验证码
    '''
    total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
    # 图片大小130 x 50
    width = 130
    heighth = 50
    # 先生成一个新图片对象
    im = Image.new('RGB', (width, heighth), 'white')
    # 设置字体
    font = ImageFont.truetype('arial.ttf', 40)
    # font = ImageFont.load_default().font
    # font.size = 40
    # 创建draw对象
    draw = ImageDraw.Draw(im)
    str = ''
    # 输出每一个文字
    for item in range(5):
        text = random.choice(total)
        str += text
        draw.text((5+random.randint(4, 7)+20*item, 5 +
                   random.randint(3, 7)), text=text, fill='black', font=font)

    # 划几根干扰线
    for num in range(8):
        x1 = random.randint(0, width/2)
        y1 = random.randint(0, heighth/2)
        x2 = random.randint(0, width)
        y2 = random.randint(heighth/2, heighth)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    # 模糊下,加个帅帅的滤镜～
    im = im.filter(ImageFilter.FIND_EDGES)
    return im, str


@main_blueprint.route('/')
def index():
    notice = "新站上线，请多关照！"
    # notice = ""
    return render_template('index.html', title="主页", notice=notice)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('.index'))

    return render_template('login.html', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(form.username.data)
        user.set_password(form.password.data)
        user.activated = True
        user.email = form.email.data
        user.roles.append(Role.query.filter_by(title='default').first())
        db.session.add(user)
        db.session.commit()

        session['username'] = form.username.data
        # 生成头像
        image_size = 40
        img = render_identicon(str(user.id ^ int(time.time()))[::-1], image_size)
        img.save(os.path.join(main_blueprint.root_path, "..", "static", 'uploads',
                              'avatars', '%s.jpg' % user.username))
        return redirect(url_for('.index'))
    return render_template('register.html', form=form)


@main_blueprint.route('/verify_code')
def get_verify_code():
    image, string = validate_picture()
    # 将验证码图片以二进制形式写入在内存中，防止将图片都放在文件夹中，占用大量磁盘
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把二进制作为response发回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = string
    return response


@main_blueprint.route('/home/<string:username>')
def home(username):
    if not g.current_user or g.current_user.username != username:
        flash('请先登录再查看主页!', category='error')
        return redirect(url_for('main.login'))
    user = User.query.filter_by(
        username=username
    ).first()
    return render_template('home.html', user=user)


@main_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))
