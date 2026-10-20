from __future__ import annotations

from collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping
from typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple
import math
import re
import cdy_rt.table
import cdy_rt.table_defs


class Pos(_cdy_NamedTuple):
    file: str
    line: int
    col: int
NOWHERE: Pos = Pos('', 0, 0)

class Sym(_cdy_NamedTuple):
    name: str
    pos: Pos

class Lst(_cdy_NamedTuple):
    items: tuple[Form, ...]
    pos: Pos

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

def form_pos(form: Form) -> Pos:
    _cdy_t2: object = form
    if isinstance(_cdy_t2, Sym):
        pos = _cdy_t2.pos
        return pos
    elif isinstance(_cdy_t2, Lst):
        _cdy_pos_7 = _cdy_t2.pos
        return _cdy_pos_7
    else:
        return NOWHERE

def pos_text(pos: Pos) -> str:
    _cdy_line_9 = pos.line
    col = pos.col
    file = pos.file
    if (_cdy_line_9 == 0):
        return ''
    elif (file == ''):
        return ('line ' + str(_cdy_line_9) + ', column ' + str(col) + ': ')
    else:
        return (str(file) + ':' + str(_cdy_line_9) + ':' + str(col) + ': ')

def gensym(prefix: str) -> Form:
    return Sym(cdy_rt.table_defs.fresh_name(prefix), NOWHERE)

class Macro(_cdy_NamedTuple):
    name: str
    arity: int
    run: _cdy_Any
    pos: Pos

def read_forms(text: str) -> tuple[Form, ...]:
    return read_all(Source('', ()), text, skip(text, 0), ())

def read_source(file: str, text: str) -> tuple[Form, ...]:
    return read_all(Source(file, line_starts(text, 0, cdy_rt.table_defs.to_list(0))), text, skip(text, 0), ())

class Source(_cdy_NamedTuple):
    file: str
    starts: tuple[int, ...]

def line_starts(text: str, pos: int, acc: tuple[int, ...]) -> tuple[int, ...]:
    while True:
        if (pos >= len(text)):
            return acc
        elif (text[pos] == '\n'):
            pos, acc = ((pos + 1), (acc + cdy_rt.table_defs.to_list((pos + 1))))
            continue
        else:
            pos = (pos + 1)
            continue

def pos_at(src: Source, pos: int) -> Pos:
    starts = src.starts
    if (len(starts) == 0):
        return NOWHERE
    else:
        i = line_of(starts, pos, 0, len(starts))
        return Pos(src.file, (i + 1), ((pos - starts[i]) + 1))

