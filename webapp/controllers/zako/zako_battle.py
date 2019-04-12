# coding: utf-8
from collections import namedtuple
from .zako_strategy import StrategyCompiler

peace_rules = [
    [(1, 1), (5, 0)],
    [(0, 5), (3, 3)]
]


def battle(battle_round, attacker, defender):
    ''' 入参对战回合数以及对抗双方的语法树, 得到各自的比分,以及对抗经过
    '''
    score_of_attacker = 0
    score_of_defender = 0
    record_for_attacker = [-1]
    record_for_defender = [-1]
    attacker_worked = StrategyCompiler(attacker)
    defender_worked = StrategyCompiler(defender)
    pass_of_battle = []
    nt = namedtuple("round", ["attacker_choice", "attacker_current_score",
                              "defender_choice", "defender_current_score"])
    # 处理第一回合
    # 相互处理各自的比分
    attacker_choice = int(attacker_worked(1, 1, False))
    record_for_attacker.append(attacker_choice)
    defender_choice = int(defender_worked(1, 1, False))
    record_for_defender.append(defender_choice)
    # 计算回合分数
    temp_a, temp_b = peace_rules[attacker_choice][defender_choice]
    score_of_attacker += temp_a
    score_of_defender += temp_b
    # 保存回合对战结果
    round_com = nt(attacker_choice=attacker_choice, attacker_current_score=score_of_attacker,
                   defender_choice=defender_choice, defender_current_score=score_of_defender)
    pass_of_battle.append(round_com)

    for i in range(2, battle_round+1):
        attacker_choice = int(attacker_worked(
            record_for_defender[i-1], i, not all(record_for_defender)))
        record_for_attacker.append(attacker_choice)
        defender_choice = int(defender_worked(
            record_for_attacker[i-1], i, not all(record_for_attacker)))
        record_for_defender.append(defender_choice)
        # 计算回合分数
        temp_a, temp_b = peace_rules[attacker_choice][defender_choice]
        score_of_attacker += temp_a
        score_of_defender += temp_b
        # 保存回合对战结果
        round_com = nt(attacker_choice=attacker_choice, attacker_current_score=score_of_attacker,
                       defender_choice=defender_choice, defender_current_score=score_of_defender)
        pass_of_battle.append(round_com)

    return score_of_attacker, score_of_defender, pass_of_battle
