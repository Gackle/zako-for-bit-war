# coding: utf-8
import os
from sqlalchemy import func
from flask_script import Manager, Server
from flask_script.commands import Clean, ShowUrls
from webapp import create_app
from webapp.models import db, User, Role, Script, Post, Comment, PostCategory

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

manager = Manager(app)

manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.command
def setup():
    db.create_all()

    admin_role = Role("admin")
    admin_role.description = "admin"
    db.session.add(admin_role)

    default_role = Role("default")
    default_role.description = "default"
    db.session.add(default_role)

    guest_role = Role("guest")
    guest_role.description = "guest"
    db.session.add(guest_role)

    db.session.commit()

    admin = User("Admin")
    admin.nickname = "管理员"
    admin.email = "example@gmail.com"
    admin.set_password('admin')
    admin.roles.append(admin_role)
    db.session.add(admin)

    official = User("PublicOfficial")
    official.nickname = "公共库用户"
    official.email = "official@gmail.com"
    official.set_password('official')
    admin.roles.append(admin_role)
    db.session.add(official)

    db.session.commit()

    # 创建原始公共库目录（共5个）
    script1 = Script('always_work.sg')
    script1.content = """Strategy T1:
    return 1"""
    script1.description = "永远合作"
    script1.user = official
    script1.is_private = False
    db.session.add(script1)

    script2 = Script('random_example.sg')
    script2.content = "Strategy T2:i = RANDOM(1);if(i==0){return 0}else{return 1}"
    script2.description = "`听天由命`，背叛与合作的几率为 50% （RANDOM 为系统范围内真随机）"
    script2.user = official
    script2.is_private = False
    db.session.add(script2)

    script3 = Script('slow_work.sg')
    script3.content = "Strategy T3:if(COUNT == 1){return 1}else{return CUR}"
    script3.description = "`慢半拍`：开局合作，随后一直跟随对方上一轮的选择"
    script3.user = official
    script3.is_private = False
    db.session.add(script3)

    script4 = Script('elusive_work.sg')
    script4.content = "Strategy T4:if (COUNT == 1){return 1}else {i = RANDOM(9);if (i == 9){return 0}else{return CUR}}"
    script4.description = "改进版`慢半拍`，开局合作，随后随机自我背叛，大几率跟随对方上一轮的选择"
    script4.user = official
    script4.is_private = False
    db.session.add(script4)

    script5 = Script('never_forgive.sg')
    script5.content = "Strategy T5:if(FLAG){return 0}else{return 1}"
    script5.description = "永不原谅，只要对方存在过背叛行为，就一直背叛"
    script5.user = official
    script5.is_private = False
    db.session.add(script5)

    db.session.commit()

    # 创建文章评论
    comment1 = Comment('comment1')
    comment1.user = admin
    comment2 = Comment('comment2')
    comment2.user = official
    comment3 = Comment('comment3')
    comment3.user = admin
    db.session.add(comment1)
    db.session.add(comment2)
    db.session.add(comment3)
    db.session.commit()

    post1 = Post('Post1', 'Content1')
    post1.user = official
    post1.category = PostCategory.General
    post1.comments.append(comment1)
    post1.comments.append(comment2)

    post2 = Post('Post2', 'Content2')
    post2.user = admin
    post2.category = PostCategory.Feedback
    post2.comments.append(comment3)

    db.session.add(post1)
    db.session.add(post2)

    db.session.commit()


@manager.shell
def make_shell_context():
    '''
    创建一个 Python 命令行，并且在应用上下文中执行。
    返回的字典会告诉 Flask Script 在打开命令行时进行一些默认的导入工作
    '''
    return dict(app=app, db=db, User=User, Role=Role, Script=Script, Post=Post, Comment=Comment, func=func)


if __name__ == '__main__':
    manager.run()
