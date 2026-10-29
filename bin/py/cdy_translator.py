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
    pos: form__Pos

class core__If(_cdy_NamedTuple):
    test: core__Expr
    then: core__Expr
    other: core__Expr
    pos: form__Pos

class core__Do(_cdy_NamedTuple):
    body: tuple[core__Expr, ...]

class core__Lambda(_cdy_NamedTuple):
    params: tuple[core__Expr, ...]
    body: core__Expr
    pos: form__Pos

class core__Tuple(_cdy_NamedTuple):
    items: tuple[core__Expr, ...]
    pos: form__Pos

class core__Fmt(_cdy_NamedTuple):
    parts: tuple[core__FPart, ...]
    pos: form__Pos

class core__Field(_cdy_NamedTuple):
    obj: core__Expr
    field: str
    pos: form__Pos

class core__Assoc(_cdy_NamedTuple):
    obj: core__Expr
    fields: tuple[tuple[str, core__Expr], ...]
    pos: form__Pos

class core__MatchE(_cdy_NamedTuple):
    subject: core__Expr
    clauses: tuple[core__Clause, ...]
    default: tuple[core__Expr, ...]
    pos: form__Pos

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
    types: _cdy_Mapping[str, int]

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
        return core__Call(core__Global(core__global_name(name, scope.names)), (), scope.here)
    elif (cdy_rt.primitives.map_has(scope.top, name) and cdy_rt.primitives.map_get(scope.top, name)):
        return core__Global(core__global_name(name, scope.names))
    elif core__is_special(name, scope.builtins):
        return cdy_rt.primitives.fail(core__located(scope, (str(name) + ' is a special form, not a value')))
    elif (cdy_rt.primitives.map_has(scope.builtins, name) and (not core__is_builtin_type(name, scope.builtins))):
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
            return (core__Call(callee, args, scope.here), n2)

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
        return (core__If(parts[0], parts[1], core__NIL, scope.here), n1)
    elif (len(parts) == 3):
        return (core__If(parts[0], parts[1], parts[2], scope.here), n1)
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
        return (core__nest(pairs, body, scope.here), n2)

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
            item = core__Call(core__Prim('at'), (tmp, core__Lit(form__IntLit(i))), scope.here)
            if (name == ''):
                return cdy_rt.primitives.fail(core__located(scope, 'let name must be a name'))
            else:
                names, i, scope, n, acc = (prelude__rest(names), (i + 1), core__bind_local(scope, name, loc), (n + 1), (acc + cdy_rt.primitives.to_list((loc, item))))
                continue

def core__nest(pairs: tuple[tuple[core__Expr, core__Expr], ...], body: core__Expr, pos: form__Pos) -> core__Expr:
    if (len(pairs) == 0):
        return body
    else:
        _tup = pairs[0]
        loc = _tup[0]
        init = _tup[1]
        return core__Call(core__Lambda(cdy_rt.primitives.to_list(loc), core__nest(prelude__rest(pairs), body, pos), pos), cdy_rt.primitives.to_list(init), pos)

def core__an_fn(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) != 2):
        return cdy_rt.primitives.fail(core__located(scope, 'fn: expected (fn (args+) body), with exactly one body form'))
    else:
        _tup = core__bind_params(form__list_items(args[0]), scope, n, ())
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_124 = core__analyse_expr(args[1], inner, n1)
        body = _cdy__tup_124[0]
        n2 = _cdy__tup_124[1]
        if (len(params) == 0):
            return cdy_rt.primitives.fail(core__located(scope, 'fn arguments: at least one is needed'))
        else:
            return (core__Lambda(params, body, scope.here), n2)

def core__an_tup(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'tup: needs at least one item'))
    else:
        _tup = core__analyse_all(args, scope, n, ())
        items = _tup[0]
        n1 = _tup[1]
        return (core__Tuple(items, scope.here), n1)

def core__an_get(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if ((len(args) != 2) or (form__sym_name(args[1]) == '')):
        return cdy_rt.primitives.fail(core__located(scope, 'get: expected (get obj field)'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        return (core__Field(obj, form__sym_name(args[1]), scope.here), n1)

def core__an_assoc(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) < 3):
        return cdy_rt.primitives.fail(core__located(scope, 'assoc: expected (assoc obj field value ...)'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        _cdy__tup_145 = core__assoc_fields(prelude__rest(args), scope, n1, ())
        fields = _cdy__tup_145[0]
        n2 = _cdy__tup_145[1]
        return (core__Assoc(obj, fields, scope.here), n2)

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
            return (core__Fmt(parts, scope.here), n1)
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
    _cdy__tup_189 = core__match_clauses(prelude__rest(args), scope, n1, core__MatchE(subject, (), (), scope.here), '')
    m = _cdy__tup_189[0]
    n2 = _cdy__tup_189[1]
    sum_ = (core__match_sum(core__match_clause_list(m), scope) if (len(core__match_clause_list(m)) > 0) else '')
    return (core__global_clauses(core__check_exhaustive(m, sum_, scope), scope.names), n2)

def core__global_clauses(m: core__Expr, names: _cdy_Mapping[str, str]) -> core__Expr:
    _cdy_t14: object = m
    if isinstance(_cdy_t14, core__MatchE):
        subject = _cdy_t14.subject
        clauses = _cdy_t14.clauses
        default = _cdy_t14.default
        pos = _cdy_t14.pos
        return core__MatchE(subject, core__rename_clauses(clauses, names, ()), default, pos)
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
        _cdy__tup_213 = core__tup_binds(names, tmp, 0, scope, (n1 + 1), ())
        pairs = _cdy__tup_213[0]
        inner = _cdy__tup_213[1]
        n2 = _cdy__tup_213[2]
        _cdy__tup_217 = core__analyse_expr(items[1], inner, n2)
        body = _cdy__tup_217[0]
        n3 = _cdy__tup_217[1]
        return (core__nest((cdy_rt.primitives.to_list((tmp, subject)) + pairs), body, scope.here), n3)

def core__tup_binds(names: tuple[form__Form, ...], tmp: core__Expr, i: int, scope: core__Scope, n: int, acc: tuple[tuple[core__Expr, core__Expr], ...]) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = form__sym_name(names[0])
            loc = core__Local(name, n)
            item = core__Call(core__Prim('at'), (tmp, core__Lit(form__IntLit(i))), scope.here)
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
                _cdy__tup_260 = core__pattern_binds(core__variant_fields(variant, scope), prelude__rest(pattern), scope, n, ())
                binds = _cdy__tup_260[0]
                inner = _cdy__tup_260[1]
                _cdy_n1_263 = _cdy__tup_260[2]
                _cdy__tup_264 = core__analyse_expr(items[1], inner, _cdy_n1_263)
                body = _cdy__tup_264[0]
                n2 = _cdy__tup_264[1]
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
        pos = _cdy_t18.pos
        return core__MatchE(subject, (clauses + cdy_rt.primitives.to_list(clause)), default, pos)
    else:
        return m

def core__set_default(m: core__Expr, e: core__Expr) -> core__Expr:
    _cdy_t19: object = m
    if isinstance(_cdy_t19, core__MatchE):
        subject = _cdy_t19.subject
        clauses = _cdy_t19.clauses
        pos = _cdy_t19.pos
        return core__MatchE(subject, clauses, cdy_rt.primitives.to_list(e), pos)
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
        return core__Call(core__Global('Sym'), (core__Lit(form__Txt(name)), core__Global('NOWHERE')), form__NOWHERE)
    elif isinstance(_cdy_t21, form__Lst):
        items = _cdy_t21.items
        return core__Call(core__Global('Lst'), (core__form_list(core__quoted_all(items, ())), core__Global('NOWHERE')), form__NOWHERE)
    else:
        return core__Call(core__Global(core__literal_variant(form)), cdy_rt.primitives.to_list(core__Lit(form)), form__NOWHERE)

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
        return core__Tuple(items, form__NOWHERE)

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
    return (core__Call(core__Global('Lst'), (core__join_parts(parts), core__Global('NOWHERE')), form__NOWHERE), n1)

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
                _cdy__tup_340 = core__quasi_form(item, scope, n)
                _cdy_e_341 = _cdy__tup_340[0]
                _cdy_n1_342 = _cdy__tup_340[1]
                items, n, run = (prelude__rest(items), _cdy_n1_342, (run + cdy_rt.primitives.to_list(_cdy_e_341)))
                continue

def core__close_run(run: tuple[core__Expr, ...], parts: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    if (len(run) == 0):
        return parts
    else:
        return (parts + cdy_rt.primitives.to_list(core__Tuple(run, form__NOWHERE)))

def core__join_parts(parts: tuple[core__Expr, ...]) -> core__Expr:
    if (len(parts) == 0):
        return core__Prim('empty-list')
    elif (len(parts) == 1):
        return parts[0]
    else:
        return core__Call(core__Prim('+'), parts, form__NOWHERE)

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

class core__BType(_cdy_NamedTuple):
    arity: int
type core__Builtin = core__Special | core__Op | core__Typed | core__BType

def core__is_builtin_type(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t29 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t29:
        _cdy_t28: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t28, core__BType):
            _cdy_t27 = True
        else:
            _cdy_t27 = False
        _cdy_t29 = _cdy_t27
    return _cdy_t29

def core__is_special(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t32 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t32:
        _cdy_t31: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t31, core__Special):
            _cdy_t30 = True
        else:
            _cdy_t30 = False
        _cdy_t32 = _cdy_t30
    return _cdy_t32

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
core__TYPE_KINDS: tuple[str, ...] = ('type',)

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
            head = (form__sym_name(items[0]) if (len(items) > 0) else '')
            name = (form__sym_name(items[1]) if ((len(items) == 3) and (head == 'sig')) else '')
            where = form__pos_text(form__form_pos(form))
            if (head == 'deft'):
                forms, acc = (prelude__rest(forms), core__read_type(form, items, where, spellings, acc))
                continue
            elif (name == ''):
                return cdy_rt.primitives.fail((where + 'system.cdy: expected (sig name Type) or (deft Name)'))
            elif cdy_rt.primitives.map_has(acc, name):
                return cdy_rt.primitives.fail((str(where) + 'system.cdy: ' + str(name) + ' is already declared'))
            elif (not cdy_rt.primitives.in_(core__spelling_kind(spellings, name), core__TYPED_KINDS)):
                return cdy_rt.primitives.fail((str(where) + 'system.cdy: ' + str(name) + ' has no Python mapping in spelling.py'))
            else:
                forms, acc = (prelude__rest(forms), cdy_rt.primitives.map_set(acc, name, core__Typed(core__analyse_type(items[2]))))
                continue

def core__read_type(form: form__Form, items: tuple[form__Form, ...], where: str, spellings: _cdy_Mapping[str, tuple[str, str]], acc: _cdy_Mapping[str, core__Builtin]) -> _cdy_Mapping[str, core__Builtin]:
    header = (items[1] if (len(items) == 2) else form)
    _cdy_t34: object = header
    if isinstance(_cdy_t34, form__Sym):
        _cdy_t33 = cdy_rt.primitives.to_list(header)
    elif isinstance(_cdy_t34, form__Lst):
        xs = _cdy_t34.items
        _cdy_t33 = xs
    else:
        _cdy_t33 = ()
    parts = _cdy_t33
    name = (form__sym_name(parts[0]) if (len(parts) > 0) else '')
    tvars = (prelude__rest(parts) if (len(parts) > 0) else ())
    if ((name == '') or core__is_lower(name) or (not core__all_lower(tvars))):
        return cdy_rt.primitives.fail((where + 'system.cdy: expected (deft Name) or (deft (Name a ...))'))
    elif cdy_rt.primitives.map_has(acc, name):
        return cdy_rt.primitives.fail((str(where) + 'system.cdy: ' + str(name) + ' is already declared'))
    elif (not cdy_rt.primitives.in_(core__spelling_kind(spellings, name), core__TYPE_KINDS)):
        return cdy_rt.primitives.fail((str(where) + 'system.cdy: ' + str(name) + ' has no Python type in spelling.py'))
    else:
        return cdy_rt.primitives.map_set(acc, name, core__BType(len(tvars)))

def core__all_lower(forms: tuple[form__Form, ...]) -> bool:
    while True:
        if (len(forms) == 0):
            return True
        elif (not core__is_lower(form__sym_name(forms[0]))):
            return False
        else:
            forms = prelude__rest(forms)
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
    types: _cdy_Mapping[str, int]

def core__module_exports(forms: tuple[form__Form, ...], stem: str, prefix: str) -> core__Exports:
    top = core__top_names(forms, {})
    found = core__find_variants(forms, core__blank_scope(top))
    return core__Exports(stem, top, found.variants, found.sums, core__prefixed(cdy_rt.primitives.map_keys(top), prefix, {}), core__type_arities(forms, {}))

def core__type_arities(forms: tuple[form__Form, ...], acc: _cdy_Mapping[str, int]) -> _cdy_Mapping[str, int]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = form__list_items(forms[0])
            head = (form__sym_name(items[0]) if (len(items) > 1) else '')
            _cdy_t39 = prelude__rest(forms)
            if ((head == 'deft') and (core__deft_name(items[1]) != '')):
                _cdy_t37 = core__deft_name(items[1])
                _cdy_t36: object = items[1]
                if isinstance(_cdy_t36, form__Lst):
                    xs = _cdy_t36.items
                    _cdy_t35 = (len(xs) - 1)
                else:
                    _cdy_t35 = 0
                _cdy_t38 = cdy_rt.primitives.map_set(acc, _cdy_t37, _cdy_t35)
            else:
                _cdy_t38 = acc
            forms, acc = (_cdy_t39, _cdy_t38)
            continue

def core__prefixed(names: tuple[str, ...], prefix: str, acc: _cdy_Mapping[str, str]) -> _cdy_Mapping[str, str]:
    while True:
        if (len(names) == 0):
            return acc
        else:
            names, acc = (prelude__rest(names), cdy_rt.primitives.map_set(acc, names[0], (prefix + names[0])))
            continue

def core__blank_scope(top: _cdy_Mapping[str, bool]) -> core__Scope:
    return core__Scope({}, top, (lambda text: ()), {}, {}, form__NOWHERE, {}, False, {}, {}, {}, {})

def core__analyse_program(forms: tuple[form__Form, ...], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    return core__analyse_module(forms, core__module_exports(forms, '', ''), (), {}, builtins, parse, macros, quoting)

def core__analyse_module(forms: tuple[form__Form, ...], own: core__Exports, imports: tuple[tuple[core__Exports, form__Pos], ...], elsewhere: _cdy_Mapping[str, str], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    seen = core__with_own(core__with_imports(imports, core__Seen(core__Exports('', {}, {}, {}, {}, {}), {})), own)
    vis = seen.vis
    scope = core__Scope({}, vis.top, parse, vis.variants, vis.sums, form__NOWHERE, macros, quoting, vis.names, elsewhere, builtins, vis.types)
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
            return seen._replace(vis=seen.vis._replace(variants=core__put_all(ex.variants, cdy_rt.primitives.map_keys(ex.variants), seen.vis.variants), sums=core__put_all(ex.sums, cdy_rt.primitives.map_keys(ex.sums), seen.vis.sums), types=core__put_all(ex.types, cdy_rt.primitives.map_keys(ex.types), seen.vis.types)))
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
    return seen._replace(vis=vis._replace(top=core__put_all(own.top, cdy_rt.primitives.map_keys(own.top), vis.top), variants=core__put_all(own.variants, cdy_rt.primitives.map_keys(own.variants), vis.variants), sums=core__put_all(own.sums, cdy_rt.primitives.map_keys(own.sums), vis.sums), names=core__put_all(own.names, cdy_rt.primitives.map_keys(own.names), vis.names), types=core__put_all(own.types, cdy_rt.primitives.map_keys(own.types), vis.types)))

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
    _cdy_t40: object = top
    if isinstance(_cdy_t40, core__TDeft):
        name = _cdy_t40.name
        tvars = _cdy_t40.tvars
        fields = _cdy_t40.fields
        return core__TDeft(core__global_name(name, names), tvars, core__rename_fields(fields, names, ()))
    elif isinstance(_cdy_t40, core__TDeftSum):
        _cdy_name_493 = _cdy_t40.name
        _cdy_tvars_494 = _cdy_t40.tvars
        variants = _cdy_t40.variants
        return core__TDeftSum(core__global_name(_cdy_name_493, names), _cdy_tvars_494, core__rename_variants(variants, names, ()))
    elif isinstance(_cdy_t40, core__TDef):
        _cdy_name_496 = _cdy_t40.name
        init = _cdy_t40.init
        t = _cdy_t40.t
        return core__TDef(core__global_name(_cdy_name_496, names), init, core__rename_type(t, names))
    elif isinstance(_cdy_t40, core__TDefn):
        _cdy_name_499 = _cdy_t40.name
        params = _cdy_t40.params
        body = _cdy_t40.body
        _cdy_t_502 = _cdy_t40.t
        return core__TDefn(core__global_name(_cdy_name_499, names), params, body, core__rename_type(_cdy_t_502, names))
    else:
        assert isinstance(_cdy_t40, core__TExpr)
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
    _cdy_t41: object = t
    if isinstance(_cdy_t41, core__TCon):
        name = _cdy_t41.name
        args = _cdy_t41.args
        return core__TCon(core__global_name(name, names), core__rename_types(args, names, ()))
    elif isinstance(_cdy_t41, core__TVar):
        return t
    else:
        assert isinstance(_cdy_t41, core__TFn)
        params = _cdy_t41.params
        ret = _cdy_t41.ret
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
        t = core__analyse_type(items[2])
        checked = core__check_type(t, scope)
        return prog._replace(sigs=cdy_rt.primitives.map_set(prog.sigs, name, t))

def core__check_type(t: core__CType, scope: core__Scope) -> bool:
    _cdy_t42: object = t
    if isinstance(_cdy_t42, core__TVar):
        return True
    elif isinstance(_cdy_t42, core__TFn):
        params = _cdy_t42.params
        ret = _cdy_t42.ret
        return (core__check_types(params, scope) and core__check_type(ret, scope))
    else:
        assert isinstance(_cdy_t42, core__TCon)
        name = _cdy_t42.name
        args = _cdy_t42.args
        builtins = scope.builtins
        if (name == 'Tup'):
            _cdy_t45 = len(args)
        elif cdy_rt.primitives.map_has(scope.types, name):
            _cdy_t45 = cdy_rt.primitives.map_get(scope.types, name)
        elif core__is_builtin_type(name, builtins):
            _cdy_t44: object = cdy_rt.primitives.map_get(builtins, name)
            if isinstance(_cdy_t44, core__BType):
                n = _cdy_t44.arity
                _cdy_t43 = n
            else:
                _cdy_t43 = 0
            _cdy_t45 = _cdy_t43
        elif cdy_rt.primitives.map_has(scope.elsewhere, name):
            stem = cdy_rt.primitives.map_get(scope.elsewhere, name)
            _cdy_t45 = cdy_rt.primitives.fail(core__located(scope, (str(name) + ' is not defined here; ' + str(stem) + " defines it, but this file doesn't import " + str(stem))))
        else:
            _cdy_t45 = cdy_rt.primitives.fail(core__located(scope, ('unknown type ' + str(name))))
        arity = _cdy_t45
        if (arity != len(args)):
            return cdy_rt.primitives.fail(core__located(scope, (str(name) + ' takes ' + str(arity) + ' type argument(s), got ' + str(len(args)))))
        else:
            return core__check_types(args, scope)

def core__check_types(ts: tuple[core__CType, ...], scope: core__Scope) -> bool:
    while True:
        if (len(ts) == 0):
            return True
        elif core__check_type(ts[0], scope):
            ts = prelude__rest(ts)
            continue
        else:
            return False

def core__top_deft(items: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    name = (core__deft_name(items[1]) if (len(items) > 1) else '')
    tvar_forms = (prelude__rest(form__list_items(items[1])) if (len(items) > 1) else ())
    tvars = core__syms(tvar_forms, ())
    dup = core__repeated(tvar_forms, (), 0)
    body = items[2:len(items)]
    field_forms = (form__list_items(items[2]) if (len(items) == 3) else ())
    if (name == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+)) or (deft Name variant+)'))
    elif (dup >= 0):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(tvar_forms[dup])) + ('deft ' + str(name) + ': type variables must be different (' + str(tvars[dup]) + ')')))
    elif core__is_sum_body(body):
        variants = core__deft_variants(name, body, ())
        checked = core__check_variants(variants, scope)
        return core__add_top(prog, core__TDeftSum(name, tvars, variants), prog.n)
    elif (len(field_forms) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+))'))
    else:
        fields = core__deft_fields(('deft ' + str(name)), field_forms, ())
        _cdy_checked_573 = core__check_fields(fields, scope)
        return core__add_top(prog, core__TDeft(name, tvars, fields), prog.n)

def core__check_fields(fields: tuple[tuple[str, core__CType], ...], scope: core__Scope) -> bool:
    while True:
        if (len(fields) == 0):
            return True
        elif core__check_type(fields[0][1], scope):
            fields = prelude__rest(fields)
            continue
        else:
            return False

def core__check_variants(variants: tuple[core__Variant, ...], scope: core__Scope) -> bool:
    while True:
        if (len(variants) == 0):
            return True
        elif core__check_fields(variants[0].fields, scope):
            variants = prelude__rest(variants)
            continue
        else:
            return False

def core__deft_variants(sum_: str, body: tuple[form__Form, ...], acc: tuple[core__Variant, ...]) -> tuple[core__Variant, ...]:
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
                body, acc = (prelude__rest(body), (acc + cdy_rt.primitives.to_list(core__Variant(name, core__deft_fields(('deft ' + str(sum_) + ', variant ' + str(name)), form__list_items(v_items[1]), ())))))
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

def core__deft_fields(owner: str, forms: tuple[form__Form, ...], acc: tuple[tuple[str, core__CType], ...]) -> tuple[tuple[str, core__CType], ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            items = form__list_items(forms[0])
            if ((len(items) != 2) or (form__sym_name(items[0]) == '')):
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(forms[0])) + 'deft: field must be (name Type)'))
            elif core__has_field(form__sym_name(items[0]), acc):
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(forms[0])) + (str(owner) + ': field names must be different (' + str(form__sym_name(items[0])) + ')')))
            else:
                forms, acc = (prelude__rest(forms), (acc + cdy_rt.primitives.to_list((form__sym_name(items[0]), core__analyse_type(items[1])))))
                continue

