# coding: utf-8
''' forum 论坛控制器视图
'''
import datetime
from collections import namedtuple
from sqlalchemy import func
from flask import render_template, Blueprint, redirect, url_for, flash, session, request, make_response, g, abort
from webapp.models import db, User, Post, Comment, PostCategory
from webapp.forms import PostForm, CommentForm, select_choice_names


forum_blueprint = Blueprint(
    'forum',
    __name__,
    template_folder='../templates/forum',
    url_prefix='/forum'
)

category_tuple = namedtuple('Category', ['code', 'name'])
sort_key_tuple = namedtuple('SortKey', ['code', 'name'])


categories = {k: v for (k, v) in [(x.code, x) for x in (category_tuple(
    x[0], x[1]) for x in zip([i.name for i in PostCategory], select_choice_names))]}
sort_keys = {
    'recent': sort_key_tuple('recent', '最新'),
    'hotest': sort_key_tuple('hotest', '最热')
}


@forum_blueprint.before_request
def check_user():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session["username"]
        ).one()
    else:
        g.current_user = None


@forum_blueprint.route('/<string:category>/<string:sort_key>')
def index(category, sort_key):
    page = request.args.get('p', 1, type=int)
    print(page)
    if category not in categories.keys():
        abort(404)
    if sort_key not in sort_keys.keys():
        abort(404)
    if sort_key == "recent":
        posts = db.session.query(Post, func.count(Comment.post_id).label(
            'total_comments')).join(Comment, isouter=True).filter(Post.category == category).group_by(Post.id).order_by(Post.publish_date.desc()).paginate(int(page), 10, False)
    else:
        posts = db.session.query(Post, func.count(Comment.post_id).label('total_comments')).join(Comment, isouter=True).filter(
            Post.category == category).group_by(Post.id).order_by('total_comments DESC').paginate(int(page), 10, False)
    return render_template('forum.html', category=categories[category], sort=sort_keys[sort_key], posts=posts)


@forum_blueprint.route('/t/<int:post_id>', methods=['GET', 'POST'])
def get_post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if g.current_user and form.validate_on_submit():
        comment = Comment(form.text.data)
        comment.post_id = post_id
        comment.user_id = g.current_user.id
        comment.date = datetime.datetime.now()
        db.session.add(comment)
        db.session.commit()
        form.text.data = ""

    return render_template('post.html', post=post, form=form)


@forum_blueprint.route('/add', methods=['GET', 'POST'])
def add_post():
    if not g.current_user:
        flash('发表新想法前请先登录!', category='error')
        return redirect(url_for('main.login'))
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(form.title.data, form.content.data)
        new_post.publish_date = datetime.datetime.now()
        new_post.user = g.current_user
        new_post.category = PostCategory(form.category.data)

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('.get_post', post_id=new_post.id))

    return render_template('add.html', form=form)
