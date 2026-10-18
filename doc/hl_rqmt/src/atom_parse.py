
import re

from parsec import *
from lex.ignore_parse import *

lexeme = lambda p: p << ignore  # skip all ignored characters.

lparen = lexeme(string('('))
rparen = lexeme(string(')'))
lbrac = lexeme(string('['))
rbrac = lexeme(string(']'))
lqbrac = lexeme(string('{'))
rqbrac = lexeme(string('}'))

lgroup_lit = lparen | lbrac | lqbrac
rgroup_lit = rparen | rbrac | rqbrac

#number = lexeme(regex(r'\d+')) # .parsecmap(int)
number = lexeme(regex(r'-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?')) # .parsecmap(int)

#indenifier = lexeme(regex(r'[\d\w_!$/:%&*?~+-]+'))
#indenifier = lexeme(regex(r'[\d\w_!$/./:%&*?~+-]+'))
indenifier = lexeme(regex(r'[\d\w_!$\.\:%&*?~+-]+'))
operator = lexeme(regex(r'[=\/\*\+-<>]'))

true = lexeme(string('true')) # .result('true')
false = lexeme(string('false')) # .result('false')

def charseq():
    '''Parse string. (normal string and escaped string)'''
    def string_part():
        '''Parse normal string.'''
        return regex(r'[^"\\]+')

    def string_esc():
        '''Parse escaped string.'''
        return string('\\') >> (
            string('\\')
            | string('/')
            | string('"')
            | string('b').result('\b')
            | string('f').result('\f')
            | string('n').result('\n')
            | string('r').result('\r')
            | string('t').result('\t')
            | regex(r'u[0-9a-fA-F]{4}').parsecmap(lambda s: chr(int(s[1:], 16)))
        )
    return string_part() | string_esc()

@lexeme
@generate
def quoted_string():
    '''Parse quoted string.'''
    yield string('"')
    body = yield many(charseq())
    yield string('"')
    return ''.join(body)

atom = number | quoted_string | indenifier | operator | (true ^ false)