def core__has_field(name: str, fields: tuple[tuple[str, core__CType], ...]) -> bool:
    while True:
        if (len(fields) == 0):
            return False
        elif (fields[0][0] == name):
            return True
        else:
            fields = prelude__rest(fields)
            continue

def core__repeated(forms: tuple[form__Form, ...], seen: tuple[str, ...], i: int) -> int:
    while True:
        if (i == len(forms)):
            return -1
        elif cdy_rt.primitives.list_contains(form__sym_name(forms[i]), seen):
            return i
        else:
            seen, i = ((seen + cdy_rt.primitives.to_list(form__sym_name(forms[i]))), (i + 1))
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
        _cdy__tup_616 = core__analyse_expr(items[3], inner, n1)
        body = _cdy__tup_616[0]
        n2 = _cdy__tup_616[1]
        if (len(params) == 0):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + str(name) + ': at least one argument is needed')))
        elif (len(params) != core__fn_arity(t)):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + str(name) + ': its sig must be a function type with one type per argument')))
        else:
            return core__mark_defined(core__add_top(prog, core__TDefn(name, params, body, t), n2), name)

def core__fn_arity(t: core__CType) -> int:
    _cdy_t46: object = t
    if isinstance(_cdy_t46, core__TFn):
        params = _cdy_t46.params
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
    _cdy_t47: object = top
    if isinstance(_cdy_t47, core__TDefn):
        name = _cdy_t47.name
        t = _cdy_t47.t
        if (name != 'main'):
            return False
        elif (t == core__MAIN_TYPE):
            return True
        else:
            return cdy_rt.primitives.fail('main must be typed (Fn ((List String)) Int)')
    elif isinstance(_cdy_t47, core__TDef):
        _cdy_name_631 = _cdy_t47.name
        if (_cdy_name_631 == 'main'):
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
    _cdy_t48: object = e
    if isinstance(_cdy_t48, core__Lit):
        return True
    elif isinstance(_cdy_t48, core__Local):
        return True
    elif isinstance(_cdy_t48, core__Global):
        return True
    elif isinstance(_cdy_t48, core__Prim):
        return True
    elif isinstance(_cdy_t48, core__Temp):
        return True
    else:
        return False

def lower__is_applied(e: core__Expr) -> bool:
    _cdy_t49: object = e
    if isinstance(_cdy_t49, core__Call):
        callee = _cdy_t49.callee
        args = _cdy_t49.args
        _cdy_t50: object = callee
        if isinstance(_cdy_t50, core__Lambda):
            params = _cdy_t50.params
            return (len(params) == len(args))
        else:
            return False
    else:
        return False

def lower__bind_applied(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], core__Expr, int]:
    _cdy_t51: object = e
    if isinstance(_cdy_t51, core__Call):
        callee = _cdy_t51.callee
        args = _cdy_t51.args
        _cdy_t52: object = callee
        if isinstance(_cdy_t52, core__Lambda):
            params = _cdy_t52.params
            body = _cdy_t52.body
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
        _cdy_t53: object = e
        if isinstance(_cdy_t53, core__Call):
            callee = _cdy_t53.callee
            args = _cdy_t53.args
            pos = _cdy_t53.pos
            return lower__value_call(callee, args, pos, n)
        elif isinstance(_cdy_t53, core__If):
            test = _cdy_t53.test
            then = _cdy_t53.then
            other = _cdy_t53.other
            _cdy_pos_31 = _cdy_t53.pos
            return lower__value_if(test, then, other, _cdy_pos_31, n)
        elif isinstance(_cdy_t53, core__Do):
            _cdy_body_32 = _cdy_t53.body
            return lower__value_do(_cdy_body_32, n)
        elif isinstance(_cdy_t53, core__Lambda):
            params = _cdy_t53.params
            _cdy_body_34 = _cdy_t53.body
            _cdy_pos_35 = _cdy_t53.pos
            return lower__value_fn(params, _cdy_body_34, _cdy_pos_35, n)
        elif isinstance(_cdy_t53, core__Tuple):
            items = _cdy_t53.items
            _cdy_pos_37 = _cdy_t53.pos
            _cdy__tup_38 = lower__value_seq(items, n)
            _cdy_stmts_39 = _cdy__tup_38[0]
            vals = _cdy__tup_38[1]
            _cdy_n1_41 = _cdy__tup_38[2]
            return lower__Low(_cdy_stmts_39, core__Tuple(vals, _cdy_pos_37), _cdy_n1_41)
        elif isinstance(_cdy_t53, core__Fmt):
            parts = _cdy_t53.parts
            _cdy_pos_43 = _cdy_t53.pos
            _cdy__tup_44 = lower__value_seq(lower__holes(parts, ()), n)
            _cdy_stmts_45 = _cdy__tup_44[0]
            _cdy_vals_46 = _cdy__tup_44[1]
            _cdy_n1_47 = _cdy__tup_44[2]
            return lower__Low(_cdy_stmts_45, core__Fmt(lower__fill_holes(parts, _cdy_vals_46, ()), _cdy_pos_43), _cdy_n1_47)
        elif isinstance(_cdy_t53, core__Field):
            obj = _cdy_t53.obj
            field = _cdy_t53.field
            _cdy_pos_50 = _cdy_t53.pos
            _cdy_low_51 = lower__value(obj, n)
            return lower__Low(_cdy_low_51.stmts, core__Field(_cdy_low_51.expr, field, _cdy_pos_50), _cdy_low_51.n)
        elif isinstance(_cdy_t53, core__Assoc):
            _cdy_obj_52 = _cdy_t53.obj
            fields = _cdy_t53.fields
            _cdy_pos_54 = _cdy_t53.pos
            _cdy__tup_55 = lower__value_seq((cdy_rt.primitives.to_list(_cdy_obj_52) + lower__field_vals(fields, ())), n)
            _cdy_stmts_56 = _cdy__tup_55[0]
            _cdy_vals_57 = _cdy__tup_55[1]
            _cdy_n1_58 = _cdy__tup_55[2]
            return lower__Low(_cdy_stmts_56, core__Assoc(_cdy_vals_57[0], lower__refill(fields, prelude__rest(_cdy_vals_57), ()), _cdy_pos_54), _cdy_n1_58)
        elif isinstance(_cdy_t53, core__MatchE):
            tmp = core__Temp(n)
            _cdy__tup_60 = lower__lower_match(e, 'value', tmp, (n + 1))
            _cdy_stmts_61 = _cdy__tup_60[0]
            _cdy_n1_62 = _cdy__tup_60[1]
            return lower__Low(_cdy_stmts_61, tmp, _cdy_n1_62)
        else:
            return lower__Low((), e, n)

