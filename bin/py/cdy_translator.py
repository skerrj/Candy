from __future__ import annotations

from collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping
from typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple
import math
import re
import cdy_rt.table
import cdy_rt.table_defs


class Sym(_cdy_NamedTuple):
    name: str

class Lst(_cdy_NamedTuple):
    items: tuple[Form, ...]

class Txt(_cdy_NamedTuple):
    val: str

class IntLit(_cdy_NamedTuple):
    val: int

class LongLit(_cdy_NamedTuple):
    val: int

class ByteLit(_cdy_NamedTuple):
    val: int

class FloatLit(_cdy_NamedTuple):
    val: float

class DoubleLit(_cdy_NamedTuple):
    val: float

class CharLit(_cdy_NamedTuple):
    val: str

class BoolLit(_cdy_NamedTuple):
    val: bool
type Form = Sym | Lst | Txt | IntLit | LongLit | ByteLit | FloatLit | DoubleLit | CharLit | BoolLit

def sym_name(form: Form) -> str:
    _cdy_t0: object = form
    if isinstance(_cdy_t0, Sym):
        name = _cdy_t0.name
        return name
    else:
        return ''

def list_items(form: Form) -> tuple[Form, ...]:
    _cdy_t1: object = form
    if isinstance(_cdy_t1, Lst):
        items = _cdy_t1.items
        return items
    else:
        return ()

def rest_of(forms: tuple[Form, ...]) -> tuple[Form, ...]:
    return forms[1:len(forms)]

def read_forms(text: str) -> tuple[Form, ...]:
    return read_source('', text)

def read_source(file: str, text: str) -> tuple[Form, ...]:
    return read_all(file, text, skip(text, 0), ())

def read_all(file: str, text: str, pos: int, acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (pos >= len(text)):
            return acc
        else:
            _tup = read_form(file, text, pos)
            form = _tup[0]
            next_ = _tup[1]
            pos, acc = (skip(text, next_), (acc + cdy_rt.table_defs.to_list(form)))
            continue

def skip(text: str, pos: int) -> int:
    while True:
        if (pos >= len(text)):
            return pos
        else:
            if cdy_rt.table_defs.isspace_at(text, pos):
                pos = (pos + 1)
                continue
            else:
                if (text[pos] == ';'):
                    pos = line_end(text, pos)
                    continue
                else:
                    return pos

def line_end(text: str, pos: int) -> int:
    while True:
        if ((pos >= len(text)) or (text[pos] == '\n')):
            return pos
        else:
            pos = (pos + 1)
            continue

def ends_at(text: str, pos: int) -> bool:
    return ((pos >= len(text)) or cdy_rt.table_defs.isspace_at(text, pos) or cdy_rt.table_defs.in_(text[pos], '();'))

def word_end(text: str, pos: int) -> int:
    while True:
        if ends_at(text, pos):
            return pos
        else:
            pos = (pos + 1)
            continue

def read_form(file: str, text: str, pos: int) -> tuple[Form, int]:
    ch = text[pos]
    if (ch == '('):
        return read_list(file, text, skip(text, (pos + 1)), (), pos)
    else:
        if (ch == ')'):
            return cdy_rt.table_defs.fail(parse_error(file, text, pos, 'unexpected )'))
        else:
            if (ch == '"'):
                return read_str(file, text, (pos + 1), '', pos)
            else:
                if (ch == '\\'):
                    return read_char(file, text, pos)
                else:
                    return read_atom(file, text, pos, word_end(text, pos))

def read_list(file: str, text: str, pos: int, acc: tuple[Form, ...], start: int) -> tuple[Form, int]:
    while True:
        if (pos >= len(text)):
            return cdy_rt.table_defs.fail(parse_error(file, text, start, '( is never closed'))
        else:
            if (text[pos] == ')'):
                return (Lst(acc), (pos + 1))
            else:
                _tup = read_form(file, text, pos)
                form = _tup[0]
                next_ = _tup[1]
                pos, acc = (skip(text, next_), (acc + cdy_rt.table_defs.to_list(form)))
                continue

def read_char(file: str, text: str, pos: int) -> tuple[Form, int]:
    if (((pos + 1) < len(text)) and (not cdy_rt.table_defs.isspace_at(text, (pos + 1))) and ends_at(text, (pos + 2))):
        return (CharLit(text[(pos + 1)]), (pos + 2))
    else:
        return cdy_rt.table_defs.fail(parse_error(file, text, pos, 'a char is \\ and one character, then a delimiter'))

def read_atom(file: str, text: str, pos: int, end: int) -> tuple[Form, int]:
    word = text[pos:end]
    kind = number_kind(word)
    if (kind != ''):
        return (number_form(word, kind), end)
    else:
        if (word == 'true'):
            return (BoolLit(True), end)
        else:
            if (word == 'false'):
                return (BoolLit(False), end)
            else:
                if symbol_start(text[pos]):
                    stop = symbol_end(text, (pos + 1))
                    return (Sym(text[pos:stop]), stop)
                else:
                    return cdy_rt.table_defs.fail(parse_error(file, text, pos, ('unexpected ' + str(text[pos]))))

def symbol_start(ch: str) -> bool:
    return (not (cdy_rt.table_defs.in_(ch, '\'#"\\') or cdy_rt.table_defs.is_decimal(ch)))

def symbol_end(text: str, pos: int) -> int:
    while True:
        if ((pos >= len(text)) or cdy_rt.table_defs.isspace_at(text, pos) or cdy_rt.table_defs.in_(text[pos], '()\'";\\')):
            return pos
        else:
            pos = (pos + 1)
            continue

def digits_end(word: str, pos: int) -> int:
    while True:
        if ((pos < len(word)) and cdy_rt.table_defs.is_decimal(word[pos])):
            pos = (pos + 1)
            continue
        else:
            return pos

def number_kind(word: str) -> str:
    start = (1 if (word[0] == '-') else 0)
    i = digits_end(word, start)
    rest = word[i:len(word)]
    if (i == start):
        return ''
    else:
        if (rest == ''):
            return 'int'
        else:
            if (rest == 'l'):
                return 'long'
            else:
                if (rest == 'b'):
                    return 'byte'
                else:
                    if (rest[0] == '.'):
                        j = digits_end(word, (i + 1))
                        _cdy_tail_55 = word[j:len(word)]
                        if (j == (i + 1)):
                            return ''
                        else:
                            if (_cdy_tail_55 == ''):
                                return 'double'
                            else:
                                if (_cdy_tail_55 == 'f'):
                                    return 'float'
                                else:
                                    return ''
                    else:
                        return ''

def number_form(word: str, kind: str) -> Form:
    body = word[0:(len(word) - 1)]
    if (kind == 'int'):
        return IntLit(cdy_rt.table_defs.to_int(word))
    else:
        if (kind == 'long'):
            return LongLit(cdy_rt.table_defs.to_int(body))
        else:
            if (kind == 'byte'):
                return ByteLit(cdy_rt.table_defs.to_int(body))
            else:
                if (kind == 'double'):
                    return DoubleLit(cdy_rt.table_defs.to_float(word))
                else:
                    return FloatLit(cdy_rt.table_defs.to_float(body))

def read_str(file: str, text: str, pos: int, acc: str, start: int) -> tuple[Form, int]:
    while True:
        if (pos >= len(text)):
            return cdy_rt.table_defs.fail(parse_error(file, text, start, 'string is never closed'))
        else:
            if (text[pos] == '"'):
                return (Txt(acc), (pos + 1))
            else:
                if (text[pos] == '\\'):
                    _tup = escape(file, text, pos)
                    ch = _tup[0]
                    next_ = _tup[1]
                    pos, acc = (next_, (acc + ch))
                    continue
                else:
                    pos, acc = ((pos + 1), (acc + text[pos]))
                    continue

def escape(file: str, text: str, pos: int) -> tuple[str, int]:
    c = (text[(pos + 1)] if ((pos + 1) < len(text)) else '')
    if cdy_rt.table_defs.in_(c, ('\\', '/', '"')):
        return (c, (pos + 2))
    else:
        if (c == 'b'):
            return ('\x08', (pos + 2))
        else:
            if (c == 'f'):
                return ('\x0c', (pos + 2))
            else:
                if (c == 'n'):
                    return ('\n', (pos + 2))
                else:
                    if (c == 'r'):
                        return ('\r', (pos + 2))
                    else:
                        if (c == 't'):
                            return ('\t', (pos + 2))
                        else:
                            if ((c == 'u') and ((pos + 6) <= len(text)) and all_hex(text, (pos + 2), (pos + 6))):
                                return (cdy_rt.table_defs.hex_char(text[(pos + 2):(pos + 6)]), (pos + 6))
                            else:
                                return cdy_rt.table_defs.fail(parse_error(file, text, pos, 'bad escape sequence'))

def all_hex(text: str, pos: int, end: int) -> bool:
    while True:
        if (pos >= end):
            return True
        else:
            if cdy_rt.table_defs.in_(text[pos], '0123456789abcdefABCDEF'):
                pos = (pos + 1)
                continue
            else:
                return False

def parse_error(file: str, text: str, pos: int, msg: str) -> str:
    _tup = row_col(text, 0, pos, 1, 1)
    row = _tup[0]
    col = _tup[1]
    return (str(where(file)) + 'parse error at line ' + str(row) + ', column ' + str(col) + ': ' + str(msg))

def where(file: str) -> str:
    if (file == ''):
        return ''
    else:
        return (file + ': ')

def row_col(text: str, i: int, pos: int, row: int, col: int) -> tuple[int, int]:
    while True:
        if (i >= pos):
            return (row, col)
        else:
            if (text[i] == '\n'):
                i, row, col = ((i + 1), (row + 1), 1)
                continue
            else:
                i, col = ((i + 1), (col + 1))
                continue

class Incl(_cdy_NamedTuple):
    done: tuple[Form, ...]
    seen: _cdy_Mapping[str, bool]

def read_program(path: str) -> tuple[Form, ...]:
    return include_file(path, Incl((), {})).done

def include_imports(forms: tuple[Form, ...], dir_: str) -> tuple[Form, ...]:
    return include_forms(forms, '', dir_, Incl((), {})).done

def include_file(path: str, acc: Incl) -> Incl:
    key = cdy_rt.table_defs.path_resolve(path)
    if cdy_rt.table_defs.map_has(acc.seen, key):
        return acc
    else:
        return include_forms(read_source(path, cdy_rt.table_defs.slurp(path)), path, cdy_rt.table_defs.path_dir(path), acc._replace(seen=cdy_rt.table_defs.map_set(acc.seen, key, True)))

def include_forms(forms: tuple[Form, ...], file: str, dir_: str, acc: Incl) -> Incl:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            name = import_name(forms[0], file)
            forms, acc = (rest_of(forms), (acc._replace(done=(acc.done + cdy_rt.table_defs.to_list(forms[0]))) if (name == '') else include_file(import_path(dir_, name, file), acc)))
            continue

def import_name(form: Form, file: str) -> str:
    items = list_items(form)
    if ((len(items) == 0) or (sym_name(items[0]) != 'import')):
        return ''
    else:
        if ((len(items) == 2) and (sym_name(items[1]) != '')):
            return sym_name(items[1])
        else:
            return cdy_rt.table_defs.fail((where(file) + 'import: expected (import name)'))

def import_path(dir_: str, name: str, file: str) -> str:
    path = cdy_rt.table_defs.path_join(dir_, (name + '.cdy'))
    if cdy_rt.table_defs.file_exists(path):
        return path
    else:
        return cdy_rt.table_defs.fail((str(where(file)) + "import: can't find " + str(name) + '.cdy in ' + str(dir_)))

class TCon(_cdy_NamedTuple):
    name: str
    args: tuple[CType, ...]

class TVar(_cdy_NamedTuple):
    name: str

class TFn(_cdy_NamedTuple):
    params: tuple[CType, ...]
    ret: CType
type CType = TCon | TVar | TFn

class Lit(_cdy_NamedTuple):
    form: Form

class Local(_cdy_NamedTuple):
    name: str
    id_: int

class Global(_cdy_NamedTuple):
    name: str

class Prim(_cdy_NamedTuple):
    name: str

class Call(_cdy_NamedTuple):
    callee: Expr
    args: tuple[Expr, ...]

class If(_cdy_NamedTuple):
    test: Expr
    then: Expr
    other: Expr

class Do(_cdy_NamedTuple):
    body: tuple[Expr, ...]

class Lambda(_cdy_NamedTuple):
    params: tuple[Expr, ...]
    body: Expr

class Tuple(_cdy_NamedTuple):
    items: tuple[Expr, ...]

class Fmt(_cdy_NamedTuple):
    parts: tuple[FPart, ...]

class Field(_cdy_NamedTuple):
    obj: Expr
    field: str

class Assoc(_cdy_NamedTuple):
    obj: Expr
    fields: tuple[tuple[str, Expr], ...]

class MatchE(_cdy_NamedTuple):
    subject: Expr
    clauses: tuple[Clause, ...]
    default: tuple[Expr, ...]

class Temp(_cdy_NamedTuple):
    id_: int
type Expr = Lit | Local | Global | Prim | Call | If | Do | Lambda | Tuple | Fmt | Field | Assoc | MatchE | Temp

class Clause(_cdy_NamedTuple):
    variant: str
    binds: tuple[tuple[str, Expr], ...]
    body: Expr

class FText(_cdy_NamedTuple):
    text: str

class FHole(_cdy_NamedTuple):
    expr: Expr
type FPart = FText | FHole

class Variant(_cdy_NamedTuple):
    name: str
    fields: tuple[tuple[str, CType], ...]

class TDeft(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, CType], ...]