def line_of(starts: tuple[int, ...], pos: int, lo: int, hi: int) -> int:
    while True:
        if ((hi - lo) <= 1):
            return lo
        else:
            mid = ((lo + hi) // 2)
            if (starts[mid] <= pos):
                lo = mid
                continue
            else:
                hi = mid
                continue

def read_all(src: Source, text: str, pos: int, acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (pos >= len(text)):
            return acc
        else:
            _tup = read_form(src, text, pos)
            form = _tup[0]
            next_ = _tup[1]
            pos, acc = (skip(text, next_), (acc + cdy_rt.table_defs.to_list(form)))
            continue

def skip(text: str, pos: int) -> int:
    while True:
        if (pos >= len(text)):
            return pos
        elif cdy_rt.table_defs.isspace_at(text, pos):
            pos = (pos + 1)
            continue
        elif (text[pos] == ';'):
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

def read_form(src: Source, text: str, pos: int) -> tuple[Form, int]:
    ch = text[pos]
    if (ch == '('):
        return read_list(src, text, skip(text, (pos + 1)), (), pos)
    elif (ch == ')'):
        return cdy_rt.table_defs.fail(parse_error(src, text, pos, 'unexpected )'))
    elif (ch == '"'):
        return read_str(src, text, (pos + 1), '', pos)
    elif (ch == '\\'):
        return read_char(src, text, pos)
    else:
        return read_atom(src, text, pos, word_end(text, pos))

def read_list(src: Source, text: str, pos: int, acc: tuple[Form, ...], start: int) -> tuple[Form, int]:
    while True:
        if (pos >= len(text)):
            return cdy_rt.table_defs.fail(parse_error(src, text, start, '( is never closed'))
        elif (text[pos] == ')'):
            return (Lst(acc, pos_at(src, start)), (pos + 1))
        else:
            _tup = read_form(src, text, pos)
            form = _tup[0]
            next_ = _tup[1]
            pos, acc = (skip(text, next_), (acc + cdy_rt.table_defs.to_list(form)))
            continue

def read_char(src: Source, text: str, pos: int) -> tuple[Form, int]:
    if (((pos + 1) < len(text)) and (not cdy_rt.table_defs.isspace_at(text, (pos + 1))) and ends_at(text, (pos + 2))):
        return (CharLit(text[(pos + 1)]), (pos + 2))
    else:
        return cdy_rt.table_defs.fail(parse_error(src, text, pos, 'a char is \\ and one character, then a delimiter'))

def read_atom(src: Source, text: str, pos: int, end: int) -> tuple[Form, int]:
    word = text[pos:end]
    kind = number_kind(word)
    if (kind != ''):
        return (number_form(word, kind), end)
    elif (word == 'true'):
        return (BoolLit(True), end)
    elif (word == 'false'):
        return (BoolLit(False), end)
    elif symbol_start(text[pos]):
        stop = symbol_end(text, (pos + 1))
        name = text[pos:stop]
        if cdy_rt.table_defs.in_('__', name):
            return cdy_rt.table_defs.fail(parse_error(src, text, pos, "a name can't contain __ (only gensym makes such names)"))
        else:
            return (Sym(name, pos_at(src, pos)), stop)
    else:
        return cdy_rt.table_defs.fail(parse_error(src, text, pos, ('unexpected ' + str(text[pos]))))

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
    elif (rest == ''):
        return 'int'
    elif (rest == 'l'):
        return 'long'
    elif (rest == 'b'):
        return 'byte'
    elif (rest[0] == '.'):
        j = digits_end(word, (i + 1))
        _cdy_tail_76 = word[j:len(word)]
        if (j == (i + 1)):
            return ''
        elif (_cdy_tail_76 == ''):
            return 'double'
        elif (_cdy_tail_76 == 'f'):
            return 'float'
        else:
            return ''
    else:
        return ''

def number_form(word: str, kind: str) -> Form:
    body = word[0:(len(word) - 1)]
    if (kind == 'int'):
        return IntLit(cdy_rt.table_defs.to_int(word))
    elif (kind == 'long'):
        return LongLit(cdy_rt.table_defs.to_int(body))
    elif (kind == 'byte'):
        return ByteLit(cdy_rt.table_defs.to_int(body))
    elif (kind == 'double'):
        return DoubleLit(cdy_rt.table_defs.to_float(word))
    else:
        return FloatLit(cdy_rt.table_defs.to_float(body))

def read_str(src: Source, text: str, pos: int, acc: str, start: int) -> tuple[Form, int]:
    while True:
        if (pos >= len(text)):
            return cdy_rt.table_defs.fail(parse_error(src, text, start, 'string is never closed'))
        elif (text[pos] == '"'):
            return (Txt(acc), (pos + 1))
        elif (text[pos] == '\\'):
            _tup = escape(src, text, pos)
            ch = _tup[0]
            next_ = _tup[1]
            pos, acc = (next_, (acc + ch))
            continue
        else:
            pos, acc = ((pos + 1), (acc + text[pos]))
            continue

def escape(src: Source, text: str, pos: int) -> tuple[str, int]:
    c = (text[(pos + 1)] if ((pos + 1) < len(text)) else '')
    if cdy_rt.table_defs.in_(c, ('\\', '/', '"')):
        return (c, (pos + 2))
    elif (c == 'b'):
        return ('\x08', (pos + 2))
    elif (c == 'f'):
        return ('\x0c', (pos + 2))
    elif (c == 'n'):
        return ('\n', (pos + 2))
    elif (c == 'r'):
        return ('\r', (pos + 2))
    elif (c == 't'):
        return ('\t', (pos + 2))
    elif ((c == 'u') and ((pos + 6) <= len(text)) and all_hex(text, (pos + 2), (pos + 6))):
        return (cdy_rt.table_defs.hex_char(text[(pos + 2):(pos + 6)]), (pos + 6))
    else:
        return cdy_rt.table_defs.fail(parse_error(src, text, pos, 'bad escape sequence'))

def all_hex(text: str, pos: int, end: int) -> bool:
    while True:
        if (pos >= end):
            return True
        elif cdy_rt.table_defs.in_(text[pos], '0123456789abcdefABCDEF'):
            pos = (pos + 1)
            continue
        else:
            return False

def parse_error(src: Source, text: str, pos: int, msg: str) -> str:
    _tup = row_col(text, 0, pos, 1, 1)
    row = _tup[0]
    col = _tup[1]
    return (str(pos_text(Pos(src.file, row, col))) + 'parse error: ' + str(msg))

def row_col(text: str, i: int, pos: int, row: int, col: int) -> tuple[int, int]:
    while True:
        if (i >= pos):
            return (row, col)
        elif (text[i] == '\n'):
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
    return include_forms(forms, dir_, Incl((), {})).done

def include_file(path: str, acc: Incl) -> Incl:
    key = cdy_rt.table_defs.path_resolve(path)
    if cdy_rt.table_defs.map_has(acc.seen, key):
        return acc
    else:
        return include_forms(read_source(path, cdy_rt.table_defs.slurp(path)), cdy_rt.table_defs.path_dir(path), acc._replace(seen=cdy_rt.table_defs.map_set(acc.seen, key, True)))

def include_forms(forms: tuple[Form, ...], dir_: str, acc: Incl) -> Incl:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            name = import_name(form)
            forms, acc = (rest_of(forms), (acc._replace(done=(acc.done + cdy_rt.table_defs.to_list(macro_import(form, dir_)))) if (name == '') else include_file(import_path('import', dir_, name, form_pos(form)), acc)))
            continue

def macro_import(form: Form, dir_: str) -> Form:
    items = list_items(form)
    pos = form_pos(form)
    if ((len(items) == 0) or (sym_name(items[0]) != 'import-macros')):
        return form
    elif ((len(items) == 2) and (sym_name(items[1]) != '')):
        return Lst((items[0], Txt(import_path('import-macros', dir_, sym_name(items[1]), pos))), pos)
    else:
        return cdy_rt.table_defs.fail((pos_text(pos) + 'import-macros: expected (import-macros name)'))

def import_name(form: Form) -> str:
    items = list_items(form)
    if ((len(items) == 0) or (sym_name(items[0]) != 'import')):
        return ''
    elif ((len(items) == 2) and (sym_name(items[1]) != '')):
        return sym_name(items[1])
    else:
        return cdy_rt.table_defs.fail((pos_text(form_pos(form)) + 'import: expected (import name)'))

def import_path(what: str, dir_: str, name: str, pos: Pos) -> str:
    path = cdy_rt.table_defs.path_join(dir_, (name + '.cdy'))
    if cdy_rt.table_defs.file_exists(path):
        return path
    else:
        return cdy_rt.table_defs.fail((str(pos_text(pos)) + str(what) + ": can't find " + str(name) + '.cdy in ' + str(dir_)))

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
    here: Pos
    macros: _cdy_Mapping[str, Macro]
    quoting: bool

def at_pos(scope: Scope, pos: Pos) -> Scope:
    if (pos.line == 0):
        return scope
    else:
        return scope._replace(here=pos)

def located(scope: Scope, msg: str) -> str:
    return (pos_text(scope.here) + msg)

def bind_local(scope: Scope, name: str, loc: Expr) -> Scope:
    if cdy_rt.table_defs.map_has(scope.macros, name):
        return cdy_rt.table_defs.fail(located(scope, (str(name) + " is a macro, so it can't be bound")))
    else:
        return scope._replace(env=cdy_rt.table_defs.map_set(scope.env, name, loc))

class VInfo(_cdy_NamedTuple):
    sum_: str
    fields: tuple[str, ...]

def is_variant(name: str, scope: Scope) -> bool:
    return (cdy_rt.table_defs.map_has(scope.variants, name) and (not cdy_rt.table_defs.map_has(scope.env, name)))

def variant_fields(name: str, scope: Scope) -> tuple[str, ...]:
    return cdy_rt.table_defs.map_get(scope.variants, name).fields

def analyse_expr(form: Form, scope: Scope, n: int) -> tuple[Expr, int]:
    _cdy_t3: object = form
    if isinstance(_cdy_t3, Sym):
        name = _cdy_t3.name
        pos = _cdy_t3.pos
        return (resolve(name, at_pos(scope, pos)), n)
    elif isinstance(_cdy_t3, Lst):
        items = _cdy_t3.items
        _cdy_pos_146 = _cdy_t3.pos
        return analyse_list(items, at_pos(scope, _cdy_pos_146), n)
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
    elif (is_variant(name, scope) and (len(variant_fields(name, scope)) == 0)):
        return Call(Global(name), ())
    elif (cdy_rt.table_defs.map_has(scope.top, name) and cdy_rt.table_defs.map_get(scope.top, name)):
        return Global(name)
    elif cdy_rt.table.is_special(scope.table, name):
        return cdy_rt.table_defs.fail(located(scope, (str(name) + ' is a special form, not a value')))
    elif cdy_rt.table.is_op(scope.table, name):
        return Prim(name)
    else:
        return cdy_rt.table_defs.fail(located(scope, ('unknown name ' + str(name))))

def is_special_head(name: str, scope: Scope) -> bool:
    return ((not cdy_rt.table_defs.map_has(scope.env, name)) and cdy_rt.table.is_special(scope.table, name))

def analyse_list(items: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(items) == 0):
        return cdy_rt.table_defs.fail(located(scope, 'empty form (): use empty-list for an empty list'))
    else:
        head = sym_name(items[0])
        if is_special_head(head, scope):
            return analyse_special(head, rest_of(items), scope, n)
        else:
            checked = check_variant_call(head, (len(items) - 1), scope)
            _tup = analyse_expr(items[0], scope, n)
            callee = _tup[0]
            n1 = _tup[1]
            _cdy__tup_166 = analyse_all(rest_of(items), scope, n1, ())
            args = _cdy__tup_166[0]
            n2 = _cdy__tup_166[1]
            arity_ok = check_call(callee, len(args), scope)
            return (Call(callee, args), n2)

def check_call(callee: Expr, count: int, scope: Scope) -> bool:
    _cdy_t4: object = callee
    if isinstance(_cdy_t4, Prim):
        name = _cdy_t4.name
        kind = cdy_rt.table.get_kind(scope.table, name)
        arity = cdy_rt.table.get_arity(scope.table, name)
        if (cdy_rt.table_defs.in_(kind, ('binop', 'compare', 'boolop')) and (count < 2)):
            return cdy_rt.table_defs.fail(located(scope, ('(' + str(name) + ' ...) needs at least 2 arguments, got ' + str(count))))
        elif ((arity != None) and (arity != count)):
            return cdy_rt.table_defs.fail(located(scope, ('(' + str(name) + ' ...) takes ' + str(arity) + ' argument(s), got ' + str(count))))
        else:
            return True
    else:
        return True

def check_variant_call(name: str, count: int, scope: Scope) -> bool:
    if (not is_variant(name, scope)):
        return True
    elif (len(variant_fields(name, scope)) == 0):
        return cdy_rt.table_defs.fail(located(scope, (str(name) + ' has no fields, so it is a value: write ' + str(name) + ', not (' + str(name) + ')')))
    elif (count != len(variant_fields(name, scope))):
        return cdy_rt.table_defs.fail(located(scope, ('(' + str(name) + ' ...) takes ' + str(len(variant_fields(name, scope))) + ' field(s), got ' + str(count))))
    else:
        return True

def analyse_special(head: str, rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (head == 'if'):
        return an_if(rest, scope, n)
    elif (head == 'do'):
        return an_do(rest, scope, n)
    elif (head == 'let'):
        return an_let(rest, scope, n)
    elif (head == 'fn'):
        return an_fn(rest, scope, n)
    elif (head == 'tup'):
        return an_tup(rest, scope, n)
    elif (head == 'format'):
        return an_format(rest, scope, n)
    elif (head == 'get'):
        return an_get(rest, scope, n)
    elif (head == 'assoc'):
        return an_assoc(rest, scope, n)
    elif (head == 'match'):
        return an_match(rest, scope, n)
    elif (head == 'quo'):
        return an_quo(rest, scope, n)
    elif (head == 'quasi'):
        return an_quasi(rest, scope, n)
    elif cdy_rt.table_defs.in_(head, ('unq', 'unq-sp')):
        return cdy_rt.table_defs.fail(located(scope, (str(head) + ': only inside quasi')))
    elif cdy_rt.table_defs.in_(head, ('def', 'defn', 'deft', 'sig', 'import', 'import-macros', 'defmacro')):
        return cdy_rt.table_defs.fail(located(scope, (str(head) + ' is only allowed at top level')))
    else:
        return cdy_rt.table_defs.fail(located(scope, (str(head) + ' is not supported by the Candy translator yet')))

def an_if(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    _tup = analyse_all(rest, scope, n, ())
    parts = _tup[0]
    n1 = _tup[1]
    if (len(parts) == 2):
        return (If(parts[0], parts[1], NIL), n1)
    elif (len(parts) == 3):
        return (If(parts[0], parts[1], parts[2]), n1)
    else:
        return cdy_rt.table_defs.fail(located(scope, 'if: expected (if test then else?)'))

def is_else(form: Form) -> bool:
    return (sym_name(form) == 'else')

def an_do(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    _tup = analyse_all(rest, scope, n, ())
    body = _tup[0]
    n1 = _tup[1]
    if (len(body) == 0):
        return (NIL, n1)
    elif (len(body) == 1):
        return (body[0], n1)
    else:
        return (Do(body), n1)

def an_let(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if ((len(rest) != 2) or (not is_list_form(rest[0]))):
        return cdy_rt.table_defs.fail(located(scope, 'let: expected (let ((name init)*) body)'))
    elif (len(list_items(rest[0])) == 0):
        return analyse_expr(rest[1], scope, n)
    else:
        _tup = let_bindings(list_items(rest[0]), scope, n, ())
        pairs = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_203 = analyse_expr(rest[1], inner, n1)
        body = _cdy__tup_203[0]
        n2 = _cdy__tup_203[1]
        return (nest(pairs, body), n2)

def is_list_form(form: Form) -> bool:
    _cdy_t5: object = form
    if isinstance(_cdy_t5, Lst):
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
                return cdy_rt.table_defs.fail(located(scope, 'let: binding must be (name init)'))
            else:
                _tup = analyse_expr(items[1], scope, n)
                init = _tup[0]
                n1 = _tup[1]
                target = items[0]
                _cdy_t6: object = target
                if isinstance(_cdy_t6, Lst):
                    names = _cdy_t6.items
                    tmp = Local('_tup', n1)
                    _cdy__tup_218 = destructure(names, tmp, 0, scope, (n1 + 1), ())
                    more = _cdy__tup_218[0]
                    inner = _cdy__tup_218[1]
                    n2 = _cdy__tup_218[2]
                    bindings, scope, n, acc = (rest_of(bindings), inner, n2, (acc + cdy_rt.table_defs.to_list((tmp, init)) + more))
                    continue
                else:
                    name = sym_name(target)
                    loc = Local(name, n1)
                    if ((name == '') or cdy_rt.table.is_special(scope.table, name)):
                        return cdy_rt.table_defs.fail(located(scope, 'let name must be a name, not a special form'))
                    else:
                        bindings, scope, n, acc = (rest_of(bindings), bind_local(scope, name, loc), (n1 + 1), (acc + cdy_rt.table_defs.to_list((loc, init))))
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
                return cdy_rt.table_defs.fail(located(scope, 'let name must be a name'))
            else:
                names, i, scope, n, acc = (rest_of(names), (i + 1), bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.table_defs.to_list((loc, item))))
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
        return cdy_rt.table_defs.fail(located(scope, 'fn: expected (fn (args+) body), with exactly one body form'))
    else:
        _tup = bind_params(list_items(rest[0]), scope, n, ())
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_245 = analyse_expr(rest[1], inner, n1)
        body = _cdy__tup_245[0]
        n2 = _cdy__tup_245[1]
        if (len(params) == 0):
            return cdy_rt.table_defs.fail(located(scope, 'fn arguments: at least one is needed'))
        else:
            return (Lambda(params, body), n2)

def an_tup(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) == 0):
        return cdy_rt.table_defs.fail(located(scope, 'tup: needs at least one item'))
    else:
        _tup = analyse_all(rest, scope, n, ())
        items = _tup[0]
        n1 = _tup[1]
        return (Tuple(items), n1)

def an_get(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if ((len(rest) != 2) or (sym_name(rest[1]) == '')):
        return cdy_rt.table_defs.fail(located(scope, 'get: expected (get obj field)'))
    else:
        _tup = analyse_expr(rest[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        return (Field(obj, sym_name(rest[1])), n1)

def an_assoc(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) < 3):
        return cdy_rt.table_defs.fail(located(scope, 'assoc: expected (assoc obj field value ...)'))
    else:
        _tup = analyse_expr(rest[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        _cdy__tup_266 = assoc_fields(rest_of(rest), scope, n1, ())
        fields = _cdy__tup_266[0]
        n2 = _cdy__tup_266[1]
        return (Assoc(obj, fields), n2)

def assoc_fields(forms: tuple[Form, ...], scope: Scope, n: int, acc: tuple[tuple[str, Expr], ...]) -> tuple[tuple[tuple[str, Expr], ...], int]:
    while True:
        if (len(forms) == 0):
            return (acc, n)
        elif (len(forms) == 1):
            return cdy_rt.table_defs.fail(located(scope, 'assoc: expected (assoc obj field value ...)'))
        else:
            field = sym_name(forms[0])
            _tup = analyse_expr(forms[1], scope, n)
            val = _tup[0]
            n1 = _tup[1]
            if (field == ''):
                return cdy_rt.table_defs.fail(located(scope, 'assoc field must be a name'))
            else:
                forms, n, acc = (forms[2:len(forms)], n1, (acc + cdy_rt.table_defs.to_list((field, val))))
                continue

def an_format(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    if (len(rest) != 1):
        return cdy_rt.table_defs.fail(located(scope, 'format: expected one string literal'))
    else:
        _cdy_t7: object = rest[0]
        if isinstance(_cdy_t7, Txt):
            text = _cdy_t7.val
            _tup = format_parts(text, 0, '', scope, n, ())
            parts = _tup[0]
            n1 = _tup[1]
            return (Fmt(parts), n1)
        else:
            return cdy_rt.table_defs.fail(located(scope, 'format: expected one string literal'))

def format_parts(text: str, pos: int, acc: str, scope: Scope, n: int, parts: tuple[FPart, ...]) -> tuple[tuple[FPart, ...], int]:
    while True:
        c = (text[pos:(pos + 1)] if (pos < len(text)) else '')
        next_ = (text[(pos + 1):(pos + 2)] if ((pos + 1) < len(text)) else '')
        if (c == ''):
            return (add_text(parts, acc), n)
        elif ((c == '{') and (next_ == '{')):
            pos, acc = ((pos + 2), (acc + '{'))
            continue
        elif ((c == '}') and (next_ == '}')):
            pos, acc = ((pos + 2), (acc + '}'))
            continue
        elif (c == '}'):
            return cdy_rt.table_defs.fail(located(scope, 'format: unmatched } (write }} for a brace)'))
        elif (c == '{'):
            end = hole_end(text, (pos + 1))
            forms = scope.parse(text[(pos + 1):end])
            if (len(forms) != 1):
                return cdy_rt.table_defs.fail(located(scope, 'format: a {hole} must hold exactly one form'))
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
        elif (text[pos:(pos + 1)] == '}'):
            return pos
        elif (text[pos:(pos + 1)] == '{'):
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
        return cdy_rt.table_defs.fail(located(scope, 'match: expected (match subject ((Variant name*) expr)+ (else expr)?)'))
    elif is_tup_clause(rest[1]):
        return an_match_tup(rest, scope, n)
    else:
        return an_match_sum(rest, scope, n)

def an_match_sum(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    _tup = analyse_expr(rest[0], scope, n)
    subject = _tup[0]
    n1 = _tup[1]
    _cdy__tup_310 = match_clauses(rest_of(rest), scope, n1, MatchE(subject, (), ()), '')
    m = _cdy__tup_310[0]
    n2 = _cdy__tup_310[1]
    sum_ = (match_sum(match_clause_list(m), scope) if (len(match_clause_list(m)) > 0) else '')
    return (check_exhaustive(m, sum_, scope), n2)

def is_tup_clause(clause: Form) -> bool:
    return (sym_name(first_item(first_item(clause))) == 'tup')

def an_match_tup(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    items = list_items(rest[1])
    names = rest_of(list_items(items[0]))
    if ((len(rest) != 2) or (len(items) != 2)):
        return cdy_rt.table_defs.fail(located(scope, 'match: a (tup name+) pattern must be the only clause, with no else'))
    elif (len(names) == 0):
        return cdy_rt.table_defs.fail(located(scope, 'match: a (tup name+) pattern needs at least one name'))
    else:
        _tup = analyse_expr(rest[0], scope, n)
        subject = _tup[0]
        n1 = _tup[1]
        tmp = Local('_tup', n1)
        _cdy__tup_324 = tup_binds(names, tmp, 0, scope, (n1 + 1), ())
        pairs = _cdy__tup_324[0]
        inner = _cdy__tup_324[1]
        n2 = _cdy__tup_324[2]
        _cdy__tup_328 = analyse_expr(items[1], inner, n2)
        body = _cdy__tup_328[0]
        n3 = _cdy__tup_328[1]
        return (nest((cdy_rt.table_defs.to_list((tmp, subject)) + pairs), body), n3)

def tup_binds(names: tuple[Form, ...], tmp: Expr, i: int, scope: Scope, n: int, acc: tuple[tuple[Expr, Expr], ...]) -> tuple[tuple[tuple[Expr, Expr], ...], Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = sym_name(names[0])
            loc = Local(name, n)
            item = Call(Prim('at'), (tmp, Lit(IntLit(i))))
            if (name == ''):
                return cdy_rt.table_defs.fail(located(scope, 'match name must be a name'))
            elif (name == '_'):
                names, i = (rest_of(names), (i + 1))
                continue
            elif bound_in_pairs(name, acc):
                return cdy_rt.table_defs.fail(located(scope, 'match: names in a pattern must be different'))
            else:
                names, i, scope, n, acc = (rest_of(names), (i + 1), bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.table_defs.to_list((loc, item))))
                continue

def bound_in_pairs(name: str, pairs: tuple[tuple[Expr, Expr], ...]) -> bool:
    while True:
        if (len(pairs) == 0):
            return False
        else:
            _tup = pairs[0]
            loc = _tup[0]
            _ = _tup[1]
            _cdy_t8: object = loc
            if isinstance(_cdy_t8, Local):
                other = _cdy_t8.name
                return ((other == name) or bound_in_pairs(name, rest_of_pairs(pairs)))
            else:
                pairs = rest_of_pairs(pairs)
                continue

def rest_of_pairs(pairs: tuple[tuple[Expr, Expr], ...]) -> tuple[tuple[Expr, Expr], ...]:
    return pairs[1:len(pairs)]

def match_sum(clauses: tuple[Clause, ...], scope: Scope) -> str:
    return cdy_rt.table_defs.map_get(scope.variants, clauses[0].variant).sum_

def check_exhaustive(m: Expr, sum_: str, scope: Scope) -> Expr:
    _cdy_t9: object = m
    if isinstance(_cdy_t9, MatchE):
        clauses = _cdy_t9.clauses
        default = _cdy_t9.default
        missing = missing_variants(cdy_rt.table_defs.map_get(scope.sums, sum_), clauses, ())
        if ((len(default) == 0) and (len(missing) > 0)):
            return cdy_rt.table_defs.fail(located(scope, ('match on ' + str(sum_) + ': no clause for ' + str(cdy_rt.table_defs.join(missing, ', ')) + ' (or add else)')))
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
        elif (clauses[0].variant == name):
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
                return cdy_rt.table_defs.fail(located(scope, 'match: clause must be (pattern expr)'))
            elif is_else(items[0]):
                if ((len(forms) > 1) or (len(match_clause_list(m)) == 0)):
                    return cdy_rt.table_defs.fail(located(scope, 'match: (else expr) must be the last clause, after a pattern'))
                else:
                    _tup = analyse_expr(items[1], scope, n)
                    e = _tup[0]
                    n1 = _tup[1]
                    return (set_default(m, e), n1)
            else:
                pattern = list_items(items[0])
                variant = (sym_name(pattern[0]) if (len(pattern) > 0) else '')
                checked = check_pattern(variant, pattern, sum_, m, scope)
                _cdy__tup_372 = pattern_binds(variant_fields(variant, scope), rest_of(pattern), scope, n, ())
                binds = _cdy__tup_372[0]
                inner = _cdy__tup_372[1]
                _cdy_n1_375 = _cdy__tup_372[2]
                _cdy__tup_376 = analyse_expr(items[1], inner, _cdy_n1_375)
                body = _cdy__tup_376[0]
                n2 = _cdy__tup_376[1]
                forms, n, m, sum_ = (rest_of(forms), n2, add_clause(m, Clause(variant, binds, body)), cdy_rt.table_defs.map_get(scope.variants, variant).sum_)
                continue

def check_pattern(variant: str, pattern: tuple[Form, ...], sum_: str, m: Expr, scope: Scope) -> bool:
    if (variant == ''):
        return cdy_rt.table_defs.fail(located(scope, 'match: pattern must be (Variant name*) or else'))
    elif (variant == 'tup'):
        return cdy_rt.table_defs.fail(located(scope, 'match: a (tup name+) pattern must be the only clause, with no else'))
    elif (not is_variant(variant, scope)):
        return cdy_rt.table_defs.fail(located(scope, ('match: ' + str(variant) + ' is not a variant of a sum type')))
    elif has_clause(variant, match_clause_list(m)):
        return cdy_rt.table_defs.fail(located(scope, ('match: more than one clause for ' + str(variant))))
    elif ((sum_ != '') and (sum_ != cdy_rt.table_defs.map_get(scope.variants, variant).sum_)):
        return cdy_rt.table_defs.fail(located(scope, ('match: clauses mix variants of ' + str(sum_) + ' and ' + str(cdy_rt.table_defs.map_get(scope.variants, variant).sum_))))
    elif ((len(pattern) - 1) != len(variant_fields(variant, scope))):
        return cdy_rt.table_defs.fail(located(scope, ('match: ' + str(variant) + ' has ' + str(len(variant_fields(variant, scope))) + ' field(s), so the pattern needs that many names')))
    else:
        return True

def match_clause_list(m: Expr) -> tuple[Clause, ...]:
    _cdy_t10: object = m
    if isinstance(_cdy_t10, MatchE):
        clauses = _cdy_t10.clauses
        return clauses
    else:
        return ()

def add_clause(m: Expr, clause: Clause) -> Expr:
    _cdy_t11: object = m
    if isinstance(_cdy_t11, MatchE):
        subject = _cdy_t11.subject
        clauses = _cdy_t11.clauses
        default = _cdy_t11.default
        return MatchE(subject, (clauses + cdy_rt.table_defs.to_list(clause)), default)
    else:
        return m

def set_default(m: Expr, e: Expr) -> Expr:
    _cdy_t12: object = m
    if isinstance(_cdy_t12, MatchE):
        subject = _cdy_t12.subject
        clauses = _cdy_t12.clauses
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
                return cdy_rt.table_defs.fail(located(scope, 'match name must be a name'))
            elif (name == '_'):
                fields, names = (fields[1:len(fields)], rest_of(names))
                continue
            elif bound_in(name, acc):
                return cdy_rt.table_defs.fail(located(scope, 'match: names in a pattern must be different'))
            else:
                fields, names, scope, n, acc = (fields[1:len(fields)], rest_of(names), bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.table_defs.to_list((fields[0], loc))))
                continue

def bound_in(name: str, binds: tuple[tuple[str, Expr], ...]) -> bool:
    while True:
        if (len(binds) == 0):
            return False
        else:
            _tup = binds[0]
            _ = _tup[0]
            loc = _tup[1]
            _cdy_t13: object = loc
            if isinstance(_cdy_t13, Local):
                other = _cdy_t13.name
                return ((other == name) or bound_in(name, binds[1:len(binds)]))
            else:
                binds = binds[1:len(binds)]
                continue

def an_quo(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    checked = needs_form('quo', scope)
    if (len(rest) != 1):
        return cdy_rt.table_defs.fail(located(scope, 'quo: expected (quo form)'))
    else:
        return (quoted(rest[0]), n)

def an_quasi(rest: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    checked = needs_form('quasi', scope)
    if (len(rest) != 1):
        return cdy_rt.table_defs.fail(located(scope, 'quasi: expected (quasi form)'))
    else:
        return quasi_form(rest[0], scope, n)

def needs_form(what: str, scope: Scope) -> bool:
    if scope.quoting:
        return True
    else:
        return cdy_rt.table_defs.fail(located(scope, (str(what) + ': only in macro code')))

def quoted(form: Form) -> Expr:
    _cdy_t14: object = form
    if isinstance(_cdy_t14, Sym):
        name = _cdy_t14.name
        return Call(Global('Sym'), (Lit(Txt(name)), Global('NOWHERE')))
    elif isinstance(_cdy_t14, Lst):
        items = _cdy_t14.items
        return Call(Global('Lst'), (form_list(quoted_all(items, ())), Global('NOWHERE')))
    else:
        return Call(Global(literal_variant(form)), cdy_rt.table_defs.to_list(Lit(form)))

def quoted_all(forms: tuple[Form, ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (rest_of(forms), (acc + cdy_rt.table_defs.to_list(quoted(forms[0]))))
            continue

def form_list(items: tuple[Expr, ...]) -> Expr:
    if (len(items) == 0):
        return Prim('empty-list')
    else:
        return Tuple(items)

def literal_variant(form: Form) -> str:
    _cdy_t15: object = form
    if isinstance(_cdy_t15, Txt):
        return 'Txt'
    elif isinstance(_cdy_t15, IntLit):
        return 'IntLit'
    elif isinstance(_cdy_t15, LongLit):
        return 'LongLit'
    elif isinstance(_cdy_t15, ByteLit):
        return 'ByteLit'
    elif isinstance(_cdy_t15, FloatLit):
        return 'FloatLit'
    elif isinstance(_cdy_t15, DoubleLit):
        return 'DoubleLit'
    elif isinstance(_cdy_t15, CharLit):
        return 'CharLit'
    elif isinstance(_cdy_t15, BoolLit):
        return 'BoolLit'
    else:
        return cdy_rt.table_defs.fail('quo: not a literal')

def head_name(form: Form) -> str:
    return sym_name(first_item(form))

def quasi_form(form: Form, scope: Scope, n: int) -> tuple[Expr, int]:
    head = head_name(form)
    here = at_pos(scope, form_pos(form))
    if (head == 'unq'):
        return unq_arg(form, here, n)
    elif (head == 'unq-sp'):
        return cdy_rt.table_defs.fail(located(here, 'unq-sp: only inside a list in quasi'))
    elif (head == 'quasi'):
        return cdy_rt.table_defs.fail(located(here, "quasi: a quasi inside a quasi isn't supported yet"))
    elif is_list_form(form):
        return quasi_list(list_items(form), here, n)
    else:
        return (quoted(form), n)

def unq_arg(form: Form, scope: Scope, n: int) -> tuple[Expr, int]:
    items = list_items(form)
    if (len(items) != 2):
        return cdy_rt.table_defs.fail(located(scope, (str(head_name(form)) + ': expected (' + str(head_name(form)) + ' expr)')))
    else:
        return analyse_expr(items[1], scope, n)

def quasi_list(items: tuple[Form, ...], scope: Scope, n: int) -> tuple[Expr, int]:
    _tup = quasi_parts(items, scope, n, (), ())
    parts = _tup[0]
    n1 = _tup[1]
    return (Call(Global('Lst'), (join_parts(parts), Global('NOWHERE'))), n1)

def quasi_parts(items: tuple[Form, ...], scope: Scope, n: int, run: tuple[Expr, ...], parts: tuple[Expr, ...]) -> tuple[tuple[Expr, ...], int]:
    while True:
        if (len(items) == 0):
            return (close_run(run, parts), n)
        else:
            item = items[0]
            if (head_name(item) == 'unq-sp'):
                _tup = unq_arg(item, at_pos(scope, form_pos(item)), n)
                e = _tup[0]
                n1 = _tup[1]
                items, n, run, parts = (rest_of(items), n1, (), (close_run(run, parts) + cdy_rt.table_defs.to_list(e)))
                continue
            else:
                _cdy__tup_450 = quasi_form(item, scope, n)
                _cdy_e_451 = _cdy__tup_450[0]
                _cdy_n1_452 = _cdy__tup_450[1]
                items, n, run = (rest_of(items), _cdy_n1_452, (run + cdy_rt.table_defs.to_list(_cdy_e_451)))
                continue

def close_run(run: tuple[Expr, ...], parts: tuple[Expr, ...]) -> tuple[Expr, ...]:
    if (len(run) == 0):
        return parts
    else:
        return (parts + cdy_rt.table_defs.to_list(Tuple(run)))

def join_parts(parts: tuple[Expr, ...]) -> Expr:
    if (len(parts) == 0):
        return Prim('empty-list')
    elif (len(parts) == 1):
        return parts[0]
    else:
        return Call(Prim('+'), parts)

def is_lower(name: str) -> bool:
    return ((len(name) > 0) and (name[0:1] >= 'a') and (name[0:1] <= 'z'))

def analyse_type(form: Form) -> CType:
    _cdy_t16: object = form
    if isinstance(_cdy_t16, Sym):
        name = _cdy_t16.name
        if is_lower(name):
            return TVar(name)
        else:
            return TCon(name, ())
    elif isinstance(_cdy_t16, Lst):
        items = _cdy_t16.items
        if (len(items) == 0):
            return cdy_rt.table_defs.fail((pos_text(form_pos(form)) + 'bad type ()'))
        elif (sym_name(items[0]) == 'Fn'):
            if (len(items) == 3):
                return TFn(analyse_types(list_items(items[1]), ()), analyse_type(items[2]))
            else:
                return cdy_rt.table_defs.fail((pos_text(form_pos(form)) + 'bad function type: expected (Fn (Arg+) Ret)'))
        else:
            return TCon(sym_name(items[0]), analyse_types(rest_of(items), ()))
    else:
        return cdy_rt.table_defs.fail((pos_text(form_pos(form)) + 'bad type'))

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
            forms, acc = (rest_of(forms), (add_name(sym_name(items[1]), form_pos(items[1]), acc) if ((head == 'def') or (head == 'defn')) else (add_names(variant_names(items[2:len(items)], ()), form_pos(items[1]), cdy_rt.table_defs.map_set(add_name(deft_name(items[1]), form_pos(items[1]), acc), deft_name(items[1]), False)) if ((head == 'deft') and is_sum_body(items[2:len(items)])) else (add_name(deft_name(items[1]), form_pos(items[1]), acc) if (head == 'deft') else acc))))
            continue

def add_name(name: str, pos: Pos, acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    if cdy_rt.table_defs.map_has(acc, name):
        return cdy_rt.table_defs.fail((pos_text(pos) + ('defined more than once: ' + str(name))))
    else:
        return cdy_rt.table_defs.map_set(acc, name, True)

def add_names(names: tuple[str, ...], pos: Pos, acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (names[1:len(names)], add_name(names[0], pos, acc))
            continue

def is_sum_body(body: tuple[Form, ...]) -> bool:
    return ((len(body) > 0) and all_variant_forms(body))

def all_variant_forms(body: tuple[Form, ...]) -> bool:
    while True:
        if (len(body) == 0):
            return True
        elif (sym_name(first_item(body[0])) == ''):
            return False
        else:
            body = rest_of(body)
            continue

def first_item(form: Form) -> Form:
    items = list_items(form)
    if (len(items) == 0):
        return Lst((), NOWHERE)
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
            _cdy_t18 = rest_of(forms)
            if ((head == 'deft') and is_sum_body(body)):
                sum_ = deft_name(items[1])
                _cdy_t17 = add_variants(sum_, body, scope._replace(sums=cdy_rt.table_defs.map_set(scope.sums, sum_, variant_names(body, ()))))
            else:
                _cdy_t17 = scope
            forms, scope = (_cdy_t18, _cdy_t17)
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
    _cdy_t19: object = form
    if isinstance(_cdy_t19, Lst):
        items = _cdy_t19.items
        if (len(items) == 0):
            return ''
        else:
            return sym_name(items[0])
    else:
        return sym_name(form)

def analyse_program(forms: tuple[Form, ...], table: _cdy_Any, parse: _cdy_Callable[[str], tuple[Form, ...]], macros: _cdy_Mapping[str, Macro], quoting: bool) -> tuple[Top, ...]:
    scope = find_variants(forms, Scope({}, top_names(forms, {}), table, parse, {}, {}, NOWHERE, macros, quoting))
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
    here = at_pos(scope, form_pos(form))
    if (cdy_rt.table_defs.in_(head, ('def', 'defn')) and (len(items) > 1) and cdy_rt.table_defs.map_has(scope.macros, sym_name(items[1]))):
        return cdy_rt.table_defs.fail(located(here, (str(sym_name(items[1])) + " is a macro, so it can't be defined")))
    elif (head == 'sig'):
        return top_sig(items, here, prog)
    elif (head == 'def'):
        return top_def(items, here, prog)
    elif (head == 'defn'):
        return top_defn(items, here, prog)
    elif (head == 'deft'):
        return top_deft(items, here, prog)
    else:
        _tup = analyse_expr(form, here, prog.n)
        e = _tup[0]
        n = _tup[1]
        return add_top(prog, TExpr(e), n)

def top_sig(items: tuple[Form, ...], scope: Scope, prog: Prog) -> Prog:
    name = (sym_name(items[1]) if (len(items) == 3) else '')
    if (name == ''):
        return cdy_rt.table_defs.fail(located(scope, 'sig: expected (sig name Type)'))
    elif (not cdy_rt.table_defs.map_has(prog.defs, name)):
        return cdy_rt.table_defs.fail(located(scope, ('sig for ' + str(name) + ', but no def or defn of ' + str(name) + ' in this file')))
    elif cdy_rt.table_defs.map_has(prog.defined, name):
        return cdy_rt.table_defs.fail(located(scope, ('sig for ' + str(name) + ' comes after its definition')))
    elif cdy_rt.table_defs.map_has(prog.sigs, name):
        return cdy_rt.table_defs.fail(located(scope, ('more than one sig for ' + str(name))))
    else:
        return prog._replace(sigs=cdy_rt.table_defs.map_set(prog.sigs, name, analyse_type(items[2])))

def top_deft(items: tuple[Form, ...], scope: Scope, prog: Prog) -> Prog:
    name = (deft_name(items[1]) if (len(items) > 1) else '')
    tvars = (syms(rest_of(list_items(items[1])), ()) if (len(items) > 1) else ())
    body = items[2:len(items)]
    field_forms = (list_items(items[2]) if (len(items) == 3) else ())
    if (name == ''):
        return cdy_rt.table_defs.fail(located(scope, 'deft: expected (deft Name ((field Type)+)) or (deft Name variant+)'))
    elif is_sum_body(body):
        return add_top(prog, TDeftSum(name, tvars, deft_variants(body, ())), prog.n)
    elif (len(field_forms) == 0):
        return cdy_rt.table_defs.fail(located(scope, 'deft: expected (deft Name ((field Type)+))'))
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
                return cdy_rt.table_defs.fail((pos_text(form_pos(body[0])) + ('deft: variant names are Capitalised, not ' + str(name))))
            elif (len(v_items) == 1):
                body, acc = (rest_of(body), (acc + cdy_rt.table_defs.to_list(Variant(name, ()))))
                continue
            elif ((len(v_items) == 2) and (len(list_items(v_items[1])) > 0)):
                body, acc = (rest_of(body), (acc + cdy_rt.table_defs.to_list(Variant(name, deft_fields(list_items(v_items[1]), ())))))
                continue
            else:
                return cdy_rt.table_defs.fail((pos_text(form_pos(body[0])) + 'deft: variant must be (Name) or (Name ((field Type)+))'))

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
                return cdy_rt.table_defs.fail((pos_text(form_pos(forms[0])) + 'deft: field must be (name Type)'))
            else:
                forms, acc = (rest_of(forms), (acc + cdy_rt.table_defs.to_list((sym_name(items[0]), analyse_type(items[1])))))
                continue

def needs_sig(name: str, prog: Prog, scope: Scope) -> CType:
    if cdy_rt.table_defs.map_has(prog.sigs, name):
        return cdy_rt.table_defs.map_get(prog.sigs, name)
    else:
        return cdy_rt.table_defs.fail(located(scope, (str(name) + ' needs a (sig ' + str(name) + ' Type) before its definition')))

def top_def(items: tuple[Form, ...], scope: Scope, prog: Prog) -> Prog:
    if (len(items) != 3):
        return cdy_rt.table_defs.fail(located(scope, 'def: expected (def name init); the initial value is required'))
    else:
        name = sym_name(items[1])
        t = needs_sig(name, prog, scope)
        _tup = analyse_expr(items[2], scope, prog.n)
        init = _tup[0]
        n = _tup[1]
        return mark_defined(add_top(prog, TDef(name, init, t), n), name)

def top_defn(items: tuple[Form, ...], scope: Scope, prog: Prog) -> Prog:
    if (len(items) != 4):
        return cdy_rt.table_defs.fail(located(scope, 'defn: expected (defn name (args+) body), with exactly one body form'))
    else:
        name = sym_name(items[1])
        t = needs_sig(name, prog, scope)
        arg_forms = list_items(items[2])
        _tup = bind_params(arg_forms, scope, prog.n, ())
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_563 = analyse_expr(items[3], inner, n1)
        body = _cdy__tup_563[0]
        n2 = _cdy__tup_563[1]
        if (len(params) == 0):
            return cdy_rt.table_defs.fail(located(scope, ('defn ' + str(name) + ': at least one argument is needed')))
        elif (len(params) != fn_arity(t)):
            return cdy_rt.table_defs.fail(located(scope, ('defn ' + str(name) + ': its sig must be a function type with one type per argument')))
        else:
            return mark_defined(add_top(prog, TDefn(name, params, body, t), n2), name)

def fn_arity(t: CType) -> int:
    _cdy_t20: object = t
    if isinstance(_cdy_t20, TFn):
        params = _cdy_t20.params
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
                return cdy_rt.table_defs.fail(located(scope, 'a parameter must be a name'))
            else:
                forms, scope, n, acc = (rest_of(forms), bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.table_defs.to_list(loc)))
                continue
MAIN_TYPE: CType = TFn(cdy_rt.table_defs.to_list(TCon('List', cdy_rt.table_defs.to_list(TCon('String', ())))), TCon('Int', ()))

def has_main(tops: tuple[Top, ...]) -> bool:
    while True:
        if (len(tops) == 0):
            return False
        elif is_main(tops[0]):
            return True
        else:
            tops = tops[1:len(tops)]
            continue

def is_main(top: Top) -> bool:
    _cdy_t21: object = top
    if isinstance(_cdy_t21, TDefn):
        name = _cdy_t21.name
        t = _cdy_t21.t
        if (name != 'main'):
            return False
        elif (t == MAIN_TYPE):
            return True
        else:
            return cdy_rt.table_defs.fail('main must be typed (Fn ((List String)) Int)')
    elif isinstance(_cdy_t21, TDef):
        _cdy_name_578 = _cdy_t21.name
        if (_cdy_name_578 == 'main'):
            return cdy_rt.table_defs.fail('main must be a defn')
        else:
            return False
    else:
        return False

class Imports(_cdy_NamedTuple):
    macros: tuple[Macro, ...]
    helpers: tuple[tuple[str, tuple[Form, ...]], ...]
    seen: _cdy_Mapping[str, bool]

class Expanded(_cdy_NamedTuple):
    forms: tuple[Form, ...]
    macros: _cdy_Mapping[str, Macro]
    own: tuple[Macro, ...]
    helpers: tuple[tuple[str, tuple[Form, ...]], ...]

def expand_program(forms: tuple[Form, ...], compile_: _cdy_Callable[[tuple[Form, ...]], str]) -> tuple[tuple[Form, ...], _cdy_Mapping[str, Macro]]:
    done = expand_file(forms, False, compile_, ())
    return (done.forms, done.macros)
MACRO_HEADS: tuple[str, ...] = ('defmacro', 'import-macros')

def expand_file(forms: tuple[Form, ...], macro_file: bool, compile_: _cdy_Callable[[tuple[Form, ...]], str], loading: tuple[str, ...]) -> Expanded:
    imports = import_all((prelude_import(loading) + pick_forms(forms, ('import-macros',), True, ())), compile_, loading, Imports((), (), {}))
    imported = macro_map(imports.macros, {})
    defs = expand_defs(pick_forms(forms, ('defmacro',), True, ()), imported, ())
    rest = pick_forms(forms, MACRO_HEADS, False, ())
    helpers = (expand_all(rest, imported, ()) if macro_file else ())
    own = (() if (len(defs) == 0) else load_defs(defs, (helper_forms(imports.helpers, ()) + helpers), compile_))
    macros = macro_map(own, imported)
    return Expanded((helpers if macro_file else expand_all(rest, macros, ())), macros, own, imports.helpers)

def prelude_import(loading: tuple[str, ...]) -> tuple[Form, ...]:
    path = library_path('prelude_macros.cdy')
    if cdy_rt.table_defs.in_(cdy_rt.table_defs.path_resolve(path), loading):
        return ()
    else:
        return cdy_rt.table_defs.to_list(Lst((Sym('import-macros', NOWHERE), Txt(path)), NOWHERE))

def pick_forms(forms: tuple[Form, ...], heads: tuple[str, ...], keep: bool, acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            items = list_items(form)
            picked = ((len(items) > 0) and cdy_rt.table_defs.in_(sym_name(items[0]), heads))
            forms, acc = (rest_of(forms), ((acc + cdy_rt.table_defs.to_list(form)) if (picked == keep) else acc))
            continue

def expand_defs(defs: tuple[Form, ...], macros: _cdy_Mapping[str, Macro], acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(defs) == 0):
            return acc
        else:
            defs, acc = (rest_of(defs), (acc + cdy_rt.table_defs.to_list(Lst(expand_after(list_items(defs[0]), 3, macros), form_pos(defs[0])))))
            continue

def macro_map(macros: tuple[Macro, ...], acc: _cdy_Mapping[str, Macro]) -> _cdy_Mapping[str, Macro]:
    while True:
        if (len(macros) == 0):
            return acc
        else:
            macro = macros[0]
            name = macro.name
            if cdy_rt.table_defs.map_has(acc, name):
                return cdy_rt.table_defs.fail((str(pos_text(macro.pos)) + 'defmacro: ' + str(name) + ' is already a macro'))
            else:
                macros, acc = (macros[1:len(macros)], cdy_rt.table_defs.map_set(acc, name, macro))
                continue

def import_all(forms: tuple[Form, ...], compile_: _cdy_Callable[[tuple[Form, ...]], str], loading: tuple[str, ...], acc: Imports) -> Imports:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (rest_of(forms), import_file(forms[0], compile_, loading, acc))
            continue

def import_file(form: Form, compile_: _cdy_Callable[[tuple[Form, ...]], str], loading: tuple[str, ...], acc: Imports) -> Imports:
    path = macro_path(form)
    key = cdy_rt.table_defs.path_resolve(path)
    if cdy_rt.table_defs.map_has(acc.seen, key):
        return acc
    elif cdy_rt.table_defs.in_(key, loading):
        return cdy_rt.table_defs.fail((str(pos_text(form_pos(form))) + 'import-macros: ' + str(path) + ' imports itself'))
    else:
        done = expand_file(read_program(path), True, compile_, (loading + cdy_rt.table_defs.to_list(key)))
        return Imports((acc.macros + done.own), add_helpers((done.helpers + cdy_rt.table_defs.to_list((key, done.forms))), acc.helpers), cdy_rt.table_defs.map_set(acc.seen, key, True))

def macro_path(form: Form) -> str:
    _cdy_t22: object = list_items(form)[1]
    if isinstance(_cdy_t22, Txt):
        path = _cdy_t22.val
        return path
    else:
        return cdy_rt.table_defs.fail((pos_text(form_pos(form)) + 'import-macros: expected (import-macros name)'))

def add_helpers(groups: tuple[tuple[str, tuple[Form, ...]], ...], acc: tuple[tuple[str, tuple[Form, ...]], ...]) -> tuple[tuple[str, tuple[Form, ...]], ...]:
    while True:
        if (len(groups) == 0):
            return acc
        else:
            groups, acc = (groups[1:len(groups)], (acc if has_helpers(groups[0][0], acc) else (acc + cdy_rt.table_defs.to_list(groups[0]))))
            continue

def has_helpers(key: str, groups: tuple[tuple[str, tuple[Form, ...]], ...]) -> bool:
    return ((len(groups) > 0) and ((groups[0][0] == key) or has_helpers(key, groups[1:len(groups)])))

def helper_forms(groups: tuple[tuple[str, tuple[Form, ...]], ...], acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(groups) == 0):
            return acc
        else:
            groups, acc = (groups[1:len(groups)], (acc + groups[0][1]))
            continue

def load_defs(defs: tuple[Form, ...], helpers: tuple[Form, ...], compile_: _cdy_Callable[[tuple[Form, ...]], str]) -> tuple[Macro, ...]:
    checked = unique_names(defs, {})
    form_forms = form_defs(None)
    python = compile_((form_forms + helpers + macro_program(defs, ())))
    loaded = cdy_rt.table_defs.load_macros(python, sym_name, top_names(form_forms, {}))
    return macro_list(defs, loaded, ())

def form_defs(_: None) -> tuple[Form, ...]:
    path = library_path('form.cdy')
    return read_source(path, cdy_rt.table_defs.slurp(path))

def library_path(name: str) -> str:
    dir_ = cdy_rt.table_defs.module_dir(sym_name)
    path = cdy_rt.table_defs.path_join(dir_, name)
    if cdy_rt.table_defs.file_exists(path):
        return path
    else:
        return cdy_rt.table_defs.fail(('macros need ' + str(name) + ' next to the translator, in ' + str(dir_)))

def macro_program(defs: tuple[Form, ...], acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(defs) == 0):
            return acc
        else:
            items = defmacro_items(defs[0])
            pos = form_pos(defs[0])
            fname = Sym(macro_fn(sym_name(items[1])), pos)
            args = Sym('args__', pos)
            type_ = Lst((Sym('Fn', pos), Lst(cdy_rt.table_defs.to_list(Lst((Sym('List', pos), Sym('Form', pos)), pos)), pos), Sym('Form', pos)), pos)
            body = Lst((Sym('let', pos), Lst(param_binds(items[2], args, pos), pos), items[3]), pos)
            defs, acc = (rest_of(defs), (acc + cdy_rt.table_defs.to_list(Lst((Sym('sig', pos), fname, type_), pos)) + cdy_rt.table_defs.to_list(Lst((Sym('defn', pos), fname, Lst(cdy_rt.table_defs.to_list(args), pos), body), pos))))
            continue

def defmacro_items(form: Form) -> tuple[Form, ...]:
    items = list_items(form)
    where = pos_text(form_pos(form))
    if ((len(items) != 4) or (sym_name(items[1]) == '')):
        return cdy_rt.table_defs.fail((where + 'defmacro: expected (defmacro name (params) body) or (defmacro name args body)'))
    elif cdy_rt.table.is_special(cdy_rt.table.INITIAL_TABLE, sym_name(items[1])):
        return cdy_rt.table_defs.fail((str(where) + 'defmacro: ' + str(sym_name(items[1])) + ' is a special form'))
    elif (not params_ok(items[2])):
        return cdy_rt.table_defs.fail((where + 'defmacro: a parameter must be a name'))
    else:
        return items

def params_ok(params: Form) -> bool:
    _cdy_t23: object = params
    if isinstance(_cdy_t23, Sym):
        return True
    elif isinstance(_cdy_t23, Lst):
        items = _cdy_t23.items
        return all_names(items)
    else:
        return False

def all_names(forms: tuple[Form, ...]) -> bool:
    return ((len(forms) == 0) or ((sym_name(forms[0]) != '') and all_names(rest_of(forms))))

def param_binds(params: Form, args: Form, pos: Pos) -> tuple[Form, ...]:
    if (sym_name(params) == ''):
        return arg_binds(list_items(params), args, 0, pos, ())
    else:
        return cdy_rt.table_defs.to_list(Lst((params, args), pos))

def arg_binds(params: tuple[Form, ...], args: Form, i: int, pos: Pos, acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(params) == 0):
            return acc
        else:
            params, i, acc = (rest_of(params), (i + 1), (acc + cdy_rt.table_defs.to_list(Lst((params[0], Lst((Sym('at', pos), args, IntLit(i)), pos)), pos))))
            continue

def macro_fn(name: str) -> str:
    return ('macro__' + name)

def unique_names(defs: tuple[Form, ...], seen: _cdy_Mapping[str, bool]) -> bool:
    while True:
        if (len(defs) == 0):
            return True
        else:
            name = sym_name(defmacro_items(defs[0])[1])
            if cdy_rt.table_defs.map_has(seen, name):
                return cdy_rt.table_defs.fail((str(pos_text(form_pos(defs[0]))) + 'defmacro: ' + str(name) + ' is defined twice'))
            else:
                defs, seen = (rest_of(defs), cdy_rt.table_defs.map_set(seen, name, True))
                continue

def macro_list(defs: tuple[Form, ...], loaded: _cdy_Mapping[str, _cdy_Any], acc: tuple[Macro, ...]) -> tuple[Macro, ...]:
    while True:
        if (len(defs) == 0):
            return acc
        else:
            items = list_items(defs[0])
            name = sym_name(items[1])
            params = items[2]
            arity = (len(list_items(params)) if (sym_name(params) == '') else -1)
            run = cdy_rt.table_defs.map_get(loaded, cdy_rt.table_defs.py_mangle(macro_fn(name)))
            defs, acc = (rest_of(defs), (acc + cdy_rt.table_defs.to_list(Macro(name, arity, run, form_pos(defs[0])))))
            continue

def expand_all(forms: tuple[Form, ...], macros: _cdy_Mapping[str, Macro], acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (rest_of(forms), (acc + cdy_rt.table_defs.to_list(expand_form(forms[0], macros))))
            continue

def expand_form(form: Form, macros: _cdy_Mapping[str, Macro]) -> Form:
    while True:
        _cdy_t24: object = form
        if isinstance(_cdy_t24, Lst):
            items = _cdy_t24.items
            pos = _cdy_t24.pos
            head = ('' if (len(items) == 0) else sym_name(items[0]))
            if cdy_rt.table_defs.map_has(macros, head):
                form = expand_call(cdy_rt.table_defs.map_get(macros, head), rest_of(items), pos)
                continue
            elif cdy_rt.table_defs.in_(head, ('sig', 'deft', 'import', 'import-macros', 'quo', 'quasi')):
                return form
            elif (head == 'defn'):
                return Lst(expand_after(items, 3, macros), pos)
            elif (head == 'fn'):
                return Lst(expand_after(items, 2, macros), pos)
            elif cdy_rt.table_defs.in_(head, ('let', 'match')):
                return Lst(expand_clauses(head, items, macros), pos)
            else:
                return Lst(expand_all(items, macros, ()), pos)
        else:
            return form

def expand_after(items: tuple[Form, ...], n: int, macros: _cdy_Mapping[str, Macro]) -> tuple[Form, ...]:
    if (len(items) < n):
        return items
    else:
        return (items[0:n] + expand_all(items[n:len(items)], macros, ()))

def expand_clauses(head: str, items: tuple[Form, ...], macros: _cdy_Mapping[str, Macro]) -> tuple[Form, ...]:
    if ((head == 'let') and (len(items) == 3)):
        _cdy_t25: object = items[1]
        if isinstance(_cdy_t25, Lst):
            binds = _cdy_t25.items
            p = _cdy_t25.pos
            return (items[0], Lst(each_clause(binds, 1, macros, ()), p), expand_form(items[2], macros))
        else:
            return expand_all(items, macros, ())
    elif ((head == 'match') and (len(items) > 1)):
        return ((items[0], expand_form(items[1], macros)) + each_clause(items[2:len(items)], 1, macros, ()))
    else:
        return expand_all(items, macros, ())

def each_clause(clauses: tuple[Form, ...], n: int, macros: _cdy_Mapping[str, Macro], acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(clauses) == 0):
            return acc
        else:
            clauses, acc = (rest_of(clauses), (acc + cdy_rt.table_defs.to_list(expand_clause(clauses[0], n, macros))))
            continue

def expand_clause(clause: Form, n: int, macros: _cdy_Mapping[str, Macro]) -> Form:
    _cdy_t26: object = clause
    if isinstance(_cdy_t26, Lst):
        items = _cdy_t26.items
        p = _cdy_t26.pos
        return Lst(expand_after(items, n, macros), p)
    else:
        return expand_form(clause, macros)

def expand_call(macro: Macro, args: tuple[Form, ...], pos: Pos) -> Form:
    arity = macro.arity
    where = (str(pos_text(pos)) + str(macro.name) + ': ')
    if ((arity >= 0) and (arity != len(args))):
        return cdy_rt.table_defs.fail((str(where) + 'expected ' + str(arity) + ' argument(s), got ' + str(len(args))))
    else:
        return stamp(cdy_rt.table_defs.call_macro(macro.run, args, where), pos)

def stamp(form: Form, pos: Pos) -> Form:
    _cdy_t27: object = form
    if isinstance(_cdy_t27, Sym):
        name = _cdy_t27.name
        p = _cdy_t27.pos
        if (p.line == 0):
            return Sym(name, pos)
        else:
            return form
    elif isinstance(_cdy_t27, Lst):
        items = _cdy_t27.items
        _cdy_p_709 = _cdy_t27.pos
        return Lst(stamp_all(items, pos, ()), (pos if (_cdy_p_709.line == 0) else _cdy_p_709))
    else:
        return form

def stamp_all(forms: tuple[Form, ...], pos: Pos, acc: tuple[Form, ...]) -> tuple[Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (rest_of(forms), (acc + cdy_rt.table_defs.to_list(stamp(forms[0], pos))))
            continue

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
    _cdy_t28: object = e
    if isinstance(_cdy_t28, Lit):
        return True
    elif isinstance(_cdy_t28, Local):
        return True
    elif isinstance(_cdy_t28, Global):
        return True
    elif isinstance(_cdy_t28, Prim):
        return True
    elif isinstance(_cdy_t28, Temp):
        return True
    else:
        return False

def is_applied(e: Expr) -> bool:
    _cdy_t29: object = e
    if isinstance(_cdy_t29, Call):
        callee = _cdy_t29.callee
        args = _cdy_t29.args
        _cdy_t30: object = callee
        if isinstance(_cdy_t30, Lambda):
            params = _cdy_t30.params
            return (len(params) == len(args))
        else:
            return False
    else:
        return False

def bind_applied(e: Expr, n: int) -> tuple[tuple[Stmt, ...], Expr, int]:
    _cdy_t31: object = e
    if isinstance(_cdy_t31, Call):
        callee = _cdy_t31.callee
        args = _cdy_t31.args
        _cdy_t32: object = callee
        if isinstance(_cdy_t32, Lambda):
            params = _cdy_t32.params
            body = _cdy_t32.body
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
        _cdy_t33: object = e
        if isinstance(_cdy_t33, Call):
            callee = _cdy_t33.callee
            args = _cdy_t33.args
            return value_call(callee, args, n)
        elif isinstance(_cdy_t33, If):
            test = _cdy_t33.test
            then = _cdy_t33.then
            other = _cdy_t33.other
            return value_if(test, then, other, n)
        elif isinstance(_cdy_t33, Do):
            _cdy_body_743 = _cdy_t33.body
            return value_do(_cdy_body_743, n)
        elif isinstance(_cdy_t33, Lambda):
            params = _cdy_t33.params
            _cdy_body_745 = _cdy_t33.body
            return value_fn(params, _cdy_body_745, n)
        elif isinstance(_cdy_t33, Tuple):
            items = _cdy_t33.items
            _cdy__tup_747 = value_seq(items, n)
            _cdy_stmts_748 = _cdy__tup_747[0]
            vals = _cdy__tup_747[1]
            _cdy_n1_750 = _cdy__tup_747[2]
            return Low(_cdy_stmts_748, Tuple(vals), _cdy_n1_750)
        elif isinstance(_cdy_t33, Fmt):
            parts = _cdy_t33.parts
            _cdy__tup_752 = value_seq(holes(parts, ()), n)
            _cdy_stmts_753 = _cdy__tup_752[0]
            _cdy_vals_754 = _cdy__tup_752[1]
            _cdy_n1_755 = _cdy__tup_752[2]
            return Low(_cdy_stmts_753, Fmt(fill_holes(parts, _cdy_vals_754, ())), _cdy_n1_755)
        elif isinstance(_cdy_t33, Field):
            obj = _cdy_t33.obj
            field = _cdy_t33.field
            _cdy_low_758 = value(obj, n)
            return Low(_cdy_low_758.stmts, Field(_cdy_low_758.expr, field), _cdy_low_758.n)
        elif isinstance(_cdy_t33, Assoc):
            _cdy_obj_759 = _cdy_t33.obj
            fields = _cdy_t33.fields
            _cdy__tup_761 = value_seq((cdy_rt.table_defs.to_list(_cdy_obj_759) + field_vals(fields, ())), n)
            _cdy_stmts_762 = _cdy__tup_761[0]
            _cdy_vals_763 = _cdy__tup_761[1]
            _cdy_n1_764 = _cdy__tup_761[2]
            return Low(_cdy_stmts_762, Assoc(_cdy_vals_763[0], refill(fields, _cdy_vals_763[1:len(_cdy_vals_763)], ())), _cdy_n1_764)
        elif isinstance(_cdy_t33, MatchE):
            tmp = Temp(n)
            _cdy__tup_766 = lower_match(e, 'value', tmp, (n + 1))
            _cdy_stmts_767 = _cdy__tup_766[0]
            _cdy_n1_768 = _cdy__tup_766[1]
            return Low(_cdy_stmts_767, tmp, _cdy_n1_768)
        else:
            return Low((), e, n)

def lower_match(e: Expr, mode: str, tmp: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t34: object = e
    if isinstance(_cdy_t34, MatchE):
        subject = _cdy_t34.subject
        clauses = _cdy_t34.clauses
        default = _cdy_t34.default
        low = value(subject, n)
        temp = Temp(low.n)
        _tup = lower_cases(clauses, mode, tmp, (low.n + 1), ())
        cases = _tup[0]
        n2 = _tup[1]
        _cdy__tup_781 = lower_default(default, mode, tmp, n2)
        default_stmts = _cdy__tup_781[0]
        n3 = _cdy__tup_781[1]
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
    elif (mode == 'effect'):
        return effect(e, n)
    else:
        low = value(e, n)
        return ((low.stmts + cdy_rt.table_defs.to_list(SAssign(tmp, low.expr))), low.n)

def value_fn(params: tuple[Expr, ...], body: Expr, n: int) -> Low:
    _tup = tail(body, n)
    stmts = _tup[0]
    n1 = _tup[1]
    _cdy_t35: object = (stmts[0] if (len(stmts) == 1) else SExpr(NIL))
    if isinstance(_cdy_t35, SReturn):
        result = _cdy_t35.val
        return Low((), Lambda(params, result), n1)
    else:
        return Low(cdy_rt.table_defs.to_list(SLocalFunc(Temp(n1), params, stmts)), Temp(n1), (n1 + 1))

def holes(parts: tuple[FPart, ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t38 = parts[1:len(parts)]
            _cdy_t37: object = parts[0]
            if isinstance(_cdy_t37, FHole):
                e = _cdy_t37.expr
                _cdy_t36 = (acc + cdy_rt.table_defs.to_list(e))
            else:
                assert isinstance(_cdy_t37, FText)
                _cdy_t36 = acc
            parts, acc = (_cdy_t38, _cdy_t36)
            continue

def fill_holes(parts: tuple[FPart, ...], vals: tuple[Expr, ...], acc: tuple[FPart, ...]) -> tuple[FPart, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t39: object = parts[0]
            if isinstance(_cdy_t39, FHole):
                parts, vals, acc = (parts[1:len(parts)], vals[1:len(vals)], (acc + cdy_rt.table_defs.to_list(FHole(vals[0]))))
                continue
            else:
                assert isinstance(_cdy_t39, FText)
                text = _cdy_t39.text
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
    _cdy_t40: object = e
    if isinstance(_cdy_t40, Prim):
        name = _cdy_t40.name
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
        elif (len(lows[0].stmts) > 0):
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
    elif is_if_into(b.stmts, b.expr):
        tmp = b.expr
        return Low((t.stmts + cdy_rt.table_defs.to_list(SIf(t.expr, (a.stmts + cdy_rt.table_defs.to_list(SAssign(tmp, a.expr))), b.stmts))), tmp, b.n)
    else:
        _cdy_tmp_882 = Temp(b.n)
        return Low((t.stmts + cdy_rt.table_defs.to_list(SIf(t.expr, (a.stmts + cdy_rt.table_defs.to_list(SAssign(_cdy_tmp_882, a.expr))), (b.stmts + cdy_rt.table_defs.to_list(SAssign(_cdy_tmp_882, b.expr)))))), _cdy_tmp_882, (b.n + 1))

def is_if_into(stmts: tuple[Stmt, ...], e: Expr) -> bool:
    _cdy_t45 = (len(stmts) == 1)
    if _cdy_t45:
        _cdy_t42: object = stmts[0]
        if isinstance(_cdy_t42, SIf):
            _cdy_t41 = True
        else:
            _cdy_t41 = False
        _cdy_t45 = _cdy_t41
        if _cdy_t45:
            _cdy_t44: object = e
            if isinstance(_cdy_t44, Temp):
                _cdy_t43 = True
            else:
                _cdy_t43 = False
            _cdy_t45 = _cdy_t43
    return _cdy_t45

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
        _cdy__tup_899 = tail(body, n1)
        more = _cdy__tup_899[0]
        n2 = _cdy__tup_899[1]
        return ((stmts + more), n2)
    else:
        return tail_plain(e, n)

def tail_plain(e: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t46: object = e
    if isinstance(_cdy_t46, If):
        test = _cdy_t46.test
        then = _cdy_t46.then
        other = _cdy_t46.other
        t = value(test, n)
        _tup = tail(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_911 = tail(other, n1)
        b = _cdy__tup_911[0]
        n2 = _cdy__tup_911[1]
        return ((t.stmts + cdy_rt.table_defs.to_list(SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t46, Do):
        body = _cdy_t46.body
        _cdy__tup_915 = effect_all(all_but_last(body), n, ())
        stmts = _cdy__tup_915[0]
        _cdy_n1_917 = _cdy__tup_915[1]
        _cdy__tup_918 = tail(last_of(body), _cdy_n1_917)
        last = _cdy__tup_918[0]
        _cdy_n2_920 = _cdy__tup_918[1]
        return ((stmts + last), _cdy_n2_920)
    elif isinstance(_cdy_t46, MatchE):
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
        _cdy__tup_928 = effect(body, n1)
        more = _cdy__tup_928[0]
        n2 = _cdy__tup_928[1]
        return ((stmts + more), n2)
    else:
        return effect_plain(e, n)

def effect_plain(e: Expr, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t47: object = e
    if isinstance(_cdy_t47, If):
        test = _cdy_t47.test
        then = _cdy_t47.then
        other = _cdy_t47.other
        t = value(test, n)
        _tup = effect(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_940 = effect(other, n1)
        b = _cdy__tup_940[0]
        n2 = _cdy__tup_940[1]
        return ((t.stmts + cdy_rt.table_defs.to_list(SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t47, Do):
        body = _cdy_t47.body
        return effect_all(body, n, ())
    elif isinstance(_cdy_t47, MatchE):
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
    _cdy_t48: object = t
    if isinstance(_cdy_t48, TFn):
        ret = _cdy_t48.ret
        _cdy_t49: object = ret
        if isinstance(_cdy_t49, TCon):
            name = _cdy_t49.name
            return (name == 'Unit')
        else:
            return False
    else:
        return False

def lower_top(top: Top, n: int) -> tuple[tuple[Stmt, ...], int]:
    _cdy_t50: object = top
    if isinstance(_cdy_t50, TDeft):
        name = _cdy_t50.name
        tvars = _cdy_t50.tvars
        fields = _cdy_t50.fields
        return (cdy_rt.table_defs.to_list(SRecord(name, tvars, fields)), n)
    elif isinstance(_cdy_t50, TDeftSum):
        _cdy_name_959 = _cdy_t50.name
        _cdy_tvars_960 = _cdy_t50.tvars
        variants = _cdy_t50.variants
        return (cdy_rt.table_defs.to_list(SSum(_cdy_name_959, _cdy_tvars_960, variants)), n)
    elif isinstance(_cdy_t50, TDef):
        _cdy_name_962 = _cdy_t50.name
        init = _cdy_t50.init
        t = _cdy_t50.t
        low = value(init, n)
        return ((low.stmts + cdy_rt.table_defs.to_list(SDefAssign(_cdy_name_962, low.expr, t))), low.n)
    elif isinstance(_cdy_t50, TDefn):
        _cdy_name_966 = _cdy_t50.name
        params = _cdy_t50.params
        body = _cdy_t50.body
        _cdy_t_969 = _cdy_t50.t
        _tup = (effect(body, n) if returns_unit(_cdy_t_969) else tail(body, n))
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.table_defs.to_list(SFunc(_cdy_name_966, params, loop_tail_calls(_cdy_name_966, params, stmts, returns_unit(_cdy_t_969)), _cdy_t_969)), n1)
    else:
        assert isinstance(_cdy_t50, TExpr)
        e = _cdy_t50.expr
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
    _cdy_t51: object = s
    if isinstance(_cdy_t51, SReturn):
        val = _cdy_t51.val
        if is_self_call(val, name, params):
            return jump(params, call_args(val))
        else:
            return cdy_rt.table_defs.to_list(s)
    elif isinstance(_cdy_t51, SExpr):
        e = _cdy_t51.expr
        if is_self_call(e, name, params):
            return jump(params, call_args(e))
        else:
            return cdy_rt.table_defs.to_list(s)
    elif isinstance(_cdy_t51, SIf):
        test = _cdy_t51.test
        then = _cdy_t51.then
        other = _cdy_t51.other
        return cdy_rt.table_defs.to_list(SIf(test, retail_all(then, name, params), retail_all(other, name, params)))
    elif isinstance(_cdy_t51, SMatch):
        temp = _cdy_t51.temp
        subject = _cdy_t51.subject
        cases = _cdy_t51.cases
        default = _cdy_t51.default
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
    _cdy_t52: object = e
    if isinstance(_cdy_t52, Call):
        callee = _cdy_t52.callee
        args = _cdy_t52.args
        _cdy_t53: object = callee
        if isinstance(_cdy_t53, Global):
            g = _cdy_t53.name
            return ((g == name) and (len(args) == len(params)))
        else:
            return False
    else:
        return False

def call_args(e: Expr) -> tuple[Expr, ...]:
    _cdy_t54: object = e
    if isinstance(_cdy_t54, Call):
        args = _cdy_t54.args
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
        elif (params[0] == args[0]):
            params, args = (params[1:len(params)], args[1:len(args)])
            continue
        else:
            params, args, targets, vals = (params[1:len(params)], args[1:len(args)], (targets + cdy_rt.table_defs.to_list(params[0])), (vals + cdy_rt.table_defs.to_list(args[0])))
            continue

def stmts_have_closure(stmts: tuple[Stmt, ...]) -> bool:
    while True:
        if (len(stmts) == 0):
            return False
        elif stmt_has_closure(stmts[0]):
            return True
        else:
            stmts = stmts[1:len(stmts)]
            continue

def stmt_has_closure(s: Stmt) -> bool:
    _cdy_t55: object = s
    if isinstance(_cdy_t55, SLocalFunc):
        return True
    elif isinstance(_cdy_t55, SAssign):
        target = _cdy_t55.target
        val = _cdy_t55.val
        return (has_lambda(target) or has_lambda(val))
    elif isinstance(_cdy_t55, SDefAssign):
        _cdy_val_1024 = _cdy_t55.val
        return has_lambda(_cdy_val_1024)
    elif isinstance(_cdy_t55, SExpr):
        e = _cdy_t55.expr
        return has_lambda(e)
    elif isinstance(_cdy_t55, SReturn):
        _cdy_val_1026 = _cdy_t55.val
        return has_lambda(_cdy_val_1026)
    elif isinstance(_cdy_t55, SIf):
        test = _cdy_t55.test
        then = _cdy_t55.then
        other = _cdy_t55.other
        return (has_lambda(test) or stmts_have_closure(then) or stmts_have_closure(other))
    elif isinstance(_cdy_t55, SMatch):
        subject = _cdy_t55.subject
        cases = _cdy_t55.cases
        default = _cdy_t55.default
        return (has_lambda(subject) or cases_have_closure(cases) or lists_have_closure(default))
    elif isinstance(_cdy_t55, SLoop):
        body = _cdy_t55.body
        return stmts_have_closure(body)
    elif isinstance(_cdy_t55, SRebind):
        vals = _cdy_t55.vals
        return any_lambda(vals)
    else:
        return False

def cases_have_closure(cases: tuple[Case, ...]) -> bool:
    while True:
        if (len(cases) == 0):
            return False
        elif stmts_have_closure(cases[0].body):
            return True
        else:
            cases = cases[1:len(cases)]
            continue

def lists_have_closure(lists: tuple[tuple[Stmt, ...], ...]) -> bool:
    while True:
        if (len(lists) == 0):
            return False
        elif stmts_have_closure(lists[0]):
            return True
        else:
            lists = lists[1:len(lists)]
            continue

def any_lambda(exprs: tuple[Expr, ...]) -> bool:
    while True:
        if (len(exprs) == 0):
            return False
        elif has_lambda(exprs[0]):
            return True
        else:
            exprs = exprs[1:len(exprs)]
            continue

def has_lambda(e: Expr) -> bool:
    while True:
        _cdy_t56: object = e
        if isinstance(_cdy_t56, Lambda):
            return True
        elif isinstance(_cdy_t56, Call):
            callee = _cdy_t56.callee
            args = _cdy_t56.args
            return (has_lambda(callee) or any_lambda(args))
        elif isinstance(_cdy_t56, If):
            test = _cdy_t56.test
            then = _cdy_t56.then
            other = _cdy_t56.other
            return (has_lambda(test) or has_lambda(then) or has_lambda(other))
        elif isinstance(_cdy_t56, Do):
            body = _cdy_t56.body
            return any_lambda(body)
        elif isinstance(_cdy_t56, Tuple):
            items = _cdy_t56.items
            return any_lambda(items)
        elif isinstance(_cdy_t56, Fmt):
            parts = _cdy_t56.parts
            return any_lambda(holes(parts, ()))
        elif isinstance(_cdy_t56, Field):
            obj = _cdy_t56.obj
            e = obj
            continue
        elif isinstance(_cdy_t56, Assoc):
            _cdy_obj_1048 = _cdy_t56.obj
            fields = _cdy_t56.fields
            return (has_lambda(_cdy_obj_1048) or any_lambda(field_vals(fields, ())))
        elif isinstance(_cdy_t56, MatchE):
            subject = _cdy_t56.subject
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
    _cdy_t57: object = top
    if isinstance(_cdy_t57, TDeftSum):
        name = _cdy_t57.name
        variants = _cdy_t57.variants
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
    _cdy_t58: object = top
    if isinstance(_cdy_t58, TDeft):
        name = _cdy_t58.name
        return name
    elif isinstance(_cdy_t58, TDef):
        _cdy_name_1073 = _cdy_t58.name
        return _cdy_name_1073
    elif isinstance(_cdy_t58, TDefn):
        _cdy_name_1074 = _cdy_t58.name
        return _cdy_name_1074
    else:
        return ''

def generic_variants(tops: tuple[Top, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _cdy_t61 = tops[1:len(tops)]
            _cdy_t60: object = tops[0]
            if isinstance(_cdy_t60, TDeftSum):
                tvars = _cdy_t60.tvars
                variants = _cdy_t60.variants
                _cdy_t59 = (acc if (len(tvars) == 0) else mark_all(variant_list_names(variants, ()), acc))
            else:
                _cdy_t59 = acc
            tops, acc = (_cdy_t61, _cdy_t59)
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
            _cdy_t65 = locs[1:len(locs)]
            _cdy_t63: object = locs[0]
            if isinstance(_cdy_t63, Local):
                name = _cdy_t63.name
                id_ = _cdy_t63.id_
                if cdy_rt.table_defs.map_has(env.locals_, id_):
                    _cdy_t64 = env
                else:
                    base = cdy_rt.table_defs.py_mangle(name)
                    py = (('_cdy_' + str(base) + '_' + str(id_)) if cdy_rt.table_defs.map_has(env.taken, base) else base)
                    _cdy_t64 = env._replace(locals_=cdy_rt.table_defs.map_set(env.locals_, id_, py), taken=cdy_rt.table_defs.map_set(env.taken, py, True))
                _cdy_t62 = _cdy_t64
            else:
                _cdy_t62 = env
            locs, env = (_cdy_t65, _cdy_t62)
            continue

def bound_locals(stmts: tuple[Stmt, ...], acc: tuple[Expr, ...]) -> tuple[Expr, ...]:
    while True:
        if (len(stmts) == 0):
            return acc
        else:
            _cdy_t70 = stmts[1:len(stmts)]
            _cdy_t67: object = stmts[0]
            if isinstance(_cdy_t67, SAssign):
                target = _cdy_t67.target
                _cdy_t69: object = target
                if isinstance(_cdy_t69, Local):
                    _cdy_t68 = (acc + cdy_rt.table_defs.to_list(target))
                else:
                    _cdy_t68 = acc
                _cdy_t66 = _cdy_t68
            elif isinstance(_cdy_t67, SIf):
                then = _cdy_t67.then
                other = _cdy_t67.other
                _cdy_t66 = bound_locals(other, bound_locals(then, acc))
            elif isinstance(_cdy_t67, SMatch):
                cases = _cdy_t67.cases
                default = _cdy_t67.default
                _cdy_t66 = bound_in_cases(cases, bound_in_lists(default, acc))
            elif isinstance(_cdy_t67, SLoop):
                body = _cdy_t67.body
                _cdy_t66 = bound_locals(body, acc)
            else:
                _cdy_t66 = acc
            stmts, acc = (_cdy_t70, _cdy_t66)
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
    _cdy_t71: object = e
    if isinstance(_cdy_t71, Lit):
        form = _cdy_t71.form
        return emit_lit(form)
    elif isinstance(_cdy_t71, Local):
        name = _cdy_t71.name
        id_ = _cdy_t71.id_
        return local_py(name, id_, env)
    elif isinstance(_cdy_t71, Global):
        _cdy_name_1113 = _cdy_t71.name
        return cdy_rt.table_defs.map_get(env.globals_, _cdy_name_1113)
    elif isinstance(_cdy_t71, Prim):
        _cdy_name_1114 = _cdy_t71.name
        return emit_prim(_cdy_name_1114, env)
    elif isinstance(_cdy_t71, Call):
        callee = _cdy_t71.callee
        args = _cdy_t71.args
        return emit_call(callee, args, env)
    elif isinstance(_cdy_t71, If):
        test = _cdy_t71.test
        then = _cdy_t71.then
        other = _cdy_t71.other
        return ('(' + str(emit_expr(then, env)) + ' if ' + str(emit_expr(test, env)) + ' else ' + str(emit_expr(other, env)) + ')')
    elif isinstance(_cdy_t71, Do):
        return cdy_rt.table_defs.fail('emit: a do inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t71, MatchE):
        return cdy_rt.table_defs.fail('emit: a match inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t71, Lambda):
        params = _cdy_t71.params
        body = _cdy_t71.body
        inner = bind_locals(params, env)
        return ('(lambda ' + str(comma_join(emit_exprs(params, inner, ()))) + ': ' + str(emit_expr(body, inner)) + ')')
    elif isinstance(_cdy_t71, Tuple):
        items = _cdy_t71.items
        strs = emit_exprs(items, env, ())
        if (len(strs) == 1):
            return ('(' + str(strs[0]) + ',)')
        else:
            return ('(' + str(comma_join(strs)) + ')')
    elif isinstance(_cdy_t71, Fmt):
        parts = _cdy_t71.parts
        return emit_format(parts, env)
    elif isinstance(_cdy_t71, Field):
        obj = _cdy_t71.obj
        field = _cdy_t71.field
        return (str(emit_expr(obj, env)) + '.' + str(cdy_rt.table_defs.py_mangle(field)))
    elif isinstance(_cdy_t71, Assoc):
        _cdy_obj_1128 = _cdy_t71.obj
        fields = _cdy_t71.fields
        return (str(emit_expr(_cdy_obj_1128, env)) + '._replace(' + str(comma_join(emit_fields(fields, env, ()))) + ')')
    else:
        assert isinstance(_cdy_t71, Temp)
        _cdy_id__1130 = _cdy_t71.id_
        return ('_cdy_t' + str(_cdy_id__1130))

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
            _cdy_t74 = parts[1:len(parts)]
            _cdy_t73: object = parts[0]
            if isinstance(_cdy_t73, FText):
                text = _cdy_t73.text
                _cdy_t72 = cdy_rt.table_defs.py_repr(text)
            else:
                assert isinstance(_cdy_t73, FHole)
                e = _cdy_t73.expr
                _cdy_t72 = ('str(' + str(emit_expr(e, env)) + ')')
            parts, acc = (_cdy_t74, (acc + cdy_rt.table_defs.to_list(_cdy_t72)))
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
    _cdy_t75: object = form
    if isinstance(_cdy_t75, Txt):
        v = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(v)
    elif isinstance(_cdy_t75, CharLit):
        _cdy_v_1149 = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(_cdy_v_1149)
    elif isinstance(_cdy_t75, IntLit):
        _cdy_v_1150 = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(_cdy_v_1150)
    elif isinstance(_cdy_t75, LongLit):
        _cdy_v_1151 = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(_cdy_v_1151)
    elif isinstance(_cdy_t75, ByteLit):
        _cdy_v_1152 = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(_cdy_v_1152)
    elif isinstance(_cdy_t75, FloatLit):
        _cdy_v_1153 = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(_cdy_v_1153)
    elif isinstance(_cdy_t75, DoubleLit):
        _cdy_v_1154 = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(_cdy_v_1154)
    elif isinstance(_cdy_t75, BoolLit):
        _cdy_v_1155 = _cdy_t75.val
        return cdy_rt.table_defs.py_repr(_cdy_v_1155)
    else:
        return cdy_rt.table_defs.fail('emit: not a literal')

def emit_prim(name: str, env: Env) -> str:
    if cdy_rt.table_defs.in_(cdy_rt.table.get_kind(env.table, name), ('call', 'value', 'index', 'slice')):
        return cdy_rt.table.get_py(env.table, name)
    else:
        return cdy_rt.table_defs.fail(('the operator ' + str(name) + " can't be used as a value yet; wrap it in a fn"))

def emit_call(callee: Expr, args: tuple[Expr, ...], env: Env) -> str:
    strs = emit_exprs(args, env, ())
    _cdy_t76: object = callee
    if isinstance(_cdy_t76, Prim):
        name = _cdy_t76.name
        return emit_prim_call(name, strs, env)
    else:
        return (str(emit_expr(callee, env)) + '(' + str(comma_join(strs)) + ')')

def emit_prim_call(name: str, strs: tuple[str, ...], env: Env) -> str:
    kind = cdy_rt.table.get_kind(env.table, name)
    py = cdy_rt.table.get_py(env.table, name)
    op = (' ' + py + ' ')
    if cdy_rt.table_defs.in_(kind, ('binop', 'compare', 'boolop')):
        return ('(' + str(cdy_rt.table_defs.join(strs, op)) + ')')
    elif (kind == 'unary'):
        return ('(' + str(py) + ' ' + str(strs[0]) + ')')
    elif (kind == 'index'):
        return (str(strs[0]) + '[' + str(strs[1]) + ']')
    elif (kind == 'slice'):
        return (str(strs[0]) + '[' + str(strs[1]) + ':' + str(strs[2]) + ']')
    else:
        return (str(py) + '(' + str(comma_join(strs)) + ')')

def emit_type(t: CType, env: Env) -> str:
    _cdy_t77: object = t
    if isinstance(_cdy_t77, TVar):
        name = _cdy_t77.name
        return cdy_rt.table_defs.py_mangle(name)
    elif isinstance(_cdy_t77, TFn):
        params = _cdy_t77.params
        ret = _cdy_t77.ret
        return ('_cdy_Callable[[' + str(comma_join(emit_types(params, env, ()))) + '], ' + str(emit_type(ret, env)) + ']')
    else:
        assert isinstance(_cdy_t77, TCon)
        _cdy_name_1174 = _cdy_t77.name
        args = _cdy_t77.args
        return emit_tcon(_cdy_name_1174, emit_types(args, env, ()))

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
    elif cdy_rt.table_defs.in_(name, ('Float', 'Double')):
        return 'float'
    elif (name == 'Bool'):
        return 'bool'
    elif cdy_rt.table_defs.in_(name, ('Char', 'String')):
        return 'str'
    elif (name == 'Unit'):
        return 'None'
    elif (name == 'Any'):
        return '_cdy_Any'
    elif (name == 'Maybe'):
        return (str(args[0]) + ' | None')
    elif (name == 'List'):
        return ('tuple[' + str(args[0]) + ', ...]')
    elif (name == 'Tup'):
        return ('tuple[' + str(comma_join(args)) + ']')
    elif (name == 'Map'):
        return ('_cdy_Mapping[' + str(comma_join(args)) + ']')
    elif (len(args) == 0):
        return cdy_rt.table_defs.py_mangle(name)
    else:
        return (str(cdy_rt.table_defs.py_mangle(name)) + '[' + str(comma_join(args)) + ']')

def type_vars(types: tuple[CType, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            _cdy_t80 = types[1:len(types)]
            _cdy_t79: object = types[0]
            if isinstance(_cdy_t79, TVar):
                name = _cdy_t79.name
                _cdy_t78 = (acc if cdy_rt.table_defs.in_(name, acc) else (acc + cdy_rt.table_defs.to_list(name)))
            elif isinstance(_cdy_t79, TCon):
                args = _cdy_t79.args
                _cdy_t78 = type_vars(args, acc)
            else:
                assert isinstance(_cdy_t79, TFn)
                params = _cdy_t79.params
                ret = _cdy_t79.ret
                _cdy_t78 = type_vars((params + cdy_rt.table_defs.to_list(ret)), acc)
            types, acc = (_cdy_t80, _cdy_t78)
            continue

def emit_stmt(s: Stmt, level: int, env: Env) -> str:
    _cdy_t81: object = s
    if isinstance(_cdy_t81, SRecord):
        name = _cdy_t81.name
        tvars = _cdy_t81.tvars
        fields = _cdy_t81.fields
        return ('\n' + line(level, ('class ' + str(cdy_rt.table_defs.map_get(env.globals_, name)) + str(type_params(tvars)) + '(_cdy_NamedTuple):')) + emit_record_fields(fields, (level + 1), env, ''))
    elif isinstance(_cdy_t81, SSum):
        _cdy_name_1193 = _cdy_t81.name
        _cdy_tvars_1194 = _cdy_t81.tvars
        variants = _cdy_t81.variants
        return (emit_variants(variants, _cdy_tvars_1194, level, env, '') + line(level, ('type ' + str(cdy_rt.table_defs.map_get(env.globals_, _cdy_name_1193)) + str(type_params(_cdy_tvars_1194)) + ' = ' + str(cdy_rt.table_defs.join(variant_refs(variants, _cdy_tvars_1194, env, ()), ' | ')))))
    elif isinstance(_cdy_t81, SMatch):
        temp = _cdy_t81.temp
        subject = _cdy_t81.subject
        cases = _cdy_t81.cases
        default = _cdy_t81.default
        t = emit_expr(temp, env)
        val = emit_expr(subject, env)
        generic = cdy_rt.table_defs.map_has(env.generic, cases[0].variant)
        return (line(level, ((str(t) + ' = ' + str(val)) if generic else (str(t) + ': object = ' + str(val)))) + emit_match(t, cases, default, ((not generic) and (len(default) == 0)), 'if', level, env))
    elif isinstance(_cdy_t81, SLoop):
        body = _cdy_t81.body
        return (line(level, 'while True:') + emit_block(body, (level + 1), env))
    elif isinstance(_cdy_t81, SRebind):
        targets = _cdy_t81.targets
        vals = _cdy_t81.vals
        return line(level, ((str(emit_expr(targets[0], env)) + ' = ' + str(emit_expr(vals[0], env))) if (len(targets) == 1) else (str(comma_join(emit_exprs(targets, env, ()))) + ' = (' + str(comma_join(emit_exprs(vals, env, ()))) + ')')))
    elif isinstance(_cdy_t81, SContinue):
        return line(level, 'continue')
    elif isinstance(_cdy_t81, SAssign):
        target = _cdy_t81.target
        _cdy_val_1207 = _cdy_t81.val
        return line(level, (str(emit_expr(target, env)) + ' = ' + str(emit_expr(_cdy_val_1207, env))))
    elif isinstance(_cdy_t81, SDefAssign):
        _cdy_name_1208 = _cdy_t81.name
        _cdy_val_1209 = _cdy_t81.val
        _cdy_t_1210 = _cdy_t81.t
        return line(level, (str(cdy_rt.table_defs.map_get(env.globals_, _cdy_name_1208)) + ': ' + str(emit_type(_cdy_t_1210, env)) + ' = ' + str(emit_expr(_cdy_val_1209, env))))
    elif isinstance(_cdy_t81, SExpr):
        e = _cdy_t81.expr
        return line(level, emit_expr(e, env))
    elif isinstance(_cdy_t81, SReturn):
        _cdy_e_1212 = _cdy_t81.val
        return line(level, ('return ' + str(emit_expr(_cdy_e_1212, env))))
    elif isinstance(_cdy_t81, SIf):
        test = _cdy_t81.test
        then = _cdy_t81.then
        other = _cdy_t81.other
        return emit_if('if', test, then, other, level, env)
    elif isinstance(_cdy_t81, SFunc):
        _cdy_name_1216 = _cdy_t81.name
        params = _cdy_t81.params
        _cdy_body_1218 = _cdy_t81.body
        _cdy_t_1219 = _cdy_t81.t
        return emit_func(_cdy_name_1216, params, _cdy_body_1218, _cdy_t_1219, level, env)
    else:
        assert isinstance(_cdy_t81, SLocalFunc)
        _cdy_target_1220 = _cdy_t81.target
        _cdy_params_1221 = _cdy_t81.params
        _cdy_body_1222 = _cdy_t81.body
        inner = bind_locals((_cdy_params_1221 + bound_locals(_cdy_body_1222, ())), env)
        args = comma_join(emit_any_params(_cdy_params_1221, inner, ()))
        return (line(level, ('def ' + str(emit_expr(_cdy_target_1220, env)) + '(' + str(args) + ') -> _cdy_Any:')) + emit_block(_cdy_body_1222, (level + 1), inner))

def emit_if(keyword: str, test: Expr, then: tuple[Stmt, ...], other: tuple[Stmt, ...], level: int, env: Env) -> str:
    _cdy_t85 = line(level, (str(keyword) + ' ' + str(emit_expr(test, env)) + ':'))
    _cdy_t86 = emit_block(then, (level + 1), env)
    if (len(other) == 0):
        _cdy_t84 = ''
    elif (len(other) == 1):
        _cdy_t83: object = other[0]
        if isinstance(_cdy_t83, SIf):
            test2 = _cdy_t83.test
            then2 = _cdy_t83.then
            other2 = _cdy_t83.other
            _cdy_t82 = emit_if('elif', test2, then2, other2, level, env)
        else:
            _cdy_t82 = (line(level, 'else:') + emit_block(other, (level + 1), env))
        _cdy_t84 = _cdy_t82
    else:
        _cdy_t84 = (line(level, 'else:') + emit_block(other, (level + 1), env))
    return (_cdy_t85 + _cdy_t86 + _cdy_t84)

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
    elif (assert_last and (len(cases) == 1)):
        c = cases[0]
        inner = (level if (keyword == 'if') else (level + 1))
        return (('' if (keyword == 'if') else line(level, 'else:')) + line(inner, ('assert isinstance(' + str(subj) + ', ' + str(cdy_rt.table_defs.map_get(env.globals_, c.variant)) + ')')) + emit_binds(c.binds, subj, inner, env, '') + emit_stmts(c.body, inner, env, ''))
    else:
        _cdy_c_1280 = cases[0]
        test = (str(keyword) + ' isinstance(' + str(subj) + ', ' + str(cdy_rt.table_defs.map_get(env.globals_, _cdy_c_1280.variant)) + '):')
        binds = emit_binds(_cdy_c_1280.binds, subj, (level + 1), env, '')
        body = ((line((level + 1), 'pass') if (binds == '') else '') if (len(_cdy_c_1280.body) == 0) else emit_stmts(_cdy_c_1280.body, (level + 1), env, ''))
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
    _cdy_t87: object = t
    if isinstance(_cdy_t87, TFn):
        types = _cdy_t87.params
        ret = _cdy_t87.ret
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
    _tup = expand_program(forms, compile_macros)
    program = _tup[0]
    macros = _tup[1]
    return translate_expanded(program, (lambda text: expand_all(parse(text), macros, ())), macros, False)

def compile_macros(forms: tuple[Form, ...]) -> str:
    return translate_expanded(forms, read_forms, {}, True)

def translate_expanded(forms: tuple[Form, ...], parse: _cdy_Callable[[str], tuple[Form, ...]], macros: _cdy_Mapping[str, Macro], quoting: bool) -> str:
    tops = analyse_program(forms, cdy_rt.table.INITIAL_TABLE, parse, macros, quoting)
    stmts = lower_program(tops, 0, ())
    globals_ = global_names(tops, Env({}, {}, {}, generic_variants(tops, {}), cdy_rt.table.INITIAL_TABLE))
    env = bind_locals(bound_locals(stmts, ()), globals_)
    return (HEADER + emit_imports(cdy_rt.table.IMPORTS, '') + '\n' + emit_stmts(stmts, 0, env, '') + (emit_main(env) if has_main(tops) else ''))

def translate_text(text: str) -> str:
    return translate(include_imports(read_source('', text), '.'), read_forms)

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