def lower__lower_match(e: core__Expr, mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t54: object = e
    if isinstance(_cdy_t54, core__MatchE):
        subject = _cdy_t54.subject
        clauses = _cdy_t54.clauses
        default = _cdy_t54.default
        low = lower__value(subject, n)
        temp = core__Temp(low.n)
        _tup = lower__lower_cases(clauses, mode, tmp, (low.n + 1), ())
        cases = _tup[0]
        n2 = _tup[1]
        _cdy__tup_75 = lower__lower_default(default, mode, tmp, n2)
        default_stmts = _cdy__tup_75[0]
        n3 = _cdy__tup_75[1]
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

def lower__value_fn(params: tuple[core__Expr, ...], body: core__Expr, pos: form__Pos, n: int) -> lower__Low:
    _tup = lower__tail(body, n)
    stmts = _tup[0]
    n1 = _tup[1]
    _cdy_t55: object = (stmts[0] if (len(stmts) == 1) else lower__SExpr(core__NIL))
    if isinstance(_cdy_t55, lower__SReturn):
        result = _cdy_t55.val
        return lower__Low((), core__Lambda(params, result, pos), n1)
    else:
        return lower__Low(cdy_rt.primitives.to_list(lower__SLocalFunc(core__Temp(n1), params, stmts)), core__Temp(n1), (n1 + 1))

def lower__holes(parts: tuple[core__FPart, ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t58 = prelude__rest(parts)
            _cdy_t57: object = parts[0]
            if isinstance(_cdy_t57, core__FHole):
                e = _cdy_t57.expr
                _cdy_t56 = (acc + cdy_rt.primitives.to_list(e))
            else:
                assert isinstance(_cdy_t57, core__FText)
                _cdy_t56 = acc
            parts, acc = (_cdy_t58, _cdy_t56)
            continue

def lower__fill_holes(parts: tuple[core__FPart, ...], vals: tuple[core__Expr, ...], acc: tuple[core__FPart, ...]) -> tuple[core__FPart, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t59: object = parts[0]
            if isinstance(_cdy_t59, core__FHole):
                parts, vals, acc = (prelude__rest(parts), prelude__rest(vals), (acc + cdy_rt.primitives.to_list(core__FHole(vals[0]))))
                continue
            else:
                assert isinstance(_cdy_t59, core__FText)
                text = _cdy_t59.text
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

def lower__value_call(callee: core__Expr, args: tuple[core__Expr, ...], pos: form__Pos, n: int) -> lower__Low:
    if cdy_rt.primitives.in_(lower__prim_name(callee), ('and', 'or')):
        return lower__value_boolop(callee, args, pos, n)
    else:
        _tup = lower__value_seq((cdy_rt.primitives.to_list(callee) + args), n)
        stmts = _tup[0]
        items = _tup[1]
        n1 = _tup[2]
        return lower__Low(stmts, core__Call(items[0], prelude__rest(items), pos), n1)

def lower__prim_name(e: core__Expr) -> str:
    _cdy_t60: object = e
    if isinstance(_cdy_t60, core__Prim):
        name = _cdy_t60.name
        return name
    else:
        return ''

def lower__value_boolop(op: core__Expr, args: tuple[core__Expr, ...], pos: form__Pos, n: int) -> lower__Low:
    _tup = lower__low_all(args, n, ())
    lows = _tup[0]
    n1 = _tup[1]
    first = lows[0]
    later = prelude__rest(lows)
    if lower__has_stmts(later):
        tmp = core__Temp(n1)
        return lower__Low((first.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, first.expr)) + cdy_rt.primitives.to_list(lower__guard(op, tmp, lower__guarded(op, later, tmp)))), tmp, (n1 + 1))
    else:
        return lower__Low(first.stmts, core__Call(op, lower__low_exprs(lows, ()), pos), n1)

def lower__guarded(op: core__Expr, lows: tuple[lower__Low, ...], tmp: core__Expr) -> tuple[lower__Stmt, ...]:
    low = lows[0]
    assign = (low.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, low.expr)))
    if (len(lows) == 1):
        return assign
    else:
        return (assign + cdy_rt.primitives.to_list(lower__guard(op, tmp, lower__guarded(op, prelude__rest(lows), tmp))))

def lower__guard(op: core__Expr, tmp: core__Expr, body: tuple[lower__Stmt, ...]) -> lower__Stmt:
    return lower__SIf((tmp if (lower__prim_name(op) == 'and') else core__Call(core__Prim('not'), cdy_rt.primitives.to_list(tmp), form__NOWHERE)), body, ())

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

def lower__value_if(test: core__Expr, then: core__Expr, other: core__Expr, pos: form__Pos, n: int) -> lower__Low:
    t = lower__value(test, n)
    a = lower__value(then, t.n)
    b = lower__value(other, a.n)
    if ((len(a.stmts) == 0) and (len(b.stmts) == 0)):
        return lower__Low(t.stmts, core__If(t.expr, a.expr, b.expr, pos), b.n)
    elif lower__is_if_into(b.stmts, b.expr):
        tmp = b.expr
        return lower__Low((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, (a.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, a.expr))), b.stmts))), tmp, b.n)
    else:
        _cdy_tmp_180 = core__Temp(b.n)
        return lower__Low((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, (a.stmts + cdy_rt.primitives.to_list(lower__SAssign(_cdy_tmp_180, a.expr))), (b.stmts + cdy_rt.primitives.to_list(lower__SAssign(_cdy_tmp_180, b.expr)))))), _cdy_tmp_180, (b.n + 1))

def lower__is_if_into(stmts: tuple[lower__Stmt, ...], e: core__Expr) -> bool:
    _cdy_t65 = (len(stmts) == 1)
    if _cdy_t65:
        _cdy_t62: object = stmts[0]
        if isinstance(_cdy_t62, lower__SIf):
            _cdy_t61 = True
        else:
            _cdy_t61 = False
        _cdy_t65 = _cdy_t61
        if _cdy_t65:
            _cdy_t64: object = e
            if isinstance(_cdy_t64, core__Temp):
                _cdy_t63 = True
            else:
                _cdy_t63 = False
            _cdy_t65 = _cdy_t63
    return _cdy_t65

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
        _cdy__tup_197 = lower__tail(body, n1)
        more = _cdy__tup_197[0]
        n2 = _cdy__tup_197[1]
        return ((stmts + more), n2)
    else:
        return lower__tail_plain(e, n)