class TDeftSum(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    variants: tuple[Variant, ...]

class TDef(_cdy_NamedTuple):
    name: str
    init: Expr
    t: CType

class TDefn(_cdy_NamedTuple):
    name: str
    params: tuple[Expr, ...]
    body: Expr
    t: CType

class TExpr(_cdy_NamedTuple):
    expr: Expr
type Top = TDeft | TDeftSum | TDef | TDefn | TExpr
NIL: Expr = Prim('nil')

class Scope(_cdy_NamedTuple):
    env: _cdy_Mapping[str, Expr]
    top: _cdy_Mapping[str, bool]
    table: _cdy_Any
    parse: _cdy_Callable[[str], tuple[Form, ...]]
    variants: _cdy_Mapping[str, VInfo]
    sums: _cdy_Mapping[str, tuple[str, ...]]

class VInfo(_cdy_NamedTuple):
    sum_: str
    fields: tuple[str, ...]

def is_variant(name: str, scope: Scope) -> bool:
    return (cdy_rt.table_defs.map_has(scope.variants, name) and (not cdy_rt.table_defs.map_has(scope.env, name)))

def variant_fields(name: str, scope: Scope) -> tuple[str, ...]:
    return cdy_rt.table_defs.map_get(scope.variants, name).fields

def analyse_expr(form: Form, scope: Scope, n: int) -> tuple[Expr, int]:
    _cdy_t2: object = form
    if isinstance(_cdy_t2, Sym):
        name = _cdy_t2.name
        return (resolve(name, scope), n)
    elif isinstance(_cdy_t2, Lst):
        items = _cdy_t2.items
        return analyse_list(items, scope, n)
    else:
        return (Lit(form), n)

def analyse_all(forms: tuple[Form, ...], scope: Scope, n: int, acc: tuple[Expr, ...]) -> tuple[tuple[Expr, ...], int]:
    while True:
        if (len(forms) == 0):
            return (acc, n)
        else:
            _tup = analyse_expr(forms[0], scope, n)
            e = _tup[0]
            n1 = _tup[1]
            forms, n, acc = (rest_of(forms), n1, (acc + cdy_rt.table_defs.to_list(e)))
            continue

def resolve(name: str, scope: Scope) -> Expr:
    if cdy_rt.table_defs.map_has(scope.env, name):
        return cdy_rt.table_defs.map_get(scope.env, name)
    else:
        if (is_variant(name, scope) and (len(variant_fields(name, scope)) == 0)):
            return Call(Global(name), ())
        else:
            if (cdy_rt.table_defs.map_has(scope.top, name) and cdy_rt.table_defs.map_get(scope.top, name)):
                return Global(name)
            else:
                if cdy_rt.table.is_special(scope.table, name):
                    return cdy_rt.table_defs.fail((str(name) + ' is a special form, not a value'))
                else:
                    if cdy_rt.table.is_op(scope.table, name):
                        return Prim(name)
                    else:
                        return cdy_rt.table_defs.fail(('unknown name ' + str(name)))

def is_special_head(name: str, scope: Scope) -> bool:
    return ((not cdy_rt.table_defs.map_has(scope.env, name)) and cdy_rt.table.is_special(scope.table, name))

def analyse_list(items: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(items) == 0):
        return cdy_rt.table_defs.fail('empty form (): use empty-list for an empty list')
    else:
        head = sym_name(items[0])
        if is_special_head(head, scope):
            return analyse_special(head, rest_of(items), scope, n)
        else:
            checked = check_variant_call(head, (len(items) - 1), scope)
            _tup = analyse_expr(items[0], scope, n)
            callee = _tup[0]
            n1 = _tup[1]
            _cdy__tup_133 = analyse_all(rest_of(items), scope, n1, ())
            args = _cdy__tup_133[0]
            n2 = _cdy__tup_133[1]
            arity_ok = check_call(callee, len(args), scope)
            return (Call(callee, args), n2)

def check_call(callee: Expr, count: int, scope: Scope) -> bool:
    _cdy_t3: object = callee
    if isinstance(_cdy_t3, Prim):
        name = _cdy_t3.name
        kind = cdy_rt.table.get_kind(scope.table, name)
        arity = cdy_rt.table.get_arity(scope.table, name)
        if (cdy_rt.table_defs.in_(kind, ('binop', 'compare', 'boolop')) and (count < 2)):
            return cdy_rt.table_defs.fail(('(' + str(name) + ' ...) needs at least 2 arguments, got ' + str(count)))
        else:
            if ((arity != None) and (arity != count)):
                return cdy_rt.table_defs.fail(('(' + str(name) + ' ...) takes ' + str(arity) + ' argument(s), got ' + str(count)))
            else:
                return True
    else:
        return True

def check_variant_call(name: str, count: int, scope: Scope) -> bool:
    if (not is_variant(name, scope)):
        return True
    else:
        if (len(variant_fields(name, scope)) == 0):
            return cdy_rt.table_defs.fail((str(name) + ' has no fields, so it is a value: write ' + str(name) + ', not (' + str(name) + ')'))
        else:
            if (count != len(variant_fields(name, scope))):
                return cdy_rt.table_defs.fail(('(' + str(name) + ' ...) takes ' + str(len(variant_fields(name, scope))) + ' field(s), got ' + str(count)))
            else:
                return True

def analyse_special(head: str, rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (head == 'if'):
        return an_if(rest, scope, n)
    else:
        if (head == 'cond'):
            return an_cond(rest, scope, n)
        else:
            if (head == 'do'):
                return an_do(rest, scope, n)
            else:
                if (head == 'let'):
                    return an_let(rest, scope, n)
                else:
                    if (head == 'fn'):
                        return an_fn(rest, scope, n)
                    else:
                        if (head == 'tup'):
                            return an_tup(rest, scope, n)
                        else:
                            if (head == 'format'):
                                return an_format(rest, scope, n)
                            else:
                                if (head == 'get'):
                                    return an_get(rest, scope, n)
                                else:
                                    if (head == 'assoc'):
                                        return an_assoc(rest, scope, n)
                                    else:
                                        if (head == 'match'):
                                            return an_match(rest, scope, n)
                                        else:
                                            if cdy_rt.table_defs.in_(head, ('def', 'defn', 'deft', 'sig', 'import')):
                                                return cdy_rt.table_defs.fail((str(head) + ' is only allowed at top level'))
                                            else:
                                                return cdy_rt.table_defs.fail((str(head) + ' is not supported by the Candy translator yet'))

def an_if(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    _tup = analyse_all(rest, scope, n, ())
    parts = _tup[0]
    n1 = _tup[1]
    if (len(parts) == 2):
        return (If(parts[0], parts[1], NIL), n1)
    else:
        if (len(parts) == 3):
            return (If(parts[0], parts[1], parts[2]), n1)
        else:
            return cdy_rt.table_defs.fail('if: expected (if test then else?)')

def is_else(form: Form) -> bool:
    return (sym_name(form) == 'else')

def an_cond(clauses: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(clauses) == 0):
        return cdy_rt.table_defs.fail('cond: needs at least one (test expr) clause')
    else:
        return cond_clauses(clauses, scope, n)

def cond_clauses(clauses: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(clauses) == 0):
        return (NIL, n)
    else:
        items = list_items(clauses[0])
        if (len(items) != 2):
            return cdy_rt.table_defs.fail('cond: clause must be (test expr)')
        else:
            if is_else(items[0]):
                if (len(clauses) == 1):
                    return analyse_expr(items[1], scope, n)
                else:
                    return cdy_rt.table_defs.fail('cond: (else expr) must be the last clause')
            else:
                _tup = analyse_expr(items[0], scope, n)
                test = _tup[0]
                n1 = _tup[1]
                _cdy__tup_167 = analyse_expr(items[1], scope, n1)
                expr = _cdy__tup_167[0]
                n2 = _cdy__tup_167[1]
                _cdy__tup_170 = cond_clauses(rest_of(clauses), scope, n2)
                other = _cdy__tup_170[0]
                n3 = _cdy__tup_170[1]
                return (If(test, expr, other), n3)

def an_do(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    _tup = analyse_all(rest, scope, n, ())
    body = _tup[0]
    n1 = _tup[1]
    if (len(body) == 0):
        return (NIL, n1)
    else:
        if (len(body) == 1):
            return (body[0], n1)
        else:
            return (Do(body), n1)

def an_let(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if ((len(rest) != 2) or (not is_list_form(rest[0]))):
        return cdy_rt.table_defs.fail('let: expected (let ((name init)*) body)')
    else:
        if (len(list_items(rest[0])) == 0):
            return analyse_expr(rest[1], scope, n)
        else:
            _tup = let_bindings(list_items(rest[0]), scope, n, ())
            pairs = _tup[0]
            inner = _tup[1]
            n1 = _tup[2]
            _cdy__tup_186 = analyse_expr(rest[1], inner, n1)
            body = _cdy__tup_186[0]
            n2 = _cdy__tup_186[1]
            return (nest(pairs, body), n2)

def is_list_form(form: Form) -> bool:
    _cdy_t4: object = form
    if isinstance(_cdy_t4, Lst):
        return True
    else:
        return False

def let_bindings(bindings: tuple[Form, ...], scope: Scope, n: int, acc: tuple[tuple[Expr, Expr], ...]) -> tuple[tuple[tuple[Expr, Expr], ...], Scope, int]:
    while True:
        if (len(bindings) == 0):
            return (acc, scope, n)
        else:
            items = list_items(bindings[0])
            if (len(items) != 2):
                return cdy_rt.table_defs.fail('let: binding must be (name init)')
            else:
                _tup = analyse_expr(items[1], scope, n)
                init = _tup[0]
                n1 = _tup[1]
                target = items[0]
                _cdy_t5: object = target
                if isinstance(_cdy_t5, Lst):
                    names = _cdy_t5.items
                    tmp = Local('_tup', n1)
                    _cdy__tup_201 = destructure(names, tmp, 0, scope, (n1 + 1), ())
                    more = _cdy__tup_201[0]
                    inner = _cdy__tup_201[1]
                    n2 = _cdy__tup_201[2]
                    bindings, scope, n, acc = (rest_of(bindings), inner, n2, (acc + cdy_rt.table_defs.to_list((tmp, init)) + more))
                    continue
                else:
                    name = sym_name(target)
                    loc = Local(name, n1)
                    if ((name == '') or cdy_rt.table.is_special(scope.table, name)):
                        return cdy_rt.table_defs.fail('let name must be a name, not a special form')
                    else:
                        bindings, scope, n, acc = (rest_of(bindings), scope._replace(env=cdy_rt.table_defs.map_set(scope.env, name, loc)), (n1 + 1), (acc + cdy_rt.table_defs.to_list((loc, init))))
                        continue

def destructure(names: tuple[Form, ...], tmp: Expr, i: int, scope: Scope, n: int, acc: tuple[tuple[Expr, Expr], ...]) -> tuple[tuple[tuple[Expr, Expr], ...], Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = sym_name(names[0])
            loc = Local(name, n)
            item = Call(Prim('at'), (tmp, Lit(IntLit(i))))
            if (name == ''):
                return cdy_rt.table_defs.fail('let name must be a name')
            else:
                names, i, scope, n, acc = (rest_of(names), (i + 1), scope._replace(env=cdy_rt.table_defs.map_set(scope.env, name, loc)), (n + 1), (acc + cdy_rt.table_defs.to_list((loc, item))))
                continue

def nest(pairs: tuple[tuple[Expr, Expr], ...], body: Expr) -> Expr:
    if (len(pairs) == 0):
        return body
    else:
        _tup = pairs[0]
        loc = _tup[0]
        init = _tup[1]
        return Call(Lambda(cdy_rt.table_defs.to_list(loc), nest(pairs[1:len(pairs)], body)), cdy_rt.table_defs.to_list(init))

def an_fn(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) != 2):
        return cdy_rt.table_defs.fail('fn: expected (fn (args+) body), with exactly one body form')
    else:
        _tup = bind_params(list_items(rest[0]), scope, n, ())
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_228 = analyse_expr(rest[1], inner, n1)
        body = _cdy__tup_228[0]
        n2 = _cdy__tup_228[1]
        if (len(params) == 0):
            return cdy_rt.table_defs.fail('fn arguments: at least one is needed')
        else:
            return (Lambda(params, body), n2)

def an_tup(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) == 0):
        return cdy_rt.table_defs.fail('tup: needs at least one item')
    else:
        _tup = analyse_all(rest, scope, n, ())
        items = _tup[0]
        n1 = _tup[1]
        return (Tuple(items), n1)

def an_get(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if ((len(rest) != 2) or (sym_name(rest[1]) == '')):
        return cdy_rt.table_defs.fail('get: expected (get obj field)')
    else:
        _tup = analyse_expr(rest[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        return (Field(obj, sym_name(rest[1])), n1)

def an_assoc(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) < 3):
        return cdy_rt.table_defs.fail('assoc: expected (assoc obj field value ...)')
    else:
        _tup = analyse_expr(rest[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        _cdy__tup_249 = assoc_fields(rest_of(rest), scope, n1, ())
        fields = _cdy__tup_249[0]
        n2 = _cdy__tup_249[1]
        return (Assoc(obj, fields), n2)

def assoc_fields(forms: tuple[Form, ...], scope: Scope, n: int, acc: tuple[tuple[str, Expr], ...]) -> tuple[tuple[tuple[str, Expr], ...], int]:
    while True:
        if (len(forms) == 0):
            return (acc, n)
        else:
            if (len(forms) == 1):
                return cdy_rt.table_defs.fail('assoc: expected (assoc obj field value ...)')
            else:
                field = sym_name(forms[0])
                _tup = analyse_expr(forms[1], scope, n)
                val = _tup[0]
                n1 = _tup[1]
                if (field == ''):
                    return cdy_rt.table_defs.fail('assoc field must be a name')
                else:
                    forms, n, acc = (forms[2:len(forms)], n1, (acc + cdy_rt.table_defs.to_list((field, val))))
                    continue

def an_format(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) != 1):
        return cdy_rt.table_defs.fail('format: expected one string literal')
    else:
        _cdy_t6: object = rest[0]
        if isinstance(_cdy_t6, Txt):
            text = _cdy_t6.val
            _tup = format_parts(text, 0, '', scope, n, ())
            parts = _tup[0]
            n1 = _tup[1]
            return (Fmt(parts), n1)
        else:
            return cdy_rt.table_defs.fail('format: expected one string literal')

def format_parts(text: str, pos: int, acc: str, scope: Scope, n: int, parts: tuple[FPart, ...]) -> tuple[tuple[FPart, ...], int]:
    while True:
        c = (text[pos:(pos + 1)] if (pos < len(text)) else '')
        next_ = (text[(pos + 1):(pos + 2)] if ((pos + 1) < len(text)) else '')
        if (c == ''):
            return (add_text(parts, acc), n)
        else:
            if ((c == '{') and (next_ == '{')):
                pos, acc = ((pos + 2), (acc + '{'))
                continue
            else:
                if ((c == '}') and (next_ == '}')):
                    pos, acc = ((pos + 2), (acc + '}'))
                    continue
                else:
                    if (c == '}'):
                        return cdy_rt.table_defs.fail('format: unmatched } (write }} for a brace)')
                    else:
                        if (c == '{'):
                            end = hole_end(text, (pos + 1))
                            forms = scope.parse(text[(pos + 1):end])
                            if (len(forms) != 1):
                                return cdy_rt.table_defs.fail('format: a {hole} must hold exactly one form')
                            else:
                                _tup = analyse_expr(forms[0], scope, n)
                                e = _tup[0]
                                n1 = _tup[1]
                                pos, acc, n, parts = ((end + 1), '', n1, (add_text(parts, acc) + cdy_rt.table_defs.to_list(FHole(e))))
                                continue
                        else:
                            pos, acc = ((pos + 1), (acc + c))
                            continue

def hole_end(text: str, pos: int) -> int:
    while True:
        if (pos >= len(text)):
            return cdy_rt.table_defs.fail('format: unmatched { (write {{ for a brace)')
        else:
            if (text[pos:(pos + 1)] == '}'):
                return pos
            else:
                if (text[pos:(pos + 1)] == '{'):
                    return cdy_rt.table_defs.fail("format: a {hole} can't hold a brace")
                else:
                    pos = (pos + 1)
                    continue

def add_text(parts: tuple[FPart, ...], text: str) -> tuple[FPart, ...]:
    if (text == ''):
        return parts
    else:
        return (parts + cdy_rt.table_defs.to_list(FText(text)))

def an_match(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) < 2):
        return cdy_rt.table_defs.fail('match: expected (match subject ((Variant name*) expr)+ (else expr)?)')
    else:
        _tup = analyse_expr(rest[0], scope, n)
        subject = _tup[0]
        n1 = _tup[1]
        _cdy__tup_290 = match_clauses(rest_of(rest), scope, n1, MatchE(subject, (), ()), '')
        m = _cdy__tup_290[0]
        n2 = _cdy__tup_290[1]
        sum_ = (match_sum(match_clause_list(m), scope) if (len(match_clause_list(m)) > 0) else '')
        return (check_exhaustive(m, sum_, scope), n2)

def match_sum(clauses: tuple[Clause, ...], scope: Scope) -> str:
    return cdy_rt.table_defs.map_get(scope.variants, clauses[0].variant).sum_

def check_exhaustive(m: Expr, sum_: str, scope: Scope) -> Expr:
    _cdy_t7: object = m
    if isinstance(_cdy_t7, MatchE):
        clauses = _cdy_t7.clauses
        default = _cdy_t7.default
        missing = missing_variants(cdy_rt.table_defs.map_get(scope.sums, sum_), clauses, ())
        if ((len(default) == 0) and (len(missing) > 0)):
            return cdy_rt.table_defs.fail(('match on ' + str(sum_) + ': no clause for ' + str(cdy_rt.table_defs.join(missing, ', ')) + ' (or add else)'))
        else:
            return m
    else:
        return m

def missing_variants(names: tuple[str, ...], clauses: tuple[Clause, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (names[1:len(names)], (acc if has_clause(names[0], clauses) else (acc + cdy_rt.table_defs.to_list(names[0]))))
            continue

def has_clause(name: str, clauses: tuple[Clause, ...]) -> bool:
    while True:
        if (len(clauses) == 0):
            return False
        else:
            if (clauses[0].variant == name):
                return True
            else:
                clauses = clauses[1:len(clauses)]
                continue

def match_clauses(forms: tuple[Form, ...], scope: Scope, n: int, m: Expr, sum_: str) -> tuple[Expr, int]:
    while True:
        if (len(forms) == 0):
            return (m, n)
        else:
            items = list_items(forms[0])
            if (len(items) != 2):
                return cdy_rt.table_defs.fail('match: clause must be (pattern expr)')
            else:
                if is_else(items[0]):
                    if ((len(forms) > 1) or (len(match_clause_list(m)) == 0)):
                        return cdy_rt.table_defs.fail('match: (else expr) must be the last clause, after a pattern')
                    else:
                        _tup = analyse_expr(items[1], scope, n)
                        e = _tup[0]
                        n1 = _tup[1]
                        return (set_default(m, e), n1)
                else:
                    pattern = list_items(items[0])
                    variant = (sym_name(pattern[0]) if (len(pattern) > 0) else '')
                    checked = check_pattern(variant, pattern, sum_, m, scope)
                    _cdy__tup_319 = pattern_binds(variant_fields(variant, scope), rest_of(pattern), scope, n, ())
                    binds = _cdy__tup_319[0]
                    inner = _cdy__tup_319[1]
                    _cdy_n1_322 = _cdy__tup_319[2]
                    _cdy__tup_323 = analyse_expr(items[1], inner, _cdy_n1_322)
                    body = _cdy__tup_323[0]
                    n2 = _cdy__tup_323[1]
                    forms, n, m, sum_ = (rest_of(forms), n2, add_clause(m, Clause(variant, binds, body)), cdy_rt.table_defs.map_get(scope.variants, variant).sum_)
                    continue

def check_pattern(variant: str, pattern: tuple[Form, ...], sum_: str, m: Expr, scope: Scope) -> bool:
    if (variant == ''):
        return cdy_rt.table_defs.fail('match: pattern must be (Variant name*) or else')
    else:
        if (not is_variant(variant, scope)):
            return cdy_rt.table_defs.fail(('match: ' + str(variant) + ' is not a variant of a sum type'))
        else:
            if has_clause(variant, match_clause_list(m)):
                return cdy_rt.table_defs.fail(('match: more than one clause for ' + str(variant)))
            else:
                if ((sum_ != '') and (sum_ != cdy_rt.table_defs.map_get(scope.variants, variant).sum_)):
                    return cdy_rt.table_defs.fail(('match: clauses mix variants of ' + str(sum_) + ' and ' + str(cdy_rt.table_defs.map_get(scope.variants, variant).sum_)))
                else:
                    if ((len(pattern) - 1) != len(variant_fields(variant, scope))):
                        return cdy_rt.table_defs.fail(('match: ' + str(variant) + ' has ' + str(len(variant_fields(variant, scope))) + ' field(s), so the pattern needs that many names'))
                    else:
                        return True

def match_clause_list(m: Expr) -> tuple[Clause, ...]:
    _cdy_t8: object = m
    if isinstance(_cdy_t8, MatchE):
        clauses = _cdy_t8.clauses
        return clauses
    else:
        return ()

def add_clause(m: Expr, clause: Clause) -> Expr:
    _cdy_t9: object = m
    if isinstance(_cdy_t9, MatchE):
        subject = _cdy_t9.subject
        clauses = _cdy_t9.clauses
        default = _cdy_t9.default
        return MatchE(subject, (clauses + cdy_rt.table_defs.to_list(clause)), default)
    else:
        return m

def set_default(m: Expr, e: Expr) -> Expr:
    _cdy_t10: object = m
    if isinstance(_cdy_t10, MatchE):
        subject = _cdy_t10.subject
        clauses = _cdy_t10.clauses
        return MatchE(subject, clauses, cdy_rt.table_defs.to_list(e))
    else:
        return m

def pattern_binds(fields: tuple[str, ...], names: tuple[Form, ...], scope: Scope, n: int, acc: tuple[tuple[str, Expr], ...]) -> tuple[tuple[tuple[str, Expr], ...], Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = sym_name(names[0])
            loc = Local(name, n)
            if (name == ''):
                return cdy_rt.table_defs.fail('match name must be a name')
            else:
                if (name == '_'):
                    fields, names = (fields[1:len(fields)], rest_of(names))
                    continue
                else:
                    if bound_in(name, acc):
                        return cdy_rt.table_defs.fail('match: names in a pattern must be different')
                    else:
                        fields, names, scope, n, acc = (fields[1:len(fields)], rest_of(names), scope._replace(env=cdy_rt.table_defs.map_set(scope.env, name, loc)), (n + 1), (acc + cdy_rt.table_defs.to_list((fields[0], loc))))
                        continue

def bound_in(name: str, binds: tuple[tuple[str, Expr], ...]) -> bool:
    while True:
        if (len(binds) == 0):
            return False
        else:
            _tup = binds[0]
            _ = _tup[0]
            loc = _tup[1]
            _cdy_t11: object = loc
            if isinstance(_cdy_t11, Local):
                other = _cdy_t11.name
                return ((other == name) or bound_in(name, binds[1:len(binds)]))
            else:
                binds = binds[1:len(binds)]
                continue

def is_lower(name: str) -> bool:
    return ((len(name) > 0) and (name[0:1] >= 'a') and (name[0:1] <= 'z'))

def analyse_type(form: Form) -> CType:
    _cdy_t12: object = form
    if isinstance(_cdy_t12, Sym):
        name = _cdy_t12.name
        if is_lower(name):
            return TVar(name)
        else:
            return TCon(name, ())
    elif isinstance(_cdy_t12, Lst):
        items = _cdy_t12.items
        if (len(items) == 0):
            return cdy_rt.table_defs.fail('bad type ()')
        else:
            if (sym_name(items[0]) == 'Fn'):
                if (len(items) == 3):
                    return TFn(analyse_types(list_items(items[1]), ()), analyse_type(items[2]))
                else:
                    return cdy_rt.table_defs.fail('bad function type: expected (Fn (Arg+) Ret)')
            else:
                return TCon(sym_name(items[0]), analyse_types(rest_of(items), ()))
    else:
        return cdy_rt.table_defs.fail('bad type')

def analyse_types(forms: tuple[Form, ...], acc: tuple[CType, ...]) -> tuple[CType, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (rest_of(forms), (acc + cdy_rt.table_defs.to_list(analyse_type(forms[0]))))
            continue

class Prog(_cdy_NamedTuple):
    out: tuple[Top, ...]
    sigs: _cdy_Mapping[str, CType]
    n: int
    defs: _cdy_Mapping[str, bool]
    defined: _cdy_Mapping[str, bool]

def top_names(forms: tuple[Form, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = list_items(forms[0])
            head = (sym_name(items[0]) if (len(items) > 1) else '')
            forms, acc = (rest_of(forms), (add_name(sym_name(items[1]), acc) if ((head == 'def') or (head == 'defn')) else (add_names(variant_names(items[2:len(items)], ()), cdy_rt.table_defs.map_set(add_name(deft_name(items[1]), acc), deft_name(items[1]), False)) if ((head == 'deft') and is_sum_body(items[2:len(items)])) else (add_name(deft_name(items[1]), acc) if (head == 'deft') else acc))))
            continue

def add_name(name: str, acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    if cdy_rt.table_defs.map_has(acc, name):
        return cdy_rt.table_defs.fail(('defined more than once: ' + str(name)))
    else:
        return cdy_rt.table_defs.map_set(acc, name, True)

def add_names(names: tuple[str, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (names[1:len(names)], add_name(names[0], acc))
            continue

def is_sum_body(body: tuple[Form, ...]) -> bool:
    return ((len(body) > 0) and all_variant_forms(body))

def all_variant_forms(body: tuple[Form, ...]) -> bool:
    while True:
        if (len(body) == 0):
            return True
        else:
            if (sym_name(first_item(body[0])) == ''):
                return False
            else:
                body = rest_of(body)
                continue

def first_item(form: Form) -> Form:
    items = list_items(form)
    if (len(items) == 0):
        return Lst(())
    else:
        return items[0]

def variant_names(body: tuple[Form, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(body) == 0):
            return acc
        else:
            body, acc = (rest_of(body), (acc + cdy_rt.table_defs.to_list(sym_name(first_item(body[0])))))
            continue

def find_variants(forms: tuple[Form, ...], scope: Scope) -> Scope:
    while True:
        if (len(forms) == 0):
            return scope
        else:
            items = list_items(forms[0])
            head = (sym_name(items[0]) if (len(items) > 2) else '')
            body = items[2:len(items)]
            _cdy_t14 = rest_of(forms)
            if ((head == 'deft') and is_sum_body(body)):
                sum_ = deft_name(items[1])
                _cdy_t13 = add_variants(sum_, body, scope._replace(sums=cdy_rt.table_defs.map_set(scope.sums, sum_, variant_names(body, ()))))
            else:
                _cdy_t13 = scope
            forms, scope = (_cdy_t14, _cdy_t13)
            continue

def add_variants(sum_: str, body: tuple[Form, ...], scope: Scope) -> Scope:
    while True:
        if (len(body) == 0):
            return scope
        else:
            v_items = list_items(body[0])
            name = sym_name(v_items[0])
            fields = (field_names(list_items(v_items[1]), ()) if (len(v_items) == 2) else ())
            body, scope = (rest_of(body), scope._replace(variants=cdy_rt.table_defs.map_set(scope.variants, name, VInfo(sum_, fields))))
            continue

def field_names(fields: tuple[Form, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            fields, acc = (rest_of(fields), (acc + cdy_rt.table_defs.to_list(sym_name(first_item(fields[0])))))
            continue

def deft_name(form: Form) -> str:
    _cdy_t15: object = form
    if isinstance(_cdy_t15, Lst):
        items = _cdy_t15.items
        if (len(items) == 0):
            return ''
        else:
            return sym_name(items[0])
    else:
        return sym_name(form)

def analyse_program(forms: tuple[Form, ...], table: _cdy_Any, parse: _cdy_Callable[[str], tuple[Form, ...]]) -> tuple[Top, ...]:
    scope = find_variants(forms, Scope({}, top_names(forms, {}), table, parse, {}, {}))
    return analyse_tops(forms, scope, Prog((), {}, 0, def_names(forms, {}), {})).out

def def_names(forms: tuple[Form, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = list_items(forms[0])
            head = (sym_name(items[0]) if (len(items) > 1) else '')
            forms, acc = (rest_of(forms), (cdy_rt.table_defs.map_set(acc, sym_name(items[1]), True) if ((head == 'def') or (head == 'defn')) else acc))
            continue

def analyse_tops(forms: tuple[Form, ...], scope: Scope, prog: Prog) -> Prog:
    while True:
        if (len(forms) == 0):
            return prog
        else:
            forms, prog = (rest_of(forms), analyse_top(forms[0], scope, prog))
            continue

def add_top(prog: Prog, top: Top, n: int) -> Prog:
    return prog._replace(out=(prog.out + cdy_rt.table_defs.to_list(top)), n=n)

def mark_defined(prog: Prog, name: str) -> Prog:
    return prog._replace(defined=cdy_rt.table_defs.map_set(prog.defined, name, True))

def analyse_top(form: Form, scope: Scope, prog: Prog) -> Prog:
    items = list_items(form)
    head = (sym_name(items[0]) if (len(items) > 0) else '')
    if (head == 'sig'):
        return top_sig(items, prog)
    else:
        if (head == 'def'):
            return top_def(items, scope, prog)
        else:
            if (head == 'defn'):
                return top_defn(items, scope, prog)
            else:
                if (head == 'deft'):
                    return top_deft(items, prog)
                else:
                    _tup = analyse_expr(form, scope, prog.n)
                    e = _tup[0]
                    n = _tup[1]
                    return add_top(prog, TExpr(e), n)

def top_sig(items: tuple[Form, ...], prog: Prog) -> Prog:
    name = (sym_name(items[1]) if (len(items) == 3) else '')
    if (name == ''):
        return cdy_rt.table_defs.fail('sig: expected (sig name Type)')
    else:
        if (not cdy_rt.table_defs.map_has(prog.defs, name)):
            return cdy_rt.table_defs.fail(('sig for ' + str(name) + ', but no def or defn of ' + str(name) + ' in this file'))
        else:
            if cdy_rt.table_defs.map_has(prog.defined, name):
                return cdy_rt.table_defs.fail(('sig for ' + str(name) + ' comes after its definition'))
            else:
                if cdy_rt.table_defs.map_has(prog.sigs, name):
                    return cdy_rt.table_defs.fail(('more than one sig for ' + str(name)))
                else:
                    return prog._replace(sigs=cdy_rt.table_defs.map_set(prog.sigs, name, analyse_type(items[2])))

def top_deft(items: tuple[Form, ...], prog: Prog) -> Prog:
    name = (deft_name(items[1]) if (len(items) > 1) else '')
    tvars = (syms(rest_of(list_items(items[1])), ()) if (len(items) > 1) else ())
    body = items[2:len(items)]
    field_forms = (list_items(items[2]) if (len(items) == 3) else ())
    if (name == ''):
        return cdy_rt.table_defs.fail('deft: expected (deft Name ((field Type)+)) or (deft Name variant+)')
    else:
        if is_sum_body(body):
            return add_top(prog, TDeftSum(name, tvars, deft_variants(body, ())), prog.n)
        else:
            if (len(field_forms) == 0):
                return cdy_rt.table_defs.fail('deft: expected (deft Name ((field Type)+))')
            else:
                return add_top(prog, TDeft(name, tvars, deft_fields(field_forms, ())), prog.n)

def deft_variants(body: tuple[Form, ...], acc: tuple[Variant, ...]) -> tuple[Variant, ...]:
    while True:
        if (len(body) == 0):
            return acc
        else:
            v_items = list_items(body[0])
            name = sym_name(v_items[0])
            if (not is_upper(name)):
                return cdy_rt.table_defs.fail(('deft: variant names are Capitalised, not ' + str(name)))
            else:
                if (len(v_items) == 1):
                    body, acc = (rest_of(body), (acc + cdy_rt.table_defs.to_list(Variant(name, ()))))
                    continue
                else:
                    if ((len(v_items) == 2) and (len(list_items(v_items[1])) > 0)):
                        body, acc = (rest_of(body), (acc + cdy_rt.table_defs.to_list(Variant(name, deft_fields(list_items(v_items[1]), ())))))
                        continue
                    else:
                        return cdy_rt.table_defs.fail('deft: variant must be (Name) or (Name ((field Type)+))')

def is_upper(name: str) -> bool:
    return ((len(name) > 0) and (name[0:1] >= 'A') and (name[0:1] <= 'Z'))

def syms(forms: tuple[Form, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (rest_of(forms), (acc + cdy_rt.table_defs.to_list(sym_name(forms[0]))))
            continue

def deft_fields(forms: tuple[Form, ...], acc: tuple[tuple[str, CType], ...]) -> tuple[tuple[str, CType], ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = list_items(forms[0])
            if ((len(items) != 2) or (sym_name(items[0]) == '')):
                return cdy_rt.table_defs.fail('deft: field must be (name Type)')
            else:
                forms, acc = (rest_of(forms), (acc + cdy_rt.table_defs.to_list((sym_name(items[0]), analyse_type(items[1])))))
                continue

def needs_sig(name: str, prog: Prog) -> CType:
    if cdy_rt.table_defs.map_has(prog.sigs, name):
        return cdy_rt.table_defs.map_get(prog.sigs, name)
    else:
        return cdy_rt.table_defs.fail((str(name) + ' needs a (sig ' + str(name) + ' Type) before its definition'))

def top_def(items: tuple[Form, ...], scope: Scope, prog: Prog) -> Prog:
    if (len(items) != 3):
        return cdy_rt.table_defs.fail('def: expected (def name init); the initial value is required')
    else:
        name = sym_name(items[1])
        t = needs_sig(name, prog)
        _tup = analyse_expr(items[2], scope, prog.n)
        init = _tup[0]
        n = _tup[1]
        return mark_defined(add_top(prog, TDef(name, init, t), n), name)

def top_defn(items: tuple[Form, ...], scope: Scope, prog: Prog) -> Prog:
    if (len(items) != 4):
        return cdy_rt.table_defs.fail('defn: expected (defn name (args+) body), with exactly one body form')
    else:
        name = sym_name(items[1])
        t = needs_sig(name, prog)
        arg_forms = list_items(items[2])
        _tup = bind_params(arg_forms, scope, prog.n, ())
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_454 = analyse_expr(items[3], inner, n1)
        body = _cdy__tup_454[0]
        n2 = _cdy__tup_454[1]
        if (len(params) == 0):
            return cdy_rt.table_defs.fail(('defn ' + str(name) + ': at least one argument is needed'))
        else:
            if (len(params) != fn_arity(t)):
                return cdy_rt.table_defs.fail(('defn ' + str(name) + ': its sig must be a function type with one type per argument'))
            else:
                return mark_defined(add_top(prog, TDefn(name, params, body, t), n2), name)

def fn_arity(t: CType) -> int:
    _cdy_t16: object = t
    if isinstance(_cdy_t16, TFn):
        params = _cdy_t16.params
        return len(params)
    else:
        return -1

def bind_params(forms: tuple[Form, ...], scope: Scope, n: int, acc: tuple[Expr, ...]) -> tuple[tuple[Expr, ...], Scope, int]:
    while True:
        if (len(forms) == 0):
            return (acc, scope, n)
        else:
            name = sym_name(forms[0])
            loc = Local(name, n)
            if (name == ''):
                return cdy_rt.table_defs.fail('a parameter must be a name')
            else:
                forms, scope, n, acc = (rest_of(forms), scope._replace(env=cdy_rt.table_defs.map_set(scope.env, name, loc)), (n + 1), (acc + cdy_rt.table_defs.to_list(loc)))
                continue
MAIN_TYPE: CType = TFn(cdy_rt.table_defs.to_list(TCon('List', cdy_rt.table_defs.to_list(TCon('String', ())))), TCon('Int', ()))

def has_main(tops: tuple[Top, ...]) -> bool:
    while True:
        if (len(tops) == 0):
            return False
        else:
            if is_main(tops[0]):
                return True
            else:
                tops = tops[1:len(tops)]
                continue

def is_main(top: Top) -> bool:
    _cdy_t17: object = top
    if isinstance(_cdy_t17, TDefn):
        name = _cdy_t17.name
        t = _cdy_t17.t
        if (name != 'main'):
            return False
        else:
            if (t == MAIN_TYPE):
                return True
            else:
                return cdy_rt.table_defs.fail('main must be typed (Fn ((List String)) Int)')
    elif isinstance(_cdy_t17, TDef):
        _cdy_name_469 = _cdy_t17.name
        if (_cdy_name_469 == 'main'):
            return cdy_rt.table_defs.fail('main must be a defn')
        else:
            return False
    else:
        return False

class SRecord(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, CType], ...]

class SSum(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    variants: tuple[Variant, ...]

class SMatch(_cdy_NamedTuple):
    temp: Expr
    subject: Expr
    cases: tuple[Case, ...]
    default: tuple[tuple[Stmt, ...], ...]

class SAssign(_cdy_NamedTuple):
    target: Expr
    val: Expr

class SDefAssign(_cdy_NamedTuple):
    name: str
    val: Expr
    t: CType

class SExpr(_cdy_NamedTuple):
    expr: Expr

class SReturn(_cdy_NamedTuple):
    val: Expr

class SIf(_cdy_NamedTuple):
    test: Expr
    then: tuple[Stmt, ...]
    other: tuple[Stmt, ...]

class SFunc(_cdy_NamedTuple):
    name: str
    params: tuple[Expr, ...]
    body: tuple[Stmt, ...]
    t: CType

class SLocalFunc(_cdy_NamedTuple):
    target: Expr
    params: tuple[Expr, ...]
    body: tuple[Stmt, ...]

class SLoop(_cdy_NamedTuple):
    body: tuple[Stmt, ...]

class SRebind(_cdy_NamedTuple):
    targets: tuple[Expr, ...]
    vals: tuple[Expr, ...]

class SContinue(_cdy_NamedTuple):
    pass
type Stmt = SRecord | SSum | SMatch | SAssign | SDefAssign | SExpr | SReturn | SIf | SFunc | SLocalFunc | SLoop | SRebind | SContinue

class Case(_cdy_NamedTuple):
    variant: str
    binds: tuple[tuple[str, Expr], ...]
    body: tuple[Stmt, ...]

class Low(_cdy_NamedTuple):
    stmts: tuple[Stmt, ...]
    expr: Expr
    n: int

def is_simple(e: Expr) -> bool:
    _cdy_t18: object = e
    if isinstance(_cdy_t18, Lit):
        return True
    elif isinstance(_cdy_t18, Local):
        return True
    elif isinstance(_cdy_t18, Global):
        return True
    elif isinstance(_cdy_t18, Prim):
        return True
    elif isinstance(_cdy_t18, Temp):
        return True
    else:
        return False

def is_applied(e: Expr) -> bool:
    _cdy_t19: object = e
    if isinstance(_cdy_t19, Call):
        callee = _cdy_t19.callee
        args = _cdy_t19.args
        _cdy_t20: object = callee
        if isinstance(_cdy_t20, Lambda):
            params = _cdy_t20.params
            return (len(params) == len(args))
        else:
            return False
    else:
        return False

def bind_applied(e: Expr, n: int) -> tuple[tuple[Stmt, ...], Expr, int]:
    _cdy_t21: object = e
    if isinstance(_cdy_t21, Call):
        callee = _cdy_t21.callee
        args = _cdy_t21.args
        _cdy_t22: object = callee
        if isinstance(_cdy_t22, Lambda):
            params = _cdy_t22.params
            body = _cdy_t22.body
            _tup = value_seq(args, n)
            stmts = _tup[0]
            vals = _tup[1]
            n1 = _tup[2]
            return ((stmts + assigns(params, vals, ())), body, n1)
        else:
            return cdy_rt.table_defs.fail('lower: not an applied fn')
    else:
        return cdy_rt.table_defs.fail('lower: not an applied fn')

def assigns(targets: tuple[Expr, ...], vals: tuple[Expr, ...], acc: tuple[Stmt, ...]) -> tuple[Stmt, ...]:
    while True:
        if (len(targets) == 0):
            return acc
        else:
            targets, vals, acc = (targets[1:len(targets)], vals[1:len(vals)], (acc + cdy_rt.table_defs.to_list(SAssign(targets[0], vals[0]))))
            continue

def value(e: Expr, n: int) -> Low:
    if is_applied(e):
        _tup = bind_applied(e, n)
        stmts = _tup[0]
        body = _tup[1]
        n1 = _tup[2]
        low = value(body, n1)
        return Low((stmts + low.stmts), low.expr, low.n)
    else:
        _cdy_t23: object = e
        if isinstance(_cdy_t23, Call):
            callee = _cdy_t23.callee
            args = _cdy_t23.args
            return value_call(callee, args, n)
        elif isinstance(_cdy_t23, If):
            test = _cdy_t23.test
            then = _cdy_t23.then
            other = _cdy_t23.other
            return value_if(test, then, other, n)
        elif isinstance(_cdy_t23, Do):
            _cdy_body_500 = _cdy_t23.body
            return value_do(_cdy_body_500, n)
        elif isinstance(_cdy_t23, Lambda):
            params = _cdy_t23.params
            _cdy_body_502 = _cdy_t23.body
            return value_fn(params, _cdy_body_502, n)
        elif isinstance(_cdy_t23, Tuple):
            items = _cdy_t23.items
            _cdy__tup_504 = value_seq(items, n)
            _cdy_stmts_505 = _cdy__tup_504[0]
            vals = _cdy__tup_504[1]
            _cdy_n1_507 = _cdy__tup_504[2]
            return Low(_cdy_stmts_505, Tuple(vals), _cdy_n1_507)
        elif isinstance(_cdy_t23, Fmt):
            parts = _cdy_t23.parts
            _cdy__tup_509 = value_seq(holes(parts, ()), n)
            _cdy_stmts_510 = _cdy__tup_509[0]
            _cdy_vals_511 = _cdy__tup_509[1]
            _cdy_n1_512 = _cdy__tup_509[2]
            return Low(_cdy_stmts_510, Fmt(fill_holes(parts, _cdy_vals_511, ())), _cdy_n1_512)
        elif isinstance(_cdy_t23, Field):
            obj = _cdy_t23.obj
            field = _cdy_t23.field
            _cdy_low_515 = value(obj, n)
            return Low(_cdy_low_515.stmts, Field(_cdy_low_515.expr, field), _cdy_low_515.n)
        elif isinstance(_cdy_t23, Assoc):
            _cdy_obj_516 = _cdy_t23.obj
            fields = _cdy_t23.fields
            _cdy__tup_518 = value_seq((cdy_rt.table_defs.to_list(_cdy_obj_516) + field_vals(fields, ())), n)
            _cdy_stmts_519 = _cdy__tup_518[0]
            _cdy_vals_520 = _cdy__tup_518[1]
            _cdy_n1_521 = _cdy__tup_518[2]
            return Low(_cdy_stmts_519, Assoc(_cdy_vals_520[0], refill(fields, _cdy_vals_520[1:len(_cdy_vals_520)], ())), _cdy_n1_521)
        elif isinstance(_cdy_t23, MatchE):
            tmp = Temp(n)
            _cdy__tup_523 = lower_match(e, 'value', tmp, (n + 1))
            _cdy_stmts_524 = _cdy__tup_523[0]
            _cdy_n1_525 = _cdy__tup_523[1]
            return Low(_cdy_stmts_524, tmp, _cdy_n1_525)
        else:
            return Low((), e, n)

def lower_match(e: Expr, mode: str, tmp: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t24: object = e
    if isinstance(_cdy_t24, MatchE):
        subject = _cdy_t24.subject
        clauses = _cdy_t24.clauses
        default = _cdy_t24.default
        low = value(subject, n)
        temp = Temp(low.n)
        _tup = lower_cases(clauses, mode, tmp, (low.n + 1), ())
        cases = _tup[0]
        n2 = _tup[1]
        _cdy__tup_538 = lower_default(default, mode, tmp, n2)
        default_stmts = _cdy__tup_538[0]
        n3 = _cdy__tup_538[1]
        return ((low.stmts + cdy_rt.table_defs.to_list(SMatch(temp, low.expr, cases, default_stmts))), n3)
    else:
        return cdy_rt.table_defs.fail('lower: not a match')

def lower_default(default: tuple[Expr, ...], mode: str, tmp: Expr, n: int) -> tuple[tuple[tuple[Stmt, ...], ...], int]:
    if (len(default) == 0):
        return ((), n)
    else:
        _tup = lower_body(default[0], mode, tmp, n)
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.table_defs.to_list(stmts), n1)

def lower_cases(clauses: tuple[Clause, ...], mode: str, tmp: Expr, n: int, acc: tuple[Case, ...]) -> tuple[tuple[Case, ...], int]:
    while True:
        if (len(clauses) == 0):
            return (acc, n)
        else:
            clause = clauses[0]
            _tup = lower_body(clause.body, mode, tmp, n)
            body = _tup[0]
            n1 = _tup[1]
            clauses, n, acc = (clauses[1:len(clauses)], n1, (acc + cdy_rt.table_defs.to_list(Case(clause.variant, clause.binds, body))))
            continue

def lower_body(e: Expr, mode: str, tmp: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    if (mode == 'tail'):
        return tail(e, n)
    else:
        if (mode == 'effect'):
            return effect(e, n)
        else:
            low = value(e, n)
            return ((low.stmts + cdy_rt.table_defs.to_list(SAssign(tmp, low.expr))), low.n)

def value_fn(params: tuple[Expr, ...], body: Expr, n: int) -> Low:
    _tup = tail(body, n)
    stmts = _tup[0]
    n1 = _tup[1]
    _cdy_t25: object = (stmts[0] if (len(stmts) == 1) else SExpr(NIL))
    if isinstance(_cdy_t25, SReturn):
        result = _cdy_t25.val
        return Low((), Lambda(params, result), n1)
    else:
        return Low(cdy_rt.table_defs.to_list(SLocalFunc(Temp(n1), params, stmts)), Temp(n1), (n1 + 1))

def holes(parts: tuple[FPart, ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t28 = parts[1:len(parts)]
            _cdy_t27: object = parts[0]
            if isinstance(_cdy_t27, FHole):
                e = _cdy_t27.expr
                _cdy_t26 = (acc + cdy_rt.table_defs.to_list(e))
            else:
                assert isinstance(_cdy_t27, FText)
                _cdy_t26 = acc
            parts, acc = (_cdy_t28, _cdy_t26)
            continue

def fill_holes(parts: tuple[FPart, ...], vals: tuple[Expr, ...], acc: tuple[FPart, ...]) -> tuple[FPart, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t29: object = parts[0]
            if isinstance(_cdy_t29, FHole):
                parts, vals, acc = (parts[1:len(parts)], vals[1:len(vals)], (acc + cdy_rt.table_defs.to_list(FHole(vals[0]))))
                continue
            else:
                assert isinstance(_cdy_t29, FText)
                text = _cdy_t29.text
                parts, acc = (parts[1:len(parts)], (acc + cdy_rt.table_defs.to_list(FText(text))))
                continue

def field_vals(fields: tuple[tuple[str, Expr], ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            _ = _tup[0]
            v = _tup[1]
            fields, acc = (fields[1:len(fields)], (acc + cdy_rt.table_defs.to_list(v)))
            continue

def refill(fields: tuple[tuple[str, Expr], ...], vals: tuple[Expr, ...], acc: tuple[tuple[str, Expr], ...]) -> tuple[tuple[str, Expr], ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            f = _tup[0]
            _ = _tup[1]
            fields, vals, acc = (fields[1:len(fields)], vals[1:len(vals)], (acc + cdy_rt.table_defs.to_list((f, vals[0]))))
            continue

def value_call(callee: Expr, args: tuple[Expr, ...], n: int) -> Low:
    if cdy_rt.table_defs.in_(prim_name(callee), ('and', 'or')):
        return value_boolop(callee, args, n)
    else:
        _tup = value_seq((cdy_rt.table_defs.to_list(callee) + args), n)
        stmts = _tup[0]
        items = _tup[1]
        n1 = _tup[2]
        return Low(stmts, Call(items[0], items[1:len(items)]), n1)

def prim_name(e: Expr) -> str:
    _cdy_t30: object = e
    if isinstance(_cdy_t30, Prim):
        name = _cdy_t30.name
        return name
    else:
        return ''

def value_boolop(op: Expr, args: tuple[Expr, ...], n: int) -> Low:
    _tup = low_all(args, n, ())
    lows = _tup[0]
    n1 = _tup[1]
    first = lows[0]
    later = lows[1:len(lows)]
    if has_stmts(later):
        tmp = Temp(n1)
        return Low((first.stmts + cdy_rt.table_defs.to_list(SAssign(tmp, first.expr)) + cdy_rt.table_defs.to_list(guard(op, tmp, guarded(op, later, tmp)))), tmp, (n1 + 1))
    else:
        return Low(first.stmts, Call(op, low_exprs(lows, ())), n1)

def guarded(op: Expr, lows: tuple[Low, ...], tmp: Expr) -> tuple[Stmt, ...]:
    low = lows[0]
    assign = (low.stmts + cdy_rt.table_defs.to_list(SAssign(tmp, low.expr)))
    if (len(lows) == 1):
        return assign
    else:
        return (assign + cdy_rt.table_defs.to_list(guard(op, tmp, guarded(op, lows[1:len(lows)], tmp))))

def guard(op: Expr, tmp: Expr, body: tuple[Stmt, ...]) -> Stmt:
    return SIf((tmp if (prim_name(op) == 'and') else Call(Prim('not'), cdy_rt.table_defs.to_list(tmp))), body, ())

def low_exprs(lows: tuple[Low, ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(lows) == 0):
            return acc
        else:
            lows, acc = (lows[1:len(lows)], (acc + cdy_rt.table_defs.to_list(lows[0].expr)))
            continue

def value_seq(exprs: tuple[Expr, ...], n: int) -> tuple[tuple[Stmt, ...], tuple[Expr, ...], int]:
    _tup = low_all(exprs, n, ())
    lows = _tup[0]
    n1 = _tup[1]
    return seq_build(lows, n1, (), ())

def low_all(exprs: tuple[Expr, ...], n: int, acc: tuple[Low, ...]) -> tuple[tuple[Low, ...], int]:
    while True:
        if (len(exprs) == 0):
            return (acc, n)
        else:
            low = value(exprs[0], n)
            exprs, n, acc = (exprs[1:len(exprs)], low.n, (acc + cdy_rt.table_defs.to_list(low)))
            continue

def has_stmts(lows: tuple[Low, ...]) -> bool:
    while True:
        if (len(lows) == 0):
            return False
        else:
            if (len(lows[0].stmts) > 0):
                return True
            else:
                lows = lows[1:len(lows)]
                continue

def seq_build(lows: tuple[Low, ...], n: int, stmts: tuple[Stmt, ...], out: tuple[Expr, ...]) -> tuple[tuple[Stmt, ...], tuple[Expr, ...], int]:
    while True:
        if (len(lows) == 0):
            return (stmts, out, n)
        else:
            low = lows[0]
            later = lows[1:len(lows)]
            if (has_stmts(later) and (not is_simple(low.expr))):
                lows, n, stmts, out = (later, (n + 1), (stmts + low.stmts + cdy_rt.table_defs.to_list(SAssign(Temp(n), low.expr))), (out + cdy_rt.table_defs.to_list(Temp(n))))
                continue
            else:
                lows, stmts, out = (later, (stmts + low.stmts), (out + cdy_rt.table_defs.to_list(low.expr)))
                continue

def value_if(test: Expr, then: Expr, other: Expr, n: int) -> Low:
    t = value(test, n)
    a = value(then, t.n)
    b = value(other, a.n)
    if ((len(a.stmts) == 0) and (len(b.stmts) == 0)):
        return Low(t.stmts, If(t.expr, a.expr, b.expr), b.n)
    else:
        tmp = Temp(b.n)
        return Low((t.stmts + cdy_rt.table_defs.to_list(SIf(t.expr, (a.stmts + cdy_rt.table_defs.to_list(SAssign(tmp, a.expr))), (b.stmts + cdy_rt.table_defs.to_list(SAssign(tmp, b.expr)))))), tmp, (b.n + 1))

def all_but_last(exprs: tuple[Expr, ...]) -> tuple[Expr, ...]:
    return exprs[0:(len(exprs) - 1)]

def last_of(exprs: tuple[Expr, ...]) -> Expr:
    return exprs[(len(exprs) - 1)]

def value_do(body: tuple[Expr, ...], n: int) -> Low:
    _tup = effect_all(all_but_last(body), n, ())
    stmts = _tup[0]
    n1 = _tup[1]
    low = value(last_of(body), n1)
    return Low((stmts + low.stmts), low.expr, low.n)

def tail(e: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    if is_applied(e):
        _tup = bind_applied(e, n)
        stmts = _tup[0]
        body = _tup[1]
        n1 = _tup[2]
        _cdy__tup_653 = tail(body, n1)
        more = _cdy__tup_653[0]
        n2 = _cdy__tup_653[1]
        return ((stmts + more), n2)
    else:
        return tail_plain(e, n)

def tail_plain(e: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t31: object = e
    if isinstance(_cdy_t31, If):
        test = _cdy_t31.test
        then = _cdy_t31.then
        other = _cdy_t31.other
        t = value(test, n)
        _tup = tail(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_665 = tail(other, n1)
        b = _cdy__tup_665[0]
        n2 = _cdy__tup_665[1]
        return ((t.stmts + cdy_rt.table_defs.to_list(SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t31, Do):
        body = _cdy_t31.body
        _cdy__tup_669 = effect_all(all_but_last(body), n, ())
        stmts = _cdy__tup_669[0]
        _cdy_n1_671 = _cdy__tup_669[1]
        _cdy__tup_672 = tail(last_of(body), _cdy_n1_671)
        last = _cdy__tup_672[0]
        _cdy_n2_674 = _cdy__tup_672[1]
        return ((stmts + last), _cdy_n2_674)
    elif isinstance(_cdy_t31, MatchE):
        return lower_match(e, 'tail', NIL, n)
    else:
        low = value(e, n)
        return ((low.stmts + cdy_rt.table_defs.to_list(SReturn(low.expr))), low.n)

def effect(e: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    if is_applied(e):
        _tup = bind_applied(e, n)
        stmts = _tup[0]
        body = _tup[1]
        n1 = _tup[2]
        _cdy__tup_682 = effect(body, n1)
        more = _cdy__tup_682[0]
        n2 = _cdy__tup_682[1]
        return ((stmts + more), n2)
    else:
        return effect_plain(e, n)

def effect_plain(e: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t32: object = e
    if isinstance(_cdy_t32, If):
        test = _cdy_t32.test
        then = _cdy_t32.then
        other = _cdy_t32.other
        t = value(test, n)
        _tup = effect(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_694 = effect(other, n1)
        b = _cdy__tup_694[0]
        n2 = _cdy__tup_694[1]
        return ((t.stmts + cdy_rt.table_defs.to_list(SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t32, Do):
        body = _cdy_t32.body
        return effect_all(body, n, ())
    elif isinstance(_cdy_t32, MatchE):
        return lower_match(e, 'effect', NIL, n)
    else:
        if is_simple(e):
            return ((), n)
        else:
            low = value(e, n)
            return ((low.stmts + cdy_rt.table_defs.to_list(SExpr(low.expr))), low.n)

def effect_all(exprs: tuple[Expr, ...], n: int, acc: tuple[Stmt, ...]) -> tuple[tuple[Stmt, ...], int]:
    while True:
        if (len(exprs) == 0):
            return (acc, n)
        else:
            _tup = effect(exprs[0], n)
            stmts = _tup[0]
            n1 = _tup[1]
            exprs, n, acc = (exprs[1:len(exprs)], n1, (acc + stmts))
            continue

def returns_unit(t: CType) -> bool:
    _cdy_t33: object = t
    if isinstance(_cdy_t33, TFn):
        ret = _cdy_t33.ret
        _cdy_t34: object = ret
        if isinstance(_cdy_t34, TCon):
            name = _cdy_t34.name
            return (name == 'Unit')
        else:
            return False
    else:
        return False

def lower_top(top: Top, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t35: object = top
    if isinstance(_cdy_t35, TDeft):
        name = _cdy_t35.name
        tvars = _cdy_t35.tvars
        fields = _cdy_t35.fields
        return (cdy_rt.table_defs.to_list(SRecord(name, tvars, fields)), n)
    elif isinstance(_cdy_t35, TDeftSum):
        _cdy_name_713 = _cdy_t35.name
        _cdy_tvars_714 = _cdy_t35.tvars
        variants = _cdy_t35.variants
        return (cdy_rt.table_defs.to_list(SSum(_cdy_name_713, _cdy_tvars_714, variants)), n)
    elif isinstance(_cdy_t35, TDef):
        _cdy_name_716 = _cdy_t35.name
        init = _cdy_t35.init
        t = _cdy_t35.t
        low = value(init, n)
        return ((low.stmts + cdy_rt.table_defs.to_list(SDefAssign(_cdy_name_716, low.expr, t))), low.n)
    elif isinstance(_cdy_t35, TDefn):
        _cdy_name_720 = _cdy_t35.name
        params = _cdy_t35.params
        body = _cdy_t35.body
        _cdy_t_723 = _cdy_t35.t
        _tup = (effect(body, n) if returns_unit(_cdy_t_723) else tail(body, n))
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.table_defs.to_list(SFunc(_cdy_name_720, params, loop_tail_calls(_cdy_name_720, params, stmts, returns_unit(_cdy_t_723)), _cdy_t_723)), n1)
    else:
        assert isinstance(_cdy_t35, TExpr)
        e = _cdy_t35.expr
        return effect(e, n)

def loop_tail_calls(name: str, params: tuple[Expr, ...], body: tuple[Stmt, ...], unit: bool) -> tuple[Stmt, ...]:
    if stmts_have_closure(body):
        return body
    else:
        looped = retail_all(body, name, params)
        if (looped == body):
            return body
        else:
            return cdy_rt.table_defs.to_list(SLoop(((looped + cdy_rt.table_defs.to_list(SReturn(NIL))) if unit else looped)))

def retail_all(stmts: tuple[Stmt, ...], name: str, params: tuple[Expr, ...]) -> tuple[Stmt, ...]:
    if (len(stmts) == 0):
        return stmts
    else:
        return (stmts[0:(len(stmts) - 1)] + retail(stmts[(len(stmts) - 1)], name, params))

def retail(s: Stmt, name: str, params: tuple[Expr, ...]) -> tuple[Stmt, ...]:
    _cdy_t36: object = s
    if isinstance(_cdy_t36, SReturn):
        val = _cdy_t36.val
        if is_self_call(val, name, params):
            return jump(params, call_args(val))
        else:
            return cdy_rt.table_defs.to_list(s)
    elif isinstance(_cdy_t36, SExpr):
        e = _cdy_t36.expr
        if is_self_call(e, name, params):
            return jump(params, call_args(e))
        else:
            return cdy_rt.table_defs.to_list(s)
    elif isinstance(_cdy_t36, SIf):
        test = _cdy_t36.test
        then = _cdy_t36.then
        other = _cdy_t36.other
        return cdy_rt.table_defs.to_list(SIf(test, retail_all(then, name, params), retail_all(other, name, params)))
    elif isinstance(_cdy_t36, SMatch):
        temp = _cdy_t36.temp
        subject = _cdy_t36.subject
        cases = _cdy_t36.cases
        default = _cdy_t36.default
        return cdy_rt.table_defs.to_list(SMatch(temp, subject, retail_cases(cases, name, params, ()), retail_lists(default, name, params, ())))
    else:
        return cdy_rt.table_defs.to_list(s)

def retail_cases(cases: tuple[Case, ...], name: str, params: tuple[Expr, ...], acc: tuple[Case, ...]) -> tuple[Case, ...]:
    while True:
        if (len(cases) == 0):
            return acc
        else:
            c = cases[0]
            cases, acc = (cases[1:len(cases)], (acc + cdy_rt.table_defs.to_list(c._replace(body=retail_all(c.body, name, params)))))
            continue

def retail_lists(lists: tuple[tuple[Stmt, ...], ...], name: str, params: tuple[Expr, ...], acc: tuple[tuple[Stmt, ...], ...]) -> tuple[tuple[Stmt, ...], ...]:
    while True:
        if (len(lists) == 0):
            return acc
        else:
            lists, acc = (lists[1:len(lists)], (acc + cdy_rt.table_defs.to_list(retail_all(lists[0], name, params))))
            continue

def is_self_call(e: Expr, name: str, params: tuple[Expr, ...]) -> bool:
    _cdy_t37: object = e
    if isinstance(_cdy_t37, Call):
        callee = _cdy_t37.callee
        args = _cdy_t37.args
        _cdy_t38: object = callee
        if isinstance(_cdy_t38, Global):
            g = _cdy_t38.name
            return ((g == name) and (len(args) == len(params)))
        else:
            return False
    else:
        return False

def call_args(e: Expr) -> tuple[Expr, ...]:
    _cdy_t39: object = e
    if isinstance(_cdy_t39, Call):
        args = _cdy_t39.args
        return args
    else:
        return ()

def jump(params: tuple[Expr, ...], args: tuple[Expr, ...]) -> tuple[Stmt, ...]:
    _tup = changed(params, args, (), ())
    targets = _tup[0]
    vals = _tup[1]
    if (len(targets) == 0):
        return cdy_rt.table_defs.to_list(SContinue())
    else:
        return (cdy_rt.table_defs.to_list(SRebind(targets, vals)) + cdy_rt.table_defs.to_list(SContinue()))

def changed(params: tuple[Expr, ...], args: tuple[Expr, ...], targets: tuple[Expr, ...], vals: tuple[Expr, ...]) -> tuple[tuple[Expr, ...], tuple[Expr, ...]]:
    while True:
        if (len(params) == 0):
            return (targets, vals)
        else:
            if (params[0] == args[0]):
                params, args = (params[1:len(params)], args[1:len(args)])
                continue
            else:
                params, args, targets, vals = (params[1:len(params)], args[1:len(args)], (targets + cdy_rt.table_defs.to_list(params[0])), (vals + cdy_rt.table_defs.to_list(args[0])))
                continue

def stmts_have_closure(stmts: tuple[Stmt, ...]) -> bool:
    while True:
        if (len(stmts) == 0):
            return False
        else:
            if stmt_has_closure(stmts[0]):
                return True
            else:
                stmts = stmts[1:len(stmts)]
                continue

def stmt_has_closure(s: Stmt) -> bool:
    _cdy_t40: object = s
    if isinstance(_cdy_t40, SLocalFunc):
        return True
    elif isinstance(_cdy_t40, SAssign):
        target = _cdy_t40.target
        val = _cdy_t40.val
        return (has_lambda(target) or has_lambda(val))
    elif isinstance(_cdy_t40, SDefAssign):
        _cdy_val_778 = _cdy_t40.val
        return has_lambda(_cdy_val_778)
    elif isinstance(_cdy_t40, SExpr):
        e = _cdy_t40.expr
        return has_lambda(e)
    elif isinstance(_cdy_t40, SReturn):
        _cdy_val_780 = _cdy_t40.val
        return has_lambda(_cdy_val_780)
    elif isinstance(_cdy_t40, SIf):
        test = _cdy_t40.test
        then = _cdy_t40.then
        other = _cdy_t40.other
        return (has_lambda(test) or stmts_have_closure(then) or stmts_have_closure(other))
    elif isinstance(_cdy_t40, SMatch):
        subject = _cdy_t40.subject
        cases = _cdy_t40.cases
        default = _cdy_t40.default
        return (has_lambda(subject) or cases_have_closure(cases) or lists_have_closure(default))
    elif isinstance(_cdy_t40, SLoop):
        body = _cdy_t40.body
        return stmts_have_closure(body)
    elif isinstance(_cdy_t40, SRebind):
        vals = _cdy_t40.vals
        return any_lambda(vals)
    else:
        return False

def cases_have_closure(cases: tuple[Case, ...]) -> bool:
    while True:
        if (len(cases) == 0):
            return False
        else:
            if stmts_have_closure(cases[0].body):
                return True
            else:
                cases = cases[1:len(cases)]
                continue

def lists_have_closure(lists: tuple[tuple[Stmt, ...], ...]) -> bool:
    while True:
        if (len(lists) == 0):
            return False
        else:
            if stmts_have_closure(lists[0]):
                return True
            else:
                lists = lists[1:len(lists)]
                continue

def any_lambda(exprs: tuple[Expr, ...]) -> bool:
    while True:
        if (len(exprs) == 0):
            return False
        else:
            if has_lambda(exprs[0]):
                return True
            else:
                exprs = exprs[1:len(exprs)]
                continue

def has_lambda(e: Expr) -> bool:
    while True:
        _cdy_t41: object = e
        if isinstance(_cdy_t41, Lambda):
            return True
        elif isinstance(_cdy_t41, Call):
            callee = _cdy_t41.callee
            args = _cdy_t41.args
            return (has_lambda(callee) or any_lambda(args))
        elif isinstance(_cdy_t41, If):
            test = _cdy_t41.test
            then = _cdy_t41.then
            other = _cdy_t41.other
            return (has_lambda(test) or has_lambda(then) or has_lambda(other))
        elif isinstance(_cdy_t41, Do):
            body = _cdy_t41.body
            return any_lambda(body)
        elif isinstance(_cdy_t41, Tuple):
            items = _cdy_t41.items
            return any_lambda(items)
        elif isinstance(_cdy_t41, Fmt):
            parts = _cdy_t41.parts
            return any_lambda(holes(parts, ()))
        elif isinstance(_cdy_t41, Field):
            obj = _cdy_t41.obj
            e = obj
            continue
        elif isinstance(_cdy_t41, Assoc):
            _cdy_obj_802 = _cdy_t41.obj
            fields = _cdy_t41.fields
            return (has_lambda(_cdy_obj_802) or any_lambda(field_vals(fields, ())))
        elif isinstance(_cdy_t41, MatchE):
            subject = _cdy_t41.subject
            e = subject
            continue
        else:
            return False

def lower_program(tops: tuple[Top, ...], n: int, acc: tuple[Stmt, ...]) -> tuple[Stmt, ...]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _tup = lower_top(tops[0], n)
            stmts = _tup[0]
            n1 = _tup[1]
            tops, n, acc = (tops[1:len(tops)], n1, (acc + stmts))
            continue

class Env(_cdy_NamedTuple):
    globals_: _cdy_Mapping[str, str]
    locals_: _cdy_Mapping[int, str]
    taken: _cdy_Mapping[str, bool]
    generic: _cdy_Mapping[str, bool]
    table: _cdy_Any
HEADER: str = 'from __future__ import annotations\n\nfrom collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping\nfrom typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple\n'

def comma_join(strs: tuple[str, ...]) -> str:
    return cdy_rt.table_defs.join(strs, ', ')

def line(level: int, text: str) -> str:
    return (cdy_rt.table_defs.get_indent(level) + text + '\n')

def global_names(tops: tuple[Top, ...], env: Env) -> Env:
    while True:
        if (len(tops) == 0):
            return env
        else:
            tops, env = (tops[1:len(tops)], add_globals(top_names_of(tops[0]), env))
            continue

def add_globals(names: tuple[str, ...], env: Env) -> Env:
    while True:
        if (len(names) == 0):
            return env
        else:
            name = names[0]
            py = cdy_rt.table_defs.py_mangle(name)
            names, env = (names[1:len(names)], env._replace(globals_=cdy_rt.table_defs.map_set(env.globals_, name, py), taken=cdy_rt.table_defs.map_set(env.taken, py, True)))
            continue

def top_names_of(top: Top) -> tuple[str, ...]:
    _cdy_t42: object = top
    if isinstance(_cdy_t42, TDeftSum):
        name = _cdy_t42.name
        variants = _cdy_t42.variants
        return (cdy_rt.table_defs.to_list(name) + variant_list_names(variants, ()))
    else:
        if (top_name(top) == ''):
            return ()
        else:
            return cdy_rt.table_defs.to_list(top_name(top))

def variant_list_names(variants: tuple[Variant, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            variants, acc = (variants[1:len(variants)], (acc + cdy_rt.table_defs.to_list(variants[0].name)))
            continue

def top_name(top: Top) -> str:
    _cdy_t43: object = top
    if isinstance(_cdy_t43, TDeft):
        name = _cdy_t43.name
        return name
    elif isinstance(_cdy_t43, TDef):
        _cdy_name_827 = _cdy_t43.name
        return _cdy_name_827
    elif isinstance(_cdy_t43, TDefn):
        _cdy_name_828 = _cdy_t43.name
        return _cdy_name_828
    else:
        return ''

def generic_variants(tops: tuple[Top, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _cdy_t46 = tops[1:len(tops)]
            _cdy_t45: object = tops[0]
            if isinstance(_cdy_t45, TDeftSum):
                tvars = _cdy_t45.tvars
                variants = _cdy_t45.variants
                _cdy_t44 = (acc if (len(tvars) == 0) else mark_all(variant_list_names(variants, ()), acc))
            else:
                _cdy_t44 = acc
            tops, acc = (_cdy_t46, _cdy_t44)
            continue

def mark_all(names: tuple[str, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (names[1:len(names)], cdy_rt.table_defs.map_set(acc, names[0], True))
            continue

def local_py(name: str, id_: int, env: Env) -> str:
    if cdy_rt.table_defs.map_has(env.locals_, id_):
        return cdy_rt.table_defs.map_get(env.locals_, id_)
    else:
        return cdy_rt.table_defs.fail(('emit: local ' + str(name) + ' has no Python name'))

def bind_locals(locs: tuple[Expr, ...], env: Env) -> Env:
    while True:
        if (len(locs) == 0):
            return env
        else:
            _cdy_t50 = locs[1:len(locs)]
            _cdy_t48: object = locs[0]
            if isinstance(_cdy_t48, Local):
                name = _cdy_t48.name
                id_ = _cdy_t48.id_
                if cdy_rt.table_defs.map_has(env.locals_, id_):
                    _cdy_t49 = env
                else:
                    base = cdy_rt.table_defs.py_mangle(name)
                    py = (('_cdy_' + str(base) + '_' + str(id_)) if cdy_rt.table_defs.map_has(env.taken, base) else base)
                    _cdy_t49 = env._replace(locals_=cdy_rt.table_defs.map_set(env.locals_, id_, py), taken=cdy_rt.table_defs.map_set(env.taken, py, True))
                _cdy_t47 = _cdy_t49
            else:
                _cdy_t47 = env
            locs, env = (_cdy_t50, _cdy_t47)
            continue

def bound_locals(stmts: tuple[Stmt, ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(stmts) == 0):
            return acc
        else:
            _cdy_t55 = stmts[1:len(stmts)]
            _cdy_t52: object = stmts[0]
            if isinstance(_cdy_t52, SAssign):
                target = _cdy_t52.target
                _cdy_t54: object = target
                if isinstance(_cdy_t54, Local):
                    _cdy_t53 = (acc + cdy_rt.table_defs.to_list(target))
                else:
                    _cdy_t53 = acc
                _cdy_t51 = _cdy_t53
            elif isinstance(_cdy_t52, SIf):
                then = _cdy_t52.then
                other = _cdy_t52.other
                _cdy_t51 = bound_locals(other, bound_locals(then, acc))
            elif isinstance(_cdy_t52, SMatch):
                cases = _cdy_t52.cases
                default = _cdy_t52.default
                _cdy_t51 = bound_in_cases(cases, bound_in_lists(default, acc))
            elif isinstance(_cdy_t52, SLoop):
                body = _cdy_t52.body
                _cdy_t51 = bound_locals(body, acc)
            else:
                _cdy_t51 = acc
            stmts, acc = (_cdy_t55, _cdy_t51)
            continue

def bound_in_cases(cases: tuple[Case, ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(cases) == 0):
            return acc
        else:
            c = cases[0]
            cases, acc = (cases[1:len(cases)], bound_locals(c.body, (acc + bind_locs(c.binds, ()))))
            continue

def bind_locs(binds: tuple[tuple[str, Expr], ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(binds) == 0):
            return acc
        else:
            _tup = binds[0]
            _ = _tup[0]
            loc = _tup[1]
            binds, acc = (binds[1:len(binds)], (acc + cdy_rt.table_defs.to_list(loc)))
            continue

def bound_in_lists(lists: tuple[tuple[Stmt, ...], ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(lists) == 0):
            return acc
        else:
            lists, acc = (lists[1:len(lists)], bound_locals(lists[0], acc))
            continue

def emit_expr(e: Expr, env: Env) -> str:
    _cdy_t56: object = e
    if isinstance(_cdy_t56, Lit):
        form = _cdy_t56.form
        return emit_lit(form)
    elif isinstance(_cdy_t56, Local):
        name = _cdy_t56.name
        id_ = _cdy_t56.id_
        return local_py(name, id_, env)
    elif isinstance(_cdy_t56, Global):
        _cdy_name_867 = _cdy_t56.name
        return cdy_rt.table_defs.map_get(env.globals_, _cdy_name_867)
    elif isinstance(_cdy_t56, Prim):
        _cdy_name_868 = _cdy_t56.name
        return emit_prim(_cdy_name_868, env)
    elif isinstance(_cdy_t56, Call):
        callee = _cdy_t56.callee
        args = _cdy_t56.args
        return emit_call(callee, args, env)
    elif isinstance(_cdy_t56, If):
        test = _cdy_t56.test
        then = _cdy_t56.then
        other = _cdy_t56.other
        return ('(' + str(emit_expr(then, env)) + ' if ' + str(emit_expr(test, env)) + ' else ' + str(emit_expr(other, env)) + ')')
    elif isinstance(_cdy_t56, Do):
        return cdy_rt.table_defs.fail('emit: a do inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t56, MatchE):
        return cdy_rt.table_defs.fail('emit: a match inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t56, Lambda):
        params = _cdy_t56.params
        body = _cdy_t56.body
        inner = bind_locals(params, env)
        return ('(lambda ' + str(comma_join(emit_exprs(params, inner, ()))) + ': ' + str(emit_expr(body, inner)) + ')')
    elif isinstance(_cdy_t56, Tuple):
        items = _cdy_t56.items
        strs = emit_exprs(items, env, ())
        if (len(strs) == 1):
            return ('(' + str(strs[0]) + ',)')
        else:
            return ('(' + str(comma_join(strs)) + ')')
    elif isinstance(_cdy_t56, Fmt):
        parts = _cdy_t56.parts
        return emit_format(parts, env)
    elif isinstance(_cdy_t56, Field):
        obj = _cdy_t56.obj
        field = _cdy_t56.field
        return (str(emit_expr(obj, env)) + '.' + str(cdy_rt.table_defs.py_mangle(field)))
    elif isinstance(_cdy_t56, Assoc):
        _cdy_obj_882 = _cdy_t56.obj
        fields = _cdy_t56.fields
        return (str(emit_expr(_cdy_obj_882, env)) + '._replace(' + str(comma_join(emit_fields(fields, env, ()))) + ')')
    else:
        assert isinstance(_cdy_t56, Temp)
        _cdy_id__884 = _cdy_t56.id_
        return ('_cdy_t' + str(_cdy_id__884))

def emit_format(parts: tuple[FPart, ...], env: Env) -> str:
    if (len(parts) == 0):
        return "''"
    else:
        return ('(' + str(cdy_rt.table_defs.join(emit_parts(parts, env, ()), ' + ')) + ')')

def emit_parts(parts: tuple[FPart, ...], env: Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t59 = parts[1:len(parts)]
            _cdy_t58: object = parts[0]
            if isinstance(_cdy_t58, FText):
                text = _cdy_t58.text
                _cdy_t57 = cdy_rt.table_defs.py_repr(text)
            else:
                assert isinstance(_cdy_t58, FHole)
                e = _cdy_t58.expr
                _cdy_t57 = ('str(' + str(emit_expr(e, env)) + ')')
            parts, acc = (_cdy_t59, (acc + cdy_rt.table_defs.to_list(_cdy_t57)))
            continue

def emit_fields(fields: tuple[tuple[str, Expr], ...], env: Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            f = _tup[0]
            v = _tup[1]
            fields, acc = (fields[1:len(fields)], (acc + cdy_rt.table_defs.to_list((str(cdy_rt.table_defs.py_mangle(f)) + '=' + str(emit_expr(v, env))))))
            continue

def emit_exprs(exprs: tuple[Expr, ...], env: Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(exprs) == 0):
            return acc
        else:
            exprs, acc = (exprs[1:len(exprs)], (acc + cdy_rt.table_defs.to_list(emit_expr(exprs[0], env))))
            continue

def emit_lit(form: Form) -> str:
    _cdy_t60: object = form
    if isinstance(_cdy_t60, Txt):
        v = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(v)
    elif isinstance(_cdy_t60, CharLit):
        _cdy_v_903 = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(_cdy_v_903)
    elif isinstance(_cdy_t60, IntLit):
        _cdy_v_904 = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(_cdy_v_904)
    elif isinstance(_cdy_t60, LongLit):
        _cdy_v_905 = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(_cdy_v_905)
    elif isinstance(_cdy_t60, ByteLit):
        _cdy_v_906 = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(_cdy_v_906)
    elif isinstance(_cdy_t60, FloatLit):
        _cdy_v_907 = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(_cdy_v_907)
    elif isinstance(_cdy_t60, DoubleLit):
        _cdy_v_908 = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(_cdy_v_908)
    elif isinstance(_cdy_t60, BoolLit):
        _cdy_v_909 = _cdy_t60.val
        return cdy_rt.table_defs.py_repr(_cdy_v_909)
    else:
        return cdy_rt.table_defs.fail('emit: not a literal')

def emit_prim(name: str, env: Env) -> str:
    if cdy_rt.table_defs.in_(cdy_rt.table.get_kind(env.table, name), ('call', 'value', 'index', 'slice')):
        return cdy_rt.table.get_py(env.table, name)
    else:
        return cdy_rt.table_defs.fail(('the operator ' + str(name) + " can't be used as a value yet; wrap it in a fn"))

def emit_call(callee: Expr, args: tuple[Expr, ...], env: Env) -> str:
    strs = emit_exprs(args, env, ())
    _cdy_t61: object = callee
    if isinstance(_cdy_t61, Prim):
        name = _cdy_t61.name
        return emit_prim_call(name, strs, env)
    else:
        return (str(emit_expr(callee, env)) + '(' + str(comma_join(strs)) + ')')

def emit_prim_call(name: str, strs: tuple[str, ...], env: Env) -> str:
    kind = cdy_rt.table.get_kind(env.table, name)
    py = cdy_rt.table.get_py(env.table, name)
    op = (' ' + py + ' ')
    if cdy_rt.table_defs.in_(kind, ('binop', 'compare', 'boolop')):
        return ('(' + str(cdy_rt.table_defs.join(strs, op)) + ')')
    else:
        if (kind == 'unary'):
            return ('(' + str(py) + ' ' + str(strs[0]) + ')')
        else:
            if (kind == 'index'):
                return (str(strs[0]) + '[' + str(strs[1]) + ']')
            else:
                if (kind == 'slice'):
                    return (str(strs[0]) + '[' + str(strs[1]) + ':' + str(strs[2]) + ']')
                else:
                    return (str(py) + '(' + str(comma_join(strs)) + ')')

def emit_type(t: CType, env: Env) -> str:
    _cdy_t62: object = t
    if isinstance(_cdy_t62, TVar):
        name = _cdy_t62.name
        return cdy_rt.table_defs.py_mangle(name)
    elif isinstance(_cdy_t62, TFn):
        params = _cdy_t62.params
        ret = _cdy_t62.ret
        return ('_cdy_Callable[[' + str(comma_join(emit_types(params, env, ()))) + '], ' + str(emit_type(ret, env)) + ']')
    else:
        assert isinstance(_cdy_t62, TCon)
        _cdy_name_928 = _cdy_t62.name
        args = _cdy_t62.args
        return emit_tcon(_cdy_name_928, emit_types(args, env, ()))

def emit_types(types: tuple[CType, ...], env: Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            types, acc = (types[1:len(types)], (acc + cdy_rt.table_defs.to_list(emit_type(types[0], env))))
            continue

def emit_tcon(name: str, args: tuple[str, ...]) -> str:
    if cdy_rt.table_defs.in_(name, ('Int', 'Long', 'Byte')):
        return 'int'
    else:
        if cdy_rt.table_defs.in_(name, ('Float', 'Double')):
            return 'float'
        else:
            if (name == 'Bool'):
                return 'bool'
            else:
                if cdy_rt.table_defs.in_(name, ('Char', 'String')):
                    return 'str'
                else:
                    if (name == 'Unit'):
                        return 'None'
                    else:
                        if (name == 'Any'):
                            return '_cdy_Any'
                        else:
                            if (name == 'Maybe'):
                                return (str(args[0]) + ' | None')
                            else:
                                if (name == 'List'):
                                    return ('tuple[' + str(args[0]) + ', ...]')
                                else:
                                    if (name == 'Tup'):
                                        return ('tuple[' + str(comma_join(args)) + ']')
                                    else:
                                        if (name == 'Map'):
                                            return ('_cdy_Mapping[' + str(comma_join(args)) + ']')
                                        else:
                                            if (len(args) == 0):
                                                return cdy_rt.table_defs.py_mangle(name)
                                            else:
                                                return (str(cdy_rt.table_defs.py_mangle(name)) + '[' + str(comma_join(args)) + ']')

def type_vars(types: tuple[CType, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            _cdy_t65 = types[1:len(types)]
            _cdy_t64: object = types[0]
            if isinstance(_cdy_t64, TVar):
                name = _cdy_t64.name
                _cdy_t63 = (acc if cdy_rt.table_defs.in_(name, acc) else (acc + cdy_rt.table_defs.to_list(name)))
            elif isinstance(_cdy_t64, TCon):
                args = _cdy_t64.args
                _cdy_t63 = type_vars(args, acc)
            else:
                assert isinstance(_cdy_t64, TFn)
                params = _cdy_t64.params
                ret = _cdy_t64.ret
                _cdy_t63 = type_vars((params + cdy_rt.table_defs.to_list(ret)), acc)
            types, acc = (_cdy_t65, _cdy_t63)
            continue

def emit_stmt(s: Stmt, level: int, env: Env) -> str:
    _cdy_t66: object = s
    if isinstance(_cdy_t66, SRecord):
        name = _cdy_t66.name
        tvars = _cdy_t66.tvars
        fields = _cdy_t66.fields
        return ('\n' + line(level, ('class ' + str(cdy_rt.table_defs.map_get(env.globals_, name)) + str(type_params(tvars)) + '(_cdy_NamedTuple):')) + emit_record_fields(fields, (level + 1), env, ''))
    elif isinstance(_cdy_t66, SSum):
        _cdy_name_947 = _cdy_t66.name
        _cdy_tvars_948 = _cdy_t66.tvars
        variants = _cdy_t66.variants
        return (emit_variants(variants, _cdy_tvars_948, level, env, '') + line(level, ('type ' + str(cdy_rt.table_defs.map_get(env.globals_, _cdy_name_947)) + str(type_params(_cdy_tvars_948)) + ' = ' + str(cdy_rt.table_defs.join(variant_refs(variants, _cdy_tvars_948, env, ()), ' | ')))))
    elif isinstance(_cdy_t66, SMatch):
        temp = _cdy_t66.temp
        subject = _cdy_t66.subject
        cases = _cdy_t66.cases
        default = _cdy_t66.default
        t = emit_expr(temp, env)
        val = emit_expr(subject, env)
        generic = cdy_rt.table_defs.map_has(env.generic, cases[0].variant)
        return (line(level, ((str(t) + ' = ' + str(val)) if generic else (str(t) + ': object = ' + str(val)))) + emit_match(t, cases, default, ((not generic) and (len(default) == 0)), 'if', level, env))
    elif isinstance(_cdy_t66, SLoop):
        body = _cdy_t66.body
        return (line(level, 'while True:') + emit_block(body, (level + 1), env))
    elif isinstance(_cdy_t66, SRebind):
        targets = _cdy_t66.targets
        vals = _cdy_t66.vals
        return line(level, ((str(emit_expr(targets[0], env)) + ' = ' + str(emit_expr(vals[0], env))) if (len(targets) == 1) else (str(comma_join(emit_exprs(targets, env, ()))) + ' = (' + str(comma_join(emit_exprs(vals, env, ()))) + ')')))
    elif isinstance(_cdy_t66, SContinue):
        return line(level, 'continue')
    elif isinstance(_cdy_t66, SAssign):
        target = _cdy_t66.target
        _cdy_val_961 = _cdy_t66.val
        return line(level, (str(emit_expr(target, env)) + ' = ' + str(emit_expr(_cdy_val_961, env))))
    elif isinstance(_cdy_t66, SDefAssign):
        _cdy_name_962 = _cdy_t66.name
        _cdy_val_963 = _cdy_t66.val
        _cdy_t_964 = _cdy_t66.t
        return line(level, (str(cdy_rt.table_defs.map_get(env.globals_, _cdy_name_962)) + ': ' + str(emit_type(_cdy_t_964, env)) + ' = ' + str(emit_expr(_cdy_val_963, env))))
    elif isinstance(_cdy_t66, SExpr):
        e = _cdy_t66.expr
        return line(level, emit_expr(e, env))
    elif isinstance(_cdy_t66, SReturn):
        _cdy_e_966 = _cdy_t66.val
        return line(level, ('return ' + str(emit_expr(_cdy_e_966, env))))
    elif isinstance(_cdy_t66, SIf):
        test = _cdy_t66.test
        then = _cdy_t66.then
        other = _cdy_t66.other
        return (line(level, ('if ' + str(emit_expr(test, env)) + ':')) + emit_block(then, (level + 1), env) + ('' if (len(other) == 0) else (line(level, 'else:') + emit_block(other, (level + 1), env))))
    elif isinstance(_cdy_t66, SFunc):
        _cdy_name_970 = _cdy_t66.name
        params = _cdy_t66.params
        _cdy_body_972 = _cdy_t66.body
        _cdy_t_973 = _cdy_t66.t
        return emit_func(_cdy_name_970, params, _cdy_body_972, _cdy_t_973, level, env)
    else:
        assert isinstance(_cdy_t66, SLocalFunc)
        _cdy_target_974 = _cdy_t66.target
        _cdy_params_975 = _cdy_t66.params
        _cdy_body_976 = _cdy_t66.body
        inner = bind_locals((_cdy_params_975 + bound_locals(_cdy_body_976, ())), env)
        args = comma_join(emit_any_params(_cdy_params_975, inner, ()))
        return (line(level, ('def ' + str(emit_expr(_cdy_target_974, env)) + '(' + str(args) + ') -> _cdy_Any:')) + emit_block(_cdy_body_976, (level + 1), inner))

def emit_any_params(params: tuple[Expr, ...], env: Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(params) == 0):
            return acc
        else:
            params, acc = (params[1:len(params)], (acc + cdy_rt.table_defs.to_list((str(emit_expr(params[0], env)) + ': _cdy_Any'))))
            continue

def type_params(tvars: tuple[str, ...]) -> str:
    if (len(tvars) == 0):
        return ''
    else:
        return ('[' + str(comma_join(mangle_all(tvars, ()))) + ']')

def mangle_all(names: tuple[str, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (names[1:len(names)], (acc + cdy_rt.table_defs.to_list(cdy_rt.table_defs.py_mangle(names[0]))))
            continue

def emit_record_fields(fields: tuple[tuple[str, CType], ...], level: int, env: Env, acc: str) -> str:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            f = _tup[0]
            t = _tup[1]
            fields, acc = (fields[1:len(fields)], (acc + line(level, (str(cdy_rt.table_defs.py_mangle(f)) + ': ' + str(emit_type(t, env))))))
            continue

def used_tvars(tvars: tuple[str, ...], used: tuple[str, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(tvars) == 0):
            return acc
        else:
            tvars, acc = (tvars[1:len(tvars)], ((acc + cdy_rt.table_defs.to_list(tvars[0])) if cdy_rt.table_defs.in_(tvars[0], used) else acc))
            continue

def field_types(fields: tuple[tuple[str, CType], ...], acc: tuple[CType, ...]) -> tuple[CType, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            _ = _tup[0]
            t = _tup[1]
            fields, acc = (fields[1:len(fields)], (acc + cdy_rt.table_defs.to_list(t)))
            continue

def variant_tvars(v: Variant, tvars: tuple[str, ...]) -> tuple[str, ...]:
    return used_tvars(tvars, type_vars(field_types(v.fields, ()), ()), ())

def emit_variants(variants: tuple[Variant, ...], tvars: tuple[str, ...], level: int, env: Env, acc: str) -> str:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            head = ('class ' + str(cdy_rt.table_defs.map_get(env.globals_, v.name)) + str(type_params(variant_tvars(v, tvars))) + '(_cdy_NamedTuple):')
            body = (line((level + 1), 'pass') if (len(v.fields) == 0) else emit_record_fields(v.fields, (level + 1), env, ''))
            variants, acc = (variants[1:len(variants)], (acc + '\n' + line(level, head) + body))
            continue

def variant_refs(variants: tuple[Variant, ...], tvars: tuple[str, ...], env: Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            vt = variant_tvars(v, tvars)
            variants, acc = (variants[1:len(variants)], (acc + cdy_rt.table_defs.to_list((cdy_rt.table_defs.map_get(env.globals_, v.name) + type_params(vt)))))
            continue

def emit_match(subj: str, cases: tuple[Case, ...], default: tuple[tuple[Stmt, ...], ...], assert_last: bool, keyword: str, level: int, env: Env) -> str:
    if (len(cases) == 0):
        if (len(default) == 0):
            return ''
        else:
            return (line(level, 'else:') + emit_block(default[0], (level + 1), env))
    else:
        if (assert_last and (len(cases) == 1)):
            c = cases[0]
            inner = (level if (keyword == 'if') else (level + 1))
            return (('' if (keyword == 'if') else line(level, 'else:')) + line(inner, ('assert isinstance(' + str(subj) + ', ' + str(cdy_rt.table_defs.map_get(env.globals_, c.variant)) + ')')) + emit_binds(c.binds, subj, inner, env, '') + emit_stmts(c.body, inner, env, ''))
        else:
            _cdy_c_1025 = cases[0]
            test = (str(keyword) + ' isinstance(' + str(subj) + ', ' + str(cdy_rt.table_defs.map_get(env.globals_, _cdy_c_1025.variant)) + '):')
            binds = emit_binds(_cdy_c_1025.binds, subj, (level + 1), env, '')
            body = ((line((level + 1), 'pass') if (binds == '') else '') if (len(_cdy_c_1025.body) == 0) else emit_stmts(_cdy_c_1025.body, (level + 1), env, ''))
            return (line(level, test) + binds + body + emit_match(subj, cases[1:len(cases)], default, assert_last, 'elif', level, env))

def emit_binds(binds: tuple[tuple[str, Expr], ...], subj: str, level: int, env: Env, acc: str) -> str:
    while True:
        if (len(binds) == 0):
            return acc
        else:
            _tup = binds[0]
            f = _tup[0]
            loc = _tup[1]
            binds, acc = (binds[1:len(binds)], (acc + line(level, (str(emit_expr(loc, env)) + ' = ' + str(subj) + '.' + str(cdy_rt.table_defs.py_mangle(f))))))
            continue

def emit_stmts(stmts: tuple[Stmt, ...], level: int, env: Env, acc: str) -> str:
    while True:
        if (len(stmts) == 0):
            return acc
        else:
            stmts, acc = (stmts[1:len(stmts)], (acc + emit_stmt(stmts[0], level, env)))
            continue

def emit_block(stmts: tuple[Stmt, ...], level: int, env: Env) -> str:
    if (len(stmts) == 0):
        return line(level, 'pass')
    else:
        return emit_stmts(stmts, level, env, '')

def emit_params(params: tuple[Expr, ...], types: tuple[CType, ...], env: Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(params) == 0):
            return acc
        else:
            params, types, acc = (params[1:len(params)], types[1:len(types)], (acc + cdy_rt.table_defs.to_list((str(emit_expr(params[0], env)) + ': ' + str(emit_type(types[0], env))))))
            continue

def emit_func(name: str, params: tuple[Expr, ...], body: tuple[Stmt, ...], t: CType, level: int, env: Env) -> str:
    _cdy_t67: object = t
    if isinstance(_cdy_t67, TFn):
        types = _cdy_t67.params
        ret = _cdy_t67.ret
        inner = bind_locals((params + bound_locals(body, ())), env)
        tvars = type_vars((types + cdy_rt.table_defs.to_list(ret)), ())
        tparams = type_params(tvars)
        args = comma_join(emit_params(params, types, inner, ()))
        return ('\n' + line(level, ('def ' + str(cdy_rt.table_defs.map_get(env.globals_, name)) + str(tparams) + '(' + str(args) + ') -> ' + str(emit_type(ret, env)) + ':')) + emit_block(body, (level + 1), inner))
    else:
        return cdy_rt.table_defs.fail(('defn ' + str(name) + ': its sig must be a function type'))

def emit_imports(modules: tuple[str, ...], acc: str) -> str:
    while True:
        if (len(modules) == 0):
            return acc
        else:
            modules, acc = (modules[1:len(modules)], (acc + ('import ' + str(modules[0]) + '\n')))
            continue

def emit_main(env: Env) -> str:
    name = cdy_rt.table_defs.map_get(env.globals_, 'main')
    return ('\n\nif __name__ == "__main__":\n    cdy_rt.table_defs.run_main(' + str(name) + ')\n')

def translate(forms: tuple[Form, ...], parse: _cdy_Callable[[str], tuple[Form, ...]]) -> str:
    tops = analyse_program(forms, cdy_rt.table.INITIAL_TABLE, parse)
    stmts = lower_program(tops, 0, ())
    globals_ = global_names(tops, Env({}, {}, {}, generic_variants(tops, {}), cdy_rt.table.INITIAL_TABLE))
    env = bind_locals(bound_locals(stmts, ()), globals_)
    return (HEADER + emit_imports(cdy_rt.table.IMPORTS, '') + '\n' + emit_stmts(stmts, 0, env, '') + (emit_main(env) if has_main(tops) else ''))

def translate_text(text: str) -> str:
    return translate(include_imports(read_forms(text), '.'), read_forms)

def translate_file(path: str) -> str:
    return translate(read_program(path), read_forms)
USAGE: str = 'usage: cdy_translator.py FILE.cdy [OUT.py]'

def main(args: tuple[str, ...]) -> int:
    if ((len(args) == 0) or (len(args) > 2)):
        cdy_rt.table_defs.put_err(USAGE)
        return 2
    else:
        src = args[0]
        out = (args[1] if (len(args) == 2) else cdy_rt.table_defs.path_join('output', (cdy_rt.table_defs.path_stem(src) + '.py')))
        python = translate_file(src)
        cdy_rt.table_defs.make_dirs(cdy_rt.table_defs.path_dir(out))
        cdy_rt.table_defs.spit(out, python)
        cdy_rt.table_defs.put_err(('candy: ' + str(src) + ' -> ' + str(out)))
        return 0


if __name__ == "__main__":
    cdy_rt.table_defs.run_main(main)
