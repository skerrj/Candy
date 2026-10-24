from __future__ import annotations

from collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping
from typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple
import math
import re
import cdy_rt.spelling
import cdy_rt.primitives


def prelude__rest[a](xs: tuple[a, ...]) -> tuple[a, ...]:
    return xs[1:len(xs)]

def prelude__map_update[k, v](m: _cdy_Mapping[k, v], key: k, f: _cdy_Callable[[v], v]) -> _cdy_Mapping[k, v]:
    return cdy_rt.primitives.map_set(m, key, f(cdy_rt.primitives.map_get(m, key)))

class form__Pos(_cdy_NamedTuple):
    file: str
    line: int
    col: int
form__NOWHERE: form__Pos = form__Pos('', 0, 0)

class form__Sym(_cdy_NamedTuple):
    name: str
    pos: form__Pos

class form__Lst(_cdy_NamedTuple):
    items: tuple[form__Form, ...]
    pos: form__Pos

class form__Txt(_cdy_NamedTuple):
    val: str

class form__IntLit(_cdy_NamedTuple):
    val: int

class form__LongLit(_cdy_NamedTuple):
    val: int

class form__ByteLit(_cdy_NamedTuple):
    val: int

class form__FloatLit(_cdy_NamedTuple):
    val: float

class form__DoubleLit(_cdy_NamedTuple):
    val: float

class form__CharLit(_cdy_NamedTuple):
    val: str

class form__BoolLit(_cdy_NamedTuple):
    val: bool
type form__Form = form__Sym | form__Lst | form__Txt | form__IntLit | form__LongLit | form__ByteLit | form__FloatLit | form__DoubleLit | form__CharLit | form__BoolLit

def form__sym_name(form: form__Form) -> str:
    _cdy_t0: object = form
    if isinstance(_cdy_t0, form__Sym):
        name = _cdy_t0.name
        return name
    else:
        return ''

def form__list_items(form: form__Form) -> tuple[form__Form, ...]:
    _cdy_t1: object = form
    if isinstance(_cdy_t1, form__Lst):
        items = _cdy_t1.items
        return items
    else:
        return ()

def form__rest_of(forms: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    return forms[1:len(forms)]

def form__form_pos(form: form__Form) -> form__Pos:
    _cdy_t2: object = form
    if isinstance(_cdy_t2, form__Sym):
        pos = _cdy_t2.pos
        return pos
    elif isinstance(_cdy_t2, form__Lst):
        _cdy_pos_7 = _cdy_t2.pos
        return _cdy_pos_7
    else:
        return form__NOWHERE

def form__pos_text(pos: form__Pos) -> str:
    line = pos.line
    col = pos.col
    file = pos.file
    if (line == 0):
        return ''
    elif (file == ''):
        return ('line ' + str(line) + ', column ' + str(col) + ': ')
    else:
        return (str(file) + ':' + str(line) + ':' + str(col) + ': ')

def form__gensym(prefix: str) -> form__Form:
    return form__Sym(cdy_rt.primitives.fresh_name(prefix), form__NOWHERE)

class form__Macro(_cdy_NamedTuple):
    name: str
    arity: int
    run: _cdy_Any
    pos: form__Pos

def read__read_forms(text: str) -> tuple[form__Form, ...]:
    return read__read_all(read__Source('', ()), text, read__skip(text, 0), ())

def read__read_source(file: str, text: str) -> tuple[form__Form, ...]:
    return read__read_all(read__Source(file, read__line_starts(text, 0, cdy_rt.primitives.to_list(0))), text, read__skip(text, 0), ())

class read__Source(_cdy_NamedTuple):
    file: str
    starts: tuple[int, ...]

def read__line_starts(text: str, pos: int, acc: tuple[int, ...]) -> tuple[int, ...]:
    while True:
        if (pos >= len(text)):
            return acc
        elif (text[pos] == '\n'):
            pos, acc = ((pos + 1), (acc + cdy_rt.primitives.to_list((pos + 1))))
            continue
        else:
            pos = (pos + 1)
            continue

def read__pos_at(src: read__Source, pos: int) -> form__Pos:
    starts = src.starts
    if (len(starts) == 0):
        return form__NOWHERE
    else:
        i = read__line_of(starts, pos, 0, len(starts))
        return form__Pos(src.file, (i + 1), ((pos - starts[i]) + 1))

def read__line_of(starts: tuple[int, ...], pos: int, lo: int, hi: int) -> int:
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

def read__read_all(src: read__Source, text: str, pos: int, acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (pos >= len(text)):
            return acc
        else:
            _tup = read__read_form(src, text, pos)
            form = _tup[0]
            next_ = _tup[1]
            pos, acc = (read__skip(text, next_), (acc + cdy_rt.primitives.to_list(form)))
            continue

def read__skip(text: str, pos: int) -> int:
    while True:
        if (pos >= len(text)):
            return pos
        elif cdy_rt.primitives.isspace_at(text, pos):
            pos = (pos + 1)
            continue
        elif (text[pos] == ';'):
            pos = read__line_end(text, pos)
            continue
        else:
            return pos

def read__line_end(text: str, pos: int) -> int:
    while True:
        if ((pos >= len(text)) or (text[pos] == '\n')):
            return pos
        else:
            pos = (pos + 1)
            continue

def read__ends_at(text: str, pos: int) -> bool:
    return ((pos >= len(text)) or cdy_rt.primitives.isspace_at(text, pos) or cdy_rt.primitives.in_(text[pos], '();'))

def read__word_end(text: str, pos: int) -> int:
    while True:
        if read__ends_at(text, pos):
            return pos
        else:
            pos = (pos + 1)
            continue

def read__read_form(src: read__Source, text: str, pos: int) -> tuple[form__Form, int]:
    ch = text[pos]
    if (ch == '('):
        return read__read_list(src, text, read__skip(text, (pos + 1)), (), pos)
    elif (ch == ')'):
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, 'unexpected )'))
    elif (ch == '"'):
        return read__read_str(src, text, (pos + 1), '', pos)
    elif (ch == '\\'):
        return read__read_char(src, text, pos)
    else:
        return read__read_atom(src, text, pos, read__word_end(text, pos))

def read__read_list(src: read__Source, text: str, pos: int, acc: tuple[form__Form, ...], start: int) -> tuple[form__Form, int]:
    while True:
        if (pos >= len(text)):
            return cdy_rt.primitives.fail(read__parse_error(src, text, start, '( is never closed'))
        elif (text[pos] == ')'):
            return (form__Lst(acc, read__pos_at(src, start)), (pos + 1))
        else:
            _tup = read__read_form(src, text, pos)
            form = _tup[0]
            next_ = _tup[1]
            pos, acc = (read__skip(text, next_), (acc + cdy_rt.primitives.to_list(form)))
            continue

def read__read_char(src: read__Source, text: str, pos: int) -> tuple[form__Form, int]:
    if (((pos + 1) < len(text)) and (not cdy_rt.primitives.isspace_at(text, (pos + 1))) and read__ends_at(text, (pos + 2))):
        return (form__CharLit(text[(pos + 1)]), (pos + 2))
    else:
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, 'a char is \\ and one character, then a delimiter'))

def read__read_atom(src: read__Source, text: str, pos: int, end: int) -> tuple[form__Form, int]:
    word = text[pos:end]
    kind = read__number_kind(word)
    if (kind != ''):
        return (read__number_form(word, kind), end)
    elif (word == 'true'):
        return (form__BoolLit(True), end)
    elif (word == 'false'):
        return (form__BoolLit(False), end)
    elif read__symbol_start(text[pos]):
        stop = read__symbol_end(text, (pos + 1))
        name = text[pos:stop]
        if cdy_rt.primitives.in_('__', name):
            return cdy_rt.primitives.fail(read__parse_error(src, text, pos, "a name can't contain __ (only gensym makes such names)"))
        else:
            return (form__Sym(name, read__pos_at(src, pos)), stop)
    else:
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, ('unexpected ' + str(text[pos]))))

def read__symbol_start(ch: str) -> bool:
    return (not (cdy_rt.primitives.in_(ch, '\'#"\\') or cdy_rt.primitives.is_decimal(ch)))

def read__symbol_end(text: str, pos: int) -> int:
    while True:
        if ((pos >= len(text)) or cdy_rt.primitives.isspace_at(text, pos) or cdy_rt.primitives.in_(text[pos], '()\'";\\')):
            return pos
        else:
            pos = (pos + 1)
            continue

def read__digits_end(word: str, pos: int) -> int:
    while True:
        if ((pos < len(word)) and cdy_rt.primitives.is_decimal(word[pos])):
            pos = (pos + 1)
            continue
        else:
            return pos

def read__number_kind(word: str) -> str:
    start = (1 if (word[0] == '-') else 0)
    i = read__digits_end(word, start)
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
        j = read__digits_end(word, (i + 1))
        tail = word[j:len(word)]
        if (j == (i + 1)):
            return ''
        elif (tail == ''):
            return 'double'
        elif (tail == 'f'):
            return 'float'
        else:
            return ''
    else:
        return ''

def read__number_form(word: str, kind: str) -> form__Form:
    body = word[0:(len(word) - 1)]
    if (kind == 'int'):
        return form__IntLit(cdy_rt.primitives.to_int(word))
    elif (kind == 'long'):
        return form__LongLit(cdy_rt.primitives.to_int(body))
    elif (kind == 'byte'):
        return form__ByteLit(cdy_rt.primitives.to_int(body))
    elif (kind == 'double'):
        return form__DoubleLit(cdy_rt.primitives.to_float(word))
    else:
        return form__FloatLit(cdy_rt.primitives.to_float(body))

def read__read_str(src: read__Source, text: str, pos: int, acc: str, start: int) -> tuple[form__Form, int]:
    while True:
        if (pos >= len(text)):
            return cdy_rt.primitives.fail(read__parse_error(src, text, start, 'string is never closed'))
        elif (text[pos] == '"'):
            return (form__Txt(acc), (pos + 1))
        elif (text[pos] == '\\'):
            _tup = read__escape(src, text, pos)
            ch = _tup[0]
            next_ = _tup[1]
            pos, acc = (next_, (acc + ch))
            continue
        else:
            pos, acc = ((pos + 1), (acc + text[pos]))
            continue

def read__escape(src: read__Source, text: str, pos: int) -> tuple[str, int]:
    c = (text[(pos + 1)] if ((pos + 1) < len(text)) else '')
    if cdy_rt.primitives.in_(c, ('\\', '/', '"')):
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
    elif ((c == 'u') and ((pos + 6) <= len(text)) and read__all_hex(text, (pos + 2), (pos + 6))):
        return (cdy_rt.primitives.hex_char(text[(pos + 2):(pos + 6)]), (pos + 6))
    else:
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, 'bad escape sequence'))

def read__all_hex(text: str, pos: int, end: int) -> bool:
    while True:
        if (pos >= end):
            return True
        elif cdy_rt.primitives.in_(text[pos], '0123456789abcdefABCDEF'):
            pos = (pos + 1)
            continue
        else:
            return False

def read__parse_error(src: read__Source, text: str, pos: int, msg: str) -> str:
    _tup = read__row_col(text, 0, pos, 1, 1)
    row = _tup[0]
    col = _tup[1]
    return (str(form__pos_text(form__Pos(src.file, row, col))) + 'parse error: ' + str(msg))

def read__row_col(text: str, i: int, pos: int, row: int, col: int) -> tuple[int, int]:
    while True:
        if (i >= pos):
            return (row, col)
        elif (text[i] == '\n'):
            i, row, col = ((i + 1), (row + 1), 1)
            continue
        else:
            i, col = ((i + 1), (col + 1))
            continue

class include__Module(_cdy_NamedTuple):
    path: str
    key: str
    stem: str
    forms: tuple[form__Form, ...]
    imports: tuple[include__Imp, ...]

class include__Imp(_cdy_NamedTuple):
    key: str
    pos: form__Pos

class include__Mods(_cdy_NamedTuple):
    done: tuple[include__Module, ...]
    seen: _cdy_Mapping[str, bool]

def include__read_modules(path: str) -> tuple[include__Module, ...]:
    return include__checked_stems(include__add_module(path, cdy_rt.primitives.path_resolve(path), read__read_source(path, cdy_rt.primitives.slurp(path)), cdy_rt.primitives.path_dir(path), (), include__Mods((), {})))

def include__text_modules(text: str) -> tuple[include__Module, ...]:
    return include__checked_stems(include__add_module('', '', read__read_source('', text), '.', (), include__Mods((), {})))

def include__add_module(path: str, key: str, forms: tuple[form__Form, ...], dir_: str, stack: tuple[str, ...], acc: include__Mods) -> include__Mods:
    imports = (include__prelude_module(key) + include__module_imports(forms, dir_, ()))
    inner = include__load_imports(imports, (stack + cdy_rt.primitives.to_list(key)), acc._replace(seen=cdy_rt.primitives.map_set(acc.seen, key, True)))
    return inner._replace(done=(inner.done + cdy_rt.primitives.to_list(include__Module(path, key, cdy_rt.primitives.path_stem(path), include__other_forms(forms, dir_, ()), include__imp_list(imports, ())))))

def include__prelude_module(key: str) -> tuple[tuple[str, include__Imp], ...]:
    path = include__library_path('prelude.cdy')
    prelude = cdy_rt.primitives.path_resolve(path)
    if (prelude == key):
        return ()
    else:
        return cdy_rt.primitives.to_list((path, include__Imp(prelude, form__NOWHERE)))

def include__library_path(name: str) -> str:
    dir_ = cdy_rt.primitives.module_dir(form__sym_name)
    path = cdy_rt.primitives.path_join(dir_, name)
    if cdy_rt.primitives.file_exists(path):
        return path
    else:
        return cdy_rt.primitives.fail(('the translator needs ' + str(name) + ' next to it, in ' + str(dir_)))