def lower__tail_plain(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t66: object = e
    if isinstance(_cdy_t66, core__If):
        test = _cdy_t66.test
        then = _cdy_t66.then
        other = _cdy_t66.other
        t = lower__value(test, n)
        _tup = lower__tail(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_209 = lower__tail(other, n1)
        b = _cdy__tup_209[0]
        n2 = _cdy__tup_209[1]
        return ((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t66, core__Do):
        body = _cdy_t66.body
        _cdy__tup_213 = lower__effect_all(lower__all_but_last(body), n, ())
        stmts = _cdy__tup_213[0]
        _cdy_n1_215 = _cdy__tup_213[1]
        _cdy__tup_216 = lower__tail(lower__last_of(body), _cdy_n1_215)
        last = _cdy__tup_216[0]
        _cdy_n2_218 = _cdy__tup_216[1]
        return ((stmts + last), _cdy_n2_218)
    elif isinstance(_cdy_t66, core__MatchE):
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
        _cdy__tup_226 = lower__effect(body, n1)
        more = _cdy__tup_226[0]
        n2 = _cdy__tup_226[1]
        return ((stmts + more), n2)
    else:
        return lower__effect_plain(e, n)

def lower__effect_plain(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t67: object = e
    if isinstance(_cdy_t67, core__If):
        test = _cdy_t67.test
        then = _cdy_t67.then
        other = _cdy_t67.other
        t = lower__value(test, n)
        _tup = lower__effect(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_238 = lower__effect(other, n1)
        b = _cdy__tup_238[0]
        n2 = _cdy__tup_238[1]
        return ((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t67, core__Do):
        body = _cdy_t67.body
        return lower__effect_all(body, n, ())
    elif isinstance(_cdy_t67, core__MatchE):
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
    _cdy_t68: object = t
    if isinstance(_cdy_t68, core__TFn):
        ret = _cdy_t68.ret
        _cdy_t69: object = ret
        if isinstance(_cdy_t69, core__TCon):
            name = _cdy_t69.name
            return (name == 'Unit')
        else:
            return False
    else:
        return False

def lower__lower_top(top: core__Top, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t70: object = top
    if isinstance(_cdy_t70, core__TDeft):
        name = _cdy_t70.name
        tvars = _cdy_t70.tvars
        fields = _cdy_t70.fields
        return (cdy_rt.primitives.to_list(lower__SRecord(name, tvars, fields)), n)
    elif isinstance(_cdy_t70, core__TDeftSum):
        _cdy_name_257 = _cdy_t70.name
        _cdy_tvars_258 = _cdy_t70.tvars
        variants = _cdy_t70.variants
        return (cdy_rt.primitives.to_list(lower__SSum(_cdy_name_257, _cdy_tvars_258, variants)), n)
    elif isinstance(_cdy_t70, core__TDef):
        _cdy_name_260 = _cdy_t70.name
        init = _cdy_t70.init
        t = _cdy_t70.t
        low = lower__value(init, n)
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SDefAssign(_cdy_name_260, low.expr, t))), low.n)
    elif isinstance(_cdy_t70, core__TDefn):
        _cdy_name_264 = _cdy_t70.name
        params = _cdy_t70.params
        body = _cdy_t70.body
        _cdy_t_267 = _cdy_t70.t
        _tup = (lower__effect(body, n) if lower__returns_unit(_cdy_t_267) else lower__tail(body, n))
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.primitives.to_list(lower__SFunc(_cdy_name_264, params, lower__loop_tail_calls(_cdy_name_264, params, stmts, lower__returns_unit(_cdy_t_267)), _cdy_t_267)), n1)
    else:
        assert isinstance(_cdy_t70, core__TExpr)
        e = _cdy_t70.expr
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
    _cdy_t71: object = s
    if isinstance(_cdy_t71, lower__SReturn):
        val = _cdy_t71.val
        if lower__is_self_call(val, name, params):
            return lower__jump(params, lower__call_args(val))
        else:
            return cdy_rt.primitives.to_list(s)
    elif isinstance(_cdy_t71, lower__SExpr):
        e = _cdy_t71.expr
        if lower__is_self_call(e, name, params):
            return lower__jump(params, lower__call_args(e))
        else:
            return cdy_rt.primitives.to_list(s)
    elif isinstance(_cdy_t71, lower__SIf):
        test = _cdy_t71.test
        then = _cdy_t71.then
        other = _cdy_t71.other
        return cdy_rt.primitives.to_list(lower__SIf(test, lower__retail_all(then, name, params), lower__retail_all(other, name, params)))
    elif isinstance(_cdy_t71, lower__SMatch):
        temp = _cdy_t71.temp
        subject = _cdy_t71.subject
        cases = _cdy_t71.cases
        default = _cdy_t71.default
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
    _cdy_t72: object = e
    if isinstance(_cdy_t72, core__Call):
        callee = _cdy_t72.callee
        args = _cdy_t72.args
        _cdy_t73: object = callee
        if isinstance(_cdy_t73, core__Global):
            g = _cdy_t73.name
            return ((g == name) and (len(args) == len(params)))
        else:
            return False
    else:
        return False

def lower__call_args(e: core__Expr) -> tuple[core__Expr, ...]:
    _cdy_t74: object = e
    if isinstance(_cdy_t74, core__Call):
        args = _cdy_t74.args
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
    _cdy_t75: object = s
    if isinstance(_cdy_t75, lower__SLocalFunc):
        return True
    elif isinstance(_cdy_t75, lower__SAssign):
        target = _cdy_t75.target
        val = _cdy_t75.val
        return (lower__has_lambda(target) or lower__has_lambda(val))
    elif isinstance(_cdy_t75, lower__SDefAssign):
        _cdy_val_322 = _cdy_t75.val
        return lower__has_lambda(_cdy_val_322)
    elif isinstance(_cdy_t75, lower__SExpr):
        e = _cdy_t75.expr
        return lower__has_lambda(e)
    elif isinstance(_cdy_t75, lower__SReturn):
        _cdy_val_324 = _cdy_t75.val
        return lower__has_lambda(_cdy_val_324)
    elif isinstance(_cdy_t75, lower__SIf):
        test = _cdy_t75.test
        then = _cdy_t75.then
        other = _cdy_t75.other
        return (lower__has_lambda(test) or lower__stmts_have_closure(then) or lower__stmts_have_closure(other))
    elif isinstance(_cdy_t75, lower__SMatch):
        subject = _cdy_t75.subject
        cases = _cdy_t75.cases
        default = _cdy_t75.default
        return (lower__has_lambda(subject) or lower__cases_have_closure(cases) or lower__lists_have_closure(default))
    elif isinstance(_cdy_t75, lower__SLoop):
        body = _cdy_t75.body
        return lower__stmts_have_closure(body)
    elif isinstance(_cdy_t75, lower__SRebind):
        vals = _cdy_t75.vals
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
        _cdy_t76: object = e
        if isinstance(_cdy_t76, core__Lambda):
            return True
        elif isinstance(_cdy_t76, core__Call):
            callee = _cdy_t76.callee
            args = _cdy_t76.args
            return (lower__has_lambda(callee) or lower__any_lambda(args))
        elif isinstance(_cdy_t76, core__If):
            test = _cdy_t76.test
            then = _cdy_t76.then
            other = _cdy_t76.other
            return (lower__has_lambda(test) or lower__has_lambda(then) or lower__has_lambda(other))
        elif isinstance(_cdy_t76, core__Do):
            body = _cdy_t76.body
            return lower__any_lambda(body)
        elif isinstance(_cdy_t76, core__Tuple):
            items = _cdy_t76.items
            return lower__any_lambda(items)
        elif isinstance(_cdy_t76, core__Fmt):
            parts = _cdy_t76.parts
            return lower__any_lambda(lower__holes(parts, ()))
        elif isinstance(_cdy_t76, core__Field):
            obj = _cdy_t76.obj
            e = obj
            continue
        elif isinstance(_cdy_t76, core__Assoc):
            _cdy_obj_346 = _cdy_t76.obj
            fields = _cdy_t76.fields
            return (lower__has_lambda(_cdy_obj_346) or lower__any_lambda(lower__field_vals(fields, ())))
        elif isinstance(_cdy_t76, core__MatchE):
            subject = _cdy_t76.subject
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
            if (cdy_rt.primitives.map_has(env.taken, py) and (not cdy_rt.primitives.map_has(env.globals_, name))):
                return cdy_rt.primitives.fail((str(emit__candy_name(emit__holder(py, cdy_rt.primitives.map_keys(env.globals_), env.globals_))) + ' and ' + str(emit__candy_name(name)) + ' are one name in Python (' + str(py) + ')'))
            else:
                names, env = (prelude__rest(names), env._replace(globals_=cdy_rt.primitives.map_set(env.globals_, name, py), taken=cdy_rt.primitives.map_set(env.taken, py, True)))
                continue

def emit__holder(py: str, names: tuple[str, ...], globals_: _cdy_Mapping[str, str]) -> str:
    while True:
        if (len(names) == 0):
            return py
        elif (cdy_rt.primitives.map_get(globals_, names[0]) == py):
            return names[0]
        else:
            names = prelude__rest(names)
            continue

def emit__candy_name(name: str) -> str:
    parts = cdy_rt.primitives.split(name, '__')
    own = cdy_rt.primitives.join(prelude__rest(parts), '__')
    if (len(parts) == 1):
        return name
    else:
        return (str(own) + ' (from module ' + str(parts[0]) + ')')

def emit__own_name(name: str) -> str:
    parts = cdy_rt.primitives.split(name, '__')
    if (len(parts) == 1):
        return name
    else:
        return cdy_rt.primitives.join(prelude__rest(parts), '__')

def emit__top_names_of(top: core__Top) -> tuple[str, ...]:
    _cdy_t77: object = top
    if isinstance(_cdy_t77, core__TDeftSum):
        name = _cdy_t77.name
        variants = _cdy_t77.variants
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
    _cdy_t78: object = top
    if isinstance(_cdy_t78, core__TDeft):
        name = _cdy_t78.name
        return name
    elif isinstance(_cdy_t78, core__TDef):
        _cdy_name_45 = _cdy_t78.name
        return _cdy_name_45
    elif isinstance(_cdy_t78, core__TDefn):
        _cdy_name_46 = _cdy_t78.name
        return _cdy_name_46
    else:
        return ''

def emit__generic_variants(tops: tuple[core__Top, ...], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _cdy_t81 = prelude__rest(tops)
            _cdy_t80: object = tops[0]
            if isinstance(_cdy_t80, core__TDeftSum):
                tvars = _cdy_t80.tvars
                variants = _cdy_t80.variants
                _cdy_t79 = (acc if (len(tvars) == 0) else emit__mark_all(emit__variant_list_names(variants, ()), acc))
            else:
                _cdy_t79 = acc
            tops, acc = (_cdy_t81, _cdy_t79)
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
            _cdy_t85 = prelude__rest(locs)
            _cdy_t83: object = locs[0]
            if isinstance(_cdy_t83, core__Local):
                name = _cdy_t83.name
                id_ = _cdy_t83.id_
                if cdy_rt.primitives.map_has(env.locals_, id_):
                    _cdy_t84 = env
                else:
                    base = emit__py_mangle(name)
                    py = (('_cdy_' + str(base) + '_' + str(id_)) if cdy_rt.primitives.map_has(env.taken, base) else base)
                    _cdy_t84 = env._replace(locals_=cdy_rt.primitives.map_set(env.locals_, id_, py), taken=cdy_rt.primitives.map_set(env.taken, py, True))
                _cdy_t82 = _cdy_t84
            else:
                _cdy_t82 = env
            locs, env = (_cdy_t85, _cdy_t82)
            continue

def emit__bound_locals(stmts: tuple[lower__Stmt, ...], acc: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    while True:
        if (len(stmts) == 0):
            return acc
        else:
            _cdy_t90 = prelude__rest(stmts)
            _cdy_t87: object = stmts[0]
            if isinstance(_cdy_t87, lower__SAssign):
                target = _cdy_t87.target
                _cdy_t89: object = target
                if isinstance(_cdy_t89, core__Local):
                    _cdy_t88 = (acc + cdy_rt.primitives.to_list(target))
                else:
                    _cdy_t88 = acc
                _cdy_t86 = _cdy_t88
            elif isinstance(_cdy_t87, lower__SIf):
                then = _cdy_t87.then
                other = _cdy_t87.other
                _cdy_t86 = emit__bound_locals(other, emit__bound_locals(then, acc))
            elif isinstance(_cdy_t87, lower__SMatch):
                cases = _cdy_t87.cases
                default = _cdy_t87.default
                _cdy_t86 = emit__bound_in_cases(cases, emit__bound_in_lists(default, acc))
            elif isinstance(_cdy_t87, lower__SLoop):
                body = _cdy_t87.body
                _cdy_t86 = emit__bound_locals(body, acc)
            else:
                _cdy_t86 = acc
            stmts, acc = (_cdy_t90, _cdy_t86)
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
    _cdy_t91: object = e
    if isinstance(_cdy_t91, core__Lit):
        form = _cdy_t91.form
        return emit__emit_lit(form)
    elif isinstance(_cdy_t91, core__Local):
        name = _cdy_t91.name
        id_ = _cdy_t91.id_
        return emit__local_py(name, id_, env)
    elif isinstance(_cdy_t91, core__Global):
        _cdy_name_85 = _cdy_t91.name
        return cdy_rt.primitives.map_get(env.globals_, _cdy_name_85)
    elif isinstance(_cdy_t91, core__Prim):
        _cdy_name_86 = _cdy_t91.name
        return emit__emit_prim(_cdy_name_86, env)
    elif isinstance(_cdy_t91, core__Call):
        callee = _cdy_t91.callee
        args = _cdy_t91.args
        return emit__emit_call(callee, args, env)
    elif isinstance(_cdy_t91, core__If):
        test = _cdy_t91.test
        then = _cdy_t91.then
        other = _cdy_t91.other
        return ('(' + str(emit__emit_expr(then, env)) + ' if ' + str(emit__emit_expr(test, env)) + ' else ' + str(emit__emit_expr(other, env)) + ')')
    elif isinstance(_cdy_t91, core__Do):
        return cdy_rt.primitives.fail('emit: a do inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t91, core__MatchE):
        return cdy_rt.primitives.fail('emit: a match inside an expression (lower should have removed it)')
    elif isinstance(_cdy_t91, core__Lambda):
        params = _cdy_t91.params
        body = _cdy_t91.body
        inner = emit__bind_locals(params, env)
        return ('(lambda ' + str(emit__comma_join(emit__emit_exprs(params, inner, ()))) + ': ' + str(emit__emit_expr(body, inner)) + ')')
    elif isinstance(_cdy_t91, core__Tuple):
        items = _cdy_t91.items
        strs = emit__emit_exprs(items, env, ())
        if (len(strs) == 1):
            return ('(' + str(strs[0]) + ',)')
        else:
            return ('(' + str(emit__comma_join(strs)) + ')')
    elif isinstance(_cdy_t91, core__Fmt):
        parts = _cdy_t91.parts
        return emit__emit_format(parts, env)
    elif isinstance(_cdy_t91, core__Field):
        obj = _cdy_t91.obj
        field = _cdy_t91.field
        return (str(emit__emit_expr(obj, env)) + '.' + str(emit__py_mangle(field)))
    elif isinstance(_cdy_t91, core__Assoc):
        _cdy_obj_100 = _cdy_t91.obj
        fields = _cdy_t91.fields
        return (str(emit__emit_expr(_cdy_obj_100, env)) + '._replace(' + str(emit__comma_join(emit__emit_fields(fields, env, ()))) + ')')
    else:
        assert isinstance(_cdy_t91, core__Temp)
        _cdy_id__102 = _cdy_t91.id_
        return ('_cdy_t' + str(_cdy_id__102))

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
            _cdy_t94 = prelude__rest(parts)
            _cdy_t93: object = parts[0]
            if isinstance(_cdy_t93, core__FText):
                text = _cdy_t93.text
                _cdy_t92 = emit__py_str(text)
            else:
                assert isinstance(_cdy_t93, core__FHole)
                e = _cdy_t93.expr
                _cdy_t92 = ('str(' + str(emit__emit_expr(e, env)) + ')')
            parts, acc = (_cdy_t94, (acc + cdy_rt.primitives.to_list(_cdy_t92)))
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
    _cdy_t95: object = form
    if isinstance(_cdy_t95, form__Txt):
        v = _cdy_t95.val
        return emit__py_str(v)
    elif isinstance(_cdy_t95, form__CharLit):
        _cdy_v_121 = _cdy_t95.val
        return emit__py_str((str(_cdy_v_121)))
    elif isinstance(_cdy_t95, form__IntLit):
        _cdy_v_122 = _cdy_t95.val
        return (str(_cdy_v_122))
    elif isinstance(_cdy_t95, form__LongLit):
        _cdy_v_123 = _cdy_t95.val
        return (str(_cdy_v_123))
    elif isinstance(_cdy_t95, form__ByteLit):
        _cdy_v_124 = _cdy_t95.val
        return (str(_cdy_v_124))
    elif isinstance(_cdy_t95, form__FloatLit):
        _cdy_v_125 = _cdy_t95.val
        return (str(_cdy_v_125))
    elif isinstance(_cdy_t95, form__DoubleLit):
        _cdy_v_126 = _cdy_t95.val
        return (str(_cdy_v_126))
    elif isinstance(_cdy_t95, form__BoolLit):
        _cdy_v_127 = _cdy_t95.val
        return (str(_cdy_v_127))
    else:
        return cdy_rt.primitives.fail('emit: not a literal')

def emit__emit_prim(name: str, env: emit__Env) -> str:
    if cdy_rt.primitives.in_(core__spelling_kind(env.spellings, name), core__TYPED_KINDS):
        return cdy_rt.primitives.map_get(env.spellings, name)[0]
    else:
        return cdy_rt.primitives.fail(('the operator ' + str(name) + " can't be used as a value yet; wrap it in a fn"))

def emit__emit_call(callee: core__Expr, args: tuple[core__Expr, ...], env: emit__Env) -> str:
    strs = emit__emit_exprs(args, env, ())
    _cdy_t96: object = callee
    if isinstance(_cdy_t96, core__Prim):
        name = _cdy_t96.name
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
    _cdy_t97: object = t
    if isinstance(_cdy_t97, core__TVar):
        name = _cdy_t97.name
        return emit__py_mangle(name)
    elif isinstance(_cdy_t97, core__TFn):
        params = _cdy_t97.params
        ret = _cdy_t97.ret
        return ('_cdy_Callable[[' + str(emit__comma_join(emit__emit_types(params, env, ()))) + '], ' + str(emit__emit_type(ret, env)) + ']')
    else:
        assert isinstance(_cdy_t97, core__TCon)
        _cdy_name_146 = _cdy_t97.name
        args = _cdy_t97.args
        return emit__emit_tcon(_cdy_name_146, emit__emit_types(args, env, ()), env.spellings)

def emit__emit_types(types: tuple[core__CType, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            types, acc = (prelude__rest(types), (acc + cdy_rt.primitives.to_list(emit__emit_type(types[0], env))))
            continue

def emit__emit_tcon(name: str, args: tuple[str, ...], spellings: _cdy_Mapping[str, tuple[str, str]]) -> str:
    if (cdy_rt.primitives.map_has(spellings, name) and (cdy_rt.primitives.map_get(spellings, name)[1] == 'type')):
        return cdy_rt.primitives.replace(cdy_rt.primitives.map_get(spellings, name)[0], '{}', emit__comma_join(args))
    elif (name == 'Tup'):
        return ('tuple[' + str(emit__comma_join(args)) + ']')
    elif (len(args) == 0):
        return emit__py_mangle(name)
    else:
        return (str(emit__py_mangle(name)) + '[' + str(emit__comma_join(args)) + ']')

def emit__type_vars(types: tuple[core__CType, ...], acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(types) == 0):
            return acc
        else:
            _cdy_t100 = prelude__rest(types)
            _cdy_t99: object = types[0]
            if isinstance(_cdy_t99, core__TVar):
                name = _cdy_t99.name
                _cdy_t98 = (acc if cdy_rt.primitives.in_(name, acc) else (acc + cdy_rt.primitives.to_list(name)))
            elif isinstance(_cdy_t99, core__TCon):
                args = _cdy_t99.args
                _cdy_t98 = emit__type_vars(args, acc)
            else:
                assert isinstance(_cdy_t99, core__TFn)
                params = _cdy_t99.params
                ret = _cdy_t99.ret
                _cdy_t98 = emit__type_vars((params + cdy_rt.primitives.to_list(ret)), acc)
            types, acc = (_cdy_t100, _cdy_t98)
            continue

def emit__emit_stmt(s: lower__Stmt, level: int, env: emit__Env) -> str:
    _cdy_t101: object = s
    if isinstance(_cdy_t101, lower__SRecord):
        name = _cdy_t101.name
        tvars = _cdy_t101.tvars
        fields = _cdy_t101.fields
        checked = emit__check_py_fields(('deft ' + str(emit__candy_name(name))), fields, {})
        return ('\n' + emit__line(level, ('class ' + str(cdy_rt.primitives.map_get(env.globals_, name)) + str(emit__type_params(tvars)) + '(_cdy_NamedTuple):')) + emit__emit_record_fields(fields, (level + 1), env, ''))
    elif isinstance(_cdy_t101, lower__SSum):
        _cdy_name_167 = _cdy_t101.name
        _cdy_tvars_168 = _cdy_t101.tvars
        variants = _cdy_t101.variants
        return (emit__emit_variants(_cdy_name_167, variants, _cdy_tvars_168, level, env, '') + emit__line(level, ('type ' + str(cdy_rt.primitives.map_get(env.globals_, _cdy_name_167)) + str(emit__type_params(_cdy_tvars_168)) + ' = ' + str(cdy_rt.primitives.join(emit__variant_refs(variants, _cdy_tvars_168, env, ()), ' | ')))))
    elif isinstance(_cdy_t101, lower__SMatch):
        temp = _cdy_t101.temp
        subject = _cdy_t101.subject
        cases = _cdy_t101.cases
        default = _cdy_t101.default
        t = emit__emit_expr(temp, env)
        val = emit__emit_expr(subject, env)
        generic = cdy_rt.primitives.map_has(env.generic, cases[0].variant)
        return (emit__line(level, ((str(t) + ' = ' + str(val)) if generic else (str(t) + ': object = ' + str(val)))) + emit__emit_match(t, cases, default, ((not generic) and (len(default) == 0)), 'if', level, env))
    elif isinstance(_cdy_t101, lower__SLoop):
        body = _cdy_t101.body
        return (emit__line(level, 'while True:') + emit__emit_block(body, (level + 1), env))
    elif isinstance(_cdy_t101, lower__SRebind):
        targets = _cdy_t101.targets
        vals = _cdy_t101.vals
        return emit__line(level, ((str(emit__emit_expr(targets[0], env)) + ' = ' + str(emit__emit_expr(vals[0], env))) if (len(targets) == 1) else (str(emit__comma_join(emit__emit_exprs(targets, env, ()))) + ' = (' + str(emit__comma_join(emit__emit_exprs(vals, env, ()))) + ')')))
    elif isinstance(_cdy_t101, lower__SContinue):
        return emit__line(level, 'continue')
    elif isinstance(_cdy_t101, lower__SAssign):
        target = _cdy_t101.target
        _cdy_val_181 = _cdy_t101.val
        return emit__line(level, (str(emit__emit_expr(target, env)) + ' = ' + str(emit__emit_expr(_cdy_val_181, env))))
    elif isinstance(_cdy_t101, lower__SDefAssign):
        _cdy_name_182 = _cdy_t101.name
        _cdy_val_183 = _cdy_t101.val
        _cdy_t_184 = _cdy_t101.t
        return emit__line(level, (str(cdy_rt.primitives.map_get(env.globals_, _cdy_name_182)) + ': ' + str(emit__emit_type(_cdy_t_184, env)) + ' = ' + str(emit__emit_expr(_cdy_val_183, env))))
    elif isinstance(_cdy_t101, lower__SExpr):
        e = _cdy_t101.expr
        return emit__line(level, emit__emit_expr(e, env))
    elif isinstance(_cdy_t101, lower__SReturn):
        _cdy_e_186 = _cdy_t101.val
        return emit__line(level, ('return ' + str(emit__emit_expr(_cdy_e_186, env))))
    elif isinstance(_cdy_t101, lower__SIf):
        test = _cdy_t101.test
        then = _cdy_t101.then
        other = _cdy_t101.other
        return emit__emit_if('if', test, then, other, level, env)
    elif isinstance(_cdy_t101, lower__SFunc):
        _cdy_name_190 = _cdy_t101.name
        params = _cdy_t101.params
        _cdy_body_192 = _cdy_t101.body
        _cdy_t_193 = _cdy_t101.t
        return emit__emit_func(_cdy_name_190, params, _cdy_body_192, _cdy_t_193, level, env)
    else:
        assert isinstance(_cdy_t101, lower__SLocalFunc)
        _cdy_target_194 = _cdy_t101.target
        _cdy_params_195 = _cdy_t101.params
        _cdy_body_196 = _cdy_t101.body
        inner = emit__bind_locals((_cdy_params_195 + emit__bound_locals(_cdy_body_196, ())), env)
        args = emit__comma_join(emit__emit_any_params(_cdy_params_195, inner, ()))
        return (emit__line(level, ('def ' + str(emit__emit_expr(_cdy_target_194, env)) + '(' + str(args) + ') -> _cdy_Any:')) + emit__emit_block(_cdy_body_196, (level + 1), inner))

def emit__emit_if(keyword: str, test: core__Expr, then: tuple[lower__Stmt, ...], other: tuple[lower__Stmt, ...], level: int, env: emit__Env) -> str:
    _cdy_t105 = emit__line(level, (str(keyword) + ' ' + str(emit__emit_expr(test, env)) + ':'))
    _cdy_t106 = emit__emit_block(then, (level + 1), env)
    if (len(other) == 0):
        _cdy_t104 = ''
    elif (len(other) == 1):
        _cdy_t103: object = other[0]
        if isinstance(_cdy_t103, lower__SIf):
            test2 = _cdy_t103.test
            then2 = _cdy_t103.then
            other2 = _cdy_t103.other
            _cdy_t102 = emit__emit_if('elif', test2, then2, other2, level, env)
        else:
            _cdy_t102 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
        _cdy_t104 = _cdy_t102
    else:
        _cdy_t104 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
    return (_cdy_t105 + _cdy_t106 + _cdy_t104)

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

def emit__check_py_fields(owner: str, fields: tuple[tuple[str, core__CType], ...], seen: _cdy_Mapping[str, str]) -> bool:
    while True:
        if (len(fields) == 0):
            return True
        else:
            f = fields[0][0]
            py = emit__py_mangle(f)
            if cdy_rt.primitives.map_has(seen, py):
                return cdy_rt.primitives.fail((str(owner) + ': fields ' + str(cdy_rt.primitives.map_get(seen, py)) + ' and ' + str(f) + ' are one name in Python (' + str(py) + ')'))
            elif (py[0:1] == '_'):
                return cdy_rt.primitives.fail((str(owner) + ': field ' + str(f) + " can't start with _ in Python (" + str(py) + ')'))
            else:
                fields, seen = (prelude__rest(fields), cdy_rt.primitives.map_set(seen, py, f))
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

def emit__emit_variants(sum_: str, variants: tuple[core__Variant, ...], tvars: tuple[str, ...], level: int, env: emit__Env, acc: str) -> str:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            checked = emit__check_py_fields(('deft ' + str(emit__candy_name(sum_)) + ', variant ' + str(emit__own_name(v.name))), v.fields, {})
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
        _cdy_c_261 = cases[0]
        test = (str(keyword) + ' isinstance(' + str(subj) + ', ' + str(cdy_rt.primitives.map_get(env.globals_, _cdy_c_261.variant)) + '):')
        binds = emit__emit_binds(_cdy_c_261.binds, subj, (level + 1), env, '')
        body = ((emit__line((level + 1), 'pass') if (binds == '') else '') if (len(_cdy_c_261.body) == 0) else emit__emit_stmts(_cdy_c_261.body, (level + 1), env, ''))
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
    _cdy_t107: object = t
    if isinstance(_cdy_t107, core__TFn):
        types = _cdy_t107.params
        ret = _cdy_t107.ret
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
    _cdy_t108: object = form__list_items(form)[1]
    if isinstance(_cdy_t108, form__Txt):
        path = _cdy_t108.val
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
    _cdy_t109: object = params
    if isinstance(_cdy_t109, form__Sym):
        return True
    elif isinstance(_cdy_t109, form__Lst):
        items = _cdy_t109.items
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
        _cdy_t110: object = form
        if isinstance(_cdy_t110, form__Lst):
            items = _cdy_t110.items
            pos = _cdy_t110.pos
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
        _cdy_t111: object = items[1]
        if isinstance(_cdy_t111, form__Lst):
            binds = _cdy_t111.items
            p = _cdy_t111.pos
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
    _cdy_t112: object = clause
    if isinstance(_cdy_t112, form__Lst):
        items = _cdy_t112.items
        p = _cdy_t112.pos
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
    _cdy_t113: object = form
    if isinstance(_cdy_t113, form__Sym):
        name = _cdy_t113.name
        p = _cdy_t113.pos
        if (p.line == 0):
            return form__Sym(name, pos)
        else:
            return form
    elif isinstance(_cdy_t113, form__Lst):
        items = _cdy_t113.items
        _cdy_p_136 = _cdy_t113.pos
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

class check__Ctx(_cdy_NamedTuple):
    globals_: _cdy_Mapping[str, core__CType]
    shapes: _cdy_Mapping[str, check__Shape]
    sums: _cdy_Mapping[str, check__Shape]
    builtins: _cdy_Mapping[str, core__Builtin]
    where: str
    env: _cdy_Mapping[str, core__CType]

class check__Shape(_cdy_NamedTuple):
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]
    sum_: str

class check__St(_cdy_NamedTuple):
    subst: _cdy_Mapping[str, core__CType]
    n: int
    errors: tuple[str, ...]

class check__Res(_cdy_NamedTuple):
    t: core__CType
    st: check__St
check__ANY: core__CType = core__TCon('Any', ())

def check__tcon(name: str) -> core__CType:
    return core__TCon(name, ())

def check__check_program(tops: tuple[core__Top, ...], builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[str, ...]:
    ctx = check__Ctx(check__top_types(tops, {}), check__top_shapes(tops, {}), check__top_sums(tops, {}), builtins, '', {})
    return check__check_tops(tops, ctx, check__St({}, 0, ()), 0).errors

def check__check_tops(tops: tuple[core__Top, ...], ctx: check__Ctx, st: check__St, i: int) -> check__St:
    while True:
        if (i == len(tops)):
            return st
        else:
            st, i = (check__check_top(tops[i], ctx, st._replace(subst={})), (i + 1))
            continue

def check__check_top(top: core__Top, ctx: check__Ctx, st: check__St) -> check__St:
    _cdy_t114: object = top
    if isinstance(_cdy_t114, core__TDef):
        name = _cdy_t114.name
        init = _cdy_t114.init
        t = _cdy_t114.t
        return check__check_expr(init, t, '', ctx._replace(where=('def ' + str(check__shown_name(name)))), st)
    elif isinstance(_cdy_t114, core__TDefn):
        _cdy_name_14 = _cdy_t114.name
        params = _cdy_t114.params
        body = _cdy_t114.body
        _cdy_t_17 = _cdy_t114.t
        c = ctx._replace(where=('defn ' + str(check__shown_name(_cdy_name_14))))
        _cdy_t115: object = _cdy_t_17
        if isinstance(_cdy_t115, core__TFn):
            ptypes = _cdy_t115.params
            ret = _cdy_t115.ret
            return check__check_expr(body, ret, '', c._replace(env=check__bind_all(params, ptypes, c.env, 0)), st)
        else:
            return st
    elif isinstance(_cdy_t114, core__TExpr):
        e = _cdy_t114.expr
        return check__infer(e, ctx._replace(where='a top-level form'), st).st
    else:
        return st

def check__bind_all(params: tuple[core__Expr, ...], types: tuple[core__CType, ...], env: _cdy_Mapping[str, core__CType], i: int) -> _cdy_Mapping[str, core__CType]:
    while True:
        if ((i == len(params)) or (i == len(types))):
            return env
        else:
            env, i = (cdy_rt.primitives.map_set(env, check__local_key(params[i]), types[i]), (i + 1))
            continue

def check__local_key(e: core__Expr) -> str:
    _cdy_t116: object = e
    if isinstance(_cdy_t116, core__Local):
        name = _cdy_t116.name
        id_ = _cdy_t116.id_
        return (str(name) + '#' + str(id_))
    else:
        return ''

def check__top_types(tops: tuple[core__Top, ...], acc: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _cdy_t119 = prelude__rest(tops)
            _cdy_t118: object = tops[0]
            if isinstance(_cdy_t118, core__TDef):
                name = _cdy_t118.name
                t = _cdy_t118.t
                _cdy_t117 = cdy_rt.primitives.map_set(acc, name, t)
            elif isinstance(_cdy_t118, core__TDefn):
                _cdy_name_33 = _cdy_t118.name
                _cdy_t_34 = _cdy_t118.t
                _cdy_t117 = cdy_rt.primitives.map_set(acc, _cdy_name_33, _cdy_t_34)
            elif isinstance(_cdy_t118, core__TDeft):
                _cdy_name_35 = _cdy_t118.name
                tvars = _cdy_t118.tvars
                fields = _cdy_t118.fields
                _cdy_t117 = cdy_rt.primitives.map_set(acc, _cdy_name_35, core__TFn(check__fields_types(fields), core__TCon(_cdy_name_35, check__tvar_types(tvars))))
            elif isinstance(_cdy_t118, core__TDeftSum):
                _cdy_name_38 = _cdy_t118.name
                _cdy_tvars_39 = _cdy_t118.tvars
                variants = _cdy_t118.variants
                _cdy_t117 = check__variant_types(variants, core__TCon(_cdy_name_38, check__tvar_types(_cdy_tvars_39)), acc)
            else:
                _cdy_t117 = acc
            tops, acc = (_cdy_t119, _cdy_t117)
            continue

def check__variant_types(variants: tuple[core__Variant, ...], sum_: core__CType, acc: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            variants, acc = (prelude__rest(variants), cdy_rt.primitives.map_set(acc, v.name, core__TFn(check__fields_types(v.fields), sum_)))
            continue

def check__fields_types(fields: tuple[tuple[str, core__CType], ...]) -> tuple[core__CType, ...]:
    return cdy_rt.primitives.list_map((lambda f: f[1]), fields)

def check__tvar_types(names: tuple[str, ...]) -> tuple[core__CType, ...]:
    return cdy_rt.primitives.list_map((lambda name: core__TVar(name)), names)

def check__top_shapes(tops: tuple[core__Top, ...], acc: _cdy_Mapping[str, check__Shape]) -> _cdy_Mapping[str, check__Shape]:
    while True:
        if (len(tops) == 0):
            return acc
        else:
            _cdy_t122 = prelude__rest(tops)
            _cdy_t121: object = tops[0]
            if isinstance(_cdy_t121, core__TDeft):
                name = _cdy_t121.name
                tvars = _cdy_t121.tvars
                fields = _cdy_t121.fields
                _cdy_t120 = cdy_rt.primitives.map_set(acc, name, check__Shape(tvars, fields, ''))
            elif isinstance(_cdy_t121, core__TDeftSum):
                _cdy_name_54 = _cdy_t121.name
                _cdy_tvars_55 = _cdy_t121.tvars
                variants = _cdy_t121.variants
                _cdy_t120 = check__variant_shapes(variants, _cdy_tvars_55, _cdy_name_54, acc)
            else:
                _cdy_t120 = acc
            tops, acc = (_cdy_t122, _cdy_t120)
            continue

def check__variant_shapes(variants: tuple[core__Variant, ...], tvars: tuple[str, ...], sum_: str, acc: _cdy_Mapping[str, check__Shape]) -> _cdy_Mapping[str, check__Shape]:
    while True:
        if (len(variants) == 0):
            return acc
        else:
            v = variants[0]
            variants, acc = (prelude__rest(variants), cdy_rt.primitives.map_set(acc, v.name, check__Shape(tvars, v.fields, sum_)))
            continue

def check__top_sums(tops: tuple[core__Top, ...], acc: _cdy_Mapping[str, check__Shape]) -> _cdy_Mapping[str, check__Shape]:
    if (len(tops) == 0):
        return acc
    else:
        _cdy_t125 = prelude__rest(tops)
        _cdy_t124: object = tops[0]
        if isinstance(_cdy_t124, core__TDeftSum):
            name = _cdy_t124.name
            tvars = _cdy_t124.tvars
            variants = _cdy_t124.variants
            _cdy_t123 = cdy_rt.primitives.map_set(acc, name, check__Shape(tvars, cdy_rt.primitives.list_map((lambda v: (v.name, check__ANY)), variants), ''))
        else:
            _cdy_t123 = acc
        return check__top_sums(_cdy_t125, _cdy_t123)

def check__check_expr(e: core__Expr, want: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    while True:
        _cdy_t126: object = e
        if isinstance(_cdy_t126, core__If):
            test = _cdy_t126.test
            then = _cdy_t126.then
            other = _cdy_t126.other
            rt = check__infer(test, ctx, st)
            st1 = check__expect(check__tcon('Bool'), rt.t, 'if: the test', ctx, rt.st)
            e, st = (other, check__check_expr(then, want, what, ctx, st1))
            continue
        elif isinstance(_cdy_t126, core__Do):
            body = _cdy_t126.body
            if (len(body) == 0):
                return check__expect(want, check__tcon('Unit'), what, ctx, st)
            else:
                e, st = (body[(len(body) - 1)], check__infer_do(body[0:(len(body) - 1)], ctx, check__Res(check__ANY, st)).st)
                continue
        elif isinstance(_cdy_t126, core__Call):
            callee = _cdy_t126.callee
            args = _cdy_t126.args
            _cdy_t127: object = callee
            if isinstance(_cdy_t127, core__Lambda):
                params = _cdy_t127.params
                _cdy_body_82 = _cdy_t127.body
                if (len(params) == len(args)):
                    r = check__infer_all(args, ctx, st, ())
                    e, ctx, st = (_cdy_body_82, ctx._replace(env=check__bind_all(params, r[0], ctx.env, 0)), r[1])
                    continue
                else:
                    return check__infer_expect(e, want, what, ctx, st)
            else:
                return check__infer_expect(e, want, what, ctx, st)
        elif isinstance(_cdy_t126, core__Lambda):
            return check__check_lambda(e, want, what, ctx, st)
        elif isinstance(_cdy_t126, core__MatchE):
            subject = _cdy_t126.subject
            clauses = _cdy_t126.clauses
            default = _cdy_t126.default
            if check__is_any(check__prune(want, st.subst)):
                return check__infer(e, ctx, st).st
            else:
                return check__infer_expect(e, want, what, ctx, st)
        else:
            return check__infer_expect(e, want, what, ctx, st)

def check__infer_expect(e: core__Expr, want: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    r = check__infer(e, ctx, st)
    return check__expect(want, r.t, what, ctx, r.st)

def check__infer(e: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t128: object = e
    if isinstance(_cdy_t128, core__Lit):
        form = _cdy_t128.form
        return check__Res(check__literal_type(form), st)
    elif isinstance(_cdy_t128, core__Local):
        name = _cdy_t128.name
        key = check__local_key(e)
        return check__Res((cdy_rt.primitives.map_get(ctx.env, key) if cdy_rt.primitives.map_has(ctx.env, key) else check__ANY), st)
    elif isinstance(_cdy_t128, core__Global):
        _cdy_name_99 = _cdy_t128.name
        if cdy_rt.primitives.map_has(ctx.globals_, _cdy_name_99):
            return check__instantiate(cdy_rt.primitives.map_get(ctx.globals_, _cdy_name_99), st)
        else:
            return check__Res(check__ANY, st)
    elif isinstance(_cdy_t128, core__Prim):
        _cdy_name_100 = _cdy_t128.name
        return check__prim_type(_cdy_name_100, ctx, st)
    elif isinstance(_cdy_t128, core__Call):
        callee = _cdy_t128.callee
        args = _cdy_t128.args
        return check__infer_call(callee, args, ctx, st)
    elif isinstance(_cdy_t128, core__If):
        test = _cdy_t128.test
        then = _cdy_t128.then
        other = _cdy_t128.other
        rt = check__infer(test, ctx, st)
        st1 = check__expect(check__tcon('Bool'), rt.t, 'if: the test', ctx, rt.st)
        ra = check__infer(then, ctx, st1)
        rb = check__infer(other, ctx, ra.st)
        return check__join_types(ra.t, rb.t, 'if: the branches', ctx, rb.st)
    elif isinstance(_cdy_t128, core__Do):
        body = _cdy_t128.body
        return check__infer_do(body, ctx, check__Res(check__tcon('Unit'), st))
    elif isinstance(_cdy_t128, core__Lambda):
        params = _cdy_t128.params
        _cdy_body_112 = _cdy_t128.body
        return check__infer_lambda(params, _cdy_body_112, ctx, st)
    elif isinstance(_cdy_t128, core__Tuple):
        items = _cdy_t128.items
        r = check__infer_all(items, ctx, st, ())
        return check__Res(core__TCon('Tup', r[0]), r[1])
    elif isinstance(_cdy_t128, core__Fmt):
        parts = _cdy_t128.parts
        return check__Res(check__tcon('String'), check__infer_holes(parts, ctx, st))
    elif isinstance(_cdy_t128, core__Field):
        obj = _cdy_t128.obj
        field = _cdy_t128.field
        return check__infer_field(obj, field, ctx, st)
    elif isinstance(_cdy_t128, core__Assoc):
        _cdy_obj_118 = _cdy_t128.obj
        fields = _cdy_t128.fields
        return check__infer_assoc(_cdy_obj_118, fields, ctx, st)
    elif isinstance(_cdy_t128, core__MatchE):
        subject = _cdy_t128.subject
        clauses = _cdy_t128.clauses
        default = _cdy_t128.default
        return check__infer_match(subject, clauses, default, ctx, st)
    else:
        return check__Res(check__ANY, st)

def check__literal_type(form: form__Form) -> core__CType:
    _cdy_t129: object = form
    if isinstance(_cdy_t129, form__Txt):
        return check__tcon('String')
    elif isinstance(_cdy_t129, form__IntLit):
        return check__tcon('Int')
    elif isinstance(_cdy_t129, form__LongLit):
        return check__tcon('Long')
    elif isinstance(_cdy_t129, form__ByteLit):
        return check__tcon('Byte')
    elif isinstance(_cdy_t129, form__FloatLit):
        return check__tcon('Float')
    elif isinstance(_cdy_t129, form__DoubleLit):
        return check__tcon('Double')
    elif isinstance(_cdy_t129, form__CharLit):
        return check__tcon('Char')
    elif isinstance(_cdy_t129, form__BoolLit):
        return check__tcon('Bool')
    else:
        return check__ANY

def check__prim_type(name: str, ctx: check__Ctx, st: check__St) -> check__Res:
    if cdy_rt.primitives.map_has(ctx.builtins, name):
        _cdy_t130: object = cdy_rt.primitives.map_get(ctx.builtins, name)
        if isinstance(_cdy_t130, core__Typed):
            type_ = _cdy_t130.type_
            return check__instantiate(type_, st)
        else:
            return check__Res(check__ANY, st)
    else:
        return check__Res(check__ANY, st)

def check__infer_all(es: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St, acc: tuple[core__CType, ...]) -> tuple[tuple[core__CType, ...], check__St]:
    while True:
        if (len(es) == 0):
            return (acc, st)
        else:
            r = check__infer(es[0], ctx, st)
            es, st, acc = (prelude__rest(es), r.st, (acc + cdy_rt.primitives.to_list(r.t)))
            continue

def check__infer_do(body: tuple[core__Expr, ...], ctx: check__Ctx, last: check__Res) -> check__Res:
    while True:
        if (len(body) == 0):
            return last
        else:
            body, last = (prelude__rest(body), check__infer(body[0], ctx, last.st))
            continue

def check__infer_holes(parts: tuple[core__FPart, ...], ctx: check__Ctx, st: check__St) -> check__St:
    while True:
        if (len(parts) == 0):
            return st
        else:
            _cdy_t133 = prelude__rest(parts)
            _cdy_t132: object = parts[0]
            if isinstance(_cdy_t132, core__FHole):
                e = _cdy_t132.expr
                _cdy_t131 = check__infer(e, ctx, st).st
            else:
                _cdy_t131 = st
            parts, st = (_cdy_t133, _cdy_t131)
            continue

def check__infer_lambda(params: tuple[core__Expr, ...], body: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    fr = check__fresh_types(len(params), st, ())
    ptypes = fr[0]
    inner = ctx._replace(env=check__bind_all(params, ptypes, ctx.env, 0))
    r = check__infer(body, inner, fr[1])
    return check__Res(core__TFn(ptypes, r.t), r.st)

def check__fresh_types(count: int, st: check__St, acc: tuple[core__CType, ...]) -> tuple[tuple[core__CType, ...], check__St]:
    while True:
        if (count == 0):
            return (acc, st)
        else:
            count, st, acc = ((count - 1), st._replace(n=(st.n + 1)), (acc + cdy_rt.primitives.to_list(core__TVar(('?' + str(st.n))))))
            continue

def check__fresh(st: check__St) -> check__Res:
    return check__Res(core__TVar(('?' + str(st.n))), st._replace(n=(st.n + 1)))

def check__infer_call(callee: core__Expr, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t134: object = callee
    if isinstance(_cdy_t134, core__Lambda):
        params = _cdy_t134.params
        body = _cdy_t134.body
        if (len(params) == len(args)):
            return check__infer_applied(params, body, args, ctx, st)
        else:
            return check__infer_called(callee, args, ctx, st)
    elif isinstance(_cdy_t134, core__Prim):
        name = _cdy_t134.name
        if check__is_op(name, ctx):
            return check__infer_op(name, args, ctx, st)
        elif ((name == 'at') and check__is_tup_item(args)):
            return check__infer_tup_item(args, ctx, st)
        else:
            return check__infer_called(callee, args, ctx, st)
    else:
        return check__infer_called(callee, args, ctx, st)

def check__is_op(name: str, ctx: check__Ctx) -> bool:
    _cdy_t137 = cdy_rt.primitives.map_has(ctx.builtins, name)
    if _cdy_t137:
        _cdy_t136: object = cdy_rt.primitives.map_get(ctx.builtins, name)
        if isinstance(_cdy_t136, core__Op):
            _cdy_t135 = True
        else:
            _cdy_t135 = False
        _cdy_t137 = _cdy_t135
    return _cdy_t137

def check__infer_applied(params: tuple[core__Expr, ...], body: core__Expr, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer_all(args, ctx, st, ())
    inner = ctx._replace(env=check__bind_all(params, r[0], ctx.env, 0))
    return check__infer(body, inner, r[1])

def check__infer_called(callee: core__Expr, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    rc = check__infer(callee, ctx, st)
    ct = check__prune(rc.t, rc.st.subst)
    name = check__callee_name(callee)
    _cdy_t138: object = ct
    if isinstance(_cdy_t138, core__TFn):
        params = _cdy_t138.params
        ret = _cdy_t138.ret
        if (len(params) != len(args)):
            st1 = check__report((str(name) + ' takes ' + str(len(params)) + ' argument(s), got ' + str(len(args))), ctx, rc.st)
            return check__Res(ret, check__infer_all(args, ctx, st1, ())[1])
        else:
            return check__Res(ret, check__check_args(args, params, name, ctx, rc.st))
    elif isinstance(_cdy_t138, core__TVar):
        v = _cdy_t138.name
        if check__is_flexible(v):
            r = check__infer_all(args, ctx, rc.st, ())
            rr = check__fresh(r[1])
            u = check__unify(ct, core__TFn(r[0], rr.t), rr.st.subst)
            return check__Res(rr.t, rr.st._replace(subst=u[1]))
        else:
            return check__Res(check__ANY, check__report(('expected a function, got ' + str(check__show(ct, rc.st.subst))), ctx, rc.st))
    else:
        if check__is_any(ct):
            return check__Res(check__ANY, check__infer_all(args, ctx, rc.st, ())[1])
        else:
            return check__Res(check__ANY, check__report(('expected a function, got ' + str(check__show(ct, rc.st.subst))), ctx, rc.st))

def check__check_args(args: tuple[core__Expr, ...], params: tuple[core__CType, ...], name: str, ctx: check__Ctx, st: check__St) -> check__St:
    return check__check_fn_args(args, params, name, ctx, check__check_plain_args(args, params, name, ctx, st, 0), 0)

def check__check_plain_args(args: tuple[core__Expr, ...], params: tuple[core__CType, ...], name: str, ctx: check__Ctx, st: check__St, i: int) -> check__St:
    while True:
        if (i == len(args)):
            return st
        elif check__is_lambda(args[i]):
            i = (i + 1)
            continue
        else:
            st, i = (check__check_expr(args[i], params[i], check__arg_what(i, name), ctx, st), (i + 1))
            continue

def check__check_fn_args(args: tuple[core__Expr, ...], params: tuple[core__CType, ...], name: str, ctx: check__Ctx, st: check__St, i: int) -> check__St:
    while True:
        if (i == len(args)):
            return st
        elif check__is_lambda(args[i]):
            st, i = (check__check_lambda(args[i], params[i], check__arg_what(i, name), ctx, st), (i + 1))
            continue
        else:
            i = (i + 1)
            continue

def check__arg_what(i: int, name: str) -> str:
    return ('argument ' + str((i + 1)) + ' of ' + str(name))

def check__is_lambda(e: core__Expr) -> bool:
    _cdy_t139: object = e
    if isinstance(_cdy_t139, core__Lambda):
        return True
    else:
        return False

def check__check_lambda(lam: core__Expr, expected: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    _cdy_t140: object = lam
    if isinstance(_cdy_t140, core__Lambda):
        params = _cdy_t140.params
        body = _cdy_t140.body
        _cdy_t141: object = check__prune(expected, st.subst)
        if isinstance(_cdy_t141, core__TFn):
            ptypes = _cdy_t141.params
            ret = _cdy_t141.ret
            if (len(ptypes) == len(params)):
                return check__check_expr(body, ret, (str(what) + "'s result"), ctx._replace(env=check__bind_all(params, ptypes, ctx.env, 0)), st)
            else:
                _cdy_r_211 = check__infer(lam, ctx, st)
                return check__expect(expected, _cdy_r_211.t, what, ctx, _cdy_r_211.st)
        else:
            r = check__infer(lam, ctx, st)
            return check__expect(expected, r.t, what, ctx, r.st)
    else:
        return st

def check__callee_name(e: core__Expr) -> str:
    _cdy_t142: object = e
    if isinstance(_cdy_t142, core__Global):
        name = _cdy_t142.name
        return check__shown_name(name)
    elif isinstance(_cdy_t142, core__Prim):
        _cdy_name_215 = _cdy_t142.name
        return _cdy_name_215
    elif isinstance(_cdy_t142, core__Local):
        _cdy_name_216 = _cdy_t142.name
        return _cdy_name_216
    else:
        return 'the function'

def check__is_tup_item(args: tuple[core__Expr, ...]) -> bool:
    return ((len(args) == 2) and (check__tup_name(args[0]) == '_tup') and (check__int_lit(args[1]) >= 0))

def check__tup_name(e: core__Expr) -> str:
    _cdy_t143: object = e
    if isinstance(_cdy_t143, core__Local):
        name = _cdy_t143.name
        return name
    else:
        return ''

def check__int_lit(e: core__Expr) -> int:
    _cdy_t144: object = e
    if isinstance(_cdy_t144, core__Lit):
        form = _cdy_t144.form
        _cdy_t145: object = form
        if isinstance(_cdy_t145, form__IntLit):
            k = _cdy_t145.val
            return k
        else:
            return -1
    else:
        return -1

def check__infer_tup_item(args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(args[0], ctx, st)
    i = check__int_lit(args[1])
    tt = check__prune(r.t, r.st.subst)
    items = check__tup_items(tt)
    if (check__tcon_name(tt) != 'Tup'):
        return check__Res(check__ANY, r.st)
    elif (i < len(items)):
        return check__Res(items[i], r.st)
    else:
        return check__Res(check__ANY, check__report(('a ' + str(check__show(tt, r.st.subst)) + ' has ' + str(len(items)) + ' items, not ' + str((i + 1))), ctx, r.st))

def check__tup_items(t: core__CType) -> tuple[core__CType, ...]:
    _cdy_t146: object = t
    if isinstance(_cdy_t146, core__TCon):
        args = _cdy_t146.args
        return args
    else:
        return ()
check__NUMBERS: tuple[str, ...] = ('Int', 'Long', 'Byte', 'Float', 'Double')

def check__infer_op(name: str, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer_all(args, ctx, st, ())
    types = r[0]
    st1 = r[1]
    if cdy_rt.primitives.in_(name, ('and', 'or', 'not')):
        return check__Res(check__tcon('Bool'), check__expect_all(check__tcon('Bool'), types, name, ctx, st1))
    else:
        one = check__join_all(types, name, ctx, check__Res(types[0], st1))
        t1 = check__prune(one.t, one.st.subst)
        if cdy_rt.primitives.in_(name, ('=', '!=', '<', '>', '<=', '>=')):
            return check__Res(check__tcon('Bool'), one.st)
        elif (name == '+'):
            return check__Res(t1, (one.st if (check__tcon_name(t1) == 'List') else check__needs_kind(t1, (check__NUMBERS + cdy_rt.primitives.to_list('String')), 'a number, String or a list', name, ctx, one.st)))
        elif (name == '/'):
            return check__Res(check__tcon('Double'), check__needs_kind(t1, check__NUMBERS, 'a number', name, ctx, one.st))
        else:
            return check__Res(t1, check__needs_kind(t1, check__NUMBERS, 'a number', name, ctx, one.st))

def check__needs_kind(t: core__CType, names: tuple[str, ...], what: str, name: str, ctx: check__Ctx, st: check__St) -> check__St:
    _cdy_t147: object = t
    if isinstance(_cdy_t147, core__TCon):
        tn = _cdy_t147.name
        args = _cdy_t147.args
        if ((tn == 'Any') or ((len(args) == 0) and cdy_rt.primitives.list_contains(tn, names))):
            return st
        else:
            return check__report((str(name) + ': expected ' + str(what) + ', got ' + str(check__show(t, st.subst))), ctx, st)
    elif isinstance(_cdy_t147, core__TVar):
        v = _cdy_t147.name
        if check__is_flexible(v):
            return st
        else:
            return check__report((str(name) + ': expected ' + str(what) + ', got ' + str(v)), ctx, st)
    else:
        return check__report((str(name) + ': expected ' + str(what) + ', got ' + str(check__show(t, st.subst))), ctx, st)

def check__expect_all(want: core__CType, types: tuple[core__CType, ...], what: str, ctx: check__Ctx, st: check__St) -> check__St:
    while True:
        if (len(types) == 0):
            return st
        else:
            types, st = (prelude__rest(types), check__expect(want, types[0], what, ctx, st))
            continue

def check__join_all(types: tuple[core__CType, ...], what: str, ctx: check__Ctx, acc: check__Res) -> check__Res:
    while True:
        if (len(types) <= 1):
            return acc
        else:
            types, acc = (prelude__rest(types), check__join_types(acc.t, types[1], what, ctx, acc.st))
            continue

def check__field_of(t: core__CType, field: str, ctx: check__Ctx) -> tuple[bool, core__CType]:
    _cdy_t148: object = t
    if isinstance(_cdy_t148, core__TCon):
        name = _cdy_t148.name
        args = _cdy_t148.args
        if cdy_rt.primitives.map_has(ctx.shapes, name):
            s = cdy_rt.primitives.map_get(ctx.shapes, name)
            return check__find_field(s.fields, field, check__zip_map(s.tvars, args, {}))
        elif cdy_rt.primitives.map_has(ctx.sums, name):
            return check__sum_field(cdy_rt.primitives.map_get(ctx.sums, name), args, field, ctx)
        else:
            return (False, check__ANY)
    else:
        return (False, check__ANY)

def check__sum_field(sum_: check__Shape, args: tuple[core__CType, ...], field: str, ctx: check__Ctx) -> tuple[bool, core__CType]:
    found = cdy_rt.primitives.list_map((lambda v: check__field_of(core__TCon(v[0], args), field, ctx)), sum_.fields)
    if ((len(found) > 0) and cdy_rt.primitives.list_all((lambda f: (f[0] and (f[1] == found[0][1]))), found)):
        return found[0]
    else:
        return (False, check__ANY)

def check__find_field(fields: tuple[tuple[str, core__CType], ...], field: str, vars_: _cdy_Mapping[str, core__CType]) -> tuple[bool, core__CType]:
    while True:
        if (len(fields) == 0):
            return (False, check__ANY)
        elif (fields[0][0] == field):
            return (True, check__put_vars(fields[0][1], vars_))
        else:
            fields = prelude__rest(fields)
            continue

def check__zip_map(names: tuple[str, ...], types: tuple[core__CType, ...], acc: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    while True:
        if ((len(names) == 0) or (len(types) == 0)):
            return acc
        else:
            names, types, acc = (prelude__rest(names), prelude__rest(types), cdy_rt.primitives.map_set(acc, names[0], types[0]))
            continue

def check__put_vars(t: core__CType, vars_: _cdy_Mapping[str, core__CType]) -> core__CType:
    _cdy_t149: object = t
    if isinstance(_cdy_t149, core__TVar):
        name = _cdy_t149.name
        if cdy_rt.primitives.map_has(vars_, name):
            return cdy_rt.primitives.map_get(vars_, name)
        else:
            return t
    elif isinstance(_cdy_t149, core__TCon):
        _cdy_name_281 = _cdy_t149.name
        args = _cdy_t149.args
        return core__TCon(_cdy_name_281, cdy_rt.primitives.list_map((lambda a: check__put_vars(a, vars_)), args))
    else:
        assert isinstance(_cdy_t149, core__TFn)
        params = _cdy_t149.params
        ret = _cdy_t149.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__put_vars(p, vars_)), params), check__put_vars(ret, vars_))

def check__infer_field(obj: core__Expr, field: str, ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(obj, ctx, st)
    ot = check__prune(r.t, r.st.subst)
    return check__field_type(ot, obj, field, 'get', ctx, r.st)

def check__field_type(ot: core__CType, obj: core__Expr, field: str, what: str, ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t150: object = ot
    if isinstance(_cdy_t150, core__TVar):
        v = _cdy_t150.name
        return check__Res(check__ANY, check__report(((str(what) + ': the type of ' + str(check__callee_name(obj)) + " isn't known here (" + str(field) + ')') if check__is_flexible(v) else (str(what) + ': ' + str(v) + ' has no fields')), ctx, st))
    else:
        f = check__field_of(ot, field, ctx)
        if check__is_any(ot):
            return check__Res(check__ANY, st)
        elif f[0]:
            return check__Res(f[1], st)
        else:
            return check__Res(check__ANY, check__report(((str(what) + ': ' + str(check__show(ot, st.subst)) + ' has no field ' + str(field)) if (cdy_rt.primitives.map_has(ctx.shapes, check__tcon_name(ot)) or cdy_rt.primitives.map_has(ctx.sums, check__tcon_name(ot))) else (str(what) + ': ' + str(check__show(ot, st.subst)) + ' has no fields')), ctx, st))

def check__tcon_name(t: core__CType) -> str:
    _cdy_t151: object = t
    if isinstance(_cdy_t151, core__TCon):
        name = _cdy_t151.name
        return name
    else:
        return ''

def check__infer_assoc(obj: core__Expr, fields: tuple[tuple[str, core__Expr], ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(obj, ctx, st)
    ot = check__prune(r.t, r.st.subst)
    return check__Res(r.t, check__assoc_values(ot, obj, fields, ctx, r.st))

def check__assoc_values(ot: core__CType, obj: core__Expr, fields: tuple[tuple[str, core__Expr], ...], ctx: check__Ctx, st: check__St) -> check__St:
    while True:
        if (len(fields) == 0):
            return st
        else:
            _tup = fields[0]
            field = _tup[0]
            val = _tup[1]
            ft = check__field_type(ot, obj, field, 'assoc', ctx, st)
            st1 = check__check_expr(val, ft.t, ('assoc: field ' + str(field)), ctx, ft.st)
            fields, st = (prelude__rest(fields), st1)
            continue

def check__infer_match(subject: core__Expr, clauses: tuple[core__Clause, ...], default: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    rs = check__infer(subject, ctx, st)
    variant = clauses[0].variant
    sum_ = (cdy_rt.primitives.map_get(ctx.shapes, variant).sum_ if cdy_rt.primitives.map_has(ctx.shapes, variant) else '')
    tvars = (cdy_rt.primitives.map_get(ctx.sums, sum_).tvars if cdy_rt.primitives.map_has(ctx.sums, sum_) else ())
    fr = check__fresh_types(len(tvars), rs.st, ())
    vars_ = check__zip_map(tvars, fr[0], {})
    want = core__TCon(sum_, fr[0])
    st1 = check__expect(want, rs.t, 'match: the subject', ctx, fr[1])
    rc = check__infer_clauses(clauses, vars_, ctx, st1, ())
    if (len(default) == 0):
        return check__join_all(rc[0], 'match: the clauses', ctx, check__Res(rc[0][0], rc[1]))
    else:
        rd = check__infer(default[0], ctx, rc[1])
        return check__join_all((rc[0] + cdy_rt.primitives.to_list(rd.t)), 'match: the clauses', ctx, check__Res(rc[0][0], rd.st))

def check__infer_clauses(clauses: tuple[core__Clause, ...], vars_: _cdy_Mapping[str, core__CType], ctx: check__Ctx, st: check__St, acc: tuple[core__CType, ...]) -> tuple[tuple[core__CType, ...], check__St]:
    while True:
        if (len(clauses) == 0):
            return (acc, st)
        else:
            c = clauses[0]
            shape = (cdy_rt.primitives.map_get(ctx.shapes, c.variant) if cdy_rt.primitives.map_has(ctx.shapes, c.variant) else check__Shape((), (), ''))
            inner = ctx._replace(env=check__bind_fields(c.binds, shape.fields, vars_, ctx.env))
            r = check__infer(c.body, inner, st)
            clauses, st, acc = (prelude__rest(clauses), r.st, (acc + cdy_rt.primitives.to_list(r.t)))
            continue

def check__bind_fields(binds: tuple[tuple[str, core__Expr], ...], fields: tuple[tuple[str, core__CType], ...], vars_: _cdy_Mapping[str, core__CType], env: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    while True:
        if (len(binds) == 0):
            return env
        else:
            _tup = binds[0]
            field = _tup[0]
            loc = _tup[1]
            f = check__find_field(fields, field, vars_)
            binds, env = (prelude__rest(binds), cdy_rt.primitives.map_set(env, check__local_key(loc), (f[1] if f[0] else check__ANY)))
            continue

def check__is_flexible(name: str) -> bool:
    return cdy_rt.primitives.starts_with(name, '?')

def check__prune(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> core__CType:
    while True:
        _cdy_t152: object = t
        if isinstance(_cdy_t152, core__TVar):
            name = _cdy_t152.name
            if cdy_rt.primitives.map_has(subst, name):
                t = cdy_rt.primitives.map_get(subst, name)
                continue
            else:
                return t
        else:
            return t

def check__resolve_type(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> core__CType:
    _cdy_t153: object = check__prune(t, subst)
    if isinstance(_cdy_t153, core__TCon):
        name = _cdy_t153.name
        args = _cdy_t153.args
        return core__TCon(name, cdy_rt.primitives.list_map((lambda a: check__resolve_type(a, subst)), args))
    elif isinstance(_cdy_t153, core__TFn):
        params = _cdy_t153.params
        ret = _cdy_t153.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__resolve_type(p, subst)), params), check__resolve_type(ret, subst))
    else:
        return check__prune(t, subst)

def check__occurs(v: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> bool:
    _cdy_t154: object = check__prune(t, subst)
    if isinstance(_cdy_t154, core__TVar):
        name = _cdy_t154.name
        return (name == v)
    elif isinstance(_cdy_t154, core__TCon):
        args = _cdy_t154.args
        return cdy_rt.primitives.list_any((lambda a: check__occurs(v, a, subst)), args)
    else:
        assert isinstance(_cdy_t154, core__TFn)
        params = _cdy_t154.params
        ret = _cdy_t154.ret
        return (cdy_rt.primitives.list_any((lambda p: check__occurs(v, p, subst)), params) or check__occurs(v, ret, subst))

def check__unify(a: core__CType, b: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    while True:
        pa = check__prune(a, subst)
        pb = check__prune(b, subst)
        if (check__is_any(pa) or check__is_any(pb)):
            return (True, subst)
        elif check__is_var(pa):
            return check__bind_var(check__tvar_name(pa), pb, subst)
        elif check__is_var(pb):
            return check__bind_var(check__tvar_name(pb), pa, subst)
        else:
            _cdy_t155: object = pa
            if isinstance(_cdy_t155, core__TVar):
                name = _cdy_t155.name
                _cdy_t157: object = pb
                if isinstance(_cdy_t157, core__TVar):
                    other = _cdy_t157.name
                    _cdy_t156 = (name == other)
                else:
                    _cdy_t156 = False
                return (_cdy_t156, subst)
            elif isinstance(_cdy_t155, core__TCon):
                _cdy_name_379 = _cdy_t155.name
                args = _cdy_t155.args
                _cdy_t158: object = pb
                if isinstance(_cdy_t158, core__TCon):
                    _cdy_other_381 = _cdy_t158.name
                    bargs = _cdy_t158.args
                    if ((_cdy_name_379 == _cdy_other_381) and (len(args) == len(bargs))):
                        return check__unify_all(args, bargs, subst)
                    else:
                        return (False, subst)
                else:
                    return (False, subst)
            else:
                assert isinstance(_cdy_t155, core__TFn)
                params = _cdy_t155.params
                ret = _cdy_t155.ret
                _cdy_t159: object = pb
                if isinstance(_cdy_t159, core__TFn):
                    bparams = _cdy_t159.params
                    bret = _cdy_t159.ret
                    if (len(params) == len(bparams)):
                        u = check__unify_all(params, bparams, subst)
                        if u[0]:
                            a, b, subst = (ret, bret, u[1])
                            continue
                        else:
                            return u
                    else:
                        return (False, subst)
                else:
                    return (False, subst)

def check__unify_all(xs: tuple[core__CType, ...], ys: tuple[core__CType, ...], subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    while True:
        if (len(xs) == 0):
            return (True, subst)
        else:
            u = check__unify(xs[0], ys[0], subst)
            if u[0]:
                xs, ys, subst = (prelude__rest(xs), prelude__rest(ys), u[1])
                continue
            else:
                return u

def check__bind_var(v: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    _cdy_t161: object = t
    if isinstance(_cdy_t161, core__TVar):
        other = _cdy_t161.name
        _cdy_t160 = (other == v)
    else:
        _cdy_t160 = False
    if _cdy_t160:
        return (True, subst)
    elif check__occurs(v, t, subst):
        return (False, subst)
    else:
        return (True, cdy_rt.primitives.map_set(subst, v, t))

def check__is_any(t: core__CType) -> bool:
    _cdy_t162: object = t
    if isinstance(_cdy_t162, core__TCon):
        name = _cdy_t162.name
        return (name == 'Any')
    else:
        return False

def check__is_var(t: core__CType) -> bool:
    _cdy_t163: object = t
    if isinstance(_cdy_t163, core__TVar):
        name = _cdy_t163.name
        return check__is_flexible(name)
    else:
        return False

def check__tvar_name(t: core__CType) -> str:
    _cdy_t164: object = t
    if isinstance(_cdy_t164, core__TVar):
        name = _cdy_t164.name
        return name
    else:
        return ''

def check__maybe_arg(t: core__CType) -> tuple[core__CType, ...]:
    if (check__tcon_name(t) == 'Maybe'):
        return check__tup_items(t)
    else:
        return ()

def check__is_unit(t: core__CType) -> bool:
    _cdy_t165: object = t
    if isinstance(_cdy_t165, core__TCon):
        name = _cdy_t165.name
        return (name == 'Unit')
    else:
        return False

def check__accepts(want: core__CType, actual: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    pw = check__prune(want, subst)
    pa = check__prune(actual, subst)
    inner = check__maybe_arg(pw)
    if ((check__tcon_name(pw) == 'List') and (check__tcon_name(pa) == 'Tup')):
        return check__accepts_each(check__tup_items(pw)[0], check__tup_items(pa), subst)
    elif ((len(inner) == 0) or check__is_var(pa) or check__is_any(pa)):
        return check__unify(pw, pa, subst)
    elif (len(check__maybe_arg(pa)) > 0):
        return check__unify(pw, pa, subst)
    elif check__is_unit(pa):
        return (True, subst)
    else:
        return check__unify(inner[0], pa, subst)

def check__accepts_each(want: core__CType, items: tuple[core__CType, ...], subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    while True:
        if (len(items) == 0):
            return (True, subst)
        else:
            u = check__accepts(want, items[0], subst)
            if u[0]:
                items, subst = (prelude__rest(items), u[1])
                continue
            else:
                return u

def check__expect(want: core__CType, actual: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    u = check__accepts(want, actual, st.subst)
    if u[0]:
        return st._replace(subst=u[1])
    else:
        lead = ('' if (what == '') else (what + ': '))
        return check__report((str(lead) + 'expected ' + str(check__show(want, st.subst)) + ', got ' + str(check__show(actual, st.subst))), ctx, st)

def check__join_types(a: core__CType, b: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__Res:
    while True:
        pa = check__prune(a, st.subst)
        pb = check__prune(b, st.subst)
        if (check__is_unit(pa) and (not check__is_unit(pb)) and (not check__is_var(pb))):
            return check__Res(check__as_maybe(pb), st)
        elif (check__is_unit(pb) and (not check__is_unit(pa)) and (not check__is_var(pa))):
            return check__Res(check__as_maybe(pa), st)
        elif ((len(check__maybe_arg(pa)) > 0) and (len(check__maybe_arg(pb)) == 0) and (not check__is_var(pb))):
            return check__Res(pa, check__expect(pa, pb, what, ctx, st))
        elif ((len(check__maybe_arg(pb)) > 0) and (len(check__maybe_arg(pa)) == 0) and (not check__is_var(pa))):
            return check__Res(pb, check__expect(pb, pa, what, ctx, st))
        elif ((check__tcon_name(pa) == 'Tup') and ((check__tcon_name(pb) == 'List') or ((check__tcon_name(pb) == 'Tup') and (len(check__tup_items(pa)) != len(check__tup_items(pb)))))):
            a, b = (check__as_list(pa), pb)
            continue
        elif ((check__tcon_name(pb) == 'Tup') and (check__tcon_name(pa) == 'List')):
            a, b = (pa, check__as_list(pb))
            continue
        else:
            u = check__unify(pa, pb, st.subst)
            if u[0]:
                return check__Res(pa, st._replace(subst=u[1]))
            else:
                return check__Res(check__ANY, check__report((str(what) + ' are ' + str(check__show(pa, st.subst)) + ' and ' + str(check__show(pb, st.subst))), ctx, st))

def check__as_list(t: core__CType) -> core__CType:
    items = check__tup_items(t)
    if (len(items) == 0):
        return core__TCon('List', cdy_rt.primitives.to_list(check__ANY))
    else:
        return core__TCon('List', cdy_rt.primitives.to_list(check__tup_list_type(items)))

def check__tup_list_type(items: tuple[core__CType, ...]) -> core__CType:
    if cdy_rt.primitives.list_all((lambda x: (x == items[0])), items):
        return items[0]
    else:
        return check__ANY

def check__as_maybe(t: core__CType) -> core__CType:
    if (len(check__maybe_arg(t)) > 0):
        return t
    elif check__is_any(t):
        return t
    else:
        return core__TCon('Maybe', cdy_rt.primitives.to_list(t))

def check__instantiate(t: core__CType, st: check__St) -> check__Res:
    names = check__rigid_vars(t, ())
    if (len(names) == 0):
        return check__Res(t, st)
    else:
        fr = check__fresh_types(len(names), st, ())
        return check__Res(check__put_vars(t, check__zip_map(names, fr[0], {})), fr[1])

def check__rigid_vars(t: core__CType, acc: tuple[str, ...]) -> tuple[str, ...]:
    _cdy_t166: object = t
    if isinstance(_cdy_t166, core__TVar):
        name = _cdy_t166.name
        if (check__is_flexible(name) or cdy_rt.primitives.list_contains(name, acc)):
            return acc
        else:
            return (acc + cdy_rt.primitives.to_list(name))
    elif isinstance(_cdy_t166, core__TCon):
        args = _cdy_t166.args
        return cdy_rt.primitives.list_fold((lambda a, x: check__rigid_vars(x, a)), acc, args)
    else:
        assert isinstance(_cdy_t166, core__TFn)
        params = _cdy_t166.params
        ret = _cdy_t166.ret
        return check__rigid_vars(ret, cdy_rt.primitives.list_fold((lambda a, x: check__rigid_vars(x, a)), acc, params))

def check__report(msg: str, ctx: check__Ctx, st: check__St) -> check__St:
    return st._replace(errors=(st.errors + cdy_rt.primitives.to_list((str(ctx.where) + ': ' + str(msg)))))

def check__show(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> str:
    _cdy_t167: object = check__resolve_type(t, subst)
    if isinstance(_cdy_t167, core__TCon):
        name = _cdy_t167.name
        args = _cdy_t167.args
        if (len(args) == 0):
            return check__shown_name(name)
        else:
            return ('(' + str(check__shown_name(name)) + ' ' + str(cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda a: check__show(a, subst)), args), ' ')) + ')')
    elif isinstance(_cdy_t167, core__TFn):
        params = _cdy_t167.params
        ret = _cdy_t167.ret
        return ('(Fn (' + str(cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda p: check__show(p, subst)), params), ' ')) + ') ' + str(check__show(ret, subst)) + ')')
    else:
        assert isinstance(_cdy_t167, core__TVar)
        _cdy_name_460 = _cdy_t167.name
        if check__is_flexible(_cdy_name_460):
            return ('t' + _cdy_name_460[1:len(_cdy_name_460)])
        else:
            return _cdy_name_460

def check__shown_name(name: str) -> str:
    parts = cdy_rt.primitives.split(name, '__')
    if (len(parts) == 1):
        return name
    else:
        return cdy_rt.primitives.join(prelude__rest(parts), '__')

class Ready(_cdy_NamedTuple):
    module: include__Module
    forms: tuple[form__Form, ...]
    macros: _cdy_Mapping[str, form__Macro]
    exports: core__Exports

def translate_modules(modules: tuple[include__Module, ...], parse: _cdy_Callable[[str], tuple[form__Form, ...]]) -> str:
    return python_of(program_tops(modules, parse, expand__library_builtins(None)))

def program_tops(modules: tuple[include__Module, ...], parse: _cdy_Callable[[str], tuple[form__Form, ...]], builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[core__Top, ...]:
    ready = expand_modules(modules, (len(modules) - 1), ())
    by_key = exports_by_key(ready, {})
    elsewhere = core__elsewhere_names(exports_of(ready, ()), {})
    return analyse_modules(ready, by_key, elsewhere, builtins, parse, ())

def type_survey(path: str) -> tuple[str, ...]:
    builtins = expand__library_builtins(None)
    return check__check_program(program_tops(include__read_modules(path), read__read_forms, builtins), builtins)

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
