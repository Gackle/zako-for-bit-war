import datetime
import json
from os import path
from flask import (
    render_template,
    Blueprint,
    redirect,
    url_for,
    session,
    g,
    flash,
    abort,
    request,
    make_response
)

from webapp.models import db, User, Script
from .zako_strategy import StrategyCompiler
from .zako_battle import battle

zako_blueprint = Blueprint(
    'zako',
    __name__,
    template_folder=path.join(path.pardir, '..', 'templates', 'zako'),
    url_prefix='/zako'
)


@zako_blueprint.before_request
def check_user():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session["username"]
        ).one()
    else:
        g.current_user = None


@zako_blueprint.route('/about')
def about():
    token_dict = {
        "Stategy": {
            "title": "策略开始标识",
            "usage": "Strategy T: expression",
            "description": "用法类似于常规编程语言中的 func 子程序。(必须)用在策略文件的开头，后面需要跟策略名 `T` 代表一个策略，`:` 后面是表达式。目前仅支持单文件单策略模式。",
        },
        "return": {
            "title": "策略结束标识",
            "usage": "return[ data]",
            "description": "用在策略结尾部分作为策略的输出结果。策略的输出结果会作为博弈的输入用于每一轮「博弈」过程中"
        },
        "COUNT": {
            "title": "当前博弈的回合数",
            "usage": "COUNT",
            "description": "保留字，用于获取当前「博弈」的回合数"
        },
        "FLAG": {
            "title": "「记忆伤痕」，表示是否被背叛过",
            "usage": "FLAG",
            "description": "保留字，判断直到目前为止的「博弈」中对方是否有过 “背叛” 选择"
        },
        "CUR": {
            "title": "「哨兵」，监视上一轮对方的选择",
            "usage": "COUNT",
            "description": "保留字，用于获取上一轮「博弈」时对方的选择"
        },
        "RANDOM": {
            "title": "随机函数",
            "usage": "RANDOM(n)",
            "description": "内置函数，随机返回 0 或 1"
        },
        "数据类型": {
            "title": "",
            "usage": "",
            "description": "由于在 Zako 语言中只存在 0 和 1，同时 0 也代表‘非判断’， 1 也代表 ‘是判断’"
        },
        "控制语句": {
            "title": "",
            "usage": "if (expression) {expression1} [else {expression2}]",
            "description": "常规语言的条件判断，负责实现分支流程，当 if(expression) 中的 expression 为是判断，则执行 expression1，否则，如果存在 else 分支，则执行 expression2 "
        }
    }

    token_list = ["数据类型", "控制语句", "Stategy",
                  "return", "COUNT", "FLAG", "CUR", "RANDOM"]
    return render_template(
        'about.html',
        token_list=token_list,
        token_dict=token_dict
    )


@zako_blueprint.route('/editor')
@zako_blueprint.route('/editor/<int:script_id>')
def editor(script_id=0):
    if script_id:
        script = Script.query.get(script_id)
        if script.user != g.current_user:
            abort(403)
        else:
            return render_template('editor.html', id=script.id, name=script.name, content=script.content, description=script.description)
    else:
        return render_template('editor.html')


@zako_blueprint.route('/verify', methods=['POST'])
def verify():
    content = request.values.get('content')
    if content is None or content == '':
        response = make_response('content 为空')
        response.status_code = 500
        return response
    strategy = StrategyCompiler(content)
    data = {'tree': strategy.parse_tree[0],
            'exception': strategy.parse_tree[1]}
    return json.dumps(data)


@zako_blueprint.route('/script/<script_id>', methods=['POST'])
@zako_blueprint.route('/script/', methods=['POST'])
def save_script(script_id=0):
    # 登录校验
    if not g.current_user:
        response = make_response('请先登录方可为自己保存策略脚本！')
        response.status_code = 403
        return response

    # 数据合法性校验
    name = request.values.get('name')
    if name is None or name == '':
        response = make_response('请填写文件名以便查找！')
        response.status_code = 501
        return response
    name = name+".sg" if not name.endswith('.sg') else name
    description = request.values.get('description', '')
    content = request.values.get('content')
    if content is None or content == '':
        response = make_response('请填写策略内容！')
        response.status_code = 501
        return response

    # 策略有效性校验
    try:
        strategy = StrategyCompiler(content)
        if strategy.parse_tree[1]:
            response = make_response('策略非法，请先校验！')
            response.status_code = 501
            return response

        if script_id != 0:
            script = Script.query.get(script_id)
        else:
            script = Script(name)
        script.content = content
        script.description = description
        script.user = g.current_user
        db.session.add(script)
        db.session.commit()

        response = {'message': '策略保存成功', 'id': script.id}

        return json.dumps(response)
    except Exception as e:
        response = {'message': '校验异常，请检查'}


@zako_blueprint.route('/scripts')
def get_scripts_library():
    public_library = Script.query.filter_by(
        is_private=False).order_by(Script.createtime)
    if g.current_user:
        private_library = Script.query.filter_by(
            user=g.current_user).order_by(Script.createtime.desc())
    else:
        private_library = []
    return render_template('library.html', public=public_library, private=private_library)


@zako_blueprint.route('/pve', methods=['GET'])
def pve():
    if not g.current_user:
        flash('请先登录再进行游戏!', category='error')
        return redirect(url_for('main.login'))
    public_library = Script.query.filter_by(
        is_private=False).order_by(Script.createtime)
    private_library = Script.query.filter_by(
        user=g.current_user).order_by(Script.createtime.desc())
    return render_template('pve.html', public=public_library, private=private_library)


@zako_blueprint.route('/fight', methods=['POST'])
def fight():
    if not g.current_user:
        return abort(403)
    attacker_id = request.values.get('attacker')
    defender_id = request.values.get('defender')
    round_number = int(request.values.get('round'))
    attacker_tree = Script.query.get(attacker_id).content
    defender_tree = Script.query.get(defender_id).content
    score_of_attacker, score_of_defender, pass_of_battle = battle(
        round_number, attacker_tree, defender_tree)
    # 处理战斗过程
    live = ""
    for index, item in enumerate(pass_of_battle):
        live += "第 {} 回合：<br/>".format(index+1)
        live += "玩家选择<b>{}</b>， 电脑选择<b>{}</b><br/>".format("合作" if item.attacker_choice ==
                                                           1 else "背叛", "合作" if item.defender_choice == 1 else "背叛")
        live += "当前比分 {} - {} <br/>".format(
            item.attacker_current_score, item.defender_current_score)
        live += "-----------------<br/>"
    # 处理最终结果
    if score_of_attacker > score_of_defender:
        flag = "victory"
    elif score_of_attacker == score_of_defender:
        flag = "draw"
    else:
        flag = "lose"
    data = {
        'flag': flag,
        'score': str(score_of_attacker) + ":" + str(score_of_defender),
        'live': live
    }
    return json.dumps(data)


@zako_blueprint.route('/pvp')
def pvp():
    return render_template('pvp.html')