def include__module_imports(forms: tuple[form__Form, ...], dir_: str, acc: tuple[tuple[str, include__Imp], ...]) -> tuple[tuple[str, include__Imp], ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            name = include__import_name(form)
            _cdy_t4 = prelude__rest(forms)
            if (name == ''):
                _cdy_t3 = acc
            else:
                path = include__import_path('import', dir_, name, form__form_pos(form))
                _cdy_t3 = (acc + cdy_rt.primitives.to_list((path, include__Imp(cdy_rt.primitives.path_resolve(path), form__form_pos(form)))))
            forms, acc = (_cdy_t4, _cdy_t3)
            continue

def include__imp_list(imports: tuple[tuple[str, include__Imp], ...], acc: tuple[include__Imp, ...]) -> tuple[include__Imp, ...]:
    while True:
        if (len(imports) == 0):
            return acc
        else:
            imports, acc = (prelude__rest(imports), (acc + cdy_rt.primitives.to_list(imports[0][1])))
            continue

def include__load_imports(imports: tuple[tuple[str, include__Imp], ...], stack: tuple[str, ...], acc: include__Mods) -> include__Mods:
    while True:
        if (len(imports) == 0):
            return acc
        else:
            _tup = imports[0]
            path = _tup[0]
            imp = _tup[1]
            key = imp.key
            imports, acc = (prelude__rest(imports), (cdy_rt.primitives.fail((str(form__pos_text(imp.pos)) + 'import: cycle ' + str(include__cycle_text(stack, key)))) if cdy_rt.primitives.in_(key, stack) else (acc if cdy_rt.primitives.map_has(acc.seen, key) else include__add_module(path, key, read__read_source(path, cdy_rt.primitives.slurp(path)), cdy_rt.primitives.path_dir(path), stack, acc))))
            continue

def include__cycle_text(stack: tuple[str, ...], key: str) -> str:
    while True:
        if (stack[0] == key):
            return (cdy_rt.primitives.join(include__stems_of(stack, ()), ' -> ') + ' -> ' + cdy_rt.primitives.path_stem(key))
        else:
            stack = prelude__rest(stack)
            continue

def include__stems_of(keys: tuple[str, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(keys) == 0):
            return acc
        else:
            keys, acc = (prelude__rest(keys), (acc + cdy_rt.primitives.to_list(cdy_rt.primitives.path_stem(keys[0]))))
            continue

def include__other_forms(forms: tuple[form__Form, ...], dir_: str, acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (prelude__rest(forms), ((acc + cdy_rt.primitives.to_list(include__macro_import(forms[0], dir_))) if (include__import_name(forms[0]) == '') else acc))
            continue

def include__checked_stems(mods: include__Mods) -> tuple[include__Module, ...]:
    modules = mods.done
    checked = include__unique_stems(modules[0:(len(modules) - 1)], {})
    return modules

def include__unique_stems(modules: tuple[include__Module, ...], seen: _cdy_Mapping[str, str]) -> bool:
    while True:
        if (len(modules) == 0):
            return True
        else:
            m = modules[0]
            stem = m.stem
            if cdy_rt.primitives.map_has(seen, stem):
                return cdy_rt.primitives.fail(('import: two modules are named ' + str(stem) + ': ' + str(cdy_rt.primitives.map_get(seen, stem)) + ' and ' + str(m.path)))
            else:
                modules, seen = (prelude__rest(modules), cdy_rt.primitives.map_set(seen, stem, m.path))
                continue

class include__Incl(_cdy_NamedTuple):
    done: tuple[form__Form, ...]
    seen: _cdy_Mapping[str, bool]

def include__read_program(path: str) -> tuple[form__Form, ...]:
    return include__include_file(path, include__Incl((), {})).done

def include__include_imports(forms: tuple[form__Form, ...], dir_: str) -> tuple[form__Form, ...]:
    return include__include_forms(forms, dir_, include__Incl((), {})).done

def include__include_file(path: str, acc: include__Incl) -> include__Incl:
    key = cdy_rt.primitives.path_resolve(path)
    if cdy_rt.primitives.map_has(acc.seen, key):
        return acc
    else:
        return include__include_forms(read__read_source(path, cdy_rt.primitives.slurp(path)), cdy_rt.primitives.path_dir(path), acc._replace(seen=cdy_rt.primitives.map_set(acc.seen, key, True)))

def include__include_forms(forms: tuple[form__Form, ...], dir_: str, acc: include__Incl) -> include__Incl:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            name = include__import_name(form)
            forms, acc = (prelude__rest(forms), (acc._replace(done=(acc.done + cdy_rt.primitives.to_list(include__macro_import(form, dir_)))) if (name == '') else include__include_file(include__import_path('import', dir_, name, form__form_pos(form)), acc)))
            continue

def include__macro_import(form: form__Form, dir_: str) -> form__Form:
    items = form__list_items(form)
    pos = form__form_pos(form)
    if ((len(items) == 0) or (form__sym_name(items[0]) != 'import-macros')):
        return form
    elif ((len(items) == 2) and (form__sym_name(items[1]) != '')):
        return form__Lst((items[0], form__Txt(include__import_path('import-macros', dir_, form__sym_name(items[1]), pos))), pos)
    else:
        return cdy_rt.primitives.fail((form__pos_text(pos) + 'import-macros: expected (import-macros name)'))

def include__import_name(form: form__Form) -> str:
    items = form__list_items(form)
    if ((len(items) == 0) or (form__sym_name(items[0]) != 'import')):
        return ''
    elif ((len(items) == 2) and (form__sym_name(items[1]) != '')):
        return form__sym_name(items[1])
    else:
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'import: expected (import name)'))

def include__import_path(what: str, dir_: str, name: str, pos: form__Pos) -> str:
    path = cdy_rt.primitives.path_join(dir_, (name + '.cdy'))
    if cdy_rt.primitives.file_exists(path):
        return path
    else:
        return cdy_rt.primitives.fail((str(form__pos_text(pos)) + str(what) + ": can't find " + str(name) + '.cdy in ' + str(dir_)))

class core__TCon(_cdy_NamedTuple):
    name: str
    args: tuple[core__CType, ...]

class core__TVar(_cdy_NamedTuple):
    name: str

class core__TFn(_cdy_NamedTuple):
    params: tuple[core__CType, ...]
    ret: core__CType
type core__CType = core__TCon | core__TVar | core__TFn

class core__Lit(_cdy_NamedTuple):
    form: form__Form

class core__Local(_cdy_NamedTuple):
    name: str
    id_: int

class core__Global(_cdy_NamedTuple):
    name: str

class core__Prim(_cdy_NamedTuple):
    name: str

class core__Call(_cdy_NamedTuple):
    callee: core__Expr
    args: tuple[core__Expr, ...]

class core__If(_cdy_NamedTuple):
    test: core__Expr
    then: core__Expr
    other: core__Expr

class core__Do(_cdy_NamedTuple):
    body: tuple[core__Expr, ...]

class core__Lambda(_cdy_NamedTuple):
    params: tuple[core__Expr, ...]
    body: core__Expr

class core__Tuple(_cdy_NamedTuple):
    items: tuple[core__Expr, ...]

class core__Fmt(_cdy_NamedTuple):
    parts: tuple[core__FPart, ...]

class core__Field(_cdy_NamedTuple):
    obj: core__Expr
    field: str

class core__Assoc(_cdy_NamedTuple):
    obj: core__Expr
    fields: tuple[tuple[str, core__Expr], ...]

class core__MatchE(_cdy_NamedTuple):
    subject: core__Expr
    clauses: tuple[core__Clause, ...]
    default: tuple[core__Expr, ...]

class core__Temp(_cdy_NamedTuple):
    id_: int
type core__Expr = core__Lit | core__Local | core__Global | core__Prim | core__Call | core__If | core__Do | core__Lambda | core__Tuple | core__Fmt | core__Field | core__Assoc | core__MatchE | core__Temp

class core__Clause(_cdy_NamedTuple):
    variant: str
    binds: tuple[tuple[str, core__Expr], ...]
    body: core__Expr

class core__FText(_cdy_NamedTuple):
    text: str

class core__FHole(_cdy_NamedTuple):
    expr: core__Expr
type core__FPart = core__FText | core__FHole

class core__Variant(_cdy_NamedTuple):
    name: str
    fields: tuple[tuple[str, core__CType], ...]

class core__TDeft(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]

class core__TDeftSum(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    variants: tuple[core__Variant, ...]

class core__TDef(_cdy_NamedTuple):
    name: str
    init: core__Expr
    t: core__CType

class core__TDefn(_cdy_NamedTuple):
    name: str
    params: tuple[core__Expr, ...]
    body: core__Expr
    t: core__CType

class core__TExpr(_cdy_NamedTuple):
    expr: core__Expr
type core__Top = core__TDeft | core__TDeftSum | core__TDef | core__TDefn | core__TExpr
core__NIL: core__Expr = core__Prim('nil')

class core__Scope(_cdy_NamedTuple):
    env: _cdy_Mapping[str, core__Expr]
    top: _cdy_Mapping[str, bool]
    parse: _cdy_Callable[[str], tuple[form__Form, ...]]
    variants: _cdy_Mapping[str, core__VInfo]
    sums: _cdy_Mapping[str, tuple[str, ...]]
    here: form__Pos
    macros: _cdy_Mapping[str, form__Macro]
    quoting: bool
    names: _cdy_Mapping[str, str]
    elsewhere: _cdy_Mapping[str, str]
    builtins: _cdy_Mapping[str, core__Builtin]

def core__at_pos(scope: core__Scope, pos: form__Pos) -> core__Scope:
    if (pos.line == 0):
        return scope
    else:
        return scope._replace(here=pos)

def core__located(scope: core__Scope, msg: str) -> str:
    return (form__pos_text(scope.here) + msg)

def core__bind_local(scope: core__Scope, name: str, loc: core__Expr) -> core__Scope:
    if cdy_rt.primitives.map_has(scope.macros, name):
        return cdy_rt.primitives.fail(core__located(scope, (str(name) + " is a macro, so it can't be bound")))
    else:
        return scope._replace(env=cdy_rt.primitives.map_set(scope.env, name, loc))

class core__VInfo(_cdy_NamedTuple):
    sum_: str
    fields: tuple[str, ...]

def core__is_variant(name: str, scope: core__Scope) -> bool:
    return (cdy_rt.primitives.map_has(scope.variants, name) and (not cdy_rt.primitives.map_has(scope.env, name)))

def core__variant_fields(name: str, scope: core__Scope) -> tuple[str, ...]:
    return cdy_rt.primitives.map_get(scope.variants, name).fields

def core__analyse_expr(form: form__Form, scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _cdy_t5: object = form
    if isinstance(_cdy_t5, form__Sym):
        name = _cdy_t5.name
        pos = _cdy_t5.pos
        return (core__resolve(name, core__at_pos(scope, pos)), n)
    elif isinstance(_cdy_t5, form__Lst):
        items = _cdy_t5.items
        _cdy_pos_17 = _cdy_t5.pos
        return core__analyse_list(items, core__at_pos(scope, _cdy_pos_17), n)
    else:
        return (core__Lit(form), n)

def core__analyse_all(forms: tuple[form__Form, ...], scope: core__Scope, n: int, acc: tuple[core__Expr, ...]) -> tuple[tuple[core__Expr, ...], int]:
    while True:
        if (len(forms) == 0):
            return (acc, n)
        else:
            _tup = core__analyse_expr(forms[0], scope, n)
            e = _tup[0]
            n1 = _tup[1]
            forms, n, acc = (prelude__rest(forms), n1, (acc + cdy_rt.primitives.to_list(e)))
            continue

def core__resolve(name: str, scope: core__Scope) -> core__Expr:
    if cdy_rt.primitives.map_has(scope.env, name):
        return cdy_rt.primitives.map_get(scope.env, name)
    elif (core__is_variant(name, scope) and (len(core__variant_fields(name, scope)) == 0)):
        return core__Call(core__Global(core__global_name(name, scope.names)), ())
    elif (cdy_rt.primitives.map_has(scope.top, name) and cdy_rt.primitives.map_get(scope.top, name)):
        return core__Global(core__global_name(name, scope.names))
    elif core__is_special(name, scope.builtins):
        return cdy_rt.primitives.fail(core__located(scope, (str(name) + ' is a special form, not a value')))
    elif cdy_rt.primitives.map_has(scope.builtins, name):
        return core__Prim(name)
    elif cdy_rt.primitives.map_has(scope.elsewhere, name):
        stem = cdy_rt.primitives.map_get(scope.elsewhere, name)
        return cdy_rt.primitives.fail(core__located(scope, (str(name) + ' is not defined here; ' + str(stem) + " defines it, but this file doesn't import " + str(stem))))
    else:
        return cdy_rt.primitives.fail(core__located(scope, ('unknown name ' + str(name))))

def core__global_name(name: str, names: _cdy_Mapping[str, str]) -> str:
    if cdy_rt.primitives.map_has(names, name):
        return cdy_rt.primitives.map_get(names, name)
    else:
        return name

def core__is_special_head(name: str, scope: core__Scope) -> bool:
    return ((not cdy_rt.primitives.map_has(scope.env, name)) and core__is_special(name, scope.builtins))

def core__analyse_list(items: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(items) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'empty form (): use empty-list for an empty list'))
    else:
        head = form__sym_name(items[0])
        if core__is_special_head(head, scope):
            return core__analyse_special(head, prelude__rest(items), scope, n)
        else:
            checked = core__check_variant_call(head, (len(items) - 1), scope)
            _tup = core__analyse_expr(items[0], scope, n)
            callee = _tup[0]
            n1 = _tup[1]
            _cdy__tup_40 = core__analyse_all(prelude__rest(items), scope, n1, ())
            args = _cdy__tup_40[0]
            n2 = _cdy__tup_40[1]
            arity_ok = core__check_call(callee, len(args), scope)
            return (core__Call(callee, args), n2)

def core__check_call(callee: core__Expr, count: int, scope: core__Scope) -> bool:
    _cdy_t6: object = callee
    if isinstance(_cdy_t6, core__Prim):
        name = _cdy_t6.name
        builtin = cdy_rt.primitives.map_get(scope.builtins, name)
        _cdy_t8: object = builtin
        if isinstance(_cdy_t8, core__Op):
            unary = _cdy_t8.unary
            _cdy_t7 = (not unary)
        else:
            _cdy_t7 = False
        variadic = _cdy_t7
        _cdy_t10: object = builtin
        if isinstance(_cdy_t10, core__Op):
            _cdy_unary_51 = _cdy_t10.unary
            _cdy_t9 = (1 if _cdy_unary_51 else -1)
        elif isinstance(_cdy_t10, core__Typed):
            type_ = _cdy_t10.type_
            _cdy_t9 = core__fn_arity(type_)
        else:
            _cdy_t9 = -1
        arity = _cdy_t9
        if (variadic and (count < 2)):
            return cdy_rt.primitives.fail(core__located(scope, ('(' + str(name) + ' ...) needs at least 2 arguments, got ' + str(count))))
        elif ((arity >= 0) and (arity != count)):
            return cdy_rt.primitives.fail(core__located(scope, ('(' + str(name) + ' ...) takes ' + str(arity) + ' argument(s), got ' + str(count))))
        else:
            return True
    else:
        return True

def core__check_variant_call(name: str, count: int, scope: core__Scope) -> bool:
    if (not core__is_variant(name, scope)):
        return True
    elif (len(core__variant_fields(name, scope)) == 0):
        return cdy_rt.primitives.fail(core__located(scope, (str(name) + ' has no fields, so it is a value: write ' + str(name) + ', not (' + str(name) + ')')))
    elif (count != len(core__variant_fields(name, scope))):
        return cdy_rt.primitives.fail(core__located(scope, ('(' + str(name) + ' ...) takes ' + str(len(core__variant_fields(name, scope))) + ' field(s), got ' + str(count))))
    else:
        return True

def core__analyse_special(head: str, args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (head == 'if'):
        return core__an_if(args, scope, n)
    elif (head == 'do'):
        return core__an_do(args, scope, n)
    elif (head == 'let'):
        return core__an_let(args, scope, n)
    elif (head == 'fn'):
        return core__an_fn(args, scope, n)
    elif (head == 'tup'):
        return core__an_tup(args, scope, n)
    elif (head == 'format'):
        return core__an_format(args, scope, n)
    elif (head == 'get'):
        return core__an_get(args, scope, n)
    elif (head == 'assoc'):
        return core__an_assoc(args, scope, n)
    elif (head == 'match'):
        return core__an_match(args, scope, n)
    elif (head == 'quo'):
        return core__an_quo(args, scope, n)
    elif (head == 'quasi'):
        return core__an_quasi(args, scope, n)
    elif cdy_rt.primitives.in_(head, ('unq', 'unq-sp')):
        return cdy_rt.primitives.fail(core__located(scope, (str(head) + ': only inside quasi')))
    elif cdy_rt.primitives.in_(head, ('def', 'defn', 'deft', 'sig', 'import', 'import-macros', 'defmacro')):
        return cdy_rt.primitives.fail(core__located(scope, (str(head) + ' is only allowed at top level')))
    else:
        return cdy_rt.primitives.fail(core__located(scope, (str(head) + ' is not supported by the Candy translator yet')))

def core__an_if(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__analyse_all(args, scope, n, ())
    parts = _tup[0]
    n1 = _tup[1]
    if (len(parts) == 2):
        return (core__If(parts[0], parts[1], core__NIL), n1)
    elif (len(parts) == 3):
        return (core__If(parts[0], parts[1], parts[2]), n1)
    else:
        return cdy_rt.primitives.fail(core__located(scope, 'if: expected (if test then else?)'))

def core__is_else(form: form__Form) -> bool:
    return (form__sym_name(form) == 'else')

def core__an_do(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__analyse_all(args, scope, n, ())
    body = _tup[0]
    n1 = _tup[1]
    if (len(body) == 0):
        return (core__NIL, n1)
    elif (len(body) == 1):
        return (body[0], n1)
    else:
        return (core__Do(body), n1)

def core__an_let(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if ((len(args) != 2) or (not core__is_list_form(args[0]))):
        return cdy_rt.primitives.fail(core__located(scope, 'let: expected (let ((name init)*) body)'))
    elif (len(form__list_items(args[0])) == 0):
        return core__analyse_expr(args[1], scope, n)
    else:
        _tup = core__let_bindings(form__list_items(args[0]), scope, n, ())
        pairs = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_81 = core__analyse_expr(args[1], inner, n1)
        body = _cdy__tup_81[0]
        n2 = _cdy__tup_81[1]
        return (core__nest(pairs, body), n2)

def core__is_list_form(form: form__Form) -> bool:
    _cdy_t11: object = form
    if isinstance(_cdy_t11, form__Lst):
        return True
    else:
        return False

def core__let_bindings(bindings: tuple[form__Form, ...], scope: core__Scope, n: int, acc: tuple[tuple[core__Expr, core__Expr], ...]) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    while True:
        if (len(bindings) == 0):
            return (acc, scope, n)
        else:
            items = form__list_items(bindings[0])
            if (len(items) != 2):
                return cdy_rt.primitives.fail(core__located(scope, 'let: binding must be (name init)'))
            else:
                _tup = core__analyse_expr(items[1], scope, n)
                init = _tup[0]
                n1 = _tup[1]
                target = items[0]
                _cdy_t12: object = target
                if isinstance(_cdy_t12, form__Lst):
                    names = _cdy_t12.items
                    tmp = core__Local('_tup', n1)
                    _cdy__tup_96 = core__destructure(names, tmp, 0, scope, (n1 + 1), ())
                    more = _cdy__tup_96[0]
                    inner = _cdy__tup_96[1]
                    n2 = _cdy__tup_96[2]
                    bindings, scope, n, acc = (prelude__rest(bindings), inner, n2, (acc + cdy_rt.primitives.to_list((tmp, init)) + more))
                    continue
                else:
                    name = form__sym_name(target)
                    loc = core__Local(name, n1)
                    if ((name == '') or core__is_special(name, scope.builtins)):
                        return cdy_rt.primitives.fail(core__located(scope, 'let name must be a name, not a special form'))
                    else:
                        bindings, scope, n, acc = (prelude__rest(bindings), core__bind_local(scope, name, loc), (n1 + 1), (acc + cdy_rt.primitives.to_list((loc, init))))
                        continue

def core__destructure(names: tuple[form__Form, ...], tmp: core__Expr, i: int, scope: core__Scope, n: int, acc: tuple[tuple[core__Expr, core__Expr], ...]) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = form__sym_name(names[0])
            loc = core__Local(name, n)
            item = core__Call(core__Prim('at'), (tmp, core__Lit(form__IntLit(i))))
            if (name == ''):
                return cdy_rt.primitives.fail(core__located(scope, 'let name must be a name'))
            else:
                names, i, scope, n, acc = (prelude__rest(names), (i + 1), core__bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.primitives.to_list((loc, item))))
                continue

def core__nest(pairs: tuple[tuple[core__Expr, core__Expr], ...], body: core__Expr) -> core__Expr:
    if (len(pairs) == 0):
        return body
    else:
        _tup = pairs[0]
        loc = _tup[0]
        init = _tup[1]
        return core__Call(core__Lambda(cdy_rt.primitives.to_list(loc), core__nest(prelude__rest(pairs), body)), cdy_rt.primitives.to_list(init))

def core__an_fn(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) != 2):
        return cdy_rt.primitives.fail(core__located(scope, 'fn: expected (fn (args+) body), with exactly one body form'))
    else:
        _tup = core__bind_params(form__list_items(args[0]), scope, n, ())
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_123 = core__analyse_expr(args[1], inner, n1)
        body = _cdy__tup_123[0]
        n2 = _cdy__tup_123[1]
        if (len(params) == 0):
            return cdy_rt.primitives.fail(core__located(scope, 'fn arguments: at least one is needed'))
        else:
            return (core__Lambda(params, body), n2)

def core__an_tup(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'tup: needs at least one item'))
    else:
        _tup = core__analyse_all(args, scope, n, ())
        items = _tup[0]
        n1 = _tup[1]
        return (core__Tuple(items), n1)

def core__an_get(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if ((len(args) != 2) or (form__sym_name(args[1]) == '')):
        return cdy_rt.primitives.fail(core__located(scope, 'get: expected (get obj field)'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        return (core__Field(obj, form__sym_name(args[1])), n1)

def core__an_assoc(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) < 3):
        return cdy_rt.primitives.fail(core__located(scope, 'assoc: expected (assoc obj field value ...)'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        _cdy__tup_144 = core__assoc_fields(prelude__rest(args), scope, n1, ())
        fields = _cdy__tup_144[0]
        n2 = _cdy__tup_144[1]
        return (core__Assoc(obj, fields), n2)

def core__assoc_fields(forms: tuple[form__Form, ...], scope: core__Scope, n: int, acc: tuple[tuple[str, core__Expr], ...]) -> tuple[tuple[tuple[str, core__Expr], ...], int]:
    while True:
        if (len(forms) == 0):
            return (acc, n)
        elif (len(forms) == 1):
            return cdy_rt.primitives.fail(core__located(scope, 'assoc: expected (assoc obj field value ...)'))
        else:
            field = form__sym_name(forms[0])
            _tup = core__analyse_expr(forms[1], scope, n)
            val = _tup[0]
            n1 = _tup[1]
            if (field == ''):
                return cdy_rt.primitives.fail(core__located(scope, 'assoc field must be a name'))
            else:
                forms, n, acc = (forms[2:len(forms)], n1, (acc + cdy_rt.primitives.to_list((field, val))))
                continue

def core__an_format(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) != 1):
        return cdy_rt.primitives.fail(core__located(scope, 'format: expected one string literal'))
    else:
        _cdy_t13: object = args[0]
        if isinstance(_cdy_t13, form__Txt):
            text = _cdy_t13.val
            _tup = core__format_parts(text, 0, '', scope, n, ())
            parts = _tup[0]
            n1 = _tup[1]
            return (core__Fmt(parts), n1)
        else:
            return cdy_rt.primitives.fail(core__located(scope, 'format: expected one string literal'))

def core__format_parts(text: str, pos: int, acc: str, scope: core__Scope, n: int, parts: tuple[core__FPart, ...]) -> tuple[tuple[core__FPart, ...], int]:
    while True:
        c = (text[pos:(pos + 1)] if (pos < len(text)) else '')
        next_ = (text[(pos + 1):(pos + 2)] if ((pos + 1) < len(text)) else '')
        if (c == ''):
            return (core__add_text(parts, acc), n)
        elif ((c == '{') and (next_ == '{')):
            pos, acc = ((pos + 2), (acc + '{'))
            continue
        elif ((c == '}') and (next_ == '}')):
            pos, acc = ((pos + 2), (acc + '}'))
            continue
        elif (c == '}'):
            return cdy_rt.primitives.fail(core__located(scope, 'format: unmatched } (write }} for a brace)'))
        elif (c == '{'):
            end = core__hole_end(text, (pos + 1))
            forms = scope.parse(text[(pos + 1):end])
            if (len(forms) != 1):
                return cdy_rt.primitives.fail(core__located(scope, 'format: a {hole} must hold exactly one form'))
            else:
                _tup = core__analyse_expr(forms[0], scope, n)
                e = _tup[0]
                n1 = _tup[1]
                pos, acc, n, parts = ((end + 1), '', n1, (core__add_text(parts, acc) + cdy_rt.primitives.to_list(core__FHole(e))))
                continue
        else:
            pos, acc = ((pos + 1), (acc + c))
            continue

def core__hole_end(text: str, pos: int) -> int:
    while True:
        if (pos >= len(text)):
            return cdy_rt.primitives.fail('format: unmatched { (write {{ for a brace)')
        elif (text[pos:(pos + 1)] == '}'):
            return pos
        elif (text[pos:(pos + 1)] == '{'):
            return cdy_rt.primitives.fail("format: a {hole} can't hold a brace")
        else:
            pos = (pos + 1)
            continue

def core__add_text(parts: tuple[core__FPart, ...], text: str) -> tuple[core__FPart, ...]:
    if (text == ''):
        return parts
    else:
        return (parts + cdy_rt.primitives.to_list(core__FText(text)))

def core__an_match(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) < 2):
        return cdy_rt.primitives.fail(core__located(scope, 'match: expected (match subject ((Variant name*) expr)+ (else expr)?)'))
    elif core__is_tup_clause(args[1]):
        return core__an_match_tup(args, scope, n)
    else:
        return core__an_match_sum(args, scope, n)

def core__an_match_sum(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__analyse_expr(args[0], scope, n)
    subject = _tup[0]
    n1 = _tup[1]
    _cdy__tup_188 = core__match_clauses(prelude__rest(args), scope, n1, core__MatchE(subject, (), ()), '')
    m = _cdy__tup_188[0]
    n2 = _cdy__tup_188[1]
    sum_ = (core__match_sum(core__match_clause_list(m), scope) if (len(core__match_clause_list(m)) > 0) else '')
    return (core__global_clauses(core__check_exhaustive(m, sum_, scope), scope.names), n2)

def core__global_clauses(m: core__Expr, names: _cdy_Mapping[str, str]) -> core__Expr:
    _cdy_t14: object = m
    if isinstance(_cdy_t14, core__MatchE):
        subject = _cdy_t14.subject
        clauses = _cdy_t14.clauses
        default = _cdy_t14.default
        return core__MatchE(subject, core__rename_clauses(clauses, names, ()), default)
    else:
        return m

def core__rename_clauses(clauses: tuple[core__Clause, ...], names: _cdy_Mapping[str, str], acc: tuple[core__Clause, ...]) -> tuple[core__Clause, ...]:
    while True:
        if (len(clauses) == 0):
            return acc
        else:
            c = clauses[0]
            clauses, acc = (prelude__rest(clauses), (acc + cdy_rt.primitives.to_list(c._replace(variant=core__global_name(c.variant, names)))))
            continue

def core__is_tup_clause(clause: form__Form) -> bool:
    return (form__sym_name(core__first_item(core__first_item(clause))) == 'tup')

def core__an_match_tup(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    items = form__list_items(args[1])
    names = prelude__rest(form__list_items(items[0]))
    if ((len(args) != 2) or (len(items) != 2)):
        return cdy_rt.primitives.fail(core__located(scope, 'match: a (tup name+) pattern must be the only clause, with no else'))
    elif (len(names) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'match: a (tup name+) pattern needs at least one name'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        subject = _tup[0]
        n1 = _tup[1]
        tmp = core__Local('_tup', n1)
        _cdy__tup_211 = core__tup_binds(names, tmp, 0, scope, (n1 + 1), ())
        pairs = _cdy__tup_211[0]
        inner = _cdy__tup_211[1]
        n2 = _cdy__tup_211[2]
        _cdy__tup_215 = core__analyse_expr(items[1], inner, n2)
        body = _cdy__tup_215[0]
        n3 = _cdy__tup_215[1]
        return (core__nest((cdy_rt.primitives.to_list((tmp, subject)) + pairs), body), n3)

def core__tup_binds(names: tuple[form__Form, ...], tmp: core__Expr, i: int, scope: core__Scope, n: int, acc: tuple[tuple[core__Expr, core__Expr], ...]) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = form__sym_name(names[0])
            loc = core__Local(name, n)
            item = core__Call(core__Prim('at'), (tmp, core__Lit(form__IntLit(i))))
            if (name == ''):
                return cdy_rt.primitives.fail(core__located(scope, 'match name must be a name'))
            elif (name == '_'):
                names, i = (prelude__rest(names), (i + 1))
                continue
            elif core__bound_in_pairs(name, acc):
                return cdy_rt.primitives.fail(core__located(scope, 'match: names in a pattern must be different'))
            else:
                names, i, scope, n, acc = (prelude__rest(names), (i + 1), core__bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.primitives.to_list((loc, item))))
                continue

def core__bound_in_pairs(name: str, pairs: tuple[tuple[core__Expr, core__Expr], ...]) -> bool:
    while True:
        if (len(pairs) == 0):
            return False
        else:
            _tup = pairs[0]
            loc = _tup[0]
            _ = _tup[1]
            _cdy_t15: object = loc
            if isinstance(_cdy_t15, core__Local):
                other = _cdy_t15.name
                return ((other == name) or core__bound_in_pairs(name, prelude__rest(pairs)))
            else:
                pairs = prelude__rest(pairs)
                continue

def core__match_sum(clauses: tuple[core__Clause, ...], scope: core__Scope) -> str:
    return cdy_rt.primitives.map_get(scope.variants, clauses[0].variant).sum_

def core__check_exhaustive(m: core__Expr, sum_: str, scope: core__Scope) -> core__Expr:
    _cdy_t16: object = m
    if isinstance(_cdy_t16, core__MatchE):
        clauses = _cdy_t16.clauses
        default = _cdy_t16.default
        missing = core__missing_variants(cdy_rt.primitives.map_get(scope.sums, sum_), clauses, ())
        if ((len(default) == 0) and (len(missing) > 0)):
            return cdy_rt.primitives.fail(core__located(scope, ('match on ' + str(sum_) + ': no clause for ' + str(cdy_rt.primitives.join(missing, ', ')) + ' (or add else)')))
        else:
            return m
    else:
        return m

def core__missing_variants(names: tuple[str, ...], clauses: tuple[core__Clause, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), (acc if core__has_clause(names[0], clauses) else (acc + cdy_rt.primitives.to_list(names[0]))))
            continue

def core__has_clause(name: str, clauses: tuple[core__Clause, ...]) -> bool:
    while True:
        if (len(clauses) == 0):
            return False
        elif (clauses[0].variant == name):
            return True
        else:
            clauses = prelude__rest(clauses)
            continue

def core__match_clauses(forms: tuple[form__Form, ...], scope: core__Scope, n: int, m: core__Expr, sum_: str) -> tuple[core__Expr, int]:
    while True:
        if (len(forms) == 0):
            return (m, n)
        else:
            items = form__list_items(forms[0])
            if (len(items) != 2):
                return cdy_rt.primitives.fail(core__located(scope, 'match: clause must be (pattern expr)'))
            elif core__is_else(items[0]):
                if ((len(forms) > 1) or (len(core__match_clause_list(m)) == 0)):
                    return cdy_rt.primitives.fail(core__located(scope, 'match: (else expr) must be the last clause, after a pattern'))
                else:
                    _tup = core__analyse_expr(items[1], scope, n)
                    e = _tup[0]
                    n1 = _tup[1]
                    return (core__set_default(m, e), n1)
            else:
                pattern = form__list_items(items[0])
                variant = (form__sym_name(pattern[0]) if (len(pattern) > 0) else '')
                checked = core__check_pattern(variant, pattern, sum_, m, scope)
                _cdy__tup_258 = core__pattern_binds(core__variant_fields(variant, scope), prelude__rest(pattern), scope, n, ())
                binds = _cdy__tup_258[0]
                inner = _cdy__tup_258[1]
                _cdy_n1_261 = _cdy__tup_258[2]
                _cdy__tup_262 = core__analyse_expr(items[1], inner, _cdy_n1_261)
                body = _cdy__tup_262[0]
                n2 = _cdy__tup_262[1]
                forms, n, m, sum_ = (prelude__rest(forms), n2, core__add_clause(m, core__Clause(variant, binds, body)), cdy_rt.primitives.map_get(scope.variants, variant).sum_)
                continue

def core__check_pattern(variant: str, pattern: tuple[form__Form, ...], sum_: str, m: core__Expr, scope: core__Scope) -> bool:
    if (variant == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'match: pattern must be (Variant name*) or else'))
    elif (variant == 'tup'):
        return cdy_rt.primitives.fail(core__located(scope, 'match: a (tup name+) pattern must be the only clause, with no else'))
    elif (not core__is_variant(variant, scope)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: ' + str(variant) + ' is not a variant of a sum type')))
    elif core__has_clause(variant, core__match_clause_list(m)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: more than one clause for ' + str(variant))))
    elif ((sum_ != '') and (sum_ != cdy_rt.primitives.map_get(scope.variants, variant).sum_)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: clauses mix variants of ' + str(sum_) + ' and ' + str(cdy_rt.primitives.map_get(scope.variants, variant).sum_))))
    elif ((len(pattern) - 1) != len(core__variant_fields(variant, scope))):
        return cdy_rt.primitives.fail(core__located(scope, ('match: ' + str(variant) + ' has ' + str(len(core__variant_fields(variant, scope))) + ' field(s), so the pattern needs that many names')))
    else:
        return True

def core__match_clause_list(m: core__Expr) -> tuple[core__Clause, ...]:
    _cdy_t17: object = m
    if isinstance(_cdy_t17, core__MatchE):
        clauses = _cdy_t17.clauses
        return clauses
    else:
        return ()

def core__add_clause(m: core__Expr, clause: core__Clause) -> core__Expr:
    _cdy_t18: object = m
    if isinstance(_cdy_t18, core__MatchE):
        subject = _cdy_t18.subject
        clauses = _cdy_t18.clauses
        default = _cdy_t18.default
        return core__MatchE(subject, (clauses + cdy_rt.primitives.to_list(clause)), default)
    else:
        return m

def core__set_default(m: core__Expr, e: core__Expr) -> core__Expr:
    _cdy_t19: object = m
    if isinstance(_cdy_t19, core__MatchE):
        subject = _cdy_t19.subject
        clauses = _cdy_t19.clauses
        return core__MatchE(subject, clauses, cdy_rt.primitives.to_list(e))
    else:
        return m

def core__pattern_binds(fields: tuple[str, ...], names: tuple[form__Form, ...], scope: core__Scope, n: int, acc: tuple[tuple[str, core__Expr], ...]) -> tuple[tuple[tuple[str, core__Expr], ...], core__Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = form__sym_name(names[0])
            loc = core__Local(name, n)
            if (name == ''):
                return cdy_rt.primitives.fail(core__located(scope, 'match name must be a name'))
            elif (name == '_'):
                fields, names = (prelude__rest(fields), prelude__rest(names))
                continue
            elif core__bound_in(name, acc):
                return cdy_rt.primitives.fail(core__located(scope, 'match: names in a pattern must be different'))
            else:
                fields, names, scope, n, acc = (prelude__rest(fields), prelude__rest(names), core__bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.primitives.to_list((fields[0], loc))))
                continue

def core__bound_in(name: str, binds: tuple[tuple[str, core__Expr], ...]) -> bool:
    while True:
        if (len(binds) == 0):
            return False
        else:
            _tup = binds[0]
            _ = _tup[0]
            loc = _tup[1]
            _cdy_t20: object = loc
            if isinstance(_cdy_t20, core__Local):
                other = _cdy_t20.name
                return ((other == name) or core__bound_in(name, prelude__rest(binds)))
            else:
                binds = prelude__rest(binds)
                continue

def core__an_quo(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    checked = core__needs_form('quo', scope)
    if (len(args) != 1):
        return cdy_rt.primitives.fail(core__located(scope, 'quo: expected (quo form)'))
    else:
        return (core__quoted(args[0]), n)

def core__an_quasi(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    checked = core__needs_form('quasi', scope)
    if (len(args) != 1):
        return cdy_rt.primitives.fail(core__located(scope, 'quasi: expected (quasi form)'))
    else:
        return core__quasi_form(args[0], scope, n)

def core__needs_form(what: str, scope: core__Scope) -> bool:
    if scope.quoting:
        return True
    else:
        return cdy_rt.primitives.fail(core__located(scope, (str(what) + ': only in macro code')))

def core__quoted(form: form__Form) -> core__Expr:
    _cdy_t21: object = form
    if isinstance(_cdy_t21, form__Sym):
        name = _cdy_t21.name
        return core__Call(core__Global('Sym'), (core__Lit(form__Txt(name)), core__Global('NOWHERE')))
    elif isinstance(_cdy_t21, form__Lst):
        items = _cdy_t21.items
        return core__Call(core__Global('Lst'), (core__form_list(core__quoted_all(items, ())), core__Global('NOWHERE')))
    else:
        return core__Call(core__Global(core__literal_variant(form)), cdy_rt.primitives.to_list(core__Lit(form)))

def core__quoted_all(forms: tuple[form__Form, ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (prelude__rest(forms), (acc + cdy_rt.primitives.to_list(core__quoted(forms[0]))))
            continue

def core__form_list(items: tuple[core__Expr, ...]) -> core__Expr:
    if (len(items) == 0):
        return core__Prim('empty-list')
    else:
        return core__Tuple(items)

def core__literal_variant(form: form__Form) -> str:
    _cdy_t22: object = form
    if isinstance(_cdy_t22, form__Txt):
        return 'Txt'
    elif isinstance(_cdy_t22, form__IntLit):
        return 'IntLit'
    elif isinstance(_cdy_t22, form__LongLit):
        return 'LongLit'
    elif isinstance(_cdy_t22, form__ByteLit):
        return 'ByteLit'
    elif isinstance(_cdy_t22, form__FloatLit):
        return 'FloatLit'
    elif isinstance(_cdy_t22, form__DoubleLit):
        return 'DoubleLit'
    elif isinstance(_cdy_t22, form__CharLit):
        return 'CharLit'
    elif isinstance(_cdy_t22, form__BoolLit):
        return 'BoolLit'
    else:
        return cdy_rt.primitives.fail('quo: not a literal')

def core__head_name(form: form__Form) -> str:
    return form__sym_name(core__first_item(form))

def core__quasi_form(form: form__Form, scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    head = core__head_name(form)
    here = core__at_pos(scope, form__form_pos(form))
    if (head == 'unq'):
        return core__unq_arg(form, here, n)
    elif (head == 'unq-sp'):
        return cdy_rt.primitives.fail(core__located(here, 'unq-sp: only inside a list in quasi'))
    elif (head == 'quasi'):
        return cdy_rt.primitives.fail(core__located(here, "quasi: a quasi inside a quasi isn't supported yet"))
    elif core__is_list_form(form):
        return core__quasi_list(form__list_items(form), here, n)
    else:
        return (core__quoted(form), n)

def core__unq_arg(form: form__Form, scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    items = form__list_items(form)
    if (len(items) != 2):
        return cdy_rt.primitives.fail(core__located(scope, (str(core__head_name(form)) + ': expected (' + str(core__head_name(form)) + ' expr)')))
    else:
        return core__analyse_expr(items[1], scope, n)

def core__quasi_list(items: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__quasi_parts(items, scope, n, (), ())
    parts = _tup[0]
    n1 = _tup[1]
    return (core__Call(core__Global('Lst'), (core__join_parts(parts), core__Global('NOWHERE'))), n1)

def core__quasi_parts(items: tuple[form__Form, ...], scope: core__Scope, n: int, run: tuple[core__Expr, ...], parts: tuple[core__Expr, ...]) -> tuple[tuple[core__Expr, ...], int]:
    while True:
        if (len(items) == 0):
            return (core__close_run(run, parts), n)
        else:
            item = items[0]
            if (core__head_name(item) == 'unq-sp'):
                _tup = core__unq_arg(item, core__at_pos(scope, form__form_pos(item)), n)
                e = _tup[0]
                n1 = _tup[1]
                items, n, run, parts = (prelude__rest(items), n1, (), (core__close_run(run, parts) + cdy_rt.primitives.to_list(e)))
                continue
            else:
                _cdy__tup_336 = core__quasi_form(item, scope, n)
                _cdy_e_337 = _cdy__tup_336[0]
                _cdy_n1_338 = _cdy__tup_336[1]
                items, n, run = (prelude__rest(items), _cdy_n1_338, (run + cdy_rt.primitives.to_list(_cdy_e_337)))
                continue

def core__close_run(run: tuple[core__Expr, ...], parts: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    if (len(run) == 0):
        return parts
    else:
        return (parts + cdy_rt.primitives.to_list(core__Tuple(run)))

def core__join_parts(parts: tuple[core__Expr, ...]) -> core__Expr:
    if (len(parts) == 0):
        return core__Prim('empty-list')
    elif (len(parts) == 1):
        return parts[0]
    else:
        return core__Call(core__Prim('+'), parts)

def core__is_lower(name: str) -> bool:
    return ((len(name) > 0) and (name[0:1] >= 'a') and (name[0:1] <= 'z'))

def core__analyse_type(form: form__Form) -> core__CType:
    _cdy_t23: object = form
    if isinstance(_cdy_t23, form__Sym):
        name = _cdy_t23.name
        if core__is_lower(name):
            return core__TVar(name)
        else:
            return core__TCon(name, ())
    elif isinstance(_cdy_t23, form__Lst):
        items = _cdy_t23.items
        if (len(items) == 0):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad type ()'))
        elif (form__sym_name(items[0]) == 'Fn'):
            if (len(items) == 3):
                return core__TFn(core__analyse_types(form__list_items(items[1]), ()), core__analyse_type(items[2]))
            else:
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad function type: expected (Fn (Arg+) Ret)'))
        else:
            return core__TCon(form__sym_name(items[0]), core__analyse_types(prelude__rest(items), ()))
    else:
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad type'))

def core__analyse_types(forms: tuple[form__Form, ...], acc: tuple[core__CType, ...]) -> tuple[core__CType, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (prelude__rest(forms), (acc + cdy_rt.primitives.to_list(core__analyse_type(forms[0]))))
            continue

class core__Prog(_cdy_NamedTuple):
    out: tuple[core__Top, ...]
    sigs: _cdy_Mapping[str, core__CType]
    n: int
    defs: _cdy_Mapping[str, bool]
    defined: _cdy_Mapping[str, bool]

def core__top_names(forms: tuple[form__Form, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = form__list_items(forms[0])
            head = (form__sym_name(items[0]) if (len(items) > 1) else '')
            forms, acc = (prelude__rest(forms), (core__add_name(form__sym_name(items[1]), form__form_pos(items[1]), acc) if ((head == 'def') or (head == 'defn')) else (core__add_names(core__variant_names(items[2:len(items)], ()), form__form_pos(items[1]), cdy_rt.primitives.map_set(core__add_name(core__deft_name(items[1]), form__form_pos(items[1]), acc), core__deft_name(items[1]), False)) if ((head == 'deft') and core__is_sum_body(items[2:len(items)])) else (core__add_name(core__deft_name(items[1]), form__form_pos(items[1]), acc) if (head == 'deft') else acc))))
            continue

def core__add_name(name: str, pos: form__Pos, acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    if cdy_rt.primitives.map_has(acc, name):
        return cdy_rt.primitives.fail((form__pos_text(pos) + ('defined more than once: ' + str(name))))
    else:
        return cdy_rt.primitives.map_set(acc, name, True)

def core__add_names(names: tuple[str, ...], pos: form__Pos, acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), core__add_name(names[0], pos, acc))
            continue

def core__is_sum_body(body: tuple[form__Form, ...]) -> bool:
    return ((len(body) > 0) and core__all_variant_forms(body))

def core__all_variant_forms(body: tuple[form__Form, ...]) -> bool:
    while True:
        if (len(body) == 0):
            return True
        elif (form__sym_name(core__first_item(body[0])) == ''):
            return False
        else:
            body = prelude__rest(body)
            continue

def core__first_item(form: form__Form) -> form__Form:
    items = form__list_items(form)
    if (len(items) == 0):
        return form__Lst((), form__NOWHERE)
    else:
        return items[0]

def core__variant_names(body: tuple[form__Form, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(body) == 0):
            return acc
        else:
            body, acc = (prelude__rest(body), (acc + cdy_rt.primitives.to_list(form__sym_name(core__first_item(body[0])))))
            continue

def core__find_variants(forms: tuple[form__Form, ...], scope: core__Scope) -> core__Scope:
    while True:
        if (len(forms) == 0):
            return scope
        else:
            items = form__list_items(forms[0])
            head = (form__sym_name(items[0]) if (len(items) > 2) else '')
            body = items[2:len(items)]
            _cdy_t25 = prelude__rest(forms)
            if ((head == 'deft') and core__is_sum_body(body)):
                sum_ = core__deft_name(items[1])
                _cdy_t24 = core__add_variants(sum_, body, scope._replace(sums=cdy_rt.primitives.map_set(scope.sums, sum_, core__variant_names(body, ()))))
            else:
                _cdy_t24 = scope
            forms, scope = (_cdy_t25, _cdy_t24)
            continue

def core__add_variants(sum_: str, body: tuple[form__Form, ...], scope: core__Scope) -> core__Scope:
    while True:
        if (len(body) == 0):
            return scope
        else:
            v_items = form__list_items(body[0])
            name = form__sym_name(v_items[0])
            fields = (core__field_names(form__list_items(v_items[1]), ()) if (len(v_items) == 2) else ())
            body, scope = (prelude__rest(body), scope._replace(variants=cdy_rt.primitives.map_set(scope.variants, name, core__VInfo(sum_, fields))))
            continue

def core__field_names(fields: tuple[form__Form, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            fields, acc = (prelude__rest(fields), (acc + cdy_rt.primitives.to_list(form__sym_name(core__first_item(fields[0])))))
            continue

def core__deft_name(form: form__Form) -> str:
    _cdy_t26: object = form
    if isinstance(_cdy_t26, form__Lst):
        items = _cdy_t26.items
        if (len(items) == 0):
            return ''
        else:
            return form__sym_name(items[0])
    else:
        return form__sym_name(form)

class core__Special(_cdy_NamedTuple):
    pass

class core__Op(_cdy_NamedTuple):
    unary: bool

class core__Typed(_cdy_NamedTuple):
    type_: core__CType
type core__Builtin = core__Special | core__Op | core__Typed

def core__is_special(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t29 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t29:
        _cdy_t28: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t28, core__Special):
            _cdy_t27 = True
        else:
            _cdy_t27 = False
        _cdy_t29 = _cdy_t27
    return _cdy_t29

def core__read_builtins(decls: tuple[form__Form, ...], sigs: tuple[form__Form, ...], spellings: _cdy_Mapping[str, tuple[str, str]]) -> _cdy_Mapping[str, core__Builtin]:
    builtins = core__read_sigs(sigs, spellings, core__read_decls(decls, spellings, {}))
    checked = core__all_declared(cdy_rt.primitives.map_keys(spellings), builtins)
    return builtins

def core__spelling_kind(spellings: _cdy_Mapping[str, tuple[str, str]], name: str) -> str:
    if cdy_rt.primitives.map_has(spellings, name):
        return cdy_rt.primitives.map_get(spellings, name)[1]
    else:
        return ''
core__SPECIAL_KINDS: tuple[str, ...] = ('',)
core__VARIADIC_KINDS: tuple[str, ...] = ('binop', 'compare', 'boolop')
core__UNARY_KINDS: tuple[str, ...] = ('unary',)
core__TYPED_KINDS: tuple[str, ...] = ('call', 'value', 'index', 'slice')

def core__read_decls(forms: tuple[form__Form, ...], spellings: _cdy_Mapping[str, tuple[str, str]], acc: _cdy_Mapping[str, core__Builtin]) -> _cdy_Mapping[str, core__Builtin]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            items = form__list_items(form)
            head = (form__sym_name(items[0]) if (len(items) > 0) else '')
            name = (form__sym_name(items[1]) if (len(items) > 1) else '')
            shape = (form__sym_name(items[2]) if (len(items) == 3) else '')
            where = form__pos_text(form__form_pos(form))
            decl = (('', core__Special()) if (name == '') else (('special', core__Special()) if ((head == 'special') and (len(items) == 2)) else (('variadic', core__Op(False)) if ((head == 'op') and (shape == 'variadic')) else (('unary', core__Op(True)) if ((head == 'op') and (shape == 'unary')) else ('', core__Special())))))
            class_ = decl[0]
            if (class_ == ''):
                return cdy_rt.primitives.fail((where + 'special.cdy: expected (special name), (op name variadic) or (op name unary)'))
            elif cdy_rt.primitives.map_has(acc, name):
                return cdy_rt.primitives.fail((str(where) + 'special.cdy: ' + str(name) + ' is declared more than once'))
            elif (not cdy_rt.primitives.in_(core__spelling_kind(spellings, name), core__kinds_of(class_))):
                return cdy_rt.primitives.fail(((str(where) + 'special.cdy: ' + str(name) + " is a special form, so spelling.py can't spell it") if (class_ == 'special') else (str(where) + 'special.cdy: ' + str(name) + ' has no ' + str(class_) + ' entry in spelling.py')))
            else:
                forms, acc = (prelude__rest(forms), cdy_rt.primitives.map_set(acc, name, decl[1]))
                continue

def core__kinds_of(class_: str) -> tuple[str, ...]:
    if (class_ == 'special'):
        return core__SPECIAL_KINDS
    elif (class_ == 'variadic'):
        return core__VARIADIC_KINDS
    elif (class_ == 'unary'):
        return core__UNARY_KINDS
    else:
        return core__TYPED_KINDS

def core__read_sigs(forms: tuple[form__Form, ...], spellings: _cdy_Mapping[str, tuple[str, str]], acc: _cdy_Mapping[str, core__Builtin]) -> _cdy_Mapping[str, core__Builtin]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            items = form__list_items(form)
            name = (form__sym_name(items[1]) if ((len(items) == 3) and (form__sym_name(items[0]) == 'sig')) else '')
            where = form__pos_text(form__form_pos(form))
            if (name == ''):
                return cdy_rt.primitives.fail((where + 'system.cdy: expected (sig name Type)'))
            elif cdy_rt.primitives.map_has(acc, name):
                return cdy_rt.primitives.fail((str(where) + 'system.cdy: ' + str(name) + ' is already declared'))
            elif (not cdy_rt.primitives.in_(core__spelling_kind(spellings, name), core__TYPED_KINDS)):
                return cdy_rt.primitives.fail((str(where) + 'system.cdy: ' + str(name) + ' has no Python mapping in spelling.py'))
            else:
                forms, acc = (prelude__rest(forms), cdy_rt.primitives.map_set(acc, name, core__Typed(core__analyse_type(items[2]))))
                continue

def core__all_declared(names: tuple[str, ...], builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    while True:
        if (len(names) == 0):
            return True
        elif (not cdy_rt.primitives.map_has(builtins, names[0])):
            return cdy_rt.primitives.fail(('spelling.py: ' + str(names[0]) + ' is declared in neither special.cdy nor system.cdy'))
        else:
            names = prelude__rest(names)
            continue

class core__Exports(_cdy_NamedTuple):
    stem: str
    top: _cdy_Mapping[str, bool]
    variants: _cdy_Mapping[str, core__VInfo]
    sums: _cdy_Mapping[str, tuple[str, ...]]
    names: _cdy_Mapping[str, str]

def core__module_exports(forms: tuple[form__Form, ...], stem: str, prefix: str) -> core__Exports:
    top = core__top_names(forms, {})
    found = core__find_variants(forms, core__blank_scope(top))
    return core__Exports(stem, top, found.variants, found.sums, core__prefixed(cdy_rt.primitives.map_keys(top), prefix, {}))

def core__prefixed(names: tuple[str, ...], prefix: str, acc: _cdy_Mapping[str, str]) -> _cdy_Mapping[str, str]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), cdy_rt.primitives.map_set(acc, names[0], (prefix + names[0])))
            continue

def core__blank_scope(top: _cdy_Mapping[str, bool]) -> core__Scope:
    return core__Scope({}, top, (lambda text: ()), {}, {}, form__NOWHERE, {}, False, {}, {}, {})

def core__analyse_program(forms: tuple[form__Form, ...], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    return core__analyse_module(forms, core__module_exports(forms, '', ''), (), {}, builtins, parse, macros, quoting)

def core__analyse_module(forms: tuple[form__Form, ...], own: core__Exports, imports: tuple[tuple[core__Exports, form__Pos], ...], elsewhere: _cdy_Mapping[str, str], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    seen = core__with_own(core__with_imports(imports, core__Seen(core__Exports('', {}, {}, {}, {}), {})), own)
    vis = seen.vis
    scope = core__Scope({}, vis.top, parse, vis.variants, vis.sums, form__NOWHERE, macros, quoting, vis.names, elsewhere, builtins)
    prog = core__analyse_tops(forms, scope, core__Prog((), {}, 0, core__def_names(forms, {}), {}))
    return core__rename_tops(prog.out, vis.names, ())

class core__Seen(_cdy_NamedTuple):
    vis: core__Exports
    from_: _cdy_Mapping[str, str]

def core__with_imports(imports: tuple[tuple[core__Exports, form__Pos], ...], seen: core__Seen) -> core__Seen:
    while True:
        if (len(imports) == 0):
            return seen
        else:
            _tup = imports[0]
            ex = _tup[0]
            pos = _tup[1]
            imports, seen = (prelude__rest(imports), core__import_names(cdy_rt.primitives.map_keys(ex.top), ex, pos, seen))
            continue

def core__import_names(names: tuple[str, ...], ex: core__Exports, pos: form__Pos, seen: core__Seen) -> core__Seen:
    while True:
        if (len(names) == 0):
            return seen._replace(vis=seen.vis._replace(variants=core__put_all(ex.variants, cdy_rt.primitives.map_keys(ex.variants), seen.vis.variants), sums=core__put_all(ex.sums, cdy_rt.primitives.map_keys(ex.sums), seen.vis.sums)))
        else:
            name = names[0]
            stem = ex.stem
            from_ = seen.from_
            vis = seen.vis
            if (cdy_rt.primitives.map_has(from_, name) and (cdy_rt.primitives.map_get(from_, name) != stem)):
                return cdy_rt.primitives.fail((str(form__pos_text(pos)) + 'import: ' + str(cdy_rt.primitives.map_get(from_, name)) + ' and ' + str(stem) + ' both define ' + str(name)))
            else:
                names, seen = (prelude__rest(names), core__Seen(vis._replace(top=cdy_rt.primitives.map_set(vis.top, name, cdy_rt.primitives.map_get(ex.top, name)), names=cdy_rt.primitives.map_set(vis.names, name, cdy_rt.primitives.map_get(ex.names, name))), cdy_rt.primitives.map_set(from_, name, stem)))
                continue

def core__with_own(seen: core__Seen, own: core__Exports) -> core__Seen:
    vis = seen.vis
    return seen._replace(vis=vis._replace(top=core__put_all(own.top, cdy_rt.primitives.map_keys(own.top), vis.top), variants=core__put_all(own.variants, cdy_rt.primitives.map_keys(own.variants), vis.variants), sums=core__put_all(own.sums, cdy_rt.primitives.map_keys(own.sums), vis.sums), names=core__put_all(own.names, cdy_rt.primitives.map_keys(own.names), vis.names)))

def core__put_all[a](m: _cdy_Mapping[str, a], keys: tuple[str, ...], acc: _cdy_Mapping[str, a]) -> _cdy_Mapping[str, a]:
    while True:
        if (len(keys) == 0):
            return acc
        else:
            keys, acc = (prelude__rest(keys), cdy_rt.primitives.map_set(acc, keys[0], cdy_rt.primitives.map_get(m, keys[0])))
            continue

def core__elsewhere_names(exports: tuple[core__Exports, ...], acc: _cdy_Mapping[str, str]) -> _cdy_Mapping[str, str]:
    while True:
        if (len(exports) == 0):
            return acc
        else:
            ex = exports[0]
            exports, acc = (prelude__rest(exports), core__put_all(core__stems_for(cdy_rt.primitives.map_keys(ex.top), ex.stem, {}), cdy_rt.primitives.map_keys(ex.top), acc))
            continue

def core__stems_for(names: tuple[str, ...], stem: str, acc: _cdy_Mapping[str, str]) -> _cdy_Mapping[str, str]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), cdy_rt.primitives.map_set(acc, names[0], stem))
            continue

def core__rename_tops(tops: tuple[core__Top, ...], names: _cdy_Mapping[str, str], acc: tuple[core__Top, ...]) -> tuple[core__Top, ...]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            tops, acc = (prelude__rest(tops), (acc + cdy_rt.primitives.to_list(core__rename_top(tops[0], names))))
            continue

def core__rename_top(top: core__Top, names: _cdy_Mapping[str, str]) -> core__Top:
    _cdy_t30: object = top
    if isinstance(_cdy_t30, core__TDeft):
        name = _cdy_t30.name
        tvars = _cdy_t30.tvars
        fields = _cdy_t30.fields
        return core__TDeft(core__global_name(name, names), tvars, core__rename_fields(fields, names, ()))
    elif isinstance(_cdy_t30, core__TDeftSum):
        _cdy_name_470 = _cdy_t30.name
        _cdy_tvars_471 = _cdy_t30.tvars
        variants = _cdy_t30.variants
        return core__TDeftSum(core__global_name(_cdy_name_470, names), _cdy_tvars_471, core__rename_variants(variants, names, ()))
    elif isinstance(_cdy_t30, core__TDef):
        _cdy_name_473 = _cdy_t30.name
        init = _cdy_t30.init
        t = _cdy_t30.t
        return core__TDef(core__global_name(_cdy_name_473, names), init, core__rename_type(t, names))
    elif isinstance(_cdy_t30, core__TDefn):
        _cdy_name_476 = _cdy_t30.name
        params = _cdy_t30.params
        body = _cdy_t30.body
        _cdy_t_479 = _cdy_t30.t
        return core__TDefn(core__global_name(_cdy_name_476, names), params, body, core__rename_type(_cdy_t_479, names))
    else:
        assert isinstance(_cdy_t30, core__TExpr)
        return top

def core__rename_variants(variants: tuple[core__Variant, ...], names: _cdy_Mapping[str, str], acc: tuple[core__Variant, ...]) -> tuple[core__Variant, ...]:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            variants, acc = (prelude__rest(variants), (acc + cdy_rt.primitives.to_list(core__Variant(core__global_name(v.name, names), core__rename_fields(v.fields, names, ())))))
            continue

def core__rename_fields(fields: tuple[tuple[str, core__CType], ...], names: _cdy_Mapping[str, str], acc: tuple[tuple[str, core__CType], ...]) -> tuple[tuple[str, core__CType], ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            field = _tup[0]
            t = _tup[1]
            fields, acc = (prelude__rest(fields), (acc + cdy_rt.primitives.to_list((field, core__rename_type(t, names)))))
            continue

def core__rename_type(t: core__CType, names: _cdy_Mapping[str, str]) -> core__CType:
    _cdy_t31: object = t
    if isinstance(_cdy_t31, core__TCon):
        name = _cdy_t31.name
        args = _cdy_t31.args
        return core__TCon(core__global_name(name, names), core__rename_types(args, names, ()))
    elif isinstance(_cdy_t31, core__TVar):
        return t
    else:
        assert isinstance(_cdy_t31, core__TFn)
        params = _cdy_t31.params
        ret = _cdy_t31.ret
        return core__TFn(core__rename_types(params, names, ()), core__rename_type(ret, names))

def core__rename_types(types: tuple[core__CType, ...], names: _cdy_Mapping[str, str], acc: tuple[core__CType, ...]) -> tuple[core__CType, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            types, acc = (prelude__rest(types), (acc + cdy_rt.primitives.to_list(core__rename_type(types[0], names))))
            continue

def core__def_names(forms: tuple[form__Form, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = form__list_items(forms[0])
            head = (form__sym_name(items[0]) if (len(items) > 1) else '')
            forms, acc = (prelude__rest(forms), (cdy_rt.primitives.map_set(acc, form__sym_name(items[1]), True) if ((head == 'def') or (head == 'defn')) else acc))
            continue

def core__analyse_tops(forms: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    while True:
        if (len(forms) == 0):
            return prog
        else:
            forms, prog = (prelude__rest(forms), core__analyse_top(forms[0], scope, prog))
            continue

def core__add_top(prog: core__Prog, top: core__Top, n: int) -> core__Prog:
    return prog._replace(out=(prog.out + cdy_rt.primitives.to_list(top)), n=n)

def core__mark_defined(prog: core__Prog, name: str) -> core__Prog:
    return prog._replace(defined=cdy_rt.primitives.map_set(prog.defined, name, True))

def core__analyse_top(form: form__Form, scope: core__Scope, prog: core__Prog) -> core__Prog:
    items = form__list_items(form)
    head = (form__sym_name(items[0]) if (len(items) > 0) else '')
    here = core__at_pos(scope, form__form_pos(form))
    if (cdy_rt.primitives.in_(head, ('def', 'defn')) and (len(items) > 1) and cdy_rt.primitives.map_has(scope.macros, form__sym_name(items[1]))):
        return cdy_rt.primitives.fail(core__located(here, (str(form__sym_name(items[1])) + " is a macro, so it can't be defined")))
    elif (head == 'sig'):
        return core__top_sig(items, here, prog)
    elif (head == 'def'):
        return core__top_def(items, here, prog)
    elif (head == 'defn'):
        return core__top_defn(items, here, prog)
    elif (head == 'deft'):
        return core__top_deft(items, here, prog)
    else:
        _tup = core__analyse_expr(form, here, prog.n)
        e = _tup[0]
        n = _tup[1]
        return core__add_top(prog, core__TExpr(e), n)

def core__top_sig(items: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    name = (form__sym_name(items[1]) if (len(items) == 3) else '')
    if (name == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'sig: expected (sig name Type)'))
    elif (not cdy_rt.primitives.map_has(prog.defs, name)):
        return cdy_rt.primitives.fail(core__located(scope, ('sig for ' + str(name) + ', but no def or defn of ' + str(name) + ' in this file')))
    elif cdy_rt.primitives.map_has(prog.defined, name):
        return cdy_rt.primitives.fail(core__located(scope, ('sig for ' + str(name) + ' comes after its definition')))
    elif cdy_rt.primitives.map_has(prog.sigs, name):
        return cdy_rt.primitives.fail(core__located(scope, ('more than one sig for ' + str(name))))
    else:
        return prog._replace(sigs=cdy_rt.primitives.map_set(prog.sigs, name, core__analyse_type(items[2])))

def core__top_deft(items: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    name = (core__deft_name(items[1]) if (len(items) > 1) else '')
    tvars = (core__syms(prelude__rest(form__list_items(items[1])), ()) if (len(items) > 1) else ())
    body = items[2:len(items)]
    field_forms = (form__list_items(items[2]) if (len(items) == 3) else ())
    if (name == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+)) or (deft Name variant+)'))
    elif core__is_sum_body(body):
        return core__add_top(prog, core__TDeftSum(name, tvars, core__deft_variants(body, ())), prog.n)
    elif (len(field_forms) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+))'))
    else:
        return core__add_top(prog, core__TDeft(name, tvars, core__deft_fields(field_forms, ())), prog.n)

def core__deft_variants(body: tuple[form__Form, ...], acc: tuple[core__Variant, ...]) -> tuple[core__Variant, ...]:
    while True:
        if (len(body) == 0):
            return acc
        else:
            v_items = form__list_items(body[0])
            name = form__sym_name(v_items[0])
            if (not core__is_upper(name)):
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(body[0])) + ('deft: variant names are Capitalised, not ' + str(name))))
            elif (len(v_items) == 1):
                body, acc = (prelude__rest(body), (acc + cdy_rt.primitives.to_list(core__Variant(name, ()))))
                continue
            elif ((len(v_items) == 2) and (len(form__list_items(v_items[1])) > 0)):
                body, acc = (prelude__rest(body), (acc + cdy_rt.primitives.to_list(core__Variant(name, core__deft_fields(form__list_items(v_items[1]), ())))))
                continue
            else:
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(body[0])) + 'deft: variant must be (Name) or (Name ((field Type)+))'))

def core__is_upper(name: str) -> bool:
    return ((len(name) > 0) and (name[0:1] >= 'A') and (name[0:1] <= 'Z'))

def core__syms(forms: tuple[form__Form, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (prelude__rest(forms), (acc + cdy_rt.primitives.to_list(form__sym_name(forms[0]))))
            continue

def core__deft_fields(forms: tuple[form__Form, ...], acc: tuple[tuple[str, core__CType], ...]) -> tuple[tuple[str, core__CType], ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = form__list_items(forms[0])
            if ((len(items) != 2) or (form__sym_name(items[0]) == '')):
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(forms[0])) + 'deft: field must be (name Type)'))
            else:
                forms, acc = (prelude__rest(forms), (acc + cdy_rt.primitives.to_list((form__sym_name(items[0]), core__analyse_type(items[1])))))
                continue

def core__needs_sig(name: str, prog: core__Prog, scope: core__Scope) -> core__CType:
    if cdy_rt.primitives.map_has(prog.sigs, name):
        return cdy_rt.primitives.map_get(prog.sigs, name)
    else:
        return cdy_rt.primitives.fail(core__located(scope, (str(name) + ' needs a (sig ' + str(name) + ' Type) before its definition')))

def core__top_def(items: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    if (len(items) != 3):
        return cdy_rt.primitives.fail(core__located(scope, 'def: expected (def name init); the initial value is required'))
    else:
        name = form__sym_name(items[1])
        t = core__needs_sig(name, prog, scope)
        _tup = core__analyse_expr(items[2], scope, prog.n)
        init = _tup[0]
        n = _tup[1]
        return core__mark_defined(core__add_top(prog, core__TDef(name, init, t), n), name)

def core__top_defn(items: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    if (len(items) != 4):
        return cdy_rt.primitives.fail(core__located(scope, 'defn: expected (defn name (args+) body), with exactly one body form'))
    else:
        name = form__sym_name(items[1])
        t = core__needs_sig(name, prog, scope)
        arg_forms = form__list_items(items[2])
        _tup = core__bind_params(arg_forms, scope, prog.n, ())
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_562 = core__analyse_expr(items[3], inner, n1)
        body = _cdy__tup_562[0]
        n2 = _cdy__tup_562[1]
        if (len(params) == 0):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + str(name) + ': at least one argument is needed')))
        elif (len(params) != core__fn_arity(t)):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + str(name) + ': its sig must be a function type with one type per argument')))
        else:
            return core__mark_defined(core__add_top(prog, core__TDefn(name, params, body, t), n2), name)

def core__fn_arity(t: core__CType) -> int:
    _cdy_t32: object = t
    if isinstance(_cdy_t32, core__TFn):
        params = _cdy_t32.params
        return len(params)
    else:
        return -1

def core__bind_params(forms: tuple[form__Form, ...], scope: core__Scope, n: int, acc: tuple[core__Expr, ...]) -> tuple[tuple[core__Expr, ...], core__Scope, int]:
    while True:
        if (len(forms) == 0):
            return (acc, scope, n)
        else:
            name = form__sym_name(forms[0])
            loc = core__Local(name, n)
            if (name == ''):
                return cdy_rt.primitives.fail(core__located(scope, 'a parameter must be a name'))
            else:
                forms, scope, n, acc = (prelude__rest(forms), core__bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.primitives.to_list(loc)))
                continue
core__MAIN_TYPE: core__CType = core__TFn(cdy_rt.primitives.to_list(core__TCon('List', cdy_rt.primitives.to_list(core__TCon('String', ())))), core__TCon('Int', ()))

def core__has_main(tops: tuple[core__Top, ...]) -> bool:
    while True:
        if (len(tops) == 0):
            return False
        elif core__is_main(tops[0]):
            return True
        else:
            tops = prelude__rest(tops)
            continue

def core__is_main(top: core__Top) -> bool:
    _cdy_t33: object = top
    if isinstance(_cdy_t33, core__TDefn):
        name = _cdy_t33.name
        t = _cdy_t33.t
        if (name != 'main'):
            return False
        elif (t == core__MAIN_TYPE):
            return True
        else:
            return cdy_rt.primitives.fail('main must be typed (Fn ((List String)) Int)')
    elif isinstance(_cdy_t33, core__TDef):
        _cdy_name_577 = _cdy_t33.name
        if (_cdy_name_577 == 'main'):
            return cdy_rt.primitives.fail('main must be a defn')
        else:
            return False
    else:
        return False

class lower__SRecord(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]

class lower__SSum(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    variants: tuple[core__Variant, ...]

class lower__SMatch(_cdy_NamedTuple):
    temp: core__Expr
    subject: core__Expr
    cases: tuple[lower__Case, ...]
    default: tuple[tuple[lower__Stmt, ...], ...]

class lower__SAssign(_cdy_NamedTuple):
    target: core__Expr
    val: core__Expr

class lower__SDefAssign(_cdy_NamedTuple):
    name: str
    val: core__Expr
    t: core__CType

class lower__SExpr(_cdy_NamedTuple):
    expr: core__Expr

class lower__SReturn(_cdy_NamedTuple):
    val: core__Expr

class lower__SIf(_cdy_NamedTuple):
    test: core__Expr
    then: tuple[lower__Stmt, ...]
    other: tuple[lower__Stmt, ...]

class lower__SFunc(_cdy_NamedTuple):
    name: str
    params: tuple[core__Expr, ...]
    body: tuple[lower__Stmt, ...]
    t: core__CType

class lower__SLocalFunc(_cdy_NamedTuple):
    target: core__Expr
    params: tuple[core__Expr, ...]
    body: tuple[lower__Stmt, ...]

class lower__SLoop(_cdy_NamedTuple):
    body: tuple[lower__Stmt, ...]

class lower__SRebind(_cdy_NamedTuple):
    targets: tuple[core__Expr, ...]
    vals: tuple[core__Expr, ...]

class lower__SContinue(_cdy_NamedTuple):
    pass
type lower__Stmt = lower__SRecord | lower__SSum | lower__SMatch | lower__SAssign | lower__SDefAssign | lower__SExpr | lower__SReturn | lower__SIf | lower__SFunc | lower__SLocalFunc | lower__SLoop | lower__SRebind | lower__SContinue

class lower__Case(_cdy_NamedTuple):
    variant: str
    binds: tuple[tuple[str, core__Expr], ...]
    body: tuple[lower__Stmt, ...]

class lower__Low(_cdy_NamedTuple):
    stmts: tuple[lower__Stmt, ...]
    expr: core__Expr
    n: int

def lower__is_simple(e: core__Expr) -> bool:
    _cdy_t34: object = e
    if isinstance(_cdy_t34, core__Lit):
        return True
    elif isinstance(_cdy_t34, core__Local):
        return True
    elif isinstance(_cdy_t34, core__Global):
        return True
    elif isinstance(_cdy_t34, core__Prim):
        return True
    elif isinstance(_cdy_t34, core__Temp):
        return True
    else:
        return False

def lower__is_applied(e: core__Expr) -> bool:
    _cdy_t35: object = e
    if isinstance(_cdy_t35, core__Call):
        callee = _cdy_t35.callee
        args = _cdy_t35.args
        _cdy_t36: object = callee
        if isinstance(_cdy_t36, core__Lambda):
            params = _cdy_t36.params
            return (len(params) == len(args))
        else:
            return False
    else:
        return False

def lower__bind_applied(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], core__Expr, int]:
    _cdy_t37: object = e
    if isinstance(_cdy_t37, core__Call):
        callee = _cdy_t37.callee
        args = _cdy_t37.args
        _cdy_t38: object = callee
        if isinstance(_cdy_t38, core__Lambda):
            params = _cdy_t38.params
            body = _cdy_t38.body
            _tup = lower__value_seq(args, n)
            stmts = _tup[0]
            vals = _tup[1]
            n1 = _tup[2]
            return ((stmts + lower__assigns(params, vals, ())), body, n1)
        else:
            return cdy_rt.primitives.fail('lower: not an applied fn')
    else:
        return cdy_rt.primitives.fail('lower: not an applied fn')

def lower__assigns(targets: tuple[core__Expr, ...], vals: tuple[core__Expr, ...], acc: tuple[lower__Stmt, ...]) -> tuple[lower__Stmt, ...]:
    while True:
        if (len(targets) == 0):
            return acc
        else:
            targets, vals, acc = (prelude__rest(targets), prelude__rest(vals), (acc + cdy_rt.primitives.to_list(lower__SAssign(targets[0], vals[0]))))
            continue

def lower__value(e: core__Expr, n: int) -> lower__Low:
    if lower__is_applied(e):
        _tup = lower__bind_applied(e, n)
        stmts = _tup[0]
        body = _tup[1]
        n1 = _tup[2]
        low = lower__value(body, n1)
        return lower__Low((stmts + low.stmts), low.expr, low.n)
    else:
        _cdy_t39: object = e
        if isinstance(_cdy_t39, core__Call):
            callee = _cdy_t39.callee
            args = _cdy_t39.args
            return lower__value_call(callee, args, n)
        elif isinstance(_cdy_t39, core__If):
            test = _cdy_t39.test
            then = _cdy_t39.then
            other = _cdy_t39.other
            return lower__value_if(test, then, other, n)
        elif isinstance(_cdy_t39, core__Do):
            _cdy_body_30 = _cdy_t39.body
            return lower__value_do(_cdy_body_30, n)
        elif isinstance(_cdy_t39, core__Lambda):
            params = _cdy_t39.params
            _cdy_body_32 = _cdy_t39.body
            return lower__value_fn(params, _cdy_body_32, n)
        elif isinstance(_cdy_t39, core__Tuple):
            items = _cdy_t39.items
            _cdy__tup_34 = lower__value_seq(items, n)
            _cdy_stmts_35 = _cdy__tup_34[0]
            vals = _cdy__tup_34[1]
            _cdy_n1_37 = _cdy__tup_34[2]
            return lower__Low(_cdy_stmts_35, core__Tuple(vals), _cdy_n1_37)
        elif isinstance(_cdy_t39, core__Fmt):
            parts = _cdy_t39.parts
            _cdy__tup_39 = lower__value_seq(lower__holes(parts, ()), n)
            _cdy_stmts_40 = _cdy__tup_39[0]
            _cdy_vals_41 = _cdy__tup_39[1]
            _cdy_n1_42 = _cdy__tup_39[2]
            return lower__Low(_cdy_stmts_40, core__Fmt(lower__fill_holes(parts, _cdy_vals_41, ())), _cdy_n1_42)
        elif isinstance(_cdy_t39, core__Field):
            obj = _cdy_t39.obj
            field = _cdy_t39.field
            _cdy_low_45 = lower__value(obj, n)
            return lower__Low(_cdy_low_45.stmts, core__Field(_cdy_low_45.expr, field), _cdy_low_45.n)
        elif isinstance(_cdy_t39, core__Assoc):
            _cdy_obj_46 = _cdy_t39.obj
            fields = _cdy_t39.fields
            _cdy__tup_48 = lower__value_seq((cdy_rt.primitives.to_list(_cdy_obj_46) + lower__field_vals(fields, ())), n)
            _cdy_stmts_49 = _cdy__tup_48[0]
            _cdy_vals_50 = _cdy__tup_48[1]
            _cdy_n1_51 = _cdy__tup_48[2]
            return lower__Low(_cdy_stmts_49, core__Assoc(_cdy_vals_50[0], lower__refill(fields, prelude__rest(_cdy_vals_50), ())), _cdy_n1_51)
        elif isinstance(_cdy_t39, core__MatchE):
            tmp = core__Temp(n)
            _cdy__tup_53 = lower__lower_match(e, 'value', tmp, (n + 1))
            _cdy_stmts_54 = _cdy__tup_53[0]
            _cdy_n1_55 = _cdy__tup_53[1]
            return lower__Low(_cdy_stmts_54, tmp, _cdy_n1_55)
        else:
            return lower__Low((), e, n)

def lower__lower_match(e: core__Expr, mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t40: object = e
    if isinstance(_cdy_t40, core__MatchE):
        subject = _cdy_t40.subject
        clauses = _cdy_t40.clauses
        default = _cdy_t40.default
        low = lower__value(subject, n)
        temp = core__Temp(low.n)
        _tup = lower__lower_cases(clauses, mode, tmp, (low.n + 1), ())
        cases = _tup[0]
        n2 = _tup[1]
        _cdy__tup_68 = lower__lower_default(default, mode, tmp, n2)
        default_stmts = _cdy__tup_68[0]
        n3 = _cdy__tup_68[1]
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SMatch(temp, low.expr, cases, default_stmts))), n3)
    else:
        return cdy_rt.primitives.fail('lower: not a match')

def lower__lower_default(default: tuple[core__Expr, ...], mode: str, tmp: core__Expr, n: int) -> tuple[tuple[tuple[lower__Stmt, ...], ...], int]:
    if (len(default) == 0):
        return ((), n)
    else:
        _tup = lower__lower_body(default[0], mode, tmp, n)
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.primitives.to_list(stmts), n1)

def lower__lower_cases(clauses: tuple[core__Clause, ...], mode: str, tmp: core__Expr, n: int, acc: tuple[lower__Case, ...]) -> tuple[tuple[lower__Case, ...], int]:
    while True:
        if (len(clauses) == 0):
            return (acc, n)
        else:
            clause = clauses[0]
            _tup = lower__lower_body(clause.body, mode, tmp, n)
            body = _tup[0]
            n1 = _tup[1]
            clauses, n, acc = (prelude__rest(clauses), n1, (acc + cdy_rt.primitives.to_list(lower__Case(clause.variant, clause.binds, body))))
            continue

def lower__lower_body(e: core__Expr, mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    if (mode == 'tail'):
        return lower__tail(e, n)
    elif (mode == 'effect'):
        return lower__effect(e, n)
    else:
        low = lower__value(e, n)
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, low.expr))), low.n)

def lower__value_fn(params: tuple[core__Expr, ...], body: core__Expr, n: int) -> lower__Low:
    _tup = lower__tail(body, n)
    stmts = _tup[0]
    n1 = _tup[1]
    _cdy_t41: object = (stmts[0] if (len(stmts) == 1) else lower__SExpr(core__NIL))
    if isinstance(_cdy_t41, lower__SReturn):
        result = _cdy_t41.val
        return lower__Low((), core__Lambda(params, result), n1)
    else:
        return lower__Low(cdy_rt.primitives.to_list(lower__SLocalFunc(core__Temp(n1), params, stmts)), core__Temp(n1), (n1 + 1))

def lower__holes(parts: tuple[core__FPart, ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t44 = prelude__rest(parts)
            _cdy_t43: object = parts[0]
            if isinstance(_cdy_t43, core__FHole):
                e = _cdy_t43.expr
                _cdy_t42 = (acc + cdy_rt.primitives.to_list(e))
            else:
                assert isinstance(_cdy_t43, core__FText)
                _cdy_t42 = acc
            parts, acc = (_cdy_t44, _cdy_t42)
            continue

def lower__fill_holes(parts: tuple[core__FPart, ...], vals: tuple[core__Expr, ...], acc: tuple[core__FPart, ...]) -> tuple[core__FPart, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t45: object = parts[0]
            if isinstance(_cdy_t45, core__FHole):
                parts, vals, acc = (prelude__rest(parts), prelude__rest(vals), (acc + cdy_rt.primitives.to_list(core__FHole(vals[0]))))
                continue
            else:
                assert isinstance(_cdy_t45, core__FText)
                text = _cdy_t45.text
                parts, acc = (prelude__rest(parts), (acc + cdy_rt.primitives.to_list(core__FText(text))))
                continue

def lower__field_vals(fields: tuple[tuple[str, core__Expr], ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            _ = _tup[0]
            v = _tup[1]
            fields, acc = (prelude__rest(fields), (acc + cdy_rt.primitives.to_list(v)))
            continue

def lower__refill(fields: tuple[tuple[str, core__Expr], ...], vals: tuple[core__Expr, ...], acc: tuple[tuple[str, core__Expr], ...]) -> tuple[tuple[str, core__Expr], ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            f = _tup[0]
            _ = _tup[1]
            fields, vals, acc = (prelude__rest(fields), prelude__rest(vals), (acc + cdy_rt.primitives.to_list((f, vals[0]))))
            continue

def lower__value_call(callee: core__Expr, args: tuple[core__Expr, ...], n: int) -> lower__Low:
    if cdy_rt.primitives.in_(lower__prim_name(callee), ('and', 'or')):
        return lower__value_boolop(callee, args, n)
    else:
        _tup = lower__value_seq((cdy_rt.primitives.to_list(callee) + args), n)
        stmts = _tup[0]
        items = _tup[1]
        n1 = _tup[2]
        return lower__Low(stmts, core__Call(items[0], prelude__rest(items)), n1)

def lower__prim_name(e: core__Expr) -> str:
    _cdy_t46: object = e
    if isinstance(_cdy_t46, core__Prim):
        name = _cdy_t46.name
        return name
    else:
        return ''

def lower__value_boolop(op: core__Expr, args: tuple[core__Expr, ...], n: int) -> lower__Low:
    _tup = lower__low_all(args, n, ())
    lows = _tup[0]
    n1 = _tup[1]
    first = lows[0]
    later = prelude__rest(lows)
    if lower__has_stmts(later):
        tmp = core__Temp(n1)
        return lower__Low((first.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, first.expr)) + cdy_rt.primitives.to_list(lower__guard(op, tmp, lower__guarded(op, later, tmp)))), tmp, (n1 + 1))
    else:
        return lower__Low(first.stmts, core__Call(op, lower__low_exprs(lows, ())), n1)

def lower__guarded(op: core__Expr, lows: tuple[lower__Low, ...], tmp: core__Expr) -> tuple[lower__Stmt, ...]:
    low = lows[0]
    assign = (low.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, low.expr)))
    if (len(lows) == 1):
        return assign
    else:
        return (assign + cdy_rt.primitives.to_list(lower__guard(op, tmp, lower__guarded(op, prelude__rest(lows), tmp))))

def lower__guard(op: core__Expr, tmp: core__Expr, body: tuple[lower__Stmt, ...]) -> lower__Stmt:
    return lower__SIf((tmp if (lower__prim_name(op) == 'and') else core__Call(core__Prim('not'), cdy_rt.primitives.to_list(tmp))), body, ())

def lower__low_exprs(lows: tuple[lower__Low, ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(lows) == 0):
            return acc
        else:
            lows, acc = (prelude__rest(lows), (acc + cdy_rt.primitives.to_list(lows[0].expr)))
            continue

def lower__value_seq(exprs: tuple[core__Expr, ...], n: int) -> tuple[tuple[lower__Stmt, ...], tuple[core__Expr, ...], int]:
    _tup = lower__low_all(exprs, n, ())
    lows = _tup[0]
    n1 = _tup[1]
    return lower__seq_build(lows, n1, (), ())

def lower__low_all(exprs: tuple[core__Expr, ...], n: int, acc: tuple[lower__Low, ...]) -> tuple[tuple[lower__Low, ...], int]:
    while True:
        if (len(exprs) == 0):
            return (acc, n)
        else:
            low = lower__value(exprs[0], n)
            exprs, n, acc = (prelude__rest(exprs), low.n, (acc + cdy_rt.primitives.to_list(low)))
            continue

def lower__has_stmts(lows: tuple[lower__Low, ...]) -> bool:
    while True:
        if (len(lows) == 0):
            return False
        elif (len(lows[0].stmts) > 0):
            return True
        else:
            lows = prelude__rest(lows)
            continue

def lower__seq_build(lows: tuple[lower__Low, ...], n: int, stmts: tuple[lower__Stmt, ...], out: tuple[core__Expr, ...]) -> tuple[tuple[lower__Stmt, ...], tuple[core__Expr, ...], int]:
    while True:
        if (len(lows) == 0):
            return (stmts, out, n)
        else:
            low = lows[0]
            later = prelude__rest(lows)
            if (lower__has_stmts(later) and (not lower__is_simple(low.expr))):
                lows, n, stmts, out = (later, (n + 1), (stmts + low.stmts + cdy_rt.primitives.to_list(lower__SAssign(core__Temp(n), low.expr))), (out + cdy_rt.primitives.to_list(core__Temp(n))))
                continue
            else:
                lows, stmts, out = (later, (stmts + low.stmts), (out + cdy_rt.primitives.to_list(low.expr)))
                continue

def lower__value_if(test: core__Expr, then: core__Expr, other: core__Expr, n: int) -> lower__Low:
    t = lower__value(test, n)
    a = lower__value(then, t.n)
    b = lower__value(other, a.n)
    if ((len(a.stmts) == 0) and (len(b.stmts) == 0)):
        return lower__Low(t.stmts, core__If(t.expr, a.expr, b.expr), b.n)
    elif lower__is_if_into(b.stmts, b.expr):
        tmp = b.expr
        return lower__Low((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, (a.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, a.expr))), b.stmts))), tmp, b.n)
    else:
        _cdy_tmp_169 = core__Temp(b.n)
        return lower__Low((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, (a.stmts + cdy_rt.primitives.to_list(lower__SAssign(_cdy_tmp_169, a.expr))), (b.stmts + cdy_rt.primitives.to_list(lower__SAssign(_cdy_tmp_169, b.expr)))))), _cdy_tmp_169, (b.n + 1))

def lower__is_if_into(stmts: tuple[lower__Stmt, ...], e: core__Expr) -> bool:
    _cdy_t51 = (len(stmts) == 1)
    if _cdy_t51:
        _cdy_t48: object = stmts[0]
        if isinstance(_cdy_t48, lower__SIf):
            _cdy_t47 = True
        else:
            _cdy_t47 = False
        _cdy_t51 = _cdy_t47
        if _cdy_t51:
            _cdy_t50: object = e
            if isinstance(_cdy_t50, core__Temp):
                _cdy_t49 = True
            else:
                _cdy_t49 = False
            _cdy_t51 = _cdy_t49
    return _cdy_t51

def lower__all_but_last(exprs: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    return exprs[0:(len(exprs) - 1)]

def lower__last_of(exprs: tuple[core__Expr, ...]) -> core__Expr:
    return exprs[(len(exprs) - 1)]

def lower__value_do(body: tuple[core__Expr, ...], n: int) -> lower__Low:
    _tup = lower__effect_all(lower__all_but_last(body), n, ())
    stmts = _tup[0]
    n1 = _tup[1]
    low = lower__value(lower__last_of(body), n1)
    return lower__Low((stmts + low.stmts), low.expr, low.n)

def lower__tail(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    if lower__is_applied(e):
        _tup = lower__bind_applied(e, n)
        stmts = _tup[0]
        body = _tup[1]
        n1 = _tup[2]
        _cdy__tup_186 = lower__tail(body, n1)
        more = _cdy__tup_186[0]
        n2 = _cdy__tup_186[1]
        return ((stmts + more), n2)
    else:
        return lower__tail_plain(e, n)

def lower__tail_plain(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t52: object = e
    if isinstance(_cdy_t52, core__If):
        test = _cdy_t52.test
        then = _cdy_t52.then
        other = _cdy_t52.other
        t = lower__value(test, n)
        _tup = lower__tail(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_198 = lower__tail(other, n1)
        b = _cdy__tup_198[0]
        n2 = _cdy__tup_198[1]
        return ((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t52, core__Do):
        body = _cdy_t52.body
        _cdy__tup_202 = lower__effect_all(lower__all_but_last(body), n, ())
        stmts = _cdy__tup_202[0]
        _cdy_n1_204 = _cdy__tup_202[1]
        _cdy__tup_205 = lower__tail(lower__last_of(body), _cdy_n1_204)
        last = _cdy__tup_205[0]
        _cdy_n2_207 = _cdy__tup_205[1]
        return ((stmts + last), _cdy_n2_207)
    elif isinstance(_cdy_t52, core__MatchE):
        return lower__lower_match(e, 'tail', core__NIL, n)
    else:
        low = lower__value(e, n)
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SReturn(low.expr))), low.n)

def lower__effect(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    if lower__is_applied(e):
        _tup = lower__bind_applied(e, n)
        stmts = _tup[0]
        body = _tup[1]
        n1 = _tup[2]
        _cdy__tup_215 = lower__effect(body, n1)
        more = _cdy__tup_215[0]
        n2 = _cdy__tup_215[1]
        return ((stmts + more), n2)
    else:
        return lower__effect_plain(e, n)

def lower__effect_plain(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t53: object = e
    if isinstance(_cdy_t53, core__If):
        test = _cdy_t53.test
        then = _cdy_t53.then
        other = _cdy_t53.other
        t = lower__value(test, n)
        _tup = lower__effect(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_227 = lower__effect(other, n1)
        b = _cdy__tup_227[0]
        n2 = _cdy__tup_227[1]
        return ((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t53, core__Do):
        body = _cdy_t53.body
        return lower__effect_all(body, n, ())
    elif isinstance(_cdy_t53, core__MatchE):
        return lower__lower_match(e, 'effect', core__NIL, n)
    else:
        if lower__is_simple(e):
            return ((), n)
        else:
            low = lower__value(e, n)
            return ((low.stmts + cdy_rt.primitives.to_list(lower__SExpr(low.expr))), low.n)

def lower__effect_all(exprs: tuple[core__Expr, ...], n: int, acc: tuple[lower__Stmt, ...]) -> tuple[tuple[lower__Stmt, ...], int]:
    while True:
        if (len(exprs) == 0):
            return (acc, n)
        else:
            _tup = lower__effect(exprs[0], n)
            stmts = _tup[0]
            n1 = _tup[1]
            exprs, n, acc = (prelude__rest(exprs), n1, (acc + stmts))
            continue

def lower__returns_unit(t: core__CType) -> bool:
    _cdy_t54: object = t
    if isinstance(_cdy_t54, core__TFn):
        ret = _cdy_t54.ret
        _cdy_t55: object = ret
        if isinstance(_cdy_t55, core__TCon):
            name = _cdy_t55.name
            return (name == 'Unit')
        else:
            return False
    else:
        return False

def lower__lower_top(top: core__Top, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t56: object = top
    if isinstance(_cdy_t56, core__TDeft):
        name = _cdy_t56.name
        tvars = _cdy_t56.tvars
        fields = _cdy_t56.fields
        return (cdy_rt.primitives.to_list(lower__SRecord(name, tvars, fields)), n)
    elif isinstance(_cdy_t56, core__TDeftSum):
        _cdy_name_246 = _cdy_t56.name
        _cdy_tvars_247 = _cdy_t56.tvars
        variants = _cdy_t56.variants
        return (cdy_rt.primitives.to_list(lower__SSum(_cdy_name_246, _cdy_tvars_247, variants)), n)
    elif isinstance(_cdy_t56, core__TDef):
        _cdy_name_249 = _cdy_t56.name
        init = _cdy_t56.init
        t = _cdy_t56.t
        low = lower__value(init, n)
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SDefAssign(_cdy_name_249, low.expr, t))), low.n)
    elif isinstance(_cdy_t56, core__TDefn):
        _cdy_name_253 = _cdy_t56.name
        params = _cdy_t56.params
        body = _cdy_t56.body
        _cdy_t_256 = _cdy_t56.t
        _tup = (lower__effect(body, n) if lower__returns_unit(_cdy_t_256) else lower__tail(body, n))
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.primitives.to_list(lower__SFunc(_cdy_name_253, params, lower__loop_tail_calls(_cdy_name_253, params, stmts, lower__returns_unit(_cdy_t_256)), _cdy_t_256)), n1)
    else:
        assert isinstance(_cdy_t56, core__TExpr)
        e = _cdy_t56.expr
        return lower__effect(e, n)

def lower__loop_tail_calls(name: str, params: tuple[core__Expr, ...], body: tuple[lower__Stmt, ...], unit: bool) -> tuple[lower__Stmt, ...]:
    if lower__stmts_have_closure(body):
        return body
    else:
        looped = lower__retail_all(body, name, params)
        if (looped == body):
            return body
        else:
            return cdy_rt.primitives.to_list(lower__SLoop(((looped + cdy_rt.primitives.to_list(lower__SReturn(core__NIL))) if unit else looped)))

def lower__retail_all(stmts: tuple[lower__Stmt, ...], name: str, params: tuple[core__Expr, ...]) -> tuple[lower__Stmt, ...]:
    if (len(stmts) == 0):
        return stmts
    else:
        return (stmts[0:(len(stmts) - 1)] + lower__retail(stmts[(len(stmts) - 1)], name, params))

def lower__retail(s: lower__Stmt, name: str, params: tuple[core__Expr, ...]) -> tuple[lower__Stmt, ...]:
    _cdy_t57: object = s
    if isinstance(_cdy_t57, lower__SReturn):
        val = _cdy_t57.val
        if lower__is_self_call(val, name, params):
            return lower__jump(params, lower__call_args(val))
        else:
            return cdy_rt.primitives.to_list(s)
    elif isinstance(_cdy_t57, lower__SExpr):
        e = _cdy_t57.expr
        if lower__is_self_call(e, name, params):
            return lower__jump(params, lower__call_args(e))
        else:
            return cdy_rt.primitives.to_list(s)
    elif isinstance(_cdy_t57, lower__SIf):
        test = _cdy_t57.test
        then = _cdy_t57.then
        other = _cdy_t57.other
        return cdy_rt.primitives.to_list(lower__SIf(test, lower__retail_all(then, name, params), lower__retail_all(other, name, params)))
    elif isinstance(_cdy_t57, lower__SMatch):
        temp = _cdy_t57.temp
        subject = _cdy_t57.subject
        cases = _cdy_t57.cases
        default = _cdy_t57.default
        return cdy_rt.primitives.to_list(lower__SMatch(temp, subject, lower__retail_cases(cases, name, params, ()), lower__retail_lists(default, name, params, ())))
    else:
        return cdy_rt.primitives.to_list(s)

def lower__retail_cases(cases: tuple[lower__Case, ...], name: str, params: tuple[core__Expr, ...], acc: tuple[lower__Case, ...]) -> tuple[lower__Case, ...]:
    while True:
        if (len(cases) == 0):
            return acc
        else:
            c = cases[0]
            cases, acc = (prelude__rest(cases), (acc + cdy_rt.primitives.to_list(c._replace(body=lower__retail_all(c.body, name, params)))))
            continue

def lower__retail_lists(lists: tuple[tuple[lower__Stmt, ...], ...], name: str, params: tuple[core__Expr, ...], acc: tuple[tuple[lower__Stmt, ...], ...]) -> tuple[tuple[lower__Stmt, ...], ...]:
    while True:
        if (len(lists) == 0):
            return acc
        else:
            lists, acc = (prelude__rest(lists), (acc + cdy_rt.primitives.to_list(lower__retail_all(lists[0], name, params))))
            continue

def lower__is_self_call(e: core__Expr, name: str, params: tuple[core__Expr, ...]) -> bool:
    _cdy_t58: object = e
    if isinstance(_cdy_t58, core__Call):
        callee = _cdy_t58.callee
        args = _cdy_t58.args
        _cdy_t59: object = callee
        if isinstance(_cdy_t59, core__Global):
            g = _cdy_t59.name
            return ((g == name) and (len(args) == len(params)))
        else:
            return False
    else:
        return False

def lower__call_args(e: core__Expr) -> tuple[core__Expr, ...]:
    _cdy_t60: object = e
    if isinstance(_cdy_t60, core__Call):
        args = _cdy_t60.args
        return args
    else:
        return ()

def lower__jump(params: tuple[core__Expr, ...], args: tuple[core__Expr, ...]) -> tuple[lower__Stmt, ...]:
    _tup = lower__changed(params, args, (), ())
    targets = _tup[0]
    vals = _tup[1]
    if (len(targets) == 0):
        return cdy_rt.primitives.to_list(lower__SContinue())
    else:
        return (cdy_rt.primitives.to_list(lower__SRebind(targets, vals)) + cdy_rt.primitives.to_list(lower__SContinue()))

def lower__changed(params: tuple[core__Expr, ...], args: tuple[core__Expr, ...], targets: tuple[core__Expr, ...], vals: tuple[core__Expr, ...]) -> tuple[tuple[core__Expr, ...], tuple[core__Expr, ...]]:
    while True:
        if (len(params) == 0):
            return (targets, vals)
        elif (params[0] == args[0]):
            params, args = (prelude__rest(params), prelude__rest(args))
            continue
        else:
            params, args, targets, vals = (prelude__rest(params), prelude__rest(args), (targets + cdy_rt.primitives.to_list(params[0])), (vals + cdy_rt.primitives.to_list(args[0])))
            continue

def lower__stmts_have_closure(stmts: tuple[lower__Stmt, ...]) -> bool:
    while True:
        if (len(stmts) == 0):
            return False
        elif lower__stmt_has_closure(stmts[0]):
            return True
        else:
            stmts = prelude__rest(stmts)
            continue

def lower__stmt_has_closure(s: lower__Stmt) -> bool:
    _cdy_t61: object = s
    if isinstance(_cdy_t61, lower__SLocalFunc):
        return True
    elif isinstance(_cdy_t61, lower__SAssign):
        target = _cdy_t61.target
        val = _cdy_t61.val
        return (lower__has_lambda(target) or lower__has_lambda(val))
    elif isinstance(_cdy_t61, lower__SDefAssign):
        _cdy_val_311 = _cdy_t61.val
        return lower__has_lambda(_cdy_val_311)
    elif isinstance(_cdy_t61, lower__SExpr):
        e = _cdy_t61.expr
        return lower__has_lambda(e)
    elif isinstance(_cdy_t61, lower__SReturn):
        _cdy_val_313 = _cdy_t61.val
        return lower__has_lambda(_cdy_val_313)
    elif isinstance(_cdy_t61, lower__SIf):
        test = _cdy_t61.test
        then = _cdy_t61.then
        other = _cdy_t61.other
        return (lower__has_lambda(test) or lower__stmts_have_closure(then) or lower__stmts_have_closure(other))
    elif isinstance(_cdy_t61, lower__SMatch):
        subject = _cdy_t61.subject
        cases = _cdy_t61.cases
        default = _cdy_t61.default
        return (lower__has_lambda(subject) or lower__cases_have_closure(cases) or lower__lists_have_closure(default))
    elif isinstance(_cdy_t61, lower__SLoop):
        body = _cdy_t61.body
        return lower__stmts_have_closure(body)
    elif isinstance(_cdy_t61, lower__SRebind):
        vals = _cdy_t61.vals
        return lower__any_lambda(vals)
    else:
        return False

def lower__cases_have_closure(cases: tuple[lower__Case, ...]) -> bool:
    while True:
        if (len(cases) == 0):
            return False
        elif lower__stmts_have_closure(cases[0].body):
            return True
        else:
            cases = prelude__rest(cases)
            continue

def lower__lists_have_closure(lists: tuple[tuple[lower__Stmt, ...], ...]) -> bool:
    while True:
        if (len(lists) == 0):
            return False
        elif lower__stmts_have_closure(lists[0]):
            return True
        else:
            lists = prelude__rest(lists)
            continue

def lower__any_lambda(exprs: tuple[core__Expr, ...]) -> bool:
    while True:
        if (len(exprs) == 0):
            return False
        elif lower__has_lambda(exprs[0]):
            return True
        else:
            exprs = prelude__rest(exprs)
            continue

def lower__has_lambda(e: core__Expr) -> bool:
    while True:
        _cdy_t62: object = e
        if isinstance(_cdy_t62, core__Lambda):
            return True
        elif isinstance(_cdy_t62, core__Call):
            callee = _cdy_t62.callee
            args = _cdy_t62.args
            return (lower__has_lambda(callee) or lower__any_lambda(args))
        elif isinstance(_cdy_t62, core__If):
            test = _cdy_t62.test
            then = _cdy_t62.then
            other = _cdy_t62.other
            return (lower__has_lambda(test) or lower__has_lambda(then) or lower__has_lambda(other))
        elif isinstance(_cdy_t62, core__Do):
            body = _cdy_t62.body
            return lower__any_lambda(body)
        elif isinstance(_cdy_t62, core__Tuple):
            items = _cdy_t62.items
            return lower__any_lambda(items)
        elif isinstance(_cdy_t62, core__Fmt):
            parts = _cdy_t62.parts
            return lower__any_lambda(lower__holes(parts, ()))
        elif isinstance(_cdy_t62, core__Field):
            obj = _cdy_t62.obj
            e = obj
            continue
        elif isinstance(_cdy_t62, core__Assoc):
            _cdy_obj_335 = _cdy_t62.obj
            fields = _cdy_t62.fields
            return (lower__has_lambda(_cdy_obj_335) or lower__any_lambda(lower__field_vals(fields, ())))
        elif isinstance(_cdy_t62, core__MatchE):
            subject = _cdy_t62.subject
            e = subject
            continue
        else:
            return False

def lower__lower_program(tops: tuple[core__Top, ...], n: int, acc: tuple[lower__Stmt, ...]) -> tuple[lower__Stmt, ...]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _tup = lower__lower_top(tops[0], n)
            stmts = _tup[0]
            n1 = _tup[1]
            tops, n, acc = (prelude__rest(tops), n1, (acc + stmts))
            continue

class emit__Env(_cdy_NamedTuple):
    globals_: _cdy_Mapping[str, str]
    locals_: _cdy_Mapping[int, str]
    taken: _cdy_Mapping[str, bool]
    generic: _cdy_Mapping[str, bool]
    spellings: _cdy_Mapping[str, tuple[str, str]]
emit__HEADER: str = 'from __future__ import annotations\n\nfrom collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping\nfrom typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple\n'

def emit__comma_join(strs: tuple[str, ...]) -> str:
    return cdy_rt.primitives.join(strs, ', ')

def emit__line(level: int, text: str) -> str:
    return (emit__indent(level) + text + '\n')
emit__INDENT_STEP: str = '    '

def emit__indent(level: int) -> str:
    if (level <= 0):
        return ''
    else:
        return (emit__INDENT_STEP + emit__indent((level - 1)))
emit__PY_IMPORTS: tuple[str, ...] = ('math', 're', 'cdy_rt.spelling', 'cdy_rt.primitives')

def emit__name_set(names: tuple[str, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), cdy_rt.primitives.map_set(acc, names[0], True))
            continue
emit__PY_RESERVED: _cdy_Mapping[str, bool] = emit__name_set((('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'PythonFinalizationError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '_IncompleteInputError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'and', 'anext', 'any', 'as', 'ascii', 'assert', 'async', 'await', 'bin', 'bool', 'break', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'class', 'classmethod', 'compile', 'complex', 'continue', 'copyright', 'credits', 'def', 'del', 'delattr', 'dict', 'dir', 'divmod', 'elif', 'else', 'enumerate', 'eval', 'except', 'exec', 'exit', 'filter', 'finally', 'float', 'for', 'format', 'from', 'frozenset', 'getattr', 'global', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'if', 'import', 'in', 'input', 'int', 'is', 'isinstance', 'issubclass', 'iter', 'lambda', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'nonlocal', 'not', 'object', 'oct', 'open', 'or', 'ord', 'pass', 'pow', 'print', 'property', 'quit', 'raise', 'range', 'repr', 'return', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'try', 'tuple', 'type', 'vars', 'while', 'with', 'yield', 'zip') + ('math', 're', 'cdy_rt')), {})
emit__MANGLED: _cdy_Mapping[str, str] = cdy_rt.primitives.map_set(cdy_rt.primitives.map_set(cdy_rt.primitives.map_set({}, '-', '_'), '?', '_p'), '!', '_x')

def emit__py_mangle(name: str) -> str:
    out = emit__mangle_chars(name, 0, '')
    if (cdy_rt.primitives.map_has(emit__PY_RESERVED, out) or (out[0:5] == '_cdy_')):
        return (out + '_')
    else:
        return out

def emit__mangle_chars(name: str, i: int, acc: str) -> str:
    while True:
        if (i == len(name)):
            return acc
        else:
            i, acc = ((i + 1), (acc + emit__mangle_char(name[i:(i + 1)])))
            continue

def emit__mangle_char(ch: str) -> str:
    if (('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9') or (ch == '_')):
        return ch
    elif cdy_rt.primitives.map_has(emit__MANGLED, ch):
        return cdy_rt.primitives.map_get(emit__MANGLED, ch)
    else:
        return ('_u' + emit__hex(ord(ch), 4))
emit__HEX_DIGITS: str = '0123456789abcdef'

def emit__hex(n: int, width: int) -> str:
    digit = emit__HEX_DIGITS[(n - (16 * (n // 16))):((n - (16 * (n // 16))) + 1)]
    if ((n < 16) and (width <= 1)):
        return digit
    else:
        return (emit__hex((n // 16), (width - 1)) + digit)

def emit__py_str(s: str) -> str:
    q = ('"' if (cdy_rt.primitives.in_("'", s) and (not cdy_rt.primitives.in_('"', s))) else "'")
    return (q + emit__escape_chars(s, q, 0, '') + q)

def emit__escape_chars(s: str, q: str, i: int, acc: str) -> str:
    while True:
        if (i == len(s)):
            return acc
        else:
            i, acc = ((i + 1), (acc + emit__escape_char(s[i:(i + 1)], q)))
            continue

def emit__escape_char(ch: str, q: str) -> str:
    code = ord(ch)
    if ((ch == q) or (ch == '\\')):
        return ('\\' + ch)
    elif (ch == '\n'):
        return '\\n'
    elif (ch == '\r'):
        return '\\r'
    elif (ch == '\t'):
        return '\\t'
    elif ((code < 32) or (127 <= code <= 160)):
        return ('\\x' + emit__hex(code, 2))
    else:
        return ch

def emit__global_names(tops: tuple[core__Top, ...], env: emit__Env) -> emit__Env:
    while True:
        if (len(tops) == 0):
            return env
        else:
            tops, env = (prelude__rest(tops), emit__add_globals(emit__top_names_of(tops[0]), env))
            continue

def emit__add_globals(names: tuple[str, ...], env: emit__Env) -> emit__Env:
    while True:
        if (len(names) == 0):
            return env
        else:
            name = names[0]
            py = emit__py_mangle(name)
            names, env = (prelude__rest(names), env._replace(globals_=cdy_rt.primitives.map_set(env.globals_, name, py), taken=cdy_rt.primitives.map_set(env.taken, py, True)))
            continue

def emit__top_names_of(top: core__Top) -> tuple[str, ...]:
    _cdy_t63: object = top
    if isinstance(_cdy_t63, core__TDeftSum):
        name = _cdy_t63.name
        variants = _cdy_t63.variants
        return (cdy_rt.primitives.to_list(name) + emit__variant_list_names(variants, ()))
    else:
        if (emit__top_name(top) == ''):
            return ()
        else:
            return cdy_rt.primitives.to_list(emit__top_name(top))

def emit__variant_list_names(variants: tuple[core__Variant, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            variants, acc = (prelude__rest(variants), (acc + cdy_rt.primitives.to_list(variants[0].name)))
            continue

def emit__top_name(top: core__Top) -> str:
    _cdy_t64: object = top
    if isinstance(_cdy_t64, core__TDeft):
        name = _cdy_t64.name
        return name
    elif isinstance(_cdy_t64, core__TDef):
        _cdy_name_37 = _cdy_t64.name
        return _cdy_name_37
    elif isinstance(_cdy_t64, core__TDefn):
        _cdy_name_38 = _cdy_t64.name
        return _cdy_name_38
    else:
        return ''

def emit__generic_variants(tops: tuple[core__Top, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _cdy_t67 = prelude__rest(tops)
            _cdy_t66: object = tops[0]
            if isinstance(_cdy_t66, core__TDeftSum):
                tvars = _cdy_t66.tvars
                variants = _cdy_t66.variants
                _cdy_t65 = (acc if (len(tvars) == 0) else emit__mark_all(emit__variant_list_names(variants, ()), acc))
            else:
                _cdy_t65 = acc
            tops, acc = (_cdy_t67, _cdy_t65)
            continue

def emit__mark_all(names: tuple[str, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), cdy_rt.primitives.map_set(acc, names[0], True))
            continue

def emit__local_py(name: str, id_: int, env: emit__Env) -> str:
    if cdy_rt.primitives.map_has(env.locals_, id_):
        return cdy_rt.primitives.map_get(env.locals_, id_)
    else:
        return cdy_rt.primitives.fail(('emit: local ' + str(name) + ' has no Python name'))

def emit__bind_locals(locs: tuple[core__Expr, ...], env: emit__Env) -> emit__Env:
    while True:
        if (len(locs) == 0):
            return env
        else:
            _cdy_t71 = prelude__rest(locs)
            _cdy_t69: object = locs[0]
            if isinstance(_cdy_t69, core__Local):
                name = _cdy_t69.name
                id_ = _cdy_t69.id_
                if cdy_rt.primitives.map_has(env.locals_, id_):
                    _cdy_t70 = env
                else:
                    base = emit__py_mangle(name)
                    py = (('_cdy_' + str(base) + '_' + str(id_)) if cdy_rt.primitives.map_has(env.taken, base) else base)
                    _cdy_t70 = env._replace(locals_=cdy_rt.primitives.map_set(env.locals_, id_, py), taken=cdy_rt.primitives.map_set(env.taken, py, True))
                _cdy_t68 = _cdy_t70
            else:
                _cdy_t68 = env
            locs, env = (_cdy_t71, _cdy_t68)
            continue

def emit__bound_locals(stmts: tuple[lower__Stmt, ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(stmts) == 0):
            return acc
        else:
            _cdy_t76 = prelude__rest(stmts)
            _cdy_t73: object = stmts[0]
            if isinstance(_cdy_t73, lower__SAssign):
                target = _cdy_t73.target
                _cdy_t75: object = target
                if isinstance(_cdy_t75, core__Local):
                    _cdy_t74 = (acc + cdy_rt.primitives.to_list(target))
                else:
                    _cdy_t74 = acc
                _cdy_t72 = _cdy_t74
            elif isinstance(_cdy_t73, lower__SIf):
                then = _cdy_t73.then
                other = _cdy_t73.other
                _cdy_t72 = emit__bound_locals(other, emit__bound_locals(then, acc))
            elif isinstance(_cdy_t73, lower__SMatch):
                cases = _cdy_t73.cases
                default = _cdy_t73.default
                _cdy_t72 = emit__bound_in_cases(cases, emit__bound_in_lists(default, acc))
            elif isinstance(_cdy_t73, lower__SLoop):
                body = _cdy_t73.body
                _cdy_t72 = emit__bound_locals(body, acc)
            else:
                _cdy_t72 = acc
            stmts, acc = (_cdy_t76, _cdy_t72)
            continue

def emit__bound_in_cases(cases: tuple[lower__Case, ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(cases) == 0):
            return acc
        else:
            c = cases[0]
            cases, acc = (prelude__rest(cases), emit__bound_locals(c.body, (acc + emit__bind_locs(c.binds, ()))))
            continue

def emit__bind_locs(binds: tuple[tuple[str, core__Expr], ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(binds) == 0):
            return acc
        else:
            _tup = binds[0]
            _ = _tup[0]
            loc = _tup[1]
            binds, acc = (prelude__rest(binds), (acc + cdy_rt.primitives.to_list(loc)))
            continue

def emit__bound_in_lists(lists: tuple[tuple[lower__Stmt, ...], ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(lists) == 0):
            return acc
        else:
            lists, acc = (prelude__rest(lists), emit__bound_locals(lists[0], acc))
            continue

def emit__emit_expr(e: core__Expr, env: emit__Env) -> str:
    _cdy_t77: object = e
    if isinstance(_cdy_t77, core__Lit):
        form = _cdy_t77.form
        return emit__emit_lit(form)
    elif isinstance(_cdy_t77, core__Local):
        name = _cdy_t77.name
        id_ = _cdy_t77.id_
        return emit__local_py(name, id_, env)
    elif isinstance(_cdy_t77, core__Global):
        _cdy_name_77 = _cdy_t77.name
        return cdy_rt.primitives.map_get(env.globals_, _cdy_name_77)
    elif isinstance(_cdy_t77, core__Prim):
        _cdy_name_78 = _cdy_t77.name
        return emit__emit_prim(_cdy_name_78, env)
    elif isinstance(_cdy_t77, core__Call):
        callee = _cdy_t77.callee
        args = _cdy_t77.args
        return emit__emit_call(callee, args, env)
    elif isinstance(_cdy_t77, core__If):
        test = _cdy_t77.test
        then = _cdy_t77.then
        other = _cdy_t77.other
        return ('(' + str(emit__emit_expr(then, env)) + ' if ' + str(emit__emit_expr(test, env)) + ' else ' + str(emit__emit_expr(other, env)) + ')')
    elif isinstance(_cdy_t77, core__Do):
        return cdy_rt.primitives.fail('emit: a do inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t77, core__MatchE):
        return cdy_rt.primitives.fail('emit: a match inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t77, core__Lambda):
        params = _cdy_t77.params
        body = _cdy_t77.body
        inner = emit__bind_locals(params, env)
        return ('(lambda ' + str(emit__comma_join(emit__emit_exprs(params, inner, ()))) + ': ' + str(emit__emit_expr(body, inner)) + ')')
    elif isinstance(_cdy_t77, core__Tuple):
        items = _cdy_t77.items
        strs = emit__emit_exprs(items, env, ())
        if (len(strs) == 1):
            return ('(' + str(strs[0]) + ',)')
        else:
            return ('(' + str(emit__comma_join(strs)) + ')')
    elif isinstance(_cdy_t77, core__Fmt):
        parts = _cdy_t77.parts
        return emit__emit_format(parts, env)
    elif isinstance(_cdy_t77, core__Field):
        obj = _cdy_t77.obj
        field = _cdy_t77.field
        return (str(emit__emit_expr(obj, env)) + '.' + str(emit__py_mangle(field)))
    elif isinstance(_cdy_t77, core__Assoc):
        _cdy_obj_92 = _cdy_t77.obj
        fields = _cdy_t77.fields
        return (str(emit__emit_expr(_cdy_obj_92, env)) + '._replace(' + str(emit__comma_join(emit__emit_fields(fields, env, ()))) + ')')
    else:
        assert isinstance(_cdy_t77, core__Temp)
        _cdy_id__94 = _cdy_t77.id_
        return ('_cdy_t' + str(_cdy_id__94))

def emit__emit_format(parts: tuple[core__FPart, ...], env: emit__Env) -> str:
    if (len(parts) == 0):
        return "''"
    else:
        return ('(' + str(cdy_rt.primitives.join(emit__emit_parts(parts, env, ()), ' + ')) + ')')

def emit__emit_parts(parts: tuple[core__FPart, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t80 = prelude__rest(parts)
            _cdy_t79: object = parts[0]
            if isinstance(_cdy_t79, core__FText):
                text = _cdy_t79.text
                _cdy_t78 = emit__py_str(text)
            else:
                assert isinstance(_cdy_t79, core__FHole)
                e = _cdy_t79.expr
                _cdy_t78 = ('str(' + str(emit__emit_expr(e, env)) + ')')
            parts, acc = (_cdy_t80, (acc + cdy_rt.primitives.to_list(_cdy_t78)))
            continue

def emit__emit_fields(fields: tuple[tuple[str, core__Expr], ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            f = _tup[0]
            v = _tup[1]
            fields, acc = (prelude__rest(fields), (acc + cdy_rt.primitives.to_list((str(emit__py_mangle(f)) + '=' + str(emit__emit_expr(v, env))))))
            continue

def emit__emit_exprs(exprs: tuple[core__Expr, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(exprs) == 0):
            return acc
        else:
            exprs, acc = (prelude__rest(exprs), (acc + cdy_rt.primitives.to_list(emit__emit_expr(exprs[0], env))))
            continue

def emit__emit_lit(form: form__Form) -> str:
    _cdy_t81: object = form
    if isinstance(_cdy_t81, form__Txt):
        v = _cdy_t81.val
        return emit__py_str(v)
    elif isinstance(_cdy_t81, form__CharLit):
        _cdy_v_113 = _cdy_t81.val
        return emit__py_str(_cdy_v_113)
    elif isinstance(_cdy_t81, form__IntLit):
        _cdy_v_114 = _cdy_t81.val
        return (str(_cdy_v_114))
    elif isinstance(_cdy_t81, form__LongLit):
        _cdy_v_115 = _cdy_t81.val
        return (str(_cdy_v_115))
    elif isinstance(_cdy_t81, form__ByteLit):
        _cdy_v_116 = _cdy_t81.val
        return (str(_cdy_v_116))
    elif isinstance(_cdy_t81, form__FloatLit):
        _cdy_v_117 = _cdy_t81.val
        return (str(_cdy_v_117))
    elif isinstance(_cdy_t81, form__DoubleLit):
        _cdy_v_118 = _cdy_t81.val
        return (str(_cdy_v_118))
    elif isinstance(_cdy_t81, form__BoolLit):
        _cdy_v_119 = _cdy_t81.val
        return (str(_cdy_v_119))
    else:
        return cdy_rt.primitives.fail('emit: not a literal')

def emit__emit_prim(name: str, env: emit__Env) -> str:
    if cdy_rt.primitives.in_(core__spelling_kind(env.spellings, name), core__TYPED_KINDS):
        return cdy_rt.primitives.map_get(env.spellings, name)[0]
    else:
        return cdy_rt.primitives.fail(('the operator ' + str(name) + " can't be used as a value yet; wrap it in a fn"))

def emit__emit_call(callee: core__Expr, args: tuple[core__Expr, ...], env: emit__Env) -> str:
    strs = emit__emit_exprs(args, env, ())
    _cdy_t82: object = callee
    if isinstance(_cdy_t82, core__Prim):
        name = _cdy_t82.name
        return emit__emit_prim_call(name, strs, env)
    else:
        return (str(emit__emit_expr(callee, env)) + '(' + str(emit__comma_join(strs)) + ')')

def emit__emit_prim_call(name: str, strs: tuple[str, ...], env: emit__Env) -> str:
    kind = cdy_rt.primitives.map_get(env.spellings, name)[1]
    py = cdy_rt.primitives.map_get(env.spellings, name)[0]
    op = (' ' + py + ' ')
    if cdy_rt.primitives.in_(kind, ('binop', 'compare', 'boolop')):
        return ('(' + str(cdy_rt.primitives.join(strs, op)) + ')')
    elif (kind == 'unary'):
        return ('(' + str(py) + ' ' + str(strs[0]) + ')')
    elif (kind == 'index'):
        return (str(strs[0]) + '[' + str(strs[1]) + ']')
    elif (kind == 'slice'):
        return (str(strs[0]) + '[' + str(strs[1]) + ':' + str(strs[2]) + ']')
    else:
        return (str(py) + '(' + str(emit__comma_join(strs)) + ')')

def emit__emit_type(t: core__CType, env: emit__Env) -> str:
    _cdy_t83: object = t
    if isinstance(_cdy_t83, core__TVar):
        name = _cdy_t83.name
        return emit__py_mangle(name)
    elif isinstance(_cdy_t83, core__TFn):
        params = _cdy_t83.params
        ret = _cdy_t83.ret
        return ('_cdy_Callable[[' + str(emit__comma_join(emit__emit_types(params, env, ()))) + '], ' + str(emit__emit_type(ret, env)) + ']')
    else:
        assert isinstance(_cdy_t83, core__TCon)
        _cdy_name_138 = _cdy_t83.name
        args = _cdy_t83.args
        return emit__emit_tcon(_cdy_name_138, emit__emit_types(args, env, ()))

def emit__emit_types(types: tuple[core__CType, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            types, acc = (prelude__rest(types), (acc + cdy_rt.primitives.to_list(emit__emit_type(types[0], env))))
            continue

def emit__emit_tcon(name: str, args: tuple[str, ...]) -> str:
    if cdy_rt.primitives.in_(name, ('Int', 'Long', 'Byte')):
        return 'int'
    elif cdy_rt.primitives.in_(name, ('Float', 'Double')):
        return 'float'
    elif (name == 'Bool'):
        return 'bool'
    elif cdy_rt.primitives.in_(name, ('Char', 'String')):
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
        return ('tuple[' + str(emit__comma_join(args)) + ']')
    elif (name == 'Map'):
        return ('_cdy_Mapping[' + str(emit__comma_join(args)) + ']')
    elif (len(args) == 0):
        return emit__py_mangle(name)
    else:
        return (str(emit__py_mangle(name)) + '[' + str(emit__comma_join(args)) + ']')

def emit__type_vars(types: tuple[core__CType, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            _cdy_t86 = prelude__rest(types)
            _cdy_t85: object = types[0]
            if isinstance(_cdy_t85, core__TVar):
                name = _cdy_t85.name
                _cdy_t84 = (acc if cdy_rt.primitives.in_(name, acc) else (acc + cdy_rt.primitives.to_list(name)))
            elif isinstance(_cdy_t85, core__TCon):
                args = _cdy_t85.args
                _cdy_t84 = emit__type_vars(args, acc)
            else:
                assert isinstance(_cdy_t85, core__TFn)
                params = _cdy_t85.params
                ret = _cdy_t85.ret
                _cdy_t84 = emit__type_vars((params + cdy_rt.primitives.to_list(ret)), acc)
            types, acc = (_cdy_t86, _cdy_t84)
            continue

def emit__emit_stmt(s: lower__Stmt, level: int, env: emit__Env) -> str:
    _cdy_t87: object = s
    if isinstance(_cdy_t87, lower__SRecord):
        name = _cdy_t87.name
        tvars = _cdy_t87.tvars
        fields = _cdy_t87.fields
        return ('\n' + emit__line(level, ('class ' + str(cdy_rt.primitives.map_get(env.globals_, name)) + str(emit__type_params(tvars)) + '(_cdy_NamedTuple):')) + emit__emit_record_fields(fields, (level + 1), env, ''))
    elif isinstance(_cdy_t87, lower__SSum):
        _cdy_name_157 = _cdy_t87.name
        _cdy_tvars_158 = _cdy_t87.tvars
        variants = _cdy_t87.variants
        return (emit__emit_variants(variants, _cdy_tvars_158, level, env, '') + emit__line(level, ('type ' + str(cdy_rt.primitives.map_get(env.globals_, _cdy_name_157)) + str(emit__type_params(_cdy_tvars_158)) + ' = ' + str(cdy_rt.primitives.join(emit__variant_refs(variants, _cdy_tvars_158, env, ()), ' | ')))))
    elif isinstance(_cdy_t87, lower__SMatch):
        temp = _cdy_t87.temp
        subject = _cdy_t87.subject
        cases = _cdy_t87.cases
        default = _cdy_t87.default
        t = emit__emit_expr(temp, env)
        val = emit__emit_expr(subject, env)
        generic = cdy_rt.primitives.map_has(env.generic, cases[0].variant)
        return (emit__line(level, ((str(t) + ' = ' + str(val)) if generic else (str(t) + ': object = ' + str(val)))) + emit__emit_match(t, cases, default, ((not generic) and (len(default) == 0)), 'if', level, env))
    elif isinstance(_cdy_t87, lower__SLoop):
        body = _cdy_t87.body
        return (emit__line(level, 'while True:') + emit__emit_block(body, (level + 1), env))
    elif isinstance(_cdy_t87, lower__SRebind):
        targets = _cdy_t87.targets
        vals = _cdy_t87.vals
        return emit__line(level, ((str(emit__emit_expr(targets[0], env)) + ' = ' + str(emit__emit_expr(vals[0], env))) if (len(targets) == 1) else (str(emit__comma_join(emit__emit_exprs(targets, env, ()))) + ' = (' + str(emit__comma_join(emit__emit_exprs(vals, env, ()))) + ')')))
    elif isinstance(_cdy_t87, lower__SContinue):
        return emit__line(level, 'continue')
    elif isinstance(_cdy_t87, lower__SAssign):
        target = _cdy_t87.target
        _cdy_val_171 = _cdy_t87.val
        return emit__line(level, (str(emit__emit_expr(target, env)) + ' = ' + str(emit__emit_expr(_cdy_val_171, env))))
    elif isinstance(_cdy_t87, lower__SDefAssign):
        _cdy_name_172 = _cdy_t87.name
        _cdy_val_173 = _cdy_t87.val
        _cdy_t_174 = _cdy_t87.t
        return emit__line(level, (str(cdy_rt.primitives.map_get(env.globals_, _cdy_name_172)) + ': ' + str(emit__emit_type(_cdy_t_174, env)) + ' = ' + str(emit__emit_expr(_cdy_val_173, env))))
    elif isinstance(_cdy_t87, lower__SExpr):
        e = _cdy_t87.expr
        return emit__line(level, emit__emit_expr(e, env))
    elif isinstance(_cdy_t87, lower__SReturn):
        _cdy_e_176 = _cdy_t87.val
        return emit__line(level, ('return ' + str(emit__emit_expr(_cdy_e_176, env))))
    elif isinstance(_cdy_t87, lower__SIf):
        test = _cdy_t87.test
        then = _cdy_t87.then
        other = _cdy_t87.other
        return emit__emit_if('if', test, then, other, level, env)
    elif isinstance(_cdy_t87, lower__SFunc):
        _cdy_name_180 = _cdy_t87.name
        params = _cdy_t87.params
        _cdy_body_182 = _cdy_t87.body
        _cdy_t_183 = _cdy_t87.t
        return emit__emit_func(_cdy_name_180, params, _cdy_body_182, _cdy_t_183, level, env)
    else:
        assert isinstance(_cdy_t87, lower__SLocalFunc)
        _cdy_target_184 = _cdy_t87.target
        _cdy_params_185 = _cdy_t87.params
        _cdy_body_186 = _cdy_t87.body
        inner = emit__bind_locals((_cdy_params_185 + emit__bound_locals(_cdy_body_186, ())), env)
        args = emit__comma_join(emit__emit_any_params(_cdy_params_185, inner, ()))
        return (emit__line(level, ('def ' + str(emit__emit_expr(_cdy_target_184, env)) + '(' + str(args) + ') -> _cdy_Any:')) + emit__emit_block(_cdy_body_186, (level + 1), inner))

def emit__emit_if(keyword: str, test: core__Expr, then: tuple[lower__Stmt, ...], other: tuple[lower__Stmt, ...], level: int, env: emit__Env) -> str:
    _cdy_t91 = emit__line(level, (str(keyword) + ' ' + str(emit__emit_expr(test, env)) + ':'))
    _cdy_t92 = emit__emit_block(then, (level + 1), env)
    if (len(other) == 0):
        _cdy_t90 = ''
    elif (len(other) == 1):
        _cdy_t89: object = other[0]
        if isinstance(_cdy_t89, lower__SIf):
            test2 = _cdy_t89.test
            then2 = _cdy_t89.then
            other2 = _cdy_t89.other
            _cdy_t88 = emit__emit_if('elif', test2, then2, other2, level, env)
        else:
            _cdy_t88 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
        _cdy_t90 = _cdy_t88
    else:
        _cdy_t90 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
    return (_cdy_t91 + _cdy_t92 + _cdy_t90)

def emit__emit_any_params(params: tuple[core__Expr, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(params) == 0):
            return acc
        else:
            params, acc = (prelude__rest(params), (acc + cdy_rt.primitives.to_list((str(emit__emit_expr(params[0], env)) + ': _cdy_Any'))))
            continue

def emit__type_params(tvars: tuple[str, ...]) -> str:
    if (len(tvars) == 0):
        return ''
    else:
        return ('[' + str(emit__comma_join(emit__mangle_all(tvars, ()))) + ']')

def emit__mangle_all(names: tuple[str, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), (acc + cdy_rt.primitives.to_list(emit__py_mangle(names[0]))))
            continue

def emit__emit_record_fields(fields: tuple[tuple[str, core__CType], ...], level: int, env: emit__Env, acc: str) -> str:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            f = _tup[0]
            t = _tup[1]
            fields, acc = (prelude__rest(fields), (acc + emit__line(level, (str(emit__py_mangle(f)) + ': ' + str(emit__emit_type(t, env))))))
            continue

def emit__used_tvars(tvars: tuple[str, ...], used: tuple[str, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(tvars) == 0):
            return acc
        else:
            tvars, acc = (prelude__rest(tvars), ((acc + cdy_rt.primitives.to_list(tvars[0])) if cdy_rt.primitives.in_(tvars[0], used) else acc))
            continue

def emit__field_types(fields: tuple[tuple[str, core__CType], ...], acc: tuple[core__CType, ...]) -> tuple[core__CType, ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            _ = _tup[0]
            t = _tup[1]
            fields, acc = (prelude__rest(fields), (acc + cdy_rt.primitives.to_list(t)))
            continue

def emit__variant_tvars(v: core__Variant, tvars: tuple[str, ...]) -> tuple[str, ...]:
    return emit__used_tvars(tvars, emit__type_vars(emit__field_types(v.fields, ()), ()), ())

def emit__emit_variants(variants: tuple[core__Variant, ...], tvars: tuple[str, ...], level: int, env: emit__Env, acc: str) -> str:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            head = ('class ' + str(cdy_rt.primitives.map_get(env.globals_, v.name)) + str(emit__type_params(emit__variant_tvars(v, tvars))) + '(_cdy_NamedTuple):')
            body = (emit__line((level + 1), 'pass') if (len(v.fields) == 0) else emit__emit_record_fields(v.fields, (level + 1), env, ''))
            variants, acc = (prelude__rest(variants), (acc + '\n' + emit__line(level, head) + body))
            continue

def emit__variant_refs(variants: tuple[core__Variant, ...], tvars: tuple[str, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            vt = emit__variant_tvars(v, tvars)
            variants, acc = (prelude__rest(variants), (acc + cdy_rt.primitives.to_list((cdy_rt.primitives.map_get(env.globals_, v.name) + emit__type_params(vt)))))
            continue

def emit__emit_match(subj: str, cases: tuple[lower__Case, ...], default: tuple[tuple[lower__Stmt, ...], ...], assert_last: bool, keyword: str, level: int, env: emit__Env) -> str:
    if (len(cases) == 0):
        if (len(default) == 0):
            return ''
        else:
            return (emit__line(level, 'else:') + emit__emit_block(default[0], (level + 1), env))
    elif (assert_last and (len(cases) == 1)):
        c = cases[0]
        inner = (level if (keyword == 'if') else (level + 1))
        return (('' if (keyword == 'if') else emit__line(level, 'else:')) + emit__line(inner, ('assert isinstance(' + str(subj) + ', ' + str(cdy_rt.primitives.map_get(env.globals_, c.variant)) + ')')) + emit__emit_binds(c.binds, subj, inner, env, '') + emit__emit_stmts(c.body, inner, env, ''))
    else:
        _cdy_c_244 = cases[0]
        test = (str(keyword) + ' isinstance(' + str(subj) + ', ' + str(cdy_rt.primitives.map_get(env.globals_, _cdy_c_244.variant)) + '):')
        binds = emit__emit_binds(_cdy_c_244.binds, subj, (level + 1), env, '')
        body = ((emit__line((level + 1), 'pass') if (binds == '') else '') if (len(_cdy_c_244.body) == 0) else emit__emit_stmts(_cdy_c_244.body, (level + 1), env, ''))
        return (emit__line(level, test) + binds + body + emit__emit_match(subj, prelude__rest(cases), default, assert_last, 'elif', level, env))

def emit__emit_binds(binds: tuple[tuple[str, core__Expr], ...], subj: str, level: int, env: emit__Env, acc: str) -> str:
    while True:
        if (len(binds) == 0):
            return acc
        else:
            _tup = binds[0]
            f = _tup[0]
            loc = _tup[1]
            binds, acc = (prelude__rest(binds), (acc + emit__line(level, (str(emit__emit_expr(loc, env)) + ' = ' + str(subj) + '.' + str(emit__py_mangle(f))))))
            continue

def emit__emit_stmts(stmts: tuple[lower__Stmt, ...], level: int, env: emit__Env, acc: str) -> str:
    while True:
        if (len(stmts) == 0):
            return acc
        else:
            stmts, acc = (prelude__rest(stmts), (acc + emit__emit_stmt(stmts[0], level, env)))
            continue

def emit__emit_block(stmts: tuple[lower__Stmt, ...], level: int, env: emit__Env) -> str:
    if (len(stmts) == 0):
        return emit__line(level, 'pass')
    else:
        return emit__emit_stmts(stmts, level, env, '')

def emit__emit_params(params: tuple[core__Expr, ...], types: tuple[core__CType, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(params) == 0):
            return acc
        else:
            params, types, acc = (prelude__rest(params), prelude__rest(types), (acc + cdy_rt.primitives.to_list((str(emit__emit_expr(params[0], env)) + ': ' + str(emit__emit_type(types[0], env))))))
            continue

def emit__emit_func(name: str, params: tuple[core__Expr, ...], body: tuple[lower__Stmt, ...], t: core__CType, level: int, env: emit__Env) -> str:
    _cdy_t93: object = t
    if isinstance(_cdy_t93, core__TFn):
        types = _cdy_t93.params
        ret = _cdy_t93.ret
        inner = emit__bind_locals((params + emit__bound_locals(body, ())), env)
        tvars = emit__type_vars((types + cdy_rt.primitives.to_list(ret)), ())
        tparams = emit__type_params(tvars)
        args = emit__comma_join(emit__emit_params(params, types, inner, ()))
        return ('\n' + emit__line(level, ('def ' + str(cdy_rt.primitives.map_get(env.globals_, name)) + str(tparams) + '(' + str(args) + ') -> ' + str(emit__emit_type(ret, env)) + ':')) + emit__emit_block(body, (level + 1), inner))
    else:
        return cdy_rt.primitives.fail(('defn ' + str(name) + ': its sig must be a function type'))

def emit__emit_imports(modules: tuple[str, ...], acc: str) -> str:
    while True:
        if (len(modules) == 0):
            return acc
        else:
            modules, acc = (prelude__rest(modules), (acc + ('import ' + str(modules[0]) + '\n')))
            continue

def emit__emit_main(env: emit__Env) -> str:
    name = cdy_rt.primitives.map_get(env.globals_, 'main')
    return ('\n\nif __name__ == "__main__":\n' + str(emit__indent(1)) + 'cdy_rt.primitives.run_main(' + str(name) + ')\n')

class expand__Imports(_cdy_NamedTuple):
    macros: tuple[form__Macro, ...]
    helpers: tuple[tuple[str, tuple[form__Form, ...]], ...]
    seen: _cdy_Mapping[str, bool]

class expand__Expanded(_cdy_NamedTuple):
    forms: tuple[form__Form, ...]
    macros: _cdy_Mapping[str, form__Macro]
    own: tuple[form__Macro, ...]
    helpers: tuple[tuple[str, tuple[form__Form, ...]], ...]

def expand__expand_program(forms: tuple[form__Form, ...], compile_: _cdy_Callable[[tuple[form__Form, ...]], str]) -> tuple[tuple[form__Form, ...], _cdy_Mapping[str, form__Macro]]:
    done = expand__expand_file(forms, False, compile_, ())
    return (done.forms, done.macros)
expand__MACRO_HEADS: tuple[str, ...] = ('defmacro', 'import-macros')

def expand__expand_file(forms: tuple[form__Form, ...], macro_file: bool, compile_: _cdy_Callable[[tuple[form__Form, ...]], str], loading: tuple[str, ...]) -> expand__Expanded:
    imports = expand__import_all((expand__prelude_import(loading) + expand__pick_forms(forms, ('import-macros',), True, ())), compile_, loading, expand__Imports((), (), {}))
    _cdy_imported_8 = expand__macro_map(imports.macros, {})
    defs = expand__expand_defs(expand__pick_forms(forms, ('defmacro',), True, ()), _cdy_imported_8, ())
    rest = expand__pick_forms(forms, expand__MACRO_HEADS, False, ())
    helpers = (expand__expand_all(rest, _cdy_imported_8, ()) if macro_file else ())
    own = (() if (len(defs) == 0) else expand__load_defs(defs, (expand__helper_forms(imports.helpers, ()) + helpers), compile_))
    macros = expand__macro_map(own, _cdy_imported_8)
    return expand__Expanded((helpers if macro_file else expand__expand_all(rest, macros, ())), macros, own, imports.helpers)

def expand__prelude_import(loading: tuple[str, ...]) -> tuple[form__Form, ...]:
    path = include__library_path('prelude_macros.cdy')
    if cdy_rt.primitives.in_(cdy_rt.primitives.path_resolve(path), loading):
        return ()
    else:
        return cdy_rt.primitives.to_list(form__Lst((form__Sym('import-macros', form__NOWHERE), form__Txt(path)), form__NOWHERE))

def expand__pick_forms(forms: tuple[form__Form, ...], heads: tuple[str, ...], keep: bool, acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            items = form__list_items(form)
            picked = ((len(items) > 0) and cdy_rt.primitives.in_(form__sym_name(items[0]), heads))
            forms, acc = (prelude__rest(forms), ((acc + cdy_rt.primitives.to_list(form)) if (picked == keep) else acc))
            continue

def expand__expand_defs(defs: tuple[form__Form, ...], macros: _cdy_Mapping[str, form__Macro], acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(defs) == 0):
            return acc
        else:
            defs, acc = (prelude__rest(defs), (acc + cdy_rt.primitives.to_list(form__Lst(expand__expand_after(form__list_items(defs[0]), 3, macros), form__form_pos(defs[0])))))
            continue

def expand__macro_map(macros: tuple[form__Macro, ...], acc: _cdy_Mapping[str, form__Macro]) -> _cdy_Mapping[str, form__Macro]:
    while True:
        if (len(macros) == 0):
            return acc
        else:
            macro = macros[0]
            name = macro.name
            if cdy_rt.primitives.map_has(acc, name):
                return cdy_rt.primitives.fail((str(form__pos_text(macro.pos)) + 'defmacro: ' + str(name) + ' is already a macro'))
            else:
                macros, acc = (prelude__rest(macros), cdy_rt.primitives.map_set(acc, name, macro))
                continue

def expand__import_all(forms: tuple[form__Form, ...], compile_: _cdy_Callable[[tuple[form__Form, ...]], str], loading: tuple[str, ...], acc: expand__Imports) -> expand__Imports:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (prelude__rest(forms), expand__import_file(forms[0], compile_, loading, acc))
            continue

def expand__import_file(form: form__Form, compile_: _cdy_Callable[[tuple[form__Form, ...]], str], loading: tuple[str, ...], acc: expand__Imports) -> expand__Imports:
    path = expand__macro_path(form)
    key = cdy_rt.primitives.path_resolve(path)
    if cdy_rt.primitives.map_has(acc.seen, key):
        return acc
    elif cdy_rt.primitives.in_(key, loading):
        return cdy_rt.primitives.fail((str(form__pos_text(form__form_pos(form))) + 'import-macros: ' + str(path) + ' imports itself'))
    else:
        done = expand__expand_file(include__read_program(path), True, compile_, (loading + cdy_rt.primitives.to_list(key)))
        return expand__Imports((acc.macros + done.own), expand__add_helpers((done.helpers + cdy_rt.primitives.to_list((key, done.forms))), acc.helpers), cdy_rt.primitives.map_set(acc.seen, key, True))

def expand__macro_path(form: form__Form) -> str:
    _cdy_t94: object = form__list_items(form)[1]
    if isinstance(_cdy_t94, form__Txt):
        path = _cdy_t94.val
        return path
    else:
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'import-macros: expected (import-macros name)'))

def expand__add_helpers(groups: tuple[tuple[str, tuple[form__Form, ...]], ...], acc: tuple[tuple[str, tuple[form__Form, ...]], ...]) -> tuple[tuple[str, tuple[form__Form, ...]], ...]:
    while True:
        if (len(groups) == 0):
            return acc
        else:
            groups, acc = (prelude__rest(groups), (acc if expand__has_helpers(groups[0][0], acc) else (acc + cdy_rt.primitives.to_list(groups[0]))))
            continue

def expand__has_helpers(key: str, groups: tuple[tuple[str, tuple[form__Form, ...]], ...]) -> bool:
    return ((len(groups) > 0) and ((groups[0][0] == key) or expand__has_helpers(key, prelude__rest(groups))))

def expand__helper_forms(groups: tuple[tuple[str, tuple[form__Form, ...]], ...], acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(groups) == 0):
            return acc
        else:
            groups, acc = (prelude__rest(groups), (acc + groups[0][1]))
            continue

def expand__load_defs(defs: tuple[form__Form, ...], helpers: tuple[form__Form, ...], compile_: _cdy_Callable[[tuple[form__Form, ...]], str]) -> tuple[form__Macro, ...]:
    builtins = expand__library_builtins(None)
    checked = expand__unique_names(defs, builtins, {})
    form_forms = expand__form_defs(None)
    python = compile_((form_forms + helpers + expand__macro_program(defs, builtins, ())))
    loaded = cdy_rt.primitives.load_macros(python, form__sym_name, expand__mangled_names(cdy_rt.primitives.map_keys(core__top_names(form_forms, {})), {}))
    return expand__macro_list(defs, loaded, ())

def expand__library_builtins(_: None) -> _cdy_Mapping[str, core__Builtin]:
    decls = include__library_path('special.cdy')
    sigs = include__library_path('system.cdy')
    return core__read_builtins(read__read_source(decls, cdy_rt.primitives.slurp(decls)), read__read_source(sigs, cdy_rt.primitives.slurp(sigs)), cdy_rt.spelling.SPELLINGS)

def expand__mangled_names(names: tuple[str, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), cdy_rt.primitives.map_set(acc, emit__py_mangle(names[0]), True))
            continue

def expand__form_defs(_: None) -> tuple[form__Form, ...]:
    path = include__library_path('form.cdy')
    return read__read_source(path, cdy_rt.primitives.slurp(path))

def expand__macro_program(defs: tuple[form__Form, ...], builtins: _cdy_Mapping[str, core__Builtin], acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(defs) == 0):
            return acc
        else:
            items = expand__defmacro_items(defs[0], builtins)
            pos = form__form_pos(defs[0])
            fname = form__Sym(expand__macro_fn(form__sym_name(items[1])), pos)
            args = form__Sym('args__', pos)
            type_ = form__Lst((form__Sym('Fn', pos), form__Lst(cdy_rt.primitives.to_list(form__Lst((form__Sym('List', pos), form__Sym('Form', pos)), pos)), pos), form__Sym('Form', pos)), pos)
            body = form__Lst((form__Sym('let', pos), form__Lst(expand__param_binds(items[2], args, pos), pos), items[3]), pos)
            defs, acc = (prelude__rest(defs), (acc + cdy_rt.primitives.to_list(form__Lst((form__Sym('sig', pos), fname, type_), pos)) + cdy_rt.primitives.to_list(form__Lst((form__Sym('defn', pos), fname, form__Lst(cdy_rt.primitives.to_list(args), pos), body), pos))))
            continue

def expand__defmacro_items(form: form__Form, builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[form__Form, ...]:
    items = form__list_items(form)
    where = form__pos_text(form__form_pos(form))
    if ((len(items) != 4) or (form__sym_name(items[1]) == '')):
        return cdy_rt.primitives.fail((where + 'defmacro: expected (defmacro name (params) body) or (defmacro name args body)'))
    elif core__is_special(form__sym_name(items[1]), builtins):
        return cdy_rt.primitives.fail((str(where) + 'defmacro: ' + str(form__sym_name(items[1])) + ' is a special form'))
    elif (not expand__params_ok(items[2])):
        return cdy_rt.primitives.fail((where + 'defmacro: a parameter must be a name'))
    else:
        return items

def expand__params_ok(params: form__Form) -> bool:
    _cdy_t95: object = params
    if isinstance(_cdy_t95, form__Sym):
        return True
    elif isinstance(_cdy_t95, form__Lst):
        items = _cdy_t95.items
        return expand__all_names(items)
    else:
        return False

def expand__all_names(forms: tuple[form__Form, ...]) -> bool:
    return ((len(forms) == 0) or ((form__sym_name(forms[0]) != '') and expand__all_names(prelude__rest(forms))))

def expand__param_binds(params: form__Form, args: form__Form, pos: form__Pos) -> tuple[form__Form, ...]:
    if (form__sym_name(params) == ''):
        return expand__arg_binds(form__list_items(params), args, 0, pos, ())
    else:
        return cdy_rt.primitives.to_list(form__Lst((params, args), pos))

def expand__arg_binds(params: tuple[form__Form, ...], args: form__Form, i: int, pos: form__Pos, acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(params) == 0):
            return acc
        else:
            params, i, acc = (prelude__rest(params), (i + 1), (acc + cdy_rt.primitives.to_list(form__Lst((params[0], form__Lst((form__Sym('at', pos), args, form__IntLit(i)), pos)), pos))))
            continue

def expand__macro_fn(name: str) -> str:
    return ('macro__' + name)

def expand__unique_names(defs: tuple[form__Form, ...], builtins: _cdy_Mapping[str, core__Builtin], seen: _cdy_Mapping[str, bool]) -> bool:
    while True:
        if (len(defs) == 0):
            return True
        else:
            name = form__sym_name(expand__defmacro_items(defs[0], builtins)[1])
            if cdy_rt.primitives.map_has(seen, name):
                return cdy_rt.primitives.fail((str(form__pos_text(form__form_pos(defs[0]))) + 'defmacro: ' + str(name) + ' is defined twice'))
            else:
                defs, seen = (prelude__rest(defs), cdy_rt.primitives.map_set(seen, name, True))
                continue

def expand__macro_list(defs: tuple[form__Form, ...], loaded: _cdy_Mapping[str, _cdy_Any], acc: tuple[form__Macro, ...]) -> tuple[form__Macro, ...]:
    while True:
        if (len(defs) == 0):
            return acc
        else:
            items = form__list_items(defs[0])
            name = form__sym_name(items[1])
            params = items[2]
            arity = (len(form__list_items(params)) if (form__sym_name(params) == '') else -1)
            run = cdy_rt.primitives.map_get(loaded, emit__py_mangle(expand__macro_fn(name)))
            defs, acc = (prelude__rest(defs), (acc + cdy_rt.primitives.to_list(form__Macro(name, arity, run, form__form_pos(defs[0])))))
            continue

def expand__expand_all(forms: tuple[form__Form, ...], macros: _cdy_Mapping[str, form__Macro], acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (prelude__rest(forms), (acc + cdy_rt.primitives.to_list(expand__expand_form(forms[0], macros))))
            continue

def expand__expand_form(form: form__Form, macros: _cdy_Mapping[str, form__Macro]) -> form__Form:
    while True:
        _cdy_t96: object = form
        if isinstance(_cdy_t96, form__Lst):
            items = _cdy_t96.items
            pos = _cdy_t96.pos
            head = ('' if (len(items) == 0) else form__sym_name(items[0]))
            if cdy_rt.primitives.map_has(macros, head):
                form = expand__expand_call(cdy_rt.primitives.map_get(macros, head), prelude__rest(items), pos)
                continue
            elif cdy_rt.primitives.in_(head, ('sig', 'deft', 'import', 'import-macros', 'quo', 'quasi')):
                return form
            elif (head == 'defn'):
                return form__Lst(expand__expand_after(items, 3, macros), pos)
            elif (head == 'fn'):
                return form__Lst(expand__expand_after(items, 2, macros), pos)
            elif cdy_rt.primitives.in_(head, ('let', 'match')):
                return form__Lst(expand__expand_clauses(head, items, macros), pos)
            else:
                return form__Lst(expand__expand_all(items, macros, ()), pos)
        else:
            return form

def expand__expand_after(items: tuple[form__Form, ...], n: int, macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    if (len(items) < n):
        return items
    else:
        return (items[0:n] + expand__expand_all(items[n:len(items)], macros, ()))

def expand__expand_clauses(head: str, items: tuple[form__Form, ...], macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    if ((head == 'let') and (len(items) == 3)):
        _cdy_t97: object = items[1]
        if isinstance(_cdy_t97, form__Lst):
            binds = _cdy_t97.items
            p = _cdy_t97.pos
            return (items[0], form__Lst(expand__each_clause(binds, 1, macros, ()), p), expand__expand_form(items[2], macros))
        else:
            return expand__expand_all(items, macros, ())
    elif ((head == 'match') and (len(items) > 1)):
        return ((items[0], expand__expand_form(items[1], macros)) + expand__each_clause(items[2:len(items)], 1, macros, ()))
    else:
        return expand__expand_all(items, macros, ())

def expand__each_clause(clauses: tuple[form__Form, ...], n: int, macros: _cdy_Mapping[str, form__Macro], acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(clauses) == 0):
            return acc
        else:
            clauses, acc = (prelude__rest(clauses), (acc + cdy_rt.primitives.to_list(expand__expand_clause(clauses[0], n, macros))))
            continue

def expand__expand_clause(clause: form__Form, n: int, macros: _cdy_Mapping[str, form__Macro]) -> form__Form:
    _cdy_t98: object = clause
    if isinstance(_cdy_t98, form__Lst):
        items = _cdy_t98.items
        p = _cdy_t98.pos
        return form__Lst(expand__expand_after(items, n, macros), p)
    else:
        return expand__expand_form(clause, macros)

def expand__expand_call(macro: form__Macro, args: tuple[form__Form, ...], pos: form__Pos) -> form__Form:
    arity = macro.arity
    where = (str(form__pos_text(pos)) + str(macro.name) + ': ')
    if ((arity >= 0) and (arity != len(args))):
        return cdy_rt.primitives.fail((str(where) + 'expected ' + str(arity) + ' argument(s), got ' + str(len(args))))
    else:
        return expand__stamp(cdy_rt.primitives.call_macro(macro.run, args, where), pos)

def expand__stamp(form: form__Form, pos: form__Pos) -> form__Form:
    _cdy_t99: object = form
    if isinstance(_cdy_t99, form__Sym):
        name = _cdy_t99.name
        p = _cdy_t99.pos
        if (p.line == 0):
            return form__Sym(name, pos)
        else:
            return form
    elif isinstance(_cdy_t99, form__Lst):
        items = _cdy_t99.items
        _cdy_p_136 = _cdy_t99.pos
        return form__Lst(expand__stamp_all(items, pos, ()), (pos if (_cdy_p_136.line == 0) else _cdy_p_136))
    else:
        return form

def expand__stamp_all(forms: tuple[form__Form, ...], pos: form__Pos, acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            forms, acc = (prelude__rest(forms), (acc + cdy_rt.primitives.to_list(expand__stamp(forms[0], pos))))
            continue

class Ready(_cdy_NamedTuple):
    module: include__Module
    forms: tuple[form__Form, ...]
    macros: _cdy_Mapping[str, form__Macro]
    exports: core__Exports

def translate_modules(modules: tuple[include__Module, ...], parse: _cdy_Callable[[str], tuple[form__Form, ...]]) -> str:
    ready = expand_modules(modules, (len(modules) - 1), ())
    by_key = exports_by_key(ready, {})
    elsewhere = core__elsewhere_names(exports_of(ready, ()), {})
    builtins = expand__library_builtins(None)
    return python_of(analyse_modules(ready, by_key, elsewhere, builtins, parse, ()))

def expand_modules(modules: tuple[include__Module, ...], top: int, acc: tuple[Ready, ...]) -> tuple[Ready, ...]:
    while True:
        if (len(acc) == len(modules)):
            return acc
        else:
            m = modules[len(acc)]
            _tup = expand__expand_program(m.forms, compile_macros)
            forms = _tup[0]
            macros = _tup[1]
            prefix = ('' if (len(acc) == top) else (m.stem + '__'))
            acc = (acc + cdy_rt.primitives.to_list(Ready(m, forms, macros, core__module_exports(forms, m.stem, prefix))))
            continue

def exports_by_key(ready: tuple[Ready, ...], acc: _cdy_Mapping[str, core__Exports]) -> _cdy_Mapping[str, core__Exports]:
    while True:
        if (len(ready) == 0):
            return acc
        else:
            r = ready[0]
            ready, acc = (prelude__rest(ready), cdy_rt.primitives.map_set(acc, r.module.key, r.exports))
            continue

def exports_of(ready: tuple[Ready, ...], acc: tuple[core__Exports, ...]) -> tuple[core__Exports, ...]:
    while True:
        if (len(ready) == 0):
            return acc
        else:
            ready, acc = (prelude__rest(ready), (acc + cdy_rt.primitives.to_list(ready[0].exports)))
            continue

def analyse_modules(ready: tuple[Ready, ...], by_key: _cdy_Mapping[str, core__Exports], elsewhere: _cdy_Mapping[str, str], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str], tuple[form__Form, ...]], acc: tuple[core__Top, ...]) -> tuple[core__Top, ...]:
    if (len(ready) == 0):
        return acc
    else:
        r = ready[0]
        macros = r.macros
        tops = core__analyse_module(r.forms, r.exports, imported(r.module.imports, by_key, ()), elsewhere, builtins, (lambda text: expand__expand_all(parse(text), macros, ())), macros, False)
        return analyse_modules(prelude__rest(ready), by_key, elsewhere, builtins, parse, (acc + tops))

def imported(imps: tuple[include__Imp, ...], by_key: _cdy_Mapping[str, core__Exports], acc: tuple[tuple[core__Exports, form__Pos], ...]) -> tuple[tuple[core__Exports, form__Pos], ...]:
    while True:
        if (len(imps) == 0):
            return acc
        else:
            imp = imps[0]
            imps, acc = (prelude__rest(imps), (acc + cdy_rt.primitives.to_list((cdy_rt.primitives.map_get(by_key, imp.key), imp.pos))))
            continue

def compile_macros(forms: tuple[form__Form, ...]) -> str:
    return translate_expanded(forms, read__read_forms, {}, True)

def translate_expanded(forms: tuple[form__Form, ...], parse: _cdy_Callable[[str], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> str:
    return python_of(core__analyse_program(forms, expand__library_builtins(None), parse, macros, quoting))

def python_of(tops: tuple[core__Top, ...]) -> str:
    stmts = lower__lower_program(tops, 0, ())
    globals_ = emit__global_names(tops, emit__Env({}, {}, {}, emit__generic_variants(tops, {}), cdy_rt.spelling.SPELLINGS))
    env = emit__bind_locals(emit__bound_locals(stmts, ()), globals_)
    return (emit__HEADER + emit__emit_imports(emit__PY_IMPORTS, '') + '\n' + emit__emit_stmts(stmts, 0, env, '') + (emit__emit_main(env) if core__has_main(tops) else ''))

def translate_text(text: str) -> str:
    return translate_modules(include__text_modules(text), read__read_forms)

def translate_file(path: str) -> str:
    return translate_modules(include__read_modules(path), read__read_forms)
USAGE: str = 'usage: cdy_translator.py FILE.cdy [OUT.py]'

def main(args: tuple[str, ...]) -> int:
    if ((len(args) == 0) or (len(args) > 2)):
        cdy_rt.primitives.put_err(USAGE)
        return 2
    else:
        src = args[0]
        out = (args[1] if (len(args) == 2) else cdy_rt.primitives.path_join('output', (cdy_rt.primitives.path_stem(src) + '.py')))
        python = translate_file(src)
        cdy_rt.primitives.make_dirs(cdy_rt.primitives.path_dir(out))
        cdy_rt.primitives.spit(out, python)
        cdy_rt.primitives.put_err(('candy: ' + str(src) + ' -> ' + str(out)))
        return 0


if __name__ == "__main__":
    cdy_rt.primitives.run_main(main)
