# coding: utf-8
from .zako_yacc import ParseTree
from .zako_parser import parser, exceptions, names


class StrategyCompiler(object):
    def __init__(self, file_like_object):
        self.target = file_like_object
        self.tree = ParseTree(self.target)

    @property
    def parse_tree(self):
        ''' 获取策略的语法树元组

        其中元组的第一个值为语法树，第二个值为异常信息，二者异或永远为 True
        '''
        if not self.tree.data and not self.tree.exceptions:
            self.tree.parse()
        return str(self.tree.data), self.tree.exceptions

    def __call__(self, CUR, COUNT, FLAG):
        ''' 策略运算，需要入参上一回合对方的输出结果以及当前回合数
        '''
        names.update(FLAG=FLAG)
        names.update(LCUR=CUR)
        names.update(COUNT=COUNT)
        self.result = parser.parse(self.target)
        return self.result


if __name__ == '__main__':
    pass
