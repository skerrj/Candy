from __future__ import annotations

from collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping
from typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple, cast as _cdy_cast
import math
import re
import cdy_rt.spelling
import cdy_rt.primitives

cdy_rt.primitives.stop_on_panic()

def prelude__rest[a](xs: tuple[a, ...]) -> tuple[a, ...]:
    return cdy_rt.primitives.list_drop(1, xs)

class prelude__Some[a](_cdy_NamedTuple):
    v: a
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(prelude__Some, 'Some', ('a',), ("'a",))

class prelude__None(_cdy_NamedTuple):
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(prelude__None, 'None', ('a',), ())
type prelude__Maybe[a] = prelude__Some[a] | prelude__None

class prelude__Ok[a](_cdy_NamedTuple):
    v: a
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(prelude__Ok, 'Ok', ('a', 'e'), ("'a",))

class prelude__Err[e](_cdy_NamedTuple):
    err: e
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(prelude__Err, 'Err', ('a', 'e'), ("'e",))
type prelude__Result[a, e] = prelude__Ok[a] | prelude__Err[e]

def prelude__find[a](keep: _cdy_Callable[[a], bool], xs: tuple[a, ...]) -> prelude__Maybe[a]:
    i = cdy_rt.primitives.list_find_index(keep, xs)
    if (i < 0):
        return prelude__None()
    else:
        return prelude__Some(cdy_rt.primitives.at(xs, i))

def prelude__index_of[a](x: a, xs: tuple[a, ...]) -> prelude__Maybe[int]:
    i = cdy_rt.primitives.list_elem_index(x, xs)
    if (i < 0):
        return prelude__None()
    else:
        return prelude__Some(i)

def prelude__with_default[a](fallback: a, m: prelude__Maybe[a]) -> a:
    _cdy_t0 = m
    if isinstance(_cdy_t0, prelude__Some):
        v: a = _cdy_t0.v
        return v
    elif isinstance(_cdy_t0, prelude__None):
        return fallback

def prelude__map_update[k, v](m: _cdy_Mapping[k, v], key: k, f: _cdy_Callable[[v], v]) -> _cdy_Mapping[k, v]:
    return cdy_rt.primitives.map_set(m, key, f(cdy_rt.primitives.map_get(m, key)))

class form__Pos(_cdy_NamedTuple):
    file: str
    line: int
    col: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Pos, 'Pos', (), ('String', 'Int', 'Int'))
form__NOWHERE: form__Pos = form__Pos('', 0, 0)

class form__Sym(_cdy_NamedTuple):
    name: str
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Sym, 'Sym', (), ('String', 'form__Pos'))

class form__Lst(_cdy_NamedTuple):
    items: tuple[form__Form, ...]
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Lst, 'Lst', (), (('List', 'form__Form'), 'form__Pos'))

class form__Txt(_cdy_NamedTuple):
    val: str
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Txt, 'Txt', (), ('String', 'form__Pos'))

class form__IntLit(_cdy_NamedTuple):
    val: int
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__IntLit, 'IntLit', (), ('Int', 'form__Pos'))

class form__LongLit(_cdy_NamedTuple):
    val: int
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__LongLit, 'LongLit', (), ('Int', 'form__Pos'))

class form__ByteLit(_cdy_NamedTuple):
    val: int
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__ByteLit, 'ByteLit', (), ('Int', 'form__Pos'))

class form__FloatLit(_cdy_NamedTuple):
    val: float
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__FloatLit, 'FloatLit', (), ('Double', 'form__Pos'))

class form__DoubleLit(_cdy_NamedTuple):
    val: float
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__DoubleLit, 'DoubleLit', (), ('Double', 'form__Pos'))

class form__CharLit(_cdy_NamedTuple):
    val: str
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__CharLit, 'CharLit', (), ('Char', 'form__Pos'))

class form__BoolLit(_cdy_NamedTuple):
    val: bool
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__BoolLit, 'BoolLit', (), ('Bool', 'form__Pos'))
type form__Form = form__Sym | form__Lst | form__Txt | form__IntLit | form__LongLit | form__ByteLit | form__FloatLit | form__DoubleLit | form__CharLit | form__BoolLit

def form__sym_name(form: form__Form) -> str:
    _cdy_t1: object = form
    if isinstance(_cdy_t1, form__Sym):
        name = _cdy_t1.name
        return name
    else:
        return ''

def form__list_items(form: form__Form) -> tuple[form__Form, ...]:
    _cdy_t2: object = form
    if isinstance(_cdy_t2, form__Lst):
        items = _cdy_t2.items
        return items
    else:
        return ()

def form__rest_of(forms: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    return cdy_rt.primitives.list_drop(1, forms)

def form__form_pos(form: form__Form) -> form__Pos:
    _cdy_t3: object = form
    if isinstance(_cdy_t3, form__Sym):
        pos = _cdy_t3.pos
        return pos
    elif isinstance(_cdy_t3, form__Lst):
        _cdy_pos_7 = _cdy_t3.pos
        return _cdy_pos_7
    elif isinstance(_cdy_t3, form__Txt):
        _cdy_pos_8 = _cdy_t3.pos
        return _cdy_pos_8
    elif isinstance(_cdy_t3, form__IntLit):
        _cdy_pos_9 = _cdy_t3.pos
        return _cdy_pos_9
    elif isinstance(_cdy_t3, form__LongLit):
        _cdy_pos_10 = _cdy_t3.pos
        return _cdy_pos_10
    elif isinstance(_cdy_t3, form__ByteLit):
        _cdy_pos_11 = _cdy_t3.pos
        return _cdy_pos_11
    elif isinstance(_cdy_t3, form__FloatLit):
        _cdy_pos_12 = _cdy_t3.pos
        return _cdy_pos_12
    elif isinstance(_cdy_t3, form__DoubleLit):
        _cdy_pos_13 = _cdy_t3.pos
        return _cdy_pos_13
    elif isinstance(_cdy_t3, form__CharLit):
        _cdy_pos_14 = _cdy_t3.pos
        return _cdy_pos_14
    else:
        assert isinstance(_cdy_t3, form__BoolLit)
        _cdy_pos_15 = _cdy_t3.pos
        return _cdy_pos_15

def form__pos_text(pos: form__Pos) -> str:
    line = pos.line
    col = pos.col
    file = pos.file
    if (line == 0):
        return ''
    elif (file == ''):
        return ('line ' + str(line) + ', column ' + str(col) + ': ')
    else:
        return (file + ':' + str(line) + ':' + str(col) + ': ')

def form__gensym(prefix: str) -> form__Form:
    return form__Sym(cdy_rt.primitives.fresh_name(prefix), form__NOWHERE)

class form__Macro(_cdy_NamedTuple):
    name: str
    arity: int
    run: _cdy_Any
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Macro, 'Macro', (), ('String', 'Int', 'Any', 'form__Pos'))

def read__read_forms(text: str) -> tuple[form__Form, ...]:
    return read__read_all(read__Source('', (), form__NOWHERE), text, read__skip(text, 0), ())

def read__read_source(file: str, text: str) -> tuple[form__Form, ...]:
    return read__read_all(read__Source(file, read__line_starts(text, 0, cdy_rt.primitives.to_list(0)), form__Pos(file, 1, 1)), text, read__skip(text, 0), ())

def read__read_hole(text: str, where: form__Pos) -> tuple[form__Form, ...]:
    if (where.line == 0):
        return read__read_forms(text)
    else:
        return read__read_all(read__Source(where.file, read__line_starts(text, 0, cdy_rt.primitives.to_list(0)), where), text, read__skip(text, 0), ())

class read__Source(_cdy_NamedTuple):
    file: str
    starts: tuple[int, ...]
    base: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(read__Source, 'Source', (), ('String', ('List', 'Int'), 'form__Pos'))

def read__line_starts(text: str, pos: int, acc: tuple[int, ...]) -> tuple[int, ...]:
    while True:
        if (pos >= len(text)):
            return acc
        elif (read__char_text(text, pos) == '\n'):
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
        return form__Pos(src.file, (i + src.base.line), ((pos - cdy_rt.primitives.at(starts, i)) + (src.base.col if (i == 0) else 1)))

def read__line_of(starts: tuple[int, ...], pos: int, lo: int, hi: int) -> int:
    while True:
        if ((hi - lo) <= 1):
            return lo
        else:
            mid = ((lo + hi) // 2)
            if (cdy_rt.primitives.at(starts, mid) <= pos):
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
        elif (cdy_rt.primitives.char_at(text, pos) == ';'):
            pos = read__line_end(text, pos)
            continue
        else:
            return pos

def read__line_end(text: str, pos: int) -> int:
    while True:
        if ((pos >= len(text)) or (read__char_text(text, pos) == '\n')):
            return pos
        else:
            pos = (pos + 1)
            continue

def read__ends_at(text: str, pos: int) -> bool:
    return ((pos >= len(text)) or cdy_rt.primitives.isspace_at(text, pos) or cdy_rt.primitives.str_contains(read__char_text(text, pos), '();'))

def read__word_end(text: str, pos: int) -> int:
    while True:
        if read__ends_at(text, pos):
            return pos
        else:
            pos = (pos + 1)
            continue

def read__char_text(s: str, i: int) -> str:
    return cdy_rt.primitives.char_at(s, i)

def read__read_form(src: read__Source, text: str, pos: int) -> tuple[form__Form, int]:
    ch = cdy_rt.primitives.char_at(text, pos)
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
        elif (cdy_rt.primitives.char_at(text, pos) == ')'):
            return (form__Lst(acc, read__pos_at(src, start)), (pos + 1))
        else:
            _tup = read__read_form(src, text, pos)
            form = _tup[0]
            next_ = _tup[1]
            pos, acc = (read__skip(text, next_), (acc + cdy_rt.primitives.to_list(form)))
            continue

def read__read_char(src: read__Source, text: str, pos: int) -> tuple[form__Form, int]:
    if (((pos + 1) < len(text)) and (not cdy_rt.primitives.isspace_at(text, (pos + 1))) and read__ends_at(text, (pos + 2))):
        return (form__CharLit(cdy_rt.primitives.char_at(text, (pos + 1)), read__pos_at(src, pos)), (pos + 2))
    else:
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, 'a char is \\ and one character, then a delimiter'))

def read__read_atom(src: read__Source, text: str, pos: int, end: int) -> tuple[form__Form, int]:
    word = cdy_rt.primitives.substring(text, pos, end)
    kind = read__number_kind(word)
    if (kind != ''):
        return (read__number_form(src, text, pos, word, kind), end)
    elif (word == 'true'):
        return (form__BoolLit(True, read__pos_at(src, pos)), end)
    elif (word == 'false'):
        return (form__BoolLit(False, read__pos_at(src, pos)), end)
    elif read__symbol_start(read__char_text(text, pos)):
        stop = read__symbol_end(text, (pos + 1))
        name = cdy_rt.primitives.substring(text, pos, stop)
        if cdy_rt.primitives.str_contains('__', name):
            return cdy_rt.primitives.fail(read__parse_error(src, text, pos, "a name can't contain __ (only gensym makes such names)"))
        else:
            return (form__Sym(name, read__pos_at(src, pos)), stop)
    else:
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, ('unexpected ' + cdy_rt.primitives.char_at(text, pos))))

def read__symbol_start(ch: str) -> bool:
    return (not (cdy_rt.primitives.str_contains(ch, '\'#"\\') or cdy_rt.primitives.is_decimal(ch)))

def read__symbol_end(text: str, pos: int) -> int:
    while True:
        if ((pos >= len(text)) or cdy_rt.primitives.isspace_at(text, pos) or cdy_rt.primitives.str_contains(read__char_text(text, pos), '()\'";\\')):
            return pos
        else:
            pos = (pos + 1)
            continue

def read__digits_end(word: str, pos: int) -> int:
    while True:
        if ((pos < len(word)) and cdy_rt.primitives.is_decimal(read__char_text(word, pos))):
            pos = (pos + 1)
            continue
        else:
            return pos

def read__number_kind(word: str) -> str:
    start = (1 if (word[0] == '-') else 0)
    i = read__digits_end(word, start)
    rest = cdy_rt.primitives.substring(word, i, len(word))
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
        tail = cdy_rt.primitives.substring(word, read__exponent_end(word, j), len(word))
        if ((j == (i + 1)) or (read__exponent_end(word, j) == 0)):
            return ''
        elif (tail == ''):
            return 'double'
        elif (tail == 'f'):
            return 'float'
        else:
            return ''
    else:
        return ''

def read__exponent_end(word: str, pos: int) -> int:
    if ((pos < len(word)) and (cdy_rt.primitives.char_at(word, pos) == 'e')):
        start = ((pos + 2) if (((pos + 1) < len(word)) and (cdy_rt.primitives.char_at(word, (pos + 1)) == '-')) else (pos + 1))
        end = read__digits_end(word, start)
        if (end == start):
            return 0
        else:
            return end
    else:
        return pos

def read__number_form(src: read__Source, text: str, pos: int, word: str, kind: str) -> form__Form:
    body = cdy_rt.primitives.substring(word, 0, (len(word) - 1))
    where = read__pos_at(src, pos)
    form = (form__IntLit(cdy_rt.primitives.to_int(word), where) if (kind == 'int') else (form__LongLit(cdy_rt.primitives.to_int(body), where) if (kind == 'long') else (form__ByteLit(cdy_rt.primitives.to_int(body), where) if (kind == 'byte') else (form__DoubleLit(cdy_rt.primitives.to_float(word), where) if (kind == 'double') else form__FloatLit(cdy_rt.primitives.to_float(body), where)))))
    range_ = read__number_range(form)
    if (range_ == ''):
        return form
    else:
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, (word + ' is out of range: ' + range_)))

def read__number_range(form: form__Form) -> str:
    _cdy_t4: object = form
    if isinstance(_cdy_t4, form__IntLit):
        v = _cdy_t4.val
        if ((v >= (0 - cdy_rt.primitives.to_int('2147483648'))) and (v <= cdy_rt.primitives.to_int('2147483647'))):
            return ''
        else:
            return 'an Int is -2147483648 to 2147483647'
    elif isinstance(_cdy_t4, form__LongLit):
        _cdy_v_83 = _cdy_t4.val
        if ((_cdy_v_83 >= (0 - cdy_rt.primitives.to_int('9223372036854775808'))) and (_cdy_v_83 <= cdy_rt.primitives.to_int('9223372036854775807'))):
            return ''
        else:
            return 'a Long is -9223372036854775808 to 9223372036854775807'
    elif isinstance(_cdy_t4, form__ByteLit):
        _cdy_v_84 = _cdy_t4.val
        if ((_cdy_v_84 >= 0) and (_cdy_v_84 <= 255)):
            return ''
        else:
            return 'a Byte is 0 to 255'
    elif isinstance(_cdy_t4, form__FloatLit):
        _cdy_v_85 = _cdy_t4.val
        if ((0.0 - cdy_rt.primitives.to_float('3.4028234663852886e38')) <= _cdy_v_85 <= cdy_rt.primitives.to_float('3.4028234663852886e38')):
            return ''
        else:
            return 'a Float is -3.4028234663852886e38 to 3.4028234663852886e38'
    elif isinstance(_cdy_t4, form__DoubleLit):
        _cdy_v_86 = _cdy_t4.val
        if ((0.0 - cdy_rt.primitives.to_float('1.7976931348623157e308')) <= _cdy_v_86 <= cdy_rt.primitives.to_float('1.7976931348623157e308')):
            return ''
        else:
            return 'a Double is -1.7976931348623157e308 to 1.7976931348623157e308'
    else:
        return ''

def read__read_str(src: read__Source, text: str, pos: int, acc: str, start: int) -> tuple[form__Form, int]:
    while True:
        if (pos >= len(text)):
            return cdy_rt.primitives.fail(read__parse_error(src, text, start, 'string is never closed'))
        elif (cdy_rt.primitives.char_at(text, pos) == '"'):
            return (form__Txt(acc, read__pos_at(src, start)), (pos + 1))
        elif (cdy_rt.primitives.char_at(text, pos) == '\\'):
            _tup = read__escape(src, text, pos)
            ch = _tup[0]
            next_ = _tup[1]
            pos, acc = (next_, (acc + ch))
            continue
        else:
            pos, acc = ((pos + 1), (acc + read__char_text(text, pos)))
            continue

def read__escape(src: read__Source, text: str, pos: int) -> tuple[str, int]:
    c = (read__char_text(text, (pos + 1)) if ((pos + 1) < len(text)) else '')
    if cdy_rt.primitives.list_contains(c, ('\\', '/', '"')):
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
        return (cdy_rt.primitives.hex_char(cdy_rt.primitives.substring(text, (pos + 2), (pos + 6))), (pos + 6))
    else:
        return cdy_rt.primitives.fail(read__parse_error(src, text, pos, 'bad escape sequence'))

def read__all_hex(text: str, pos: int, end: int) -> bool:
    while True:
        if (pos >= end):
            return True
        elif cdy_rt.primitives.str_contains(read__char_text(text, pos), '0123456789abcdefABCDEF'):
            pos = (pos + 1)
            continue
        else:
            return False

def read__parse_error(src: read__Source, text: str, pos: int, msg: str) -> str:
    _tup = read__row_col(text, 0, pos, 1, 1)
    row = _tup[0]
    col = _tup[1]
    return (form__pos_text(form__Pos(src.file, row, col)) + 'parse error: ' + msg)

def read__row_col(text: str, i: int, pos: int, row: int, col: int) -> tuple[int, int]:
    while True:
        if (i >= pos):
            return (row, col)
        elif (read__char_text(text, i) == '\n'):
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
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(include__Module, 'Module', (), ('String', 'String', 'String', ('List', 'form__Form'), ('List', 'include__Imp')))

class include__Imp(_cdy_NamedTuple):
    key: str
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(include__Imp, 'Imp', (), ('String', 'form__Pos'))

class include__Mods(_cdy_NamedTuple):
    done: tuple[include__Module, ...]
    seen: _cdy_Mapping[str, bool]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(include__Mods, 'Mods', (), (('List', 'include__Module'), ('Map', 'String', 'Bool')))

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
        return cdy_rt.primitives.fail(('the translator needs ' + name + ' next to it, in ' + dir_))

def include__module_imports(forms: tuple[form__Form, ...], dir_: str, acc: tuple[tuple[str, include__Imp], ...]) -> tuple[tuple[str, include__Imp], ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            name = include__import_name(form)
            _cdy_t6 = prelude__rest(forms)
            if (name == ''):
                _cdy_t5 = acc
            else:
                path = include__import_path('import', dir_, name, form__form_pos(form))
                _cdy_t5 = (acc + cdy_rt.primitives.to_list((path, include__Imp(cdy_rt.primitives.path_resolve(path), form__form_pos(form)))))
            forms, acc = (_cdy_t6, _cdy_t5)
            continue

def include__imp_list(imports: tuple[tuple[str, include__Imp], ...], acc: tuple[include__Imp, ...]) -> tuple[include__Imp, ...]:
    while True:
        if (len(imports) == 0):
            return acc
        else:
            _tup = imports[0]
            _name = _tup[0]
            imp = _tup[1]
            imports, acc = (prelude__rest(imports), (acc + cdy_rt.primitives.to_list(imp)))
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
            imports, acc = (prelude__rest(imports), (cdy_rt.primitives.fail((form__pos_text(imp.pos) + 'import: cycle ' + include__cycle_text(stack, key))) if cdy_rt.primitives.list_contains(key, stack) else (acc if cdy_rt.primitives.map_has(acc.seen, key) else include__add_module(path, key, read__read_source(path, cdy_rt.primitives.slurp(path)), cdy_rt.primitives.path_dir(path), stack, acc))))
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
    checked = include__unique_stems(cdy_rt.primitives.slice_(modules, 0, (len(modules) - 1)), {})
    return modules

def include__unique_stems(modules: tuple[include__Module, ...], seen: _cdy_Mapping[str, str]) -> bool:
    while True:
        if (len(modules) == 0):
            return True
        else:
            m = modules[0]
            stem = m.stem
            if cdy_rt.primitives.map_has(seen, stem):
                return cdy_rt.primitives.fail(('import: two modules are named ' + stem + ': ' + cdy_rt.primitives.map_get(seen, stem) + ' and ' + m.path))
            else:
                modules, seen = (prelude__rest(modules), cdy_rt.primitives.map_set(seen, stem, m.path))
                continue

class include__Incl(_cdy_NamedTuple):
    done: tuple[form__Form, ...]
    seen: _cdy_Mapping[str, bool]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(include__Incl, 'Incl', (), (('List', 'form__Form'), ('Map', 'String', 'Bool')))

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
        return form__Lst((items[0], form__Txt(include__import_path('import-macros', dir_, form__sym_name(items[1]), pos), pos)), pos)
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
        return cdy_rt.primitives.fail((form__pos_text(pos) + what + ": can't find " + name + '.cdy in ' + dir_))

class core__TCon(_cdy_NamedTuple):
    name: str
    args: tuple[core__CType, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TCon, 'TCon', (), ('String', ('List', 'core__CType')))

class core__TVar(_cdy_NamedTuple):
    name: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TVar, 'TVar', (), ('String',))

class core__TFn(_cdy_NamedTuple):
    params: tuple[core__CType, ...]
    ret: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TFn, 'TFn', (), (('List', 'core__CType'), 'core__CType'))
type core__CType = core__TCon | core__TVar | core__TFn

class core__Lit(_cdy_NamedTuple):
    form: form__Form
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Lit, 'Lit', (), ('form__Form', 'core__CType'))

class core__Local(_cdy_NamedTuple):
    name: str
    id_: int
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Local, 'Local', (), ('String', 'Int', 'form__Pos', 'core__CType'))

class core__Global(_cdy_NamedTuple):
    name: str
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Global, 'Global', (), ('String', 'form__Pos', 'core__CType'))

class core__Prim(_cdy_NamedTuple):
    name: str
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Prim, 'Prim', (), ('String', 'form__Pos', 'core__CType'))

class core__Call(_cdy_NamedTuple):
    callee: core__Expr
    args: tuple[core__Expr, ...]
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Call, 'Call', (), ('core__Expr', ('List', 'core__Expr'), 'form__Pos', 'core__CType'))

class core__If(_cdy_NamedTuple):
    test: core__Expr
    then: core__Expr
    other: core__Expr
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__If, 'If', (), ('core__Expr', 'core__Expr', 'core__Expr', 'form__Pos', 'core__CType'))

class core__Do(_cdy_NamedTuple):
    body: tuple[core__Expr, ...]
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Do, 'Do', (), (('List', 'core__Expr'), 'form__Pos', 'core__CType'))

class core__Lambda(_cdy_NamedTuple):
    params: tuple[core__Expr, ...]
    body: core__Expr
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Lambda, 'Lambda', (), (('List', 'core__Expr'), 'core__Expr', 'form__Pos', 'core__CType'))

class core__Tuple(_cdy_NamedTuple):
    items: tuple[core__Expr, ...]
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Tuple, 'Tuple', (), (('List', 'core__Expr'), 'form__Pos', 'core__CType'))

class core__ListOf(_cdy_NamedTuple):
    items: tuple[core__Expr, ...]
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__ListOf, 'ListOf', (), (('List', 'core__Expr'), 'form__Pos', 'core__CType'))

class core__Fmt(_cdy_NamedTuple):
    parts: tuple[core__FPart, ...]
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Fmt, 'Fmt', (), (('List', 'core__FPart'), 'form__Pos', 'core__CType'))

class core__Field(_cdy_NamedTuple):
    obj: core__Expr
    field: str
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Field, 'Field', (), ('core__Expr', 'String', 'form__Pos', 'core__CType'))

class core__Assoc(_cdy_NamedTuple):
    obj: core__Expr
    fields: tuple[tuple[str, core__Expr], ...]
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Assoc, 'Assoc', (), ('core__Expr', ('List', ('Tup', 'String', 'core__Expr')), 'form__Pos', 'core__CType'))

class core__MatchE(_cdy_NamedTuple):
    subject: core__Expr
    clauses: tuple[core__Clause, ...]
    default: tuple[core__Expr, ...]
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__MatchE, 'MatchE', (), ('core__Expr', ('List', 'core__Clause'), ('List', 'core__Expr'), 'form__Pos', 'core__CType'))

class core__Temp(_cdy_NamedTuple):
    id_: int
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Temp, 'Temp', (), ('Int', 'core__CType'))
type core__Expr = core__Lit | core__Local | core__Global | core__Prim | core__Call | core__If | core__Do | core__Lambda | core__Tuple | core__ListOf | core__Fmt | core__Field | core__Assoc | core__MatchE | core__Temp
core__ANY: core__CType = core__TCon('Any', ())

class core__Clause(_cdy_NamedTuple):
    variant: str
    binds: tuple[tuple[str, core__Expr], ...]
    body: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Clause, 'Clause', (), ('String', ('List', ('Tup', 'String', 'core__Expr')), 'core__Expr'))

class core__FText(_cdy_NamedTuple):
    text: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__FText, 'FText', (), ('String',))

class core__FHole(_cdy_NamedTuple):
    expr: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__FHole, 'FHole', (), ('core__Expr',))
type core__FPart = core__FText | core__FHole

class core__Variant(_cdy_NamedTuple):
    name: str
    fields: tuple[tuple[str, core__CType], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Variant, 'Variant', (), ('String', ('List', ('Tup', 'String', 'core__CType'))))

class core__TDeft(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TDeft, 'TDeft', (), ('String', ('List', 'String'), ('List', ('Tup', 'String', 'core__CType'))))

class core__TDeftSum(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    variants: tuple[core__Variant, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TDeftSum, 'TDeftSum', (), ('String', ('List', 'String'), ('List', 'core__Variant')))

class core__TDef(_cdy_NamedTuple):
    name: str
    init: core__Expr
    t: core__CType
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TDef, 'TDef', (), ('String', 'core__Expr', 'core__CType', 'form__Pos'))

class core__TDefn(_cdy_NamedTuple):
    name: str
    params: tuple[core__Expr, ...]
    body: core__Expr
    t: core__CType
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TDefn, 'TDefn', (), ('String', ('List', 'core__Expr'), 'core__Expr', 'core__CType', 'form__Pos'))

class core__TExpr(_cdy_NamedTuple):
    expr: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TExpr, 'TExpr', (), ('core__Expr',))
type core__Top = core__TDeft | core__TDeftSum | core__TDef | core__TDefn | core__TExpr
core__NIL: core__Expr = core__Prim('nil', form__NOWHERE, core__ANY)

class core__Scope(_cdy_NamedTuple):
    env: _cdy_Mapping[str, core__Expr]
    top: _cdy_Mapping[str, bool]
    parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]]
    variants: _cdy_Mapping[str, core__VInfo]
    sums: _cdy_Mapping[str, tuple[str, ...]]
    here: form__Pos
    macros: _cdy_Mapping[str, form__Macro]
    quoting: bool
    names: _cdy_Mapping[str, str]
    elsewhere: _cdy_Mapping[str, str]
    builtins: _cdy_Mapping[str, core__Builtin]
    types: _cdy_Mapping[str, int]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Scope, 'Scope', (), (('Map', 'String', 'core__Expr'), ('Map', 'String', 'Bool'), 'Fn', ('Map', 'String', 'core__VInfo'), ('Map', 'String', ('List', 'String')), 'form__Pos', ('Map', 'String', 'form__Macro'), 'Bool', ('Map', 'String', 'String'), ('Map', 'String', 'String'), ('Map', 'String', 'core__Builtin'), ('Map', 'String', 'Int')))

def core__at_pos(scope: core__Scope, pos: form__Pos) -> core__Scope:
    if (pos.line == 0):
        return scope
    else:
        return scope._replace(here=pos)

def core__located(scope: core__Scope, msg: str) -> str:
    return (form__pos_text(scope.here) + msg)

def core__bind_local(scope: core__Scope, name: str, loc: core__Expr) -> core__Scope:
    if cdy_rt.primitives.map_has(scope.macros, name):
        return cdy_rt.primitives.fail(core__located(scope, (name + " is a macro, so it can't be bound")))
    else:
        return scope._replace(env=cdy_rt.primitives.map_set(scope.env, name, loc))

class core__VInfo(_cdy_NamedTuple):
    sum_: str
    fields: tuple[str, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__VInfo, 'VInfo', (), ('String', ('List', 'String')))

def core__is_variant(name: str, scope: core__Scope) -> bool:
    return (cdy_rt.primitives.map_has(scope.variants, name) and (not cdy_rt.primitives.map_has(scope.env, name)))

def core__variant_fields(name: str, scope: core__Scope) -> tuple[str, ...]:
    return cdy_rt.primitives.map_get(scope.variants, name).fields

def core__analyse_expr(form: form__Form, scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _cdy_t7: object = form
    if isinstance(_cdy_t7, form__Sym):
        name = _cdy_t7.name
        pos = _cdy_t7.pos
        return (core__resolve(name, core__at_pos(scope, pos)), n)
    elif isinstance(_cdy_t7, form__Lst):
        items = _cdy_t7.items
        _cdy_pos_17 = _cdy_t7.pos
        return core__analyse_list(items, core__at_pos(scope, _cdy_pos_17), n)
    else:
        return (core__Lit(form, core__ANY), n)

def core__analyse_all(forms: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[tuple[core__Expr, ...], int]:
    def _cdy_t8(k: int, form: form__Form) -> tuple[int, core__Expr]:
        _cdy__tup_23 = core__analyse_expr(form, scope, k)
        e = _cdy__tup_23[0]
        k1 = _cdy__tup_23[1]
        return (k1, e)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t8, n, forms)
    n1 = _tup[0]
    es = _tup[1]
    return (es, n1)

def core__resolve(name: str, scope: core__Scope) -> core__Expr:
    if cdy_rt.primitives.map_has(scope.env, name):
        return core__at_use(cdy_rt.primitives.map_get(scope.env, name), scope.here)
    elif (core__is_variant(name, scope) and (len(core__variant_fields(name, scope)) == 0)):
        return core__Call(core__Global(core__global_name(name, scope.names), scope.here, core__ANY), (), scope.here, core__ANY)
    elif (cdy_rt.primitives.map_has(scope.top, name) and cdy_rt.primitives.map_get(scope.top, name)):
        return core__Global(core__global_name(name, scope.names), scope.here, core__ANY)
    elif core__is_special(name, scope.builtins):
        return cdy_rt.primitives.fail(core__located(scope, (name + ' is a special form, not a value')))
    elif (cdy_rt.primitives.map_has(scope.builtins, name) and (not core__is_builtin_type(name, scope.builtins))):
        return core__Prim(name, scope.here, core__ANY)
    elif cdy_rt.primitives.map_has(scope.elsewhere, name):
        stem = cdy_rt.primitives.map_get(scope.elsewhere, name)
        return cdy_rt.primitives.fail(core__located(scope, (name + ' is not defined here; ' + stem + " defines it, but this file doesn't import " + stem)))
    else:
        return cdy_rt.primitives.fail(core__located(scope, ('unknown name ' + name)))

def core__at_use(e: core__Expr, pos: form__Pos) -> core__Expr:
    _cdy_t9: object = e
    if isinstance(_cdy_t9, core__Local):
        name = _cdy_t9.name
        id_ = _cdy_t9.id_
        return core__Local(name, id_, pos, core__ANY)
    else:
        return e

def core__global_name(name: str, names: _cdy_Mapping[str, str]) -> str:
    if cdy_rt.primitives.map_has(names, name):
        return cdy_rt.primitives.map_get(names, name)
    else:
        return name

def core__is_special_head(name: str, scope: core__Scope) -> bool:
    return ((not cdy_rt.primitives.map_has(scope.env, name)) and (core__is_special(name, scope.builtins) or cdy_rt.primitives.list_contains(name, core__BUILTIN_CONSTRUCTORS)))
core__BUILTIN_CONSTRUCTORS: tuple[str, ...] = ('List', 'Tup')

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
            _cdy__tup_48 = core__analyse_all(prelude__rest(items), scope, n1)
            args = _cdy__tup_48[0]
            n2 = _cdy__tup_48[1]
            arity_ok = core__check_call(callee, len(args), scope)
            return (core__Call(callee, args, scope.here, core__ANY), n2)

def core__check_call(callee: core__Expr, count: int, scope: core__Scope) -> bool:
    _cdy_t10: object = callee
    if isinstance(_cdy_t10, core__Prim):
        name = _cdy_t10.name
        builtin = cdy_rt.primitives.map_get(scope.builtins, name)
        _cdy_t12: object = builtin
        if isinstance(_cdy_t12, core__Typed):
            type_ = _cdy_t12.type_
            _cdy_t11 = core__is_variadic(type_)
        else:
            _cdy_t11 = False
        rest_of_type = _cdy_t11
        _cdy_t14: object = builtin
        if isinstance(_cdy_t14, core__Typed):
            _cdy_type__59 = _cdy_t14.type_
            _cdy_t13 = core__fn_arity(_cdy_type__59)
        else:
            _cdy_t13 = -1
        arity = _cdy_t13
        if rest_of_type:
            if (count < (arity - 1)):
                return cdy_rt.primitives.fail(core__located(scope, ('(' + name + ' ...) takes at least ' + str((arity - 1)) + ' argument(s), got ' + str(count))))
            else:
                return True
        elif ((arity >= 0) and (arity != count)):
            return cdy_rt.primitives.fail(core__located(scope, ('(' + name + ' ...) takes ' + str(arity) + ' argument(s), got ' + str(count))))
        else:
            return True
    else:
        return True

def core__check_variant_call(name: str, count: int, scope: core__Scope) -> bool:
    if (not core__is_variant(name, scope)):
        return True
    elif (len(core__variant_fields(name, scope)) == 0):
        return cdy_rt.primitives.fail(core__located(scope, (name + ' has no fields, so it is a value: write ' + name + ', not (' + name + ')')))
    elif (count != len(core__variant_fields(name, scope))):
        return cdy_rt.primitives.fail(core__located(scope, ('(' + name + ' ...) takes ' + str(len(core__variant_fields(name, scope))) + ' field(s), got ' + str(count))))
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
    elif (head == 'Tup'):
        return core__an_tup(args, scope, n)
    elif (head == 'List'):
        return core__an_list(args, scope, n)
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
    elif cdy_rt.primitives.list_contains(head, ('unq', 'unq-sp')):
        return cdy_rt.primitives.fail(core__located(scope, (head + ': only inside quasi')))
    elif cdy_rt.primitives.list_contains(head, ('def', 'defn', 'deft', 'sig', 'import', 'import-macros', 'defmacro')):
        return cdy_rt.primitives.fail(core__located(scope, (head + ' is only allowed at top level')))
    else:
        return cdy_rt.primitives.fail(core__located(scope, (head + ' is not supported by the Candy translator yet')))

def core__an_if(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__analyse_all(args, scope, n)
    parts = _tup[0]
    n1 = _tup[1]
    if (len(parts) == 2):
        return (core__If(parts[0], parts[1], core__NIL, scope.here, core__ANY), n1)
    elif (len(parts) == 3):
        return (core__If(parts[0], parts[1], parts[2], scope.here, core__ANY), n1)
    else:
        return cdy_rt.primitives.fail(core__located(scope, 'if: expected (if test then else?)'))

def core__is_else(form: form__Form) -> bool:
    return (form__sym_name(form) == 'else')

def core__an_do(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__analyse_all(args, scope, n)
    body = _tup[0]
    n1 = _tup[1]
    if (len(body) == 0):
        return (core__NIL, n1)
    elif (len(body) == 1):
        return (body[0], n1)
    else:
        return (core__Do(body, scope.here, core__ANY), n1)

def core__an_let(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if ((len(args) != 2) or (not core__is_list_form(args[0]))):
        return cdy_rt.primitives.fail(core__located(scope, 'let: expected (let ((name init)*) body)'))
    elif (len(form__list_items(args[0])) == 0):
        return core__analyse_expr(args[1], scope, n)
    else:
        _tup = core__let_bindings(form__list_items(args[0]), scope, n)
        pairs = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_88 = core__analyse_expr(args[1], inner, n1)
        body = _cdy__tup_88[0]
        n2 = _cdy__tup_88[1]
        return (core__nest(pairs, body, scope.here), n2)

def core__is_list_form(form: form__Form) -> bool:
    _cdy_t15: object = form
    if isinstance(_cdy_t15, form__Lst):
        return True
    else:
        return False

def core__let_bindings(bindings: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    _tup = cdy_rt.primitives.list_map_acc(core__let_binding, (scope, n), bindings)
    last = _tup[0]
    pairs = _tup[1]
    _cdy__tup_98 = last
    sc = _cdy__tup_98[0]
    k = _cdy__tup_98[1]
    return (cdy_rt.primitives.list_concat(pairs), sc, k)

def core__let_binding(state: tuple[core__Scope, int], binding: form__Form) -> tuple[tuple[core__Scope, int], tuple[tuple[core__Expr, core__Expr], ...]]:
    _tup = state
    scope = _tup[0]
    n = _tup[1]
    items = form__list_items(binding)
    if (len(items) != 2):
        return cdy_rt.primitives.fail(core__located(scope, 'let: binding must be (name init)'))
    else:
        _cdy__tup_107 = core__analyse_expr(items[1], scope, n)
        init = _cdy__tup_107[0]
        n1 = _cdy__tup_107[1]
        target = items[0]
        _cdy_t16: object = target
        if isinstance(_cdy_t16, form__Lst):
            names = _cdy_t16.items
            tmp = core__Local('_tup', n1, scope.here, core__ANY)
            _cdy__tup_113 = core__destructure(names, tmp, scope, (n1 + 1))
            more = _cdy__tup_113[0]
            inner = _cdy__tup_113[1]
            n2 = _cdy__tup_113[2]
            return ((inner, n2), (((tmp, init),) + more))
        else:
            name = form__sym_name(target)
            loc = core__Local(name, n1, form__form_pos(target), core__ANY)
            if ((name == '') or core__is_special(name, scope.builtins)):
                return cdy_rt.primitives.fail(core__located(scope, 'let name must be a name, not a special form'))
            else:
                return ((core__bind_local(scope, name, loc), (n1 + 1)), ((loc, init),))

def core__destructure(names: tuple[form__Form, ...], tmp: core__Expr, scope: core__Scope, n: int) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    def _cdy_t17(state: tuple[core__Scope, int], item: tuple[int, form__Form]) -> tuple[tuple[core__Scope, int], tuple[core__Expr, core__Expr]]:
        _cdy__tup_125 = state
        _cdy_sc_126 = _cdy__tup_125[0]
        _cdy_k_127 = _cdy__tup_125[1]
        _cdy__tup_128 = item
        i = _cdy__tup_128[0]
        form = _cdy__tup_128[1]
        name = form__sym_name(form)
        loc = core__Local(name, _cdy_k_127, form__form_pos(form), core__ANY)
        read = core__Call(core__Prim('at', _cdy_sc_126.here, core__ANY), (tmp, core__Lit(form__IntLit(i, _cdy_sc_126.here), core__ANY)), _cdy_sc_126.here, core__ANY)
        if (name == ''):
            return cdy_rt.primitives.fail(core__located(_cdy_sc_126, 'let name must be a name'))
        else:
            return ((core__bind_local(_cdy_sc_126, name, loc), (_cdy_k_127 + 1)), (loc, read))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t17, (scope, n), cdy_rt.primitives.list_zip(cdy_rt.primitives.list_range(0, len(names)), names))
    last = _tup[0]
    pairs = _tup[1]
    _cdy__tup_137 = last
    sc = _cdy__tup_137[0]
    k = _cdy__tup_137[1]
    return (pairs, sc, k)

def core__nest(pairs: tuple[tuple[core__Expr, core__Expr], ...], body: core__Expr, pos: form__Pos) -> core__Expr:
    if (len(pairs) == 0):
        return body
    else:
        _tup = pairs[0]
        loc = _tup[0]
        init = _tup[1]
        return core__Call(core__Lambda(cdy_rt.primitives.to_list(loc), core__nest(prelude__rest(pairs), body, pos), pos, core__ANY), cdy_rt.primitives.to_list(init), pos, core__ANY)

def core__an_fn(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) != 2):
        return cdy_rt.primitives.fail(core__located(scope, 'fn: expected (fn (args+) body), with exactly one body form'))
    else:
        _tup = core__bind_params(form__list_items(args[0]), scope, n)
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_153 = core__analyse_expr(args[1], inner, n1)
        body = _cdy__tup_153[0]
        n2 = _cdy__tup_153[1]
        if (len(params) == 0):
            return cdy_rt.primitives.fail(core__located(scope, 'fn arguments: at least one is needed'))
        else:
            return (core__Lambda(params, body, scope.here, core__ANY), n2)

def core__an_tup(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'Tup: needs at least one item'))
    else:
        _tup = core__analyse_all(args, scope, n)
        items = _tup[0]
        n1 = _tup[1]
        return (core__Tuple(items, scope.here, core__ANY), n1)

def core__an_list(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__analyse_all(args, scope, n)
    items = _tup[0]
    n1 = _tup[1]
    return (core__ListOf(items, scope.here, core__ANY), n1)

def core__an_get(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if ((len(args) != 2) or (form__sym_name(args[1]) == '')):
        return cdy_rt.primitives.fail(core__located(scope, 'get: expected (get obj field)'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        return (core__Field(obj, form__sym_name(args[1]), scope.here, core__ANY), n1)

def core__an_assoc(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) < 3):
        return cdy_rt.primitives.fail(core__located(scope, 'assoc: expected (assoc obj field value ...)'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        obj = _tup[0]
        n1 = _tup[1]
        _cdy__tup_180 = core__assoc_fields(prelude__rest(args), scope, n1, ())
        fields = _cdy__tup_180[0]
        n2 = _cdy__tup_180[1]
        return (core__Assoc(obj, fields, scope.here, core__ANY), n2)

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
                forms, n, acc = (cdy_rt.primitives.list_drop(2, forms), n1, (acc + cdy_rt.primitives.to_list((field, val))))
                continue

def core__an_format(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) != 1):
        return cdy_rt.primitives.fail(core__located(scope, 'format: expected one string literal'))
    else:
        _cdy_t18: object = args[0]
        if isinstance(_cdy_t18, form__Txt):
            text = _cdy_t18.val
            where = _cdy_t18.pos
            _tup = core__format_parts(text, where, 0, '', scope, n, ())
            parts = _tup[0]
            n1 = _tup[1]
            return (core__Fmt(parts, scope.here, core__ANY), n1)
        else:
            return cdy_rt.primitives.fail(core__located(scope, 'format: expected one string literal'))

def core__format_parts(text: str, where: form__Pos, pos: int, acc: str, scope: core__Scope, n: int, parts: tuple[core__FPart, ...]) -> tuple[tuple[core__FPart, ...], int]:
    while True:
        c = (cdy_rt.primitives.substring(text, pos, (pos + 1)) if (pos < len(text)) else '')
        next_ = (cdy_rt.primitives.substring(text, (pos + 1), (pos + 2)) if ((pos + 1) < len(text)) else '')
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
            end = core__hole_end(text, (pos + 1), scope)
            forms = scope.parse(cdy_rt.primitives.substring(text, (pos + 1), end), core__text_pos(text, (pos + 1), where))
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

def core__text_pos(text: str, pos: int, where: form__Pos) -> form__Pos:
    if (where.line == 0):
        return where
    else:
        before = cdy_rt.primitives.substring(text, 0, pos)
        lines = cdy_rt.primitives.split(before, '\n')
        last = cdy_rt.primitives.at(lines, (len(lines) - 1))
        if (len(lines) == 1):
            return form__Pos(where.file, where.line, (where.col + 1 + pos))
        else:
            return form__Pos(where.file, (where.line + (len(lines) - 1)), (len(last) + 1))

def core__hole_end(text: str, pos: int, scope: core__Scope) -> int:
    while True:
        if (pos >= len(text)):
            return cdy_rt.primitives.fail(core__located(scope, 'format: unmatched { (write {{ for a brace)'))
        elif (cdy_rt.primitives.substring(text, pos, (pos + 1)) == '}'):
            return pos
        elif (cdy_rt.primitives.substring(text, pos, (pos + 1)) == '{'):
            return cdy_rt.primitives.fail(core__located(scope, "format: a {hole} can't hold a brace"))
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
    _cdy__tup_233 = core__match_clauses(prelude__rest(args), scope, n1, core__MatchE(subject, (), (), scope.here, core__ANY), '')
    m = _cdy__tup_233[0]
    n2 = _cdy__tup_233[1]
    sum_ = (core__match_sum(core__match_clause_list(m), scope) if (len(core__match_clause_list(m)) > 0) else '')
    return (core__global_clauses(core__check_exhaustive(m, sum_, scope), scope.names), n2)

def core__global_clauses(m: core__Expr, names: _cdy_Mapping[str, str]) -> core__Expr:
    _cdy_t19: object = m
    if isinstance(_cdy_t19, core__MatchE):
        subject = _cdy_t19.subject
        clauses = _cdy_t19.clauses
        default = _cdy_t19.default
        pos = _cdy_t19.pos
        return core__MatchE(subject, core__rename_clauses(clauses, names), default, pos, core__ANY)
    else:
        return m

def core__rename_clauses(clauses: tuple[core__Clause, ...], names: _cdy_Mapping[str, str]) -> tuple[core__Clause, ...]:
    return cdy_rt.primitives.list_map((lambda c: c._replace(variant=core__global_name(c.variant, names))), clauses)

def core__is_tup_clause(clause: form__Form) -> bool:
    return (form__sym_name(core__first_item(core__first_item(clause))) == 'Tup')

def core__an_match_tup(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    items = form__list_items(args[1])
    names = prelude__rest(form__list_items(items[0]))
    if ((len(args) != 2) or (len(items) != 2)):
        return cdy_rt.primitives.fail(core__located(scope, 'match: a (Tup name+) pattern must be the only clause, with no else'))
    elif (len(names) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'match: a (Tup name+) pattern needs at least one name'))
    else:
        _tup = core__analyse_expr(args[0], scope, n)
        subject = _tup[0]
        n1 = _tup[1]
        tmp = core__Local('_tup', n1, scope.here, core__ANY)
        _cdy__tup_256 = core__tup_binds(names, tmp, 0, scope, (n1 + 1), ())
        pairs = _cdy__tup_256[0]
        inner = _cdy__tup_256[1]
        n2 = _cdy__tup_256[2]
        _cdy__tup_260 = core__analyse_expr(items[1], inner, n2)
        body = _cdy__tup_260[0]
        n3 = _cdy__tup_260[1]
        return (core__nest((cdy_rt.primitives.to_list((tmp, subject)) + pairs), body, scope.here), n3)

def core__tup_binds(names: tuple[form__Form, ...], tmp: core__Expr, i: int, scope: core__Scope, n: int, acc: tuple[tuple[core__Expr, core__Expr], ...]) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = form__sym_name(names[0])
            loc = core__Local(name, n, form__form_pos(names[0]), core__ANY)
            item = core__Call(core__Prim('at', scope.here, core__ANY), (tmp, core__Lit(form__IntLit(i, scope.here), core__ANY)), scope.here, core__ANY)
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
            _cdy_t20: object = loc
            if isinstance(_cdy_t20, core__Local):
                other = _cdy_t20.name
                return ((other == name) or core__bound_in_pairs(name, prelude__rest(pairs)))
            else:
                pairs = prelude__rest(pairs)
                continue

def core__match_sum(clauses: tuple[core__Clause, ...], scope: core__Scope) -> str:
    return cdy_rt.primitives.map_get(scope.variants, clauses[0].variant).sum_

def core__check_exhaustive(m: core__Expr, sum_: str, scope: core__Scope) -> core__Expr:
    _cdy_t21: object = m
    if isinstance(_cdy_t21, core__MatchE):
        clauses = _cdy_t21.clauses
        default = _cdy_t21.default
        missing = core__missing_variants(cdy_rt.primitives.map_get(scope.sums, sum_), clauses)
        if ((len(default) == 0) and (len(missing) > 0)):
            return cdy_rt.primitives.fail(core__located(scope, ('match on ' + sum_ + ': no clause for ' + cdy_rt.primitives.join(missing, ', ') + ' (or add else)')))
        else:
            return m
    else:
        return m

def core__missing_variants(names: tuple[str, ...], clauses: tuple[core__Clause, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_filter((lambda name: (not core__has_clause(name, clauses))), names)

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
                _cdy__tup_303 = core__pattern_binds(core__variant_fields(variant, scope), prelude__rest(pattern), scope, n, ())
                binds = _cdy__tup_303[0]
                inner = _cdy__tup_303[1]
                _cdy_n1_306 = _cdy__tup_303[2]
                _cdy__tup_307 = core__analyse_expr(items[1], inner, _cdy_n1_306)
                body = _cdy__tup_307[0]
                n2 = _cdy__tup_307[1]
                forms, n, m, sum_ = (prelude__rest(forms), n2, core__add_clause(m, core__Clause(variant, binds, body)), cdy_rt.primitives.map_get(scope.variants, variant).sum_)
                continue

def core__check_pattern(variant: str, pattern: tuple[form__Form, ...], sum_: str, m: core__Expr, scope: core__Scope) -> bool:
    if (variant == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'match: pattern must be (Variant name*) or else'))
    elif (variant == 'Tup'):
        return cdy_rt.primitives.fail(core__located(scope, 'match: a (Tup name+) pattern must be the only clause, with no else'))
    elif (not core__is_variant(variant, scope)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: ' + variant + ' is not a variant of a sum type')))
    elif core__has_clause(variant, core__match_clause_list(m)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: more than one clause for ' + variant)))
    elif ((sum_ != '') and (sum_ != cdy_rt.primitives.map_get(scope.variants, variant).sum_)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: clauses mix variants of ' + sum_ + ' and ' + cdy_rt.primitives.map_get(scope.variants, variant).sum_)))
    elif ((len(pattern) - 1) != len(core__variant_fields(variant, scope))):
        return cdy_rt.primitives.fail(core__located(scope, ('match: ' + variant + ' has ' + str(len(core__variant_fields(variant, scope))) + ' field(s), so the pattern needs that many names')))
    else:
        return True

def core__match_clause_list(m: core__Expr) -> tuple[core__Clause, ...]:
    _cdy_t22: object = m
    if isinstance(_cdy_t22, core__MatchE):
        clauses = _cdy_t22.clauses
        return clauses
    else:
        return ()

def core__add_clause(m: core__Expr, clause: core__Clause) -> core__Expr:
    _cdy_t23: object = m
    if isinstance(_cdy_t23, core__MatchE):
        subject = _cdy_t23.subject
        clauses = _cdy_t23.clauses
        default = _cdy_t23.default
        pos = _cdy_t23.pos
        return core__MatchE(subject, (clauses + cdy_rt.primitives.to_list(clause)), default, pos, core__ANY)
    else:
        return m

def core__set_default(m: core__Expr, e: core__Expr) -> core__Expr:
    _cdy_t24: object = m
    if isinstance(_cdy_t24, core__MatchE):
        subject = _cdy_t24.subject
        clauses = _cdy_t24.clauses
        pos = _cdy_t24.pos
        return core__MatchE(subject, clauses, cdy_rt.primitives.to_list(e), pos, core__ANY)
    else:
        return m

def core__pattern_binds(fields: tuple[str, ...], names: tuple[form__Form, ...], scope: core__Scope, n: int, acc: tuple[tuple[str, core__Expr], ...]) -> tuple[tuple[tuple[str, core__Expr], ...], core__Scope, int]:
    while True:
        if (len(names) == 0):
            return (acc, scope, n)
        else:
            name = form__sym_name(names[0])
            loc = core__Local(name, n, form__form_pos(names[0]), core__ANY)
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
            _cdy_t25: object = loc
            if isinstance(_cdy_t25, core__Local):
                other = _cdy_t25.name
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
        return cdy_rt.primitives.fail(core__located(scope, (what + ': only in macro code')))

def core__quoted(form: form__Form) -> core__Expr:
    _cdy_t26: object = form
    if isinstance(_cdy_t26, form__Sym):
        name = _cdy_t26.name
        return core__Call(core__Global('Sym', form__NOWHERE, core__ANY), (core__Lit(form__Txt(name, form__NOWHERE), core__ANY), core__Global('NOWHERE', form__NOWHERE, core__ANY)), form__NOWHERE, core__ANY)
    elif isinstance(_cdy_t26, form__Lst):
        items = _cdy_t26.items
        return core__Call(core__Global('Lst', form__NOWHERE, core__ANY), (core__form_list(cdy_rt.primitives.list_map(core__quoted, items)), core__Global('NOWHERE', form__NOWHERE, core__ANY)), form__NOWHERE, core__ANY)
    else:
        return core__Call(core__Global(core__literal_variant(form), form__NOWHERE, core__ANY), (core__Lit(form, core__ANY), core__Global('NOWHERE', form__NOWHERE, core__ANY)), form__NOWHERE, core__ANY)

def core__form_list(items: tuple[core__Expr, ...]) -> core__Expr:
    if (len(items) == 0):
        return core__Prim('empty-list', form__NOWHERE, core__ANY)
    else:
        return core__Tuple(items, form__NOWHERE, core__ANY)

def core__literal_variant(form: form__Form) -> str:
    _cdy_t27: object = form
    if isinstance(_cdy_t27, form__Txt):
        return 'Txt'
    elif isinstance(_cdy_t27, form__IntLit):
        return 'IntLit'
    elif isinstance(_cdy_t27, form__LongLit):
        return 'LongLit'
    elif isinstance(_cdy_t27, form__ByteLit):
        return 'ByteLit'
    elif isinstance(_cdy_t27, form__FloatLit):
        return 'FloatLit'
    elif isinstance(_cdy_t27, form__DoubleLit):
        return 'DoubleLit'
    elif isinstance(_cdy_t27, form__CharLit):
        return 'CharLit'
    elif isinstance(_cdy_t27, form__BoolLit):
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
        return cdy_rt.primitives.fail(core__located(scope, (core__head_name(form) + ': expected (' + core__head_name(form) + ' expr)')))
    else:
        return core__analyse_expr(items[1], scope, n)

def core__quasi_list(items: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _tup = core__quasi_parts(items, scope, n, (), ())
    parts = _tup[0]
    n1 = _tup[1]
    return (core__Call(core__Global('Lst', form__NOWHERE, core__ANY), (core__join_parts(parts), core__Global('NOWHERE', form__NOWHERE, core__ANY)), form__NOWHERE, core__ANY), n1)

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
                _cdy__tup_381 = core__quasi_form(item, scope, n)
                _cdy_e_382 = _cdy__tup_381[0]
                _cdy_n1_383 = _cdy__tup_381[1]
                items, n, run = (prelude__rest(items), _cdy_n1_383, (run + cdy_rt.primitives.to_list(_cdy_e_382)))
                continue

def core__close_run(run: tuple[core__Expr, ...], parts: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    if (len(run) == 0):
        return parts
    else:
        return (parts + cdy_rt.primitives.to_list(core__Tuple(run, form__NOWHERE, core__ANY)))

def core__join_parts(parts: tuple[core__Expr, ...]) -> core__Expr:
    if (len(parts) == 0):
        return core__Prim('empty-list', form__NOWHERE, core__ANY)
    elif (len(parts) == 1):
        return parts[0]
    else:
        return core__Call(core__Prim('++', form__NOWHERE, core__ANY), parts, form__NOWHERE, core__ANY)

def core__is_lower(name: str) -> bool:
    return ((len(name) > 0) and (cdy_rt.primitives.substring(name, 0, 1) >= 'a') and (cdy_rt.primitives.substring(name, 0, 1) <= 'z'))

def core__analyse_type(form: form__Form) -> core__CType:
    _cdy_t28: object = form
    if isinstance(_cdy_t28, form__Sym):
        name = _cdy_t28.name
        if core__is_lower(name):
            return core__TVar(name)
        else:
            return core__TCon(name, ())
    elif isinstance(_cdy_t28, form__Lst):
        items = _cdy_t28.items
        if (len(items) == 0):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad type ()'))
        elif (form__sym_name(items[0]) == 'Fn'):
            if (len(items) == 3):
                return core__TFn(cdy_rt.primitives.list_map(core__analyse_type, form__list_items(items[1])), core__analyse_type(items[2]))
            else:
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad function type: expected (Fn (Arg+) Ret)'))
        elif (form__sym_name(items[0]) == 'Rest'):
            if (len(items) == 2):
                return core__TCon('Rest', cdy_rt.primitives.to_list(core__analyse_type(items[1])))
            else:
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad rest type: expected (Rest Type)'))
        else:
            return core__TCon(form__sym_name(items[0]), cdy_rt.primitives.list_map(core__analyse_type, prelude__rest(items)))
    else:
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad type'))
core__CONSTRAINTS: _cdy_Mapping[str, tuple[str, ...]] = cdy_rt.primitives.map_from((('number', ('Int', 'Long', 'Byte', 'Float', 'Double')), ('integer', ('Int', 'Long', 'Byte')), ('float', ('Float', 'Double')), ('comparable', ('Int', 'Long', 'Byte', 'Float', 'Double', 'String', 'Char')), ('appendable', ('String', 'List'))))

def core__constraint_of(name: str) -> str:
    parts = cdy_rt.primitives.split(name, ':')
    base = (parts[1] if (len(parts) == 2) else core__trim_digits(name))
    if cdy_rt.primitives.map_has(core__CONSTRAINTS, base):
        return base
    else:
        return ''

def core__trim_digits(s: str) -> str:
    while True:
        if ((len(s) > 0) and cdy_rt.primitives.list_contains(cdy_rt.primitives.substring(s, (len(s) - 1), len(s)), ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))):
            s = cdy_rt.primitives.substring(s, 0, (len(s) - 1))
            continue
        else:
            return s

class core__Prog(_cdy_NamedTuple):
    out: tuple[core__Top, ...]
    sigs: _cdy_Mapping[str, core__CType]
    n: int
    defs: _cdy_Mapping[str, bool]
    defined: _cdy_Mapping[str, bool]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Prog, 'Prog', (), (('List', 'core__Top'), ('Map', 'String', 'core__CType'), 'Int', ('Map', 'String', 'Bool'), ('Map', 'String', 'Bool')))

def core__top_names(forms: tuple[form__Form, ...]) -> _cdy_Mapping[str, bool]:
    def _cdy_t29(acc: _cdy_Mapping[str, bool], form: form__Form) -> _cdy_Mapping[str, bool]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 1) else '')
        if ((head == 'def') or (head == 'defn')):
            return core__add_name(form__sym_name(items[1]), form__form_pos(items[1]), acc)
        elif ((head == 'deft') and core__is_sum_body(cdy_rt.primitives.list_drop(2, items))):
            return core__add_names(core__variant_names(cdy_rt.primitives.list_drop(2, items)), form__form_pos(items[1]), cdy_rt.primitives.map_set(core__add_name(core__deft_name(items[1]), form__form_pos(items[1]), acc), core__deft_name(items[1]), False))
        elif (head == 'deft'):
            return core__add_name(core__deft_name(items[1]), form__form_pos(items[1]), acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t29, {}, forms)

def core__add_name(name: str, pos: form__Pos, acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    if cdy_rt.primitives.map_has(acc, name):
        return cdy_rt.primitives.fail((form__pos_text(pos) + ('defined more than once: ' + name)))
    else:
        return cdy_rt.primitives.map_set(acc, name, True)

def core__add_names(names: tuple[str, ...], pos: form__Pos, start: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    return cdy_rt.primitives.list_fold((lambda acc, name: core__add_name(name, pos, acc)), start, names)

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

def core__variant_names(body: tuple[form__Form, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda v: form__sym_name(core__first_item(v))), body)

def core__find_variants(forms: tuple[form__Form, ...], scope: core__Scope) -> core__Scope:
    while True:
        if (len(forms) == 0):
            return scope
        else:
            items = form__list_items(forms[0])
            head = (form__sym_name(items[0]) if (len(items) > 2) else '')
            body = cdy_rt.primitives.list_drop(2, items)
            _cdy_t31 = prelude__rest(forms)
            if ((head == 'deft') and core__is_sum_body(body)):
                sum_ = core__deft_name(items[1])
                _cdy_t30 = core__add_variants(sum_, body, scope._replace(sums=cdy_rt.primitives.map_set(scope.sums, sum_, core__variant_names(body))))
            else:
                _cdy_t30 = scope
            forms, scope = (_cdy_t31, _cdy_t30)
            continue

def core__add_variants(sum_: str, body: tuple[form__Form, ...], scope: core__Scope) -> core__Scope:
    while True:
        if (len(body) == 0):
            return scope
        else:
            v_items = form__list_items(body[0])
            name = form__sym_name(v_items[0])
            fields = (core__field_names(form__list_items(v_items[1])) if (len(v_items) == 2) else ())
            body, scope = (prelude__rest(body), scope._replace(variants=cdy_rt.primitives.map_set(scope.variants, name, core__VInfo(sum_, fields))))
            continue

def core__field_names(fields: tuple[form__Form, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda field: form__sym_name(core__first_item(field))), fields)

def core__deft_name(form: form__Form) -> str:
    _cdy_t32: object = form
    if isinstance(_cdy_t32, form__Lst):
        items = _cdy_t32.items
        if (len(items) == 0):
            return ''
        else:
            return form__sym_name(items[0])
    else:
        return form__sym_name(form)

class core__Special(_cdy_NamedTuple):
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Special, 'Special', (), ())

class core__Typed(_cdy_NamedTuple):
    type_: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Typed, 'Typed', (), ('core__CType',))

class core__BType(_cdy_NamedTuple):
    arity: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__BType, 'BType', (), ('Int',))
type core__Builtin = core__Special | core__Typed | core__BType

def core__is_builtin_type(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t35 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t35:
        _cdy_t34: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t34, core__BType):
            _cdy_t33 = True
        else:
            _cdy_t33 = False
        _cdy_t35 = _cdy_t33
    return _cdy_t35

def core__is_special(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t38 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t38:
        _cdy_t37: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t37, core__Special):
            _cdy_t36 = True
        else:
            _cdy_t36 = False
        _cdy_t38 = _cdy_t36
    return _cdy_t38

def core__read_builtins(decls: tuple[form__Form, ...], sigs: tuple[form__Form, ...], spellings: _cdy_Mapping[str, tuple[str, str, str]]) -> _cdy_Mapping[str, core__Builtin]:
    builtins = core__read_sigs(sigs, spellings, core__read_decls(decls, spellings))
    checked = core__all_declared(cdy_rt.primitives.map_keys(spellings), builtins)
    return builtins

def core__spelling_py(spellings: _cdy_Mapping[str, tuple[str, str, str]], name: str) -> str:
    if cdy_rt.primitives.map_has(spellings, name):
        _tup = cdy_rt.primitives.map_get(spellings, name)
        py = _tup[0]
        _kind = _tup[1]
        _value = _tup[2]
        return py
    else:
        return ''

def core__spelling_kind(spellings: _cdy_Mapping[str, tuple[str, str, str]], name: str) -> str:
    if cdy_rt.primitives.map_has(spellings, name):
        _tup = cdy_rt.primitives.map_get(spellings, name)
        _py = _tup[0]
        kind = _tup[1]
        _value = _tup[2]
        return kind
    else:
        return ''

def core__spelling_value(spellings: _cdy_Mapping[str, tuple[str, str, str]], name: str) -> str:
    if cdy_rt.primitives.map_has(spellings, name):
        _tup = cdy_rt.primitives.map_get(spellings, name)
        _py = _tup[0]
        _kind = _tup[1]
        value = _tup[2]
        return value
    else:
        return ''
core__SPECIAL_KINDS: tuple[str, ...] = ('',)
core__TYPED_KINDS: tuple[str, ...] = ('call', 'value', 'index')
core__OPERATOR_KINDS: tuple[str, ...] = ('binop', 'compare', 'boolop', 'unary')
core__TYPE_KINDS: tuple[str, ...] = ('type',)

def core__read_decls(forms: tuple[form__Form, ...], spellings: _cdy_Mapping[str, tuple[str, str, str]]) -> _cdy_Mapping[str, core__Builtin]:
    def _cdy_t39(acc: _cdy_Mapping[str, core__Builtin], form: form__Form) -> _cdy_Mapping[str, core__Builtin]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 0) else '')
        name = (form__sym_name(items[1]) if (len(items) > 1) else '')
        where = form__pos_text(form__form_pos(form))
        decl = (('', core__Special()) if (name == '') else (('special', core__Special()) if ((head == 'special') and (len(items) == 2)) else ('', core__Special())))
        _tup = decl
        class_ = _tup[0]
        kind = _tup[1]
        if (class_ == ''):
            return cdy_rt.primitives.fail((where + 'special.cdy: expected (special name)'))
        elif cdy_rt.primitives.map_has(acc, name):
            return cdy_rt.primitives.fail((where + 'special.cdy: ' + name + ' is declared more than once'))
        elif (not cdy_rt.primitives.list_contains(core__spelling_kind(spellings, name), core__kinds_of(class_))):
            return cdy_rt.primitives.fail(((where + 'special.cdy: ' + name + " is a special form, so spelling.py can't spell it") if (class_ == 'special') else (where + 'special.cdy: ' + name + ' has no ' + class_ + ' entry in spelling.py')))
        else:
            return cdy_rt.primitives.map_set(acc, name, kind)
    return cdy_rt.primitives.list_fold(_cdy_t39, {}, forms)

def core__kinds_of(class_: str) -> tuple[str, ...]:
    if (class_ == 'special'):
        return core__SPECIAL_KINDS
    else:
        return core__TYPED_KINDS

def core__read_sigs(forms: tuple[form__Form, ...], spellings: _cdy_Mapping[str, tuple[str, str, str]], start: _cdy_Mapping[str, core__Builtin]) -> _cdy_Mapping[str, core__Builtin]:
    def _cdy_t40(acc: _cdy_Mapping[str, core__Builtin], form: form__Form) -> _cdy_Mapping[str, core__Builtin]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 0) else '')
        name = (form__sym_name(items[1]) if ((len(items) == 3) and (head == 'sig')) else '')
        where = form__pos_text(form__form_pos(form))
        if (head == 'deft'):
            return core__read_type(form, items, where, spellings, acc)
        elif (name == ''):
            return cdy_rt.primitives.fail((where + 'system.cdy: expected (sig name Type) or (deft Name)'))
        elif cdy_rt.primitives.map_has(acc, name):
            return cdy_rt.primitives.fail((where + 'system.cdy: ' + name + ' is already declared'))
        elif (not cdy_rt.primitives.list_contains(core__spelling_kind(spellings, name), (core__TYPED_KINDS + core__OPERATOR_KINDS))):
            return cdy_rt.primitives.fail((where + 'system.cdy: ' + name + ' has no Python mapping in spelling.py'))
        else:
            return cdy_rt.primitives.map_set(acc, name, core__Typed(core__analyse_type(items[2])))
    return cdy_rt.primitives.list_fold(_cdy_t40, start, forms)

def core__read_type(form: form__Form, items: tuple[form__Form, ...], where: str, spellings: _cdy_Mapping[str, tuple[str, str, str]], acc: _cdy_Mapping[str, core__Builtin]) -> _cdy_Mapping[str, core__Builtin]:
    header = (items[1] if (len(items) == 2) else form)
    _cdy_t42: object = header
    if isinstance(_cdy_t42, form__Sym):
        _cdy_t41 = cdy_rt.primitives.to_list(header)
    elif isinstance(_cdy_t42, form__Lst):
        xs = _cdy_t42.items
        _cdy_t41 = xs
    else:
        _cdy_t41 = ()
    parts = _cdy_t41
    name = (form__sym_name(parts[0]) if (len(parts) > 0) else '')
    tvars = (prelude__rest(parts) if (len(parts) > 0) else ())
    if ((name == '') or core__is_lower(name) or (not core__all_lower(tvars))):
        return cdy_rt.primitives.fail((where + 'system.cdy: expected (deft Name) or (deft (Name a ...))'))
    elif cdy_rt.primitives.map_has(acc, name):
        return cdy_rt.primitives.fail((where + 'system.cdy: ' + name + ' is already declared'))
    elif (not cdy_rt.primitives.list_contains(core__spelling_kind(spellings, name), core__TYPE_KINDS)):
        return cdy_rt.primitives.fail((where + 'system.cdy: ' + name + ' has no Python type in spelling.py'))
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
            return cdy_rt.primitives.fail(('spelling.py: ' + names[0] + ' is declared in neither special.cdy nor system.cdy'))
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
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Exports, 'Exports', (), ('String', ('Map', 'String', 'Bool'), ('Map', 'String', 'core__VInfo'), ('Map', 'String', ('List', 'String')), ('Map', 'String', 'String'), ('Map', 'String', 'Int')))

def core__module_exports(forms: tuple[form__Form, ...], stem: str, prefix: str) -> core__Exports:
    top = core__top_names(forms)
    found = core__find_variants(forms, core__blank_scope(top))
    return core__Exports(stem, top, found.variants, found.sums, core__prefixed(cdy_rt.primitives.map_keys(top), prefix), core__type_arities(forms))

def core__type_arities(forms: tuple[form__Form, ...]) -> _cdy_Mapping[str, int]:
    def _cdy_t46(acc: _cdy_Mapping[str, int], form: form__Form) -> _cdy_Mapping[str, int]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 1) else '')
        if ((head == 'deft') and (core__deft_name(items[1]) != '')):
            _cdy_t45 = core__deft_name(items[1])
            _cdy_t44: object = items[1]
            if isinstance(_cdy_t44, form__Lst):
                xs = _cdy_t44.items
                _cdy_t43 = (len(xs) - 1)
            else:
                _cdy_t43 = 0
            return cdy_rt.primitives.map_set(acc, _cdy_t45, _cdy_t43)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t46, {}, forms)

def core__prefixed(names: tuple[str, ...], prefix: str) -> _cdy_Mapping[str, str]:
    return cdy_rt.primitives.list_fold((lambda acc, name: cdy_rt.primitives.map_set(acc, name, (prefix + name))), {}, names)

def core__blank_scope(top: _cdy_Mapping[str, bool]) -> core__Scope:
    return core__Scope({}, top, (lambda text, where: ()), {}, {}, form__NOWHERE, {}, False, {}, {}, {}, {})

def core__analyse_program(forms: tuple[form__Form, ...], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    return core__analyse_module(forms, core__module_exports(forms, '', ''), (), {}, builtins, parse, macros, quoting)

def core__analyse_module(forms: tuple[form__Form, ...], own: core__Exports, imports: tuple[tuple[core__Exports, form__Pos], ...], elsewhere: _cdy_Mapping[str, str], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    seen = core__with_own(core__with_imports(imports, core__Seen(core__Exports('', {}, {}, {}, {}, {}), {})), own)
    vis = seen.vis
    scope = core__Scope({}, vis.top, parse, vis.variants, vis.sums, form__NOWHERE, macros, quoting, vis.names, elsewhere, builtins, vis.types)
    prog = core__analyse_tops(forms, scope, core__Prog((), {}, 0, core__def_names(forms), {}))
    return core__rename_tops(prog.out, vis.names)

class core__Seen(_cdy_NamedTuple):
    vis: core__Exports
    from_: _cdy_Mapping[str, str]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Seen, 'Seen', (), ('core__Exports', ('Map', 'String', 'String')))

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
                return cdy_rt.primitives.fail((form__pos_text(pos) + 'import: ' + cdy_rt.primitives.map_get(from_, name) + ' and ' + stem + ' both define ' + name))
            else:
                names, seen = (prelude__rest(names), core__Seen(vis._replace(top=cdy_rt.primitives.map_set(vis.top, name, cdy_rt.primitives.map_get(ex.top, name)), names=cdy_rt.primitives.map_set(vis.names, name, cdy_rt.primitives.map_get(ex.names, name))), cdy_rt.primitives.map_set(from_, name, stem)))
                continue

def core__with_own(seen: core__Seen, own: core__Exports) -> core__Seen:
    vis = seen.vis
    return seen._replace(vis=vis._replace(top=core__put_all(own.top, cdy_rt.primitives.map_keys(own.top), vis.top), variants=core__put_all(own.variants, cdy_rt.primitives.map_keys(own.variants), vis.variants), sums=core__put_all(own.sums, cdy_rt.primitives.map_keys(own.sums), vis.sums), names=core__put_all(own.names, cdy_rt.primitives.map_keys(own.names), vis.names), types=core__put_all(own.types, cdy_rt.primitives.map_keys(own.types), vis.types)))

def core__put_all[a](m: _cdy_Mapping[str, a], keys: tuple[str, ...], start: _cdy_Mapping[str, a]) -> _cdy_Mapping[str, a]:
    return cdy_rt.primitives.list_fold((lambda acc, key: cdy_rt.primitives.map_set(acc, key, cdy_rt.primitives.map_get(m, key))), start, keys)

def core__elsewhere_names(exports: tuple[core__Exports, ...]) -> _cdy_Mapping[str, str]:
    return cdy_rt.primitives.list_fold((lambda acc, ex: core__put_all(core__stems_for(cdy_rt.primitives.map_keys(ex.top), ex.stem), cdy_rt.primitives.map_keys(ex.top), acc)), {}, exports)

def core__stems_for(names: tuple[str, ...], stem: str) -> _cdy_Mapping[str, str]:
    return cdy_rt.primitives.list_fold((lambda acc, name: cdy_rt.primitives.map_set(acc, name, stem)), {}, names)

def core__rename_tops(tops: tuple[core__Top, ...], names: _cdy_Mapping[str, str]) -> tuple[core__Top, ...]:
    return cdy_rt.primitives.list_map((lambda top: core__rename_top(top, names)), tops)

def core__rename_top(top: core__Top, names: _cdy_Mapping[str, str]) -> core__Top:
    _cdy_t47: object = top
    if isinstance(_cdy_t47, core__TDeft):
        name = _cdy_t47.name
        tvars = _cdy_t47.tvars
        fields = _cdy_t47.fields
        return core__TDeft(core__global_name(name, names), tvars, core__rename_fields(fields, names))
    elif isinstance(_cdy_t47, core__TDeftSum):
        _cdy_name_563 = _cdy_t47.name
        _cdy_tvars_564 = _cdy_t47.tvars
        variants = _cdy_t47.variants
        return core__TDeftSum(core__global_name(_cdy_name_563, names), _cdy_tvars_564, core__rename_variants(variants, names))
    elif isinstance(_cdy_t47, core__TDef):
        _cdy_name_566 = _cdy_t47.name
        init = _cdy_t47.init
        t = _cdy_t47.t
        pos = _cdy_t47.pos
        return core__TDef(core__global_name(_cdy_name_566, names), init, core__rename_type(t, names), pos)
    elif isinstance(_cdy_t47, core__TDefn):
        _cdy_name_570 = _cdy_t47.name
        params = _cdy_t47.params
        body = _cdy_t47.body
        _cdy_t_573 = _cdy_t47.t
        _cdy_pos_574 = _cdy_t47.pos
        return core__TDefn(core__global_name(_cdy_name_570, names), params, body, core__rename_type(_cdy_t_573, names), _cdy_pos_574)
    else:
        assert isinstance(_cdy_t47, core__TExpr)
        return top

def core__rename_variants(variants: tuple[core__Variant, ...], names: _cdy_Mapping[str, str]) -> tuple[core__Variant, ...]:
    return cdy_rt.primitives.list_map((lambda v: core__Variant(core__global_name(v.name, names), core__rename_fields(v.fields, names))), variants)

def core__rename_fields(fields: tuple[tuple[str, core__CType], ...], names: _cdy_Mapping[str, str]) -> tuple[tuple[str, core__CType], ...]:
    def _cdy_t48(field: tuple[str, core__CType]) -> tuple[str, core__CType]:
        _tup = field
        name = _tup[0]
        t = _tup[1]
        return (name, core__rename_type(t, names))
    return cdy_rt.primitives.list_map(_cdy_t48, fields)

def core__rename_type(t: core__CType, names: _cdy_Mapping[str, str]) -> core__CType:
    _cdy_t49: object = t
    if isinstance(_cdy_t49, core__TCon):
        name = _cdy_t49.name
        args = _cdy_t49.args
        return core__TCon(core__global_name(name, names), core__rename_types(args, names))
    elif isinstance(_cdy_t49, core__TVar):
        return t
    else:
        assert isinstance(_cdy_t49, core__TFn)
        params = _cdy_t49.params
        ret = _cdy_t49.ret
        return core__TFn(core__rename_types(params, names), core__rename_type(ret, names))

def core__rename_types(types: tuple[core__CType, ...], names: _cdy_Mapping[str, str]) -> tuple[core__CType, ...]:
    return cdy_rt.primitives.list_map((lambda t: core__rename_type(t, names)), types)

def core__def_names(forms: tuple[form__Form, ...]) -> _cdy_Mapping[str, bool]:
    def _cdy_t50(acc: _cdy_Mapping[str, bool], form: form__Form) -> _cdy_Mapping[str, bool]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 1) else '')
        if ((head == 'def') or (head == 'defn')):
            return cdy_rt.primitives.map_set(acc, form__sym_name(items[1]), True)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t50, {}, forms)

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
    if (cdy_rt.primitives.list_contains(head, ('def', 'defn')) and (len(items) > 1) and cdy_rt.primitives.map_has(scope.macros, form__sym_name(items[1]))):
        return cdy_rt.primitives.fail(core__located(here, (form__sym_name(items[1]) + " is a macro, so it can't be defined")))
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
        return cdy_rt.primitives.fail(core__located(scope, ('sig for ' + name + ', but no def or defn of ' + name + ' in this file')))
    elif cdy_rt.primitives.map_has(prog.defined, name):
        return cdy_rt.primitives.fail(core__located(scope, ('sig for ' + name + ' comes after its definition')))
    elif cdy_rt.primitives.map_has(prog.sigs, name):
        return cdy_rt.primitives.fail(core__located(scope, ('more than one sig for ' + name)))
    else:
        t = core__analyse_type(items[2])
        checked = core__check_sig_type(t, scope)
        return prog._replace(sigs=cdy_rt.primitives.map_set(prog.sigs, name, t))

def core__check_sig_type(t: core__CType, scope: core__Scope) -> bool:
    if core__is_variadic(t):
        _cdy_t51: object = t
        if isinstance(_cdy_t51, core__TFn):
            params = _cdy_t51.params
            ret = _cdy_t51.ret
            last = cdy_rt.primitives.at(params, (len(params) - 1))
            return (core__check_types(cdy_rt.primitives.slice_(params, 0, (len(params) - 1)), scope) and core__check_types(core__rest_item(last), scope) and core__check_type(ret, scope))
        else:
            return core__check_type(t, scope)
    else:
        return core__check_type(t, scope)

def core__check_type(t: core__CType, scope: core__Scope) -> bool:
    _cdy_t52: object = t
    if isinstance(_cdy_t52, core__TVar):
        return True
    elif isinstance(_cdy_t52, core__TFn):
        params = _cdy_t52.params
        ret = _cdy_t52.ret
        return (core__check_types(params, scope) and core__check_type(ret, scope))
    else:
        assert isinstance(_cdy_t52, core__TCon)
        name = _cdy_t52.name
        args = _cdy_t52.args
        builtins = scope.builtins
        if (name == 'Tup'):
            _cdy_t55 = len(args)
        elif (name == 'Rest'):
            _cdy_t55 = cdy_rt.primitives.fail(core__located(scope, "(Rest t) is only for the last argument of a sig's function type"))
        elif cdy_rt.primitives.map_has(scope.types, name):
            _cdy_t55 = cdy_rt.primitives.map_get(scope.types, name)
        elif core__is_builtin_type(name, builtins):
            _cdy_t54: object = cdy_rt.primitives.map_get(builtins, name)
            if isinstance(_cdy_t54, core__BType):
                n = _cdy_t54.arity
                _cdy_t53 = n
            else:
                _cdy_t53 = 0
            _cdy_t55 = _cdy_t53
        elif cdy_rt.primitives.map_has(scope.variants, name):
            _cdy_t55 = cdy_rt.primitives.fail(core__located(scope, (name + ' is a variant of ' + cdy_rt.primitives.map_get(scope.variants, name).sum_ + ', not a type')))
        elif cdy_rt.primitives.map_has(scope.top, name):
            _cdy_t55 = cdy_rt.primitives.fail(core__located(scope, (name + ' is a value, not a type')))
        elif cdy_rt.primitives.map_has(scope.elsewhere, name):
            stem = cdy_rt.primitives.map_get(scope.elsewhere, name)
            _cdy_t55 = cdy_rt.primitives.fail(core__located(scope, (name + ' is not defined here; ' + stem + " defines it, but this file doesn't import " + stem)))
        else:
            _cdy_t55 = cdy_rt.primitives.fail(core__located(scope, ('unknown type ' + name)))
        arity = _cdy_t55
        if (arity != len(args)):
            return cdy_rt.primitives.fail(core__located(scope, (name + ' takes ' + str(arity) + ' type argument(s), got ' + str(len(args)))))
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
    tvars = cdy_rt.primitives.list_map(form__sym_name, tvar_forms)
    dup = core__repeated(tvar_forms, (), 0)
    body = cdy_rt.primitives.list_drop(2, items)
    field_forms = (form__list_items(items[2]) if (len(items) == 3) else ())
    if (name == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+)) or (deft Name variant+)'))
    elif (dup >= 0):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(cdy_rt.primitives.at(tvar_forms, dup))) + ('deft ' + name + ': type variables must be different (' + cdy_rt.primitives.at(tvars, dup) + ')')))
    elif core__is_sum_body(body):
        variants = core__deft_variants(name, body)
        checked = core__check_variants(variants, scope)
        return core__add_top(prog, core__TDeftSum(name, tvars, variants), prog.n)
    elif (len(field_forms) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+))'))
    else:
        fields = core__deft_fields(('deft ' + name), field_forms)
        _cdy_checked_650 = core__check_fields(fields, scope)
        return core__add_top(prog, core__TDeft(name, tvars, fields), prog.n)

def core__check_fields(fields: tuple[tuple[str, core__CType], ...], scope: core__Scope) -> bool:
    if (len(fields) == 0):
        return True
    else:
        _tup = fields[0]
        _name = _tup[0]
        t = _tup[1]
        return (core__check_type(t, scope) and core__check_fields(prelude__rest(fields), scope))

def core__check_variants(variants: tuple[core__Variant, ...], scope: core__Scope) -> bool:
    while True:
        if (len(variants) == 0):
            return True
        elif core__check_fields(variants[0].fields, scope):
            variants = prelude__rest(variants)
            continue
        else:
            return False

def core__deft_variants(sum_: str, body: tuple[form__Form, ...]) -> tuple[core__Variant, ...]:
    def _cdy_t56(form: form__Form) -> core__Variant:
        v_items = form__list_items(form)
        name = form__sym_name(v_items[0])
        if (not core__is_upper(name)):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + ('deft: variant names are Capitalised, not ' + name)))
        elif (len(v_items) == 1):
            return core__Variant(name, ())
        elif ((len(v_items) == 2) and (len(form__list_items(v_items[1])) > 0)):
            return core__Variant(name, core__deft_fields(('deft ' + sum_ + ', variant ' + name), form__list_items(v_items[1])))
        else:
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'deft: variant must be (Name) or (Name ((field Type)+))'))
    return cdy_rt.primitives.list_map(_cdy_t56, body)

def core__is_upper(name: str) -> bool:
    return ((len(name) > 0) and (cdy_rt.primitives.substring(name, 0, 1) >= 'A') and (cdy_rt.primitives.substring(name, 0, 1) <= 'Z'))

def core__deft_fields(owner: str, forms: tuple[form__Form, ...]) -> tuple[tuple[str, core__CType], ...]:
    def _cdy_t57(acc: tuple[tuple[str, core__CType], ...], form: form__Form) -> tuple[tuple[str, core__CType], ...]:
        items = form__list_items(form)
        if ((len(items) != 2) or (form__sym_name(items[0]) == '')):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'deft: field must be (name Type)'))
        elif core__has_field(form__sym_name(items[0]), acc):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + (owner + ': field names must be different (' + form__sym_name(items[0]) + ')')))
        else:
            return (acc + ((form__sym_name(items[0]), core__analyse_type(items[1])),))
    return cdy_rt.primitives.list_fold(_cdy_t57, (), forms)

def core__has_field(name: str, fields: tuple[tuple[str, core__CType], ...]) -> bool:
    def _cdy_t58(f: tuple[str, core__CType]) -> bool:
        _tup = f
        field = _tup[0]
        _t = _tup[1]
        return (field == name)
    return cdy_rt.primitives.list_any(_cdy_t58, fields)

def core__repeated(forms: tuple[form__Form, ...], seen: tuple[str, ...], i: int) -> int:
    while True:
        if (i == len(forms)):
            return -1
        elif cdy_rt.primitives.list_contains(form__sym_name(cdy_rt.primitives.at(forms, i)), seen):
            return i
        else:
            seen, i = ((seen + cdy_rt.primitives.to_list(form__sym_name(cdy_rt.primitives.at(forms, i)))), (i + 1))
            continue

def core__needs_sig(name: str, prog: core__Prog, scope: core__Scope) -> core__CType:
    if cdy_rt.primitives.map_has(prog.sigs, name):
        return cdy_rt.primitives.map_get(prog.sigs, name)
    else:
        return cdy_rt.primitives.fail(core__located(scope, (name + ' needs a (sig ' + name + ' Type) before its definition')))

def core__top_def(items: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    if (len(items) != 3):
        return cdy_rt.primitives.fail(core__located(scope, 'def: expected (def name init); the initial value is required'))
    else:
        name = form__sym_name(items[1])
        t = core__needs_sig(name, prog, scope)
        _tup = core__analyse_expr(items[2], scope, prog.n)
        init = _tup[0]
        n = _tup[1]
        if core__is_variadic(t):
            return cdy_rt.primitives.fail(core__located(scope, ('def ' + name + ': only a defn can take a rest parameter, (Rest t)')))
        else:
            return core__mark_defined(core__add_top(prog, core__TDef(name, init, t, scope.here), n), name)

def core__top_defn(items: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    if (len(items) != 4):
        return cdy_rt.primitives.fail(core__located(scope, 'defn: expected (defn name (args+) body), with exactly one body form'))
    else:
        name = form__sym_name(items[1])
        t = core__needs_sig(name, prog, scope)
        arg_forms = form__list_items(items[2])
        _tup = core__bind_params(arg_forms, scope, prog.n)
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_699 = core__analyse_expr(items[3], inner, n1)
        body = _cdy__tup_699[0]
        n2 = _cdy__tup_699[1]
        if (len(params) == 0):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + name + ': at least one argument is needed')))
        elif (len(params) != core__fn_arity(t)):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + name + ': its sig must be a function type with one type per argument')))
        else:
            return core__mark_defined(core__add_top(prog, core__TDefn(name, params, body, t, scope.here), n2), name)

def core__fn_arity(t: core__CType) -> int:
    _cdy_t59: object = t
    if isinstance(_cdy_t59, core__TFn):
        params = _cdy_t59.params
        return len(params)
    else:
        return -1

def core__is_variadic(t: core__CType) -> bool:
    _cdy_t60: object = t
    if isinstance(_cdy_t60, core__TFn):
        params = _cdy_t60.params
        return ((len(params) > 0) and core__is_rest(cdy_rt.primitives.at(params, (len(params) - 1))))
    else:
        return False

def core__is_rest(t: core__CType) -> bool:
    _cdy_t61: object = t
    if isinstance(_cdy_t61, core__TCon):
        name = _cdy_t61.name
        return (name == 'Rest')
    else:
        return False

def core__rest_item(t: core__CType) -> tuple[core__CType, ...]:
    _cdy_t62: object = t
    if isinstance(_cdy_t62, core__TCon):
        name = _cdy_t62.name
        args = _cdy_t62.args
        if (name == 'Rest'):
            return args
        else:
            return ()
    else:
        return ()

def core__bind_params(forms: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[tuple[core__Expr, ...], core__Scope, int]:
    def _cdy_t63(s: tuple[core__Scope, int], form: form__Form) -> tuple[tuple[core__Scope, int], core__Expr]:
        _cdy__tup_716 = s
        _cdy_sc_717 = _cdy__tup_716[0]
        _cdy_k_718 = _cdy__tup_716[1]
        name = form__sym_name(form)
        loc = core__Local(name, _cdy_k_718, form__form_pos(form), core__ANY)
        if (name == ''):
            return cdy_rt.primitives.fail(core__located(_cdy_sc_717, 'a parameter must be a name'))
        else:
            return ((core__bind_local(_cdy_sc_717, name, loc), (_cdy_k_718 + 1)), loc)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t63, (scope, n), forms)
    last = _tup[0]
    locs = _tup[1]
    _cdy__tup_724 = last
    sc = _cdy__tup_724[0]
    k = _cdy__tup_724[1]
    return (locs, sc, k)
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
    _cdy_t64: object = top
    if isinstance(_cdy_t64, core__TDefn):
        name = _cdy_t64.name
        t = _cdy_t64.t
        pos = _cdy_t64.pos
        if (name != 'main'):
            return False
        elif (t == core__MAIN_TYPE):
            return True
        else:
            return cdy_rt.primitives.fail((form__pos_text(pos) + 'main must be typed (Fn ((List String)) Int)'))
    elif isinstance(_cdy_t64, core__TDef):
        _cdy_name_732 = _cdy_t64.name
        _cdy_pos_733 = _cdy_t64.pos
        if (_cdy_name_732 == 'main'):
            return cdy_rt.primitives.fail((form__pos_text(_cdy_pos_733) + 'main must be a defn'))
        else:
            return False
    else:
        return False

class lower__SRecord(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SRecord, 'SRecord', (), ('String', ('List', 'String'), ('List', ('Tup', 'String', 'core__CType'))))

class lower__SSum(_cdy_NamedTuple):
    name: str
    tvars: tuple[str, ...]
    variants: tuple[core__Variant, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SSum, 'SSum', (), ('String', ('List', 'String'), ('List', 'core__Variant')))

class lower__SMatch(_cdy_NamedTuple):
    temp: core__Expr
    subject: core__Expr
    cases: tuple[lower__Case, ...]
    default: tuple[tuple[lower__Stmt, ...], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SMatch, 'SMatch', (), ('core__Expr', 'core__Expr', ('List', 'lower__Case'), ('List', ('List', 'lower__Stmt'))))

class lower__SAssign(_cdy_NamedTuple):
    target: core__Expr
    val: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SAssign, 'SAssign', (), ('core__Expr', 'core__Expr'))

class lower__SDefAssign(_cdy_NamedTuple):
    name: str
    val: core__Expr
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SDefAssign, 'SDefAssign', (), ('String', 'core__Expr', 'core__CType'))

class lower__SExpr(_cdy_NamedTuple):
    expr: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SExpr, 'SExpr', (), ('core__Expr',))

class lower__SReturn(_cdy_NamedTuple):
    val: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SReturn, 'SReturn', (), ('core__Expr',))

class lower__SIf(_cdy_NamedTuple):
    test: core__Expr
    then: tuple[lower__Stmt, ...]
    other: tuple[lower__Stmt, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SIf, 'SIf', (), ('core__Expr', ('List', 'lower__Stmt'), ('List', 'lower__Stmt')))

class lower__SFunc(_cdy_NamedTuple):
    name: str
    params: tuple[core__Expr, ...]
    body: tuple[lower__Stmt, ...]
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SFunc, 'SFunc', (), ('String', ('List', 'core__Expr'), ('List', 'lower__Stmt'), 'core__CType'))

class lower__SLocalFunc(_cdy_NamedTuple):
    target: core__Expr
    params: tuple[core__Expr, ...]
    body: tuple[lower__Stmt, ...]
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SLocalFunc, 'SLocalFunc', (), ('core__Expr', ('List', 'core__Expr'), ('List', 'lower__Stmt'), 'core__CType'))

class lower__SLoop(_cdy_NamedTuple):
    body: tuple[lower__Stmt, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SLoop, 'SLoop', (), (('List', 'lower__Stmt'),))

class lower__SRebind(_cdy_NamedTuple):
    targets: tuple[core__Expr, ...]
    vals: tuple[core__Expr, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SRebind, 'SRebind', (), (('List', 'core__Expr'), ('List', 'core__Expr')))

class lower__SContinue(_cdy_NamedTuple):
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SContinue, 'SContinue', (), ())
type lower__Stmt = lower__SRecord | lower__SSum | lower__SMatch | lower__SAssign | lower__SDefAssign | lower__SExpr | lower__SReturn | lower__SIf | lower__SFunc | lower__SLocalFunc | lower__SLoop | lower__SRebind | lower__SContinue

class lower__Case(_cdy_NamedTuple):
    variant: str
    binds: tuple[tuple[str, core__Expr], ...]
    body: tuple[lower__Stmt, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__Case, 'Case', (), ('String', ('List', ('Tup', 'String', 'core__Expr')), ('List', 'lower__Stmt')))

class lower__Low(_cdy_NamedTuple):
    stmts: tuple[lower__Stmt, ...]
    expr: core__Expr
    n: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__Low, 'Low', (), (('List', 'lower__Stmt'), 'core__Expr', 'Int'))

def lower__is_simple(e: core__Expr) -> bool:
    _cdy_t65: object = e
    if isinstance(_cdy_t65, core__Lit):
        return True
    elif isinstance(_cdy_t65, core__Local):
        return True
    elif isinstance(_cdy_t65, core__Global):
        return True
    elif isinstance(_cdy_t65, core__Prim):
        return True
    elif isinstance(_cdy_t65, core__Temp):
        return True
    else:
        return False

def lower__is_applied(e: core__Expr) -> bool:
    _cdy_t66: object = e
    if isinstance(_cdy_t66, core__Call):
        callee = _cdy_t66.callee
        args = _cdy_t66.args
        _cdy_t67: object = callee
        if isinstance(_cdy_t67, core__Lambda):
            params = _cdy_t67.params
            return (len(params) == len(args))
        else:
            return False
    else:
        return False

def lower__bind_applied(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], core__Expr, int]:
    _cdy_t68: object = e
    if isinstance(_cdy_t68, core__Call):
        callee = _cdy_t68.callee
        args = _cdy_t68.args
        _cdy_t69: object = callee
        if isinstance(_cdy_t69, core__Lambda):
            params = _cdy_t69.params
            body = _cdy_t69.body
            _tup = lower__value_seq(args, n)
            stmts = _tup[0]
            vals = _tup[1]
            n1 = _tup[2]
            return ((stmts + lower__assigns(params, vals, ())), body, n1)
        else:
            return cdy_rt.primitives.fail('internal error: lower: not an applied fn')
    else:
        return cdy_rt.primitives.fail('internal error: lower: not an applied fn')

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
        _cdy_t70: object = e
        if isinstance(_cdy_t70, core__Call):
            callee = _cdy_t70.callee
            args = _cdy_t70.args
            pos = _cdy_t70.pos
            ty = _cdy_t70.t
            return lower__value_call(callee, args, pos, ty, n)
        elif isinstance(_cdy_t70, core__If):
            test = _cdy_t70.test
            then = _cdy_t70.then
            other = _cdy_t70.other
            _cdy_pos_32 = _cdy_t70.pos
            _cdy_ty_33 = _cdy_t70.t
            return lower__value_if(test, then, other, _cdy_pos_32, _cdy_ty_33, n)
        elif isinstance(_cdy_t70, core__Do):
            _cdy_body_34 = _cdy_t70.body
            return lower__value_do(_cdy_body_34, n)
        elif isinstance(_cdy_t70, core__Lambda):
            params = _cdy_t70.params
            _cdy_body_36 = _cdy_t70.body
            _cdy_pos_37 = _cdy_t70.pos
            _cdy_ty_38 = _cdy_t70.t
            return lower__value_fn(params, _cdy_body_36, _cdy_pos_37, _cdy_ty_38, n)
        elif isinstance(_cdy_t70, core__Tuple):
            items = _cdy_t70.items
            _cdy_pos_40 = _cdy_t70.pos
            _cdy_ty_41 = _cdy_t70.t
            _cdy__tup_42 = lower__value_seq(items, n)
            _cdy_stmts_43 = _cdy__tup_42[0]
            vals = _cdy__tup_42[1]
            _cdy_n1_45 = _cdy__tup_42[2]
            return lower__Low(_cdy_stmts_43, core__Tuple(vals, _cdy_pos_40, _cdy_ty_41), _cdy_n1_45)
        elif isinstance(_cdy_t70, core__ListOf):
            _cdy_items_46 = _cdy_t70.items
            _cdy_pos_47 = _cdy_t70.pos
            _cdy_ty_48 = _cdy_t70.t
            _cdy__tup_49 = lower__value_seq(_cdy_items_46, n)
            _cdy_stmts_50 = _cdy__tup_49[0]
            _cdy_vals_51 = _cdy__tup_49[1]
            _cdy_n1_52 = _cdy__tup_49[2]
            return lower__Low(_cdy_stmts_50, core__Tuple(_cdy_vals_51, _cdy_pos_47, _cdy_ty_48), _cdy_n1_52)
        elif isinstance(_cdy_t70, core__Fmt):
            parts = _cdy_t70.parts
            _cdy_pos_54 = _cdy_t70.pos
            _cdy_ty_55 = _cdy_t70.t
            _cdy__tup_56 = lower__value_seq(lower__holes(parts), n)
            _cdy_stmts_57 = _cdy__tup_56[0]
            _cdy_vals_58 = _cdy__tup_56[1]
            _cdy_n1_59 = _cdy__tup_56[2]
            return lower__Low(_cdy_stmts_57, core__Fmt(lower__fill_holes(parts, _cdy_vals_58, ()), _cdy_pos_54, _cdy_ty_55), _cdy_n1_59)
        elif isinstance(_cdy_t70, core__Field):
            obj = _cdy_t70.obj
            field = _cdy_t70.field
            _cdy_pos_62 = _cdy_t70.pos
            _cdy_ty_63 = _cdy_t70.t
            _cdy_low_64 = lower__value(obj, n)
            return lower__Low(_cdy_low_64.stmts, core__Field(_cdy_low_64.expr, field, _cdy_pos_62, _cdy_ty_63), _cdy_low_64.n)
        elif isinstance(_cdy_t70, core__Assoc):
            _cdy_obj_65 = _cdy_t70.obj
            fields = _cdy_t70.fields
            _cdy_pos_67 = _cdy_t70.pos
            _cdy_ty_68 = _cdy_t70.t
            _cdy__tup_69 = lower__value_seq((cdy_rt.primitives.to_list(_cdy_obj_65) + lower__field_vals(fields)), n)
            _cdy_stmts_70 = _cdy__tup_69[0]
            _cdy_vals_71 = _cdy__tup_69[1]
            _cdy_n1_72 = _cdy__tup_69[2]
            return lower__Low(_cdy_stmts_70, core__Assoc(_cdy_vals_71[0], lower__refill(fields, prelude__rest(_cdy_vals_71), ()), _cdy_pos_67, _cdy_ty_68), _cdy_n1_72)
        elif isinstance(_cdy_t70, core__MatchE):
            _cdy_ty_73 = _cdy_t70.t
            tmp = core__Temp(n, _cdy_ty_73)
            _cdy__tup_75 = lower__lower_match(e, 'value', tmp, (n + 1))
            _cdy_stmts_76 = _cdy__tup_75[0]
            _cdy_n1_77 = _cdy__tup_75[1]
            return lower__Low(_cdy_stmts_76, tmp, _cdy_n1_77)
        else:
            return lower__Low((), e, n)

def lower__lower_match(e: core__Expr, mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t71: object = e
    if isinstance(_cdy_t71, core__MatchE):
        subject = _cdy_t71.subject
        clauses = _cdy_t71.clauses
        default = _cdy_t71.default
        low = lower__value(subject, n)
        temp = core__Temp(low.n, core__ANY)
        _tup = lower__lower_cases(clauses, mode, tmp, (low.n + 1))
        cases = _tup[0]
        n2 = _tup[1]
        _cdy__tup_90 = lower__lower_default(default, mode, tmp, n2)
        default_stmts = _cdy__tup_90[0]
        n3 = _cdy__tup_90[1]
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SMatch(temp, low.expr, cases, default_stmts))), n3)
    else:
        return cdy_rt.primitives.fail('internal error: lower: not a match')

def lower__lower_default(default: tuple[core__Expr, ...], mode: str, tmp: core__Expr, n: int) -> tuple[tuple[tuple[lower__Stmt, ...], ...], int]:
    if (len(default) == 0):
        return ((), n)
    else:
        _tup = lower__lower_body(default[0], mode, tmp, n)
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.primitives.to_list(stmts), n1)

def lower__lower_cases(clauses: tuple[core__Clause, ...], mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Case, ...], int]:
    def _cdy_t72(k: int, clause: core__Clause) -> tuple[int, lower__Case]:
        _cdy__tup_106 = lower__lower_body(clause.body, mode, tmp, k)
        body = _cdy__tup_106[0]
        k1 = _cdy__tup_106[1]
        return (k1, lower__Case(clause.variant, clause.binds, body))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t72, n, clauses)
    n1 = _tup[0]
    cases = _tup[1]
    return (cases, n1)

def lower__lower_body(e: core__Expr, mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    if (mode == 'tail'):
        return lower__tail(e, n)
    elif (mode == 'effect'):
        return lower__effect(e, n)
    else:
        low = lower__value(e, n)
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, low.expr))), low.n)

def lower__value_fn(params: tuple[core__Expr, ...], body: core__Expr, pos: form__Pos, ty: core__CType, n: int) -> lower__Low:
    _tup = lower__tail(body, n)
    stmts = _tup[0]
    n1 = _tup[1]
    _cdy_t73: object = (stmts[0] if (len(stmts) == 1) else lower__SExpr(core__NIL))
    if isinstance(_cdy_t73, lower__SReturn):
        result = _cdy_t73.val
        return lower__Low((), core__Lambda(params, result, pos, ty), n1)
    else:
        return lower__Low(cdy_rt.primitives.to_list(lower__SLocalFunc(core__Temp(n1, ty), params, stmts, ty)), core__Temp(n1, ty), (n1 + 1))

def lower__holes(parts: tuple[core__FPart, ...]) -> tuple[core__Expr, ...]:
    def _cdy_t75(acc: tuple[core__Expr, ...], part: core__FPart) -> tuple[core__Expr, ...]:
        _cdy_t74: object = part
        if isinstance(_cdy_t74, core__FHole):
            e = _cdy_t74.expr
            return (acc + (e,))
        else:
            assert isinstance(_cdy_t74, core__FText)
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t75, (), parts)

def lower__fill_holes(parts: tuple[core__FPart, ...], vals: tuple[core__Expr, ...], acc: tuple[core__FPart, ...]) -> tuple[core__FPart, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t76: object = parts[0]
            if isinstance(_cdy_t76, core__FHole):
                parts, vals, acc = (prelude__rest(parts), prelude__rest(vals), (acc + cdy_rt.primitives.to_list(core__FHole(vals[0]))))
                continue
            else:
                assert isinstance(_cdy_t76, core__FText)
                text = _cdy_t76.text
                parts, acc = (prelude__rest(parts), (acc + cdy_rt.primitives.to_list(core__FText(text))))
                continue

def lower__field_vals(fields: tuple[tuple[str, core__Expr], ...]) -> tuple[core__Expr, ...]:
    def _cdy_t77(field: tuple[str, core__Expr]) -> core__Expr:
        _tup = field
        _ = _tup[0]
        v = _tup[1]
        return v
    return cdy_rt.primitives.list_map(_cdy_t77, fields)

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

def lower__value_call(callee: core__Expr, args: tuple[core__Expr, ...], pos: form__Pos, ty: core__CType, n: int) -> lower__Low:
    if cdy_rt.primitives.list_contains(lower__prim_name(callee), ('and', 'or')):
        return lower__value_boolop(callee, args, pos, ty, n)
    else:
        _tup = lower__value_seq((cdy_rt.primitives.to_list(callee) + args), n)
        stmts = _tup[0]
        items = _tup[1]
        n1 = _tup[2]
        return lower__Low(stmts, core__Call(items[0], prelude__rest(items), pos, ty), n1)

def lower__prim_name(e: core__Expr) -> str:
    _cdy_t78: object = e
    if isinstance(_cdy_t78, core__Prim):
        name = _cdy_t78.name
        return name
    else:
        return ''

def lower__value_boolop(op: core__Expr, args: tuple[core__Expr, ...], pos: form__Pos, ty: core__CType, n: int) -> lower__Low:
    _tup = lower__low_all(args, n)
    lows = _tup[0]
    n1 = _tup[1]
    first = lows[0]
    later = prelude__rest(lows)
    if lower__has_stmts(later):
        tmp = core__Temp(n1, ty)
        return lower__Low((first.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, first.expr)) + cdy_rt.primitives.to_list(lower__guard(op, tmp, lower__guarded(op, later, tmp)))), tmp, (n1 + 1))
    else:
        return lower__Low(first.stmts, core__Call(op, lower__low_exprs(lows), pos, ty), n1)

def lower__guarded(op: core__Expr, lows: tuple[lower__Low, ...], tmp: core__Expr) -> tuple[lower__Stmt, ...]:
    low = lows[0]
    assign = (low.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, low.expr)))
    if (len(lows) == 1):
        return assign
    else:
        return (assign + cdy_rt.primitives.to_list(lower__guard(op, tmp, lower__guarded(op, prelude__rest(lows), tmp))))

def lower__guard(op: core__Expr, tmp: core__Expr, body: tuple[lower__Stmt, ...]) -> lower__Stmt:
    return lower__SIf((tmp if (lower__prim_name(op) == 'and') else core__Call(core__Prim('not', form__NOWHERE, core__ANY), cdy_rt.primitives.to_list(tmp), form__NOWHERE, core__ANY)), body, ())

def lower__low_exprs(lows: tuple[lower__Low, ...]) -> tuple[core__Expr, ...]:
    return cdy_rt.primitives.list_map((lambda low: low.expr), lows)

def lower__value_seq(exprs: tuple[core__Expr, ...], n: int) -> tuple[tuple[lower__Stmt, ...], tuple[core__Expr, ...], int]:
    _tup = lower__low_all(exprs, n)
    lows = _tup[0]
    n1 = _tup[1]
    return lower__seq_build(lows, n1, (), ())

def lower__low_all(exprs: tuple[core__Expr, ...], n: int) -> tuple[tuple[lower__Low, ...], int]:
    def _cdy_t79(k: int, e: core__Expr) -> tuple[int, lower__Low]:
        low = lower__value(e, k)
        return (low.n, low)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t79, n, exprs)
    n1 = _tup[0]
    lows = _tup[1]
    return (lows, n1)

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
                lows, n, stmts, out = (later, (n + 1), (stmts + low.stmts + cdy_rt.primitives.to_list(lower__SAssign(core__Temp(n, low.expr.t), low.expr))), (out + cdy_rt.primitives.to_list(core__Temp(n, low.expr.t))))
                continue
            else:
                lows, stmts, out = (later, (stmts + low.stmts), (out + cdy_rt.primitives.to_list(low.expr)))
                continue

def lower__value_if(test: core__Expr, then: core__Expr, other: core__Expr, pos: form__Pos, ty: core__CType, n: int) -> lower__Low:
    t = lower__value(test, n)
    a = lower__value(then, t.n)
    b = lower__value(other, a.n)
    if ((len(a.stmts) == 0) and (len(b.stmts) == 0)):
        return lower__Low(t.stmts, core__If(t.expr, a.expr, b.expr, pos, ty), b.n)
    elif lower__is_if_into(b.stmts, b.expr):
        tmp = b.expr
        return lower__Low((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, (a.stmts + cdy_rt.primitives.to_list(lower__SAssign(tmp, a.expr))), b.stmts))), tmp, b.n)
    else:
        _cdy_tmp_207 = core__Temp(b.n, ty)
        return lower__Low((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, (a.stmts + cdy_rt.primitives.to_list(lower__SAssign(_cdy_tmp_207, a.expr))), (b.stmts + cdy_rt.primitives.to_list(lower__SAssign(_cdy_tmp_207, b.expr)))))), _cdy_tmp_207, (b.n + 1))

def lower__is_if_into(stmts: tuple[lower__Stmt, ...], e: core__Expr) -> bool:
    _cdy_t84 = (len(stmts) == 1)
    if _cdy_t84:
        _cdy_t81: object = stmts[0]
        if isinstance(_cdy_t81, lower__SIf):
            _cdy_t80 = True
        else:
            _cdy_t80 = False
        _cdy_t84 = _cdy_t80
        if _cdy_t84:
            _cdy_t83: object = e
            if isinstance(_cdy_t83, core__Temp):
                _cdy_t82 = True
            else:
                _cdy_t82 = False
            _cdy_t84 = _cdy_t82
    return _cdy_t84

def lower__all_but_last(exprs: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    return cdy_rt.primitives.slice_(exprs, 0, (len(exprs) - 1))

def lower__last_of(exprs: tuple[core__Expr, ...]) -> core__Expr:
    return cdy_rt.primitives.at(exprs, (len(exprs) - 1))

def lower__value_do(body: tuple[core__Expr, ...], n: int) -> lower__Low:
    _tup = lower__effect_all(lower__all_but_last(body), n)
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
        _cdy__tup_224 = lower__tail(body, n1)
        more = _cdy__tup_224[0]
        n2 = _cdy__tup_224[1]
        return ((stmts + more), n2)
    else:
        return lower__tail_plain(e, n)

def lower__tail_plain(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t85: object = e
    if isinstance(_cdy_t85, core__If):
        test = _cdy_t85.test
        then = _cdy_t85.then
        other = _cdy_t85.other
        t = lower__value(test, n)
        _tup = lower__tail(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_236 = lower__tail(other, n1)
        b = _cdy__tup_236[0]
        n2 = _cdy__tup_236[1]
        return ((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t85, core__Do):
        body = _cdy_t85.body
        _cdy__tup_240 = lower__effect_all(lower__all_but_last(body), n)
        stmts = _cdy__tup_240[0]
        _cdy_n1_242 = _cdy__tup_240[1]
        _cdy__tup_243 = lower__tail(lower__last_of(body), _cdy_n1_242)
        last = _cdy__tup_243[0]
        _cdy_n2_245 = _cdy__tup_243[1]
        return ((stmts + last), _cdy_n2_245)
    elif isinstance(_cdy_t85, core__MatchE):
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
        _cdy__tup_253 = lower__effect(body, n1)
        more = _cdy__tup_253[0]
        n2 = _cdy__tup_253[1]
        return ((stmts + more), n2)
    else:
        return lower__effect_plain(e, n)

def lower__effect_plain(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t86: object = e
    if isinstance(_cdy_t86, core__If):
        test = _cdy_t86.test
        then = _cdy_t86.then
        other = _cdy_t86.other
        t = lower__value(test, n)
        _tup = lower__effect(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_265 = lower__effect(other, n1)
        b = _cdy__tup_265[0]
        n2 = _cdy__tup_265[1]
        return ((t.stmts + cdy_rt.primitives.to_list(lower__SIf(t.expr, a, b))), n2)
    elif isinstance(_cdy_t86, core__Do):
        body = _cdy_t86.body
        return lower__effect_all(body, n)
    elif isinstance(_cdy_t86, core__MatchE):
        return lower__lower_match(e, 'effect', core__NIL, n)
    else:
        if lower__is_simple(e):
            return ((), n)
        else:
            low = lower__value(e, n)
            return ((low.stmts + cdy_rt.primitives.to_list(lower__SExpr(low.expr))), low.n)

def lower__effect_all(exprs: tuple[core__Expr, ...], n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    def _cdy_t87(k: int, e: core__Expr) -> tuple[int, tuple[lower__Stmt, ...]]:
        _cdy__tup_274 = lower__effect(e, k)
        stmts = _cdy__tup_274[0]
        k1 = _cdy__tup_274[1]
        return (k1, stmts)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t87, n, exprs)
    n1 = _tup[0]
    parts = _tup[1]
    return (cdy_rt.primitives.list_concat(parts), n1)

def lower__returns_unit(t: core__CType) -> bool:
    _cdy_t88: object = t
    if isinstance(_cdy_t88, core__TFn):
        ret = _cdy_t88.ret
        _cdy_t89: object = ret
        if isinstance(_cdy_t89, core__TCon):
            name = _cdy_t89.name
            return (name == 'Unit')
        else:
            return False
    else:
        return False

def lower__lower_top(top: core__Top, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t90: object = top
    if isinstance(_cdy_t90, core__TDeft):
        name = _cdy_t90.name
        tvars = _cdy_t90.tvars
        fields = _cdy_t90.fields
        return (cdy_rt.primitives.to_list(lower__SRecord(name, tvars, fields)), n)
    elif isinstance(_cdy_t90, core__TDeftSum):
        _cdy_name_288 = _cdy_t90.name
        _cdy_tvars_289 = _cdy_t90.tvars
        variants = _cdy_t90.variants
        return (cdy_rt.primitives.to_list(lower__SSum(_cdy_name_288, _cdy_tvars_289, variants)), n)
    elif isinstance(_cdy_t90, core__TDef):
        _cdy_name_291 = _cdy_t90.name
        init = _cdy_t90.init
        t = _cdy_t90.t
        low = lower__value(init, n)
        return ((low.stmts + cdy_rt.primitives.to_list(lower__SDefAssign(_cdy_name_291, low.expr, t))), low.n)
    elif isinstance(_cdy_t90, core__TDefn):
        _cdy_name_295 = _cdy_t90.name
        params = _cdy_t90.params
        body = _cdy_t90.body
        _cdy_t_298 = _cdy_t90.t
        _tup = (lower__effect(body, n) if lower__returns_unit(_cdy_t_298) else lower__tail(body, n))
        stmts = _tup[0]
        n1 = _tup[1]
        return (cdy_rt.primitives.to_list(lower__SFunc(_cdy_name_295, params, (stmts if core__is_variadic(_cdy_t_298) else lower__loop_tail_calls(_cdy_name_295, params, stmts, lower__returns_unit(_cdy_t_298))), _cdy_t_298)), n1)
    else:
        assert isinstance(_cdy_t90, core__TExpr)
        e = _cdy_t90.expr
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
        return (cdy_rt.primitives.slice_(stmts, 0, (len(stmts) - 1)) + lower__retail(cdy_rt.primitives.at(stmts, (len(stmts) - 1)), name, params))

def lower__retail(s: lower__Stmt, name: str, params: tuple[core__Expr, ...]) -> tuple[lower__Stmt, ...]:
    _cdy_t91: object = s
    if isinstance(_cdy_t91, lower__SReturn):
        val = _cdy_t91.val
        if lower__is_self_call(val, name, params):
            return lower__jump(params, lower__call_args(val))
        else:
            return cdy_rt.primitives.to_list(s)
    elif isinstance(_cdy_t91, lower__SExpr):
        e = _cdy_t91.expr
        if lower__is_self_call(e, name, params):
            return lower__jump(params, lower__call_args(e))
        else:
            return cdy_rt.primitives.to_list(s)
    elif isinstance(_cdy_t91, lower__SIf):
        test = _cdy_t91.test
        then = _cdy_t91.then
        other = _cdy_t91.other
        return cdy_rt.primitives.to_list(lower__SIf(test, lower__retail_all(then, name, params), lower__retail_all(other, name, params)))
    elif isinstance(_cdy_t91, lower__SMatch):
        temp = _cdy_t91.temp
        subject = _cdy_t91.subject
        cases = _cdy_t91.cases
        default = _cdy_t91.default
        return cdy_rt.primitives.to_list(lower__SMatch(temp, subject, lower__retail_cases(cases, name, params), lower__retail_lists(default, name, params)))
    else:
        return cdy_rt.primitives.to_list(s)

def lower__retail_cases(cases: tuple[lower__Case, ...], name: str, params: tuple[core__Expr, ...]) -> tuple[lower__Case, ...]:
    return cdy_rt.primitives.list_map((lambda c: c._replace(body=lower__retail_all(c.body, name, params))), cases)

def lower__retail_lists(lists: tuple[tuple[lower__Stmt, ...], ...], name: str, params: tuple[core__Expr, ...]) -> tuple[tuple[lower__Stmt, ...], ...]:
    return cdy_rt.primitives.list_map((lambda stmts: lower__retail_all(stmts, name, params)), lists)

def lower__is_self_call(e: core__Expr, name: str, params: tuple[core__Expr, ...]) -> bool:
    _cdy_t92: object = e
    if isinstance(_cdy_t92, core__Call):
        callee = _cdy_t92.callee
        args = _cdy_t92.args
        _cdy_t93: object = callee
        if isinstance(_cdy_t93, core__Global):
            g = _cdy_t93.name
            return ((g == name) and (len(args) == len(params)))
        else:
            return False
    else:
        return False

def lower__call_args(e: core__Expr) -> tuple[core__Expr, ...]:
    _cdy_t94: object = e
    if isinstance(_cdy_t94, core__Call):
        args = _cdy_t94.args
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

def lower__same_local(param: core__Expr, e: core__Expr) -> bool:
    _cdy_t95: object = param
    if isinstance(_cdy_t95, core__Local):
        name = _cdy_t95.name
        id_ = _cdy_t95.id_
        _cdy_t96: object = e
        if isinstance(_cdy_t96, core__Local):
            other = _cdy_t96.name
            oid = _cdy_t96.id_
            return ((name == other) and (id_ == oid))
        else:
            return False
    else:
        return False

def lower__changed(params: tuple[core__Expr, ...], args: tuple[core__Expr, ...], targets: tuple[core__Expr, ...], vals: tuple[core__Expr, ...]) -> tuple[tuple[core__Expr, ...], tuple[core__Expr, ...]]:
    while True:
        if (len(params) == 0):
            return (targets, vals)
        elif lower__same_local(params[0], args[0]):
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
    _cdy_t97: object = s
    if isinstance(_cdy_t97, lower__SLocalFunc):
        return True
    elif isinstance(_cdy_t97, lower__SAssign):
        target = _cdy_t97.target
        val = _cdy_t97.val
        return (lower__has_lambda(target) or lower__has_lambda(val))
    elif isinstance(_cdy_t97, lower__SDefAssign):
        _cdy_val_358 = _cdy_t97.val
        return lower__has_lambda(_cdy_val_358)
    elif isinstance(_cdy_t97, lower__SExpr):
        e = _cdy_t97.expr
        return lower__has_lambda(e)
    elif isinstance(_cdy_t97, lower__SReturn):
        _cdy_val_360 = _cdy_t97.val
        return lower__has_lambda(_cdy_val_360)
    elif isinstance(_cdy_t97, lower__SIf):
        test = _cdy_t97.test
        then = _cdy_t97.then
        other = _cdy_t97.other
        return (lower__has_lambda(test) or lower__stmts_have_closure(then) or lower__stmts_have_closure(other))
    elif isinstance(_cdy_t97, lower__SMatch):
        subject = _cdy_t97.subject
        cases = _cdy_t97.cases
        default = _cdy_t97.default
        return (lower__has_lambda(subject) or lower__cases_have_closure(cases) or lower__lists_have_closure(default))
    elif isinstance(_cdy_t97, lower__SLoop):
        body = _cdy_t97.body
        return lower__stmts_have_closure(body)
    elif isinstance(_cdy_t97, lower__SRebind):
        vals = _cdy_t97.vals
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
        _cdy_t98: object = e
        if isinstance(_cdy_t98, core__Lambda):
            return True
        elif isinstance(_cdy_t98, core__Call):
            callee = _cdy_t98.callee
            args = _cdy_t98.args
            return (lower__has_lambda(callee) or lower__any_lambda(args))
        elif isinstance(_cdy_t98, core__If):
            test = _cdy_t98.test
            then = _cdy_t98.then
            other = _cdy_t98.other
            return (lower__has_lambda(test) or lower__has_lambda(then) or lower__has_lambda(other))
        elif isinstance(_cdy_t98, core__Do):
            body = _cdy_t98.body
            return lower__any_lambda(body)
        elif isinstance(_cdy_t98, core__Tuple):
            items = _cdy_t98.items
            return lower__any_lambda(items)
        elif isinstance(_cdy_t98, core__ListOf):
            _cdy_items_380 = _cdy_t98.items
            return lower__any_lambda(_cdy_items_380)
        elif isinstance(_cdy_t98, core__Fmt):
            parts = _cdy_t98.parts
            return lower__any_lambda(lower__holes(parts))
        elif isinstance(_cdy_t98, core__Field):
            obj = _cdy_t98.obj
            e = obj
            continue
        elif isinstance(_cdy_t98, core__Assoc):
            _cdy_obj_383 = _cdy_t98.obj
            fields = _cdy_t98.fields
            return (lower__has_lambda(_cdy_obj_383) or lower__any_lambda(lower__field_vals(fields)))
        elif isinstance(_cdy_t98, core__MatchE):
            subject = _cdy_t98.subject
            e = subject
            continue
        else:
            return False

def lower__lower_program(tops: tuple[core__Top, ...], n: int) -> tuple[lower__Stmt, ...]:
    def _cdy_t99(k: int, top: core__Top) -> tuple[int, tuple[lower__Stmt, ...]]:
        _cdy__tup_390 = lower__lower_top(top, k)
        stmts = _cdy__tup_390[0]
        k1 = _cdy__tup_390[1]
        return (k1, stmts)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t99, n, tops)
    last = _tup[0]
    parts = _tup[1]
    return cdy_rt.primitives.list_concat(parts)

class emit__Env(_cdy_NamedTuple):
    globals_: _cdy_Mapping[str, str]
    locals_: _cdy_Mapping[int, str]
    taken: _cdy_Mapping[str, bool]
    generic: _cdy_Mapping[str, tuple[str, ...]]
    spellings: _cdy_Mapping[str, tuple[str, str, str]]
    narrowed: _cdy_Mapping[int, tuple[str, tuple[str, ...]]]
    fields: _cdy_Mapping[str, tuple[core__CType, ...]]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(emit__Env, 'Env', (), (('Map', 'String', 'String'), ('Map', 'Int', 'String'), ('Map', 'String', 'Bool'), ('Map', 'String', ('List', 'String')), ('Map', 'String', ('Tup', 'String', 'String', 'String')), ('Map', 'Int', ('Tup', 'String', ('List', 'String'))), ('Map', 'String', ('List', 'core__CType'))))
emit__HEADER: str = 'from __future__ import annotations\n\nfrom collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping\nfrom typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple, cast as _cdy_cast\n'

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

def emit__name_set(names: tuple[str, ...]) -> _cdy_Mapping[str, bool]:
    return cdy_rt.primitives.list_fold((lambda acc, n: cdy_rt.primitives.map_set(acc, n, True)), {}, names)
emit__PY_RESERVED: _cdy_Mapping[str, bool] = emit__name_set((('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'PythonFinalizationError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '_IncompleteInputError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'and', 'anext', 'any', 'as', 'ascii', 'assert', 'async', 'await', 'bin', 'bool', 'break', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'class', 'classmethod', 'compile', 'complex', 'continue', 'copyright', 'credits', 'def', 'del', 'delattr', 'dict', 'dir', 'divmod', 'elif', 'else', 'enumerate', 'eval', 'except', 'exec', 'exit', 'filter', 'finally', 'float', 'for', 'format', 'from', 'frozenset', 'getattr', 'global', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'if', 'import', 'in', 'input', 'int', 'is', 'isinstance', 'issubclass', 'iter', 'lambda', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'nonlocal', 'not', 'object', 'oct', 'open', 'or', 'ord', 'pass', 'pow', 'print', 'property', 'quit', 'raise', 'range', 'repr', 'return', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'try', 'tuple', 'type', 'vars', 'while', 'with', 'yield', 'zip') + ('math', 're', 'cdy_rt')))
emit__MANGLED: _cdy_Mapping[str, str] = cdy_rt.primitives.map_set(cdy_rt.primitives.map_set(cdy_rt.primitives.map_set({}, '-', '_'), '?', '_p'), '!', '_x')

def emit__py_mangle(name: str) -> str:
    out = emit__mangle_chars(name, 0, '')
    if (cdy_rt.primitives.map_has(emit__PY_RESERVED, out) or cdy_rt.primitives.starts_with(out, '_cdy_')):
        return (out + '_')
    else:
        return out

def emit__mangle_chars(name: str, i: int, acc: str) -> str:
    while True:
        if (i == len(name)):
            return acc
        else:
            i, acc = ((i + 1), (acc + emit__mangle_char(cdy_rt.primitives.substring(name, i, (i + 1)))))
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
    digit = cdy_rt.primitives.substring(emit__HEX_DIGITS, (n - (16 * (n // 16))), ((n - (16 * (n // 16))) + 1))
    if ((n < 16) and (width <= 1)):
        return digit
    else:
        return (emit__hex((n // 16), (width - 1)) + digit)

def emit__py_str(s: str) -> str:
    q = ('"' if (cdy_rt.primitives.str_contains("'", s) and (not cdy_rt.primitives.str_contains('"', s))) else "'")
    return (q + emit__escape_chars(s, q, 0, '') + q)

def emit__escape_chars(s: str, q: str, i: int, acc: str) -> str:
    while True:
        if (i == len(s)):
            return acc
        else:
            i, acc = ((i + 1), (acc + emit__escape_char(cdy_rt.primitives.substring(s, i, (i + 1)), q)))
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

def emit__global_names(tops: tuple[core__Top, ...], start: emit__Env) -> emit__Env:
    return cdy_rt.primitives.list_fold((lambda env, top: emit__add_globals(emit__top_names_of(top), env)), start, tops)

def emit__add_globals(names: tuple[str, ...], start: emit__Env) -> emit__Env:
    def _cdy_t100(env: emit__Env, name: str) -> emit__Env:
        py = emit__py_mangle(name)
        if (cdy_rt.primitives.map_has(env.taken, py) and (not cdy_rt.primitives.map_has(env.globals_, name))):
            return cdy_rt.primitives.fail((emit__candy_name(emit__holder(py, cdy_rt.primitives.map_keys(env.globals_), env.globals_)) + ' and ' + emit__candy_name(name) + ' are one name in Python (' + py + ')'))
        else:
            return env._replace(globals_=cdy_rt.primitives.map_set(env.globals_, name, py), taken=cdy_rt.primitives.map_set(env.taken, py, True))
    return cdy_rt.primitives.list_fold(_cdy_t100, start, names)

def emit__holder(py: str, names: tuple[str, ...], globals_: _cdy_Mapping[str, str]) -> str:
    return prelude__with_default(py, prelude__find((lambda n: (cdy_rt.primitives.map_get(globals_, n) == py)), names))

def emit__candy_name(name: str) -> str:
    parts = cdy_rt.primitives.split(name, '__')
    own = cdy_rt.primitives.join(prelude__rest(parts), '__')
    if (len(parts) == 1):
        return name
    else:
        return (own + ' (from module ' + parts[0] + ')')

def emit__own_name(name: str) -> str:
    parts = cdy_rt.primitives.split(name, '__')
    if (len(parts) == 1):
        return name
    else:
        return cdy_rt.primitives.join(prelude__rest(parts), '__')

def emit__top_names_of(top: core__Top) -> tuple[str, ...]:
    _cdy_t101: object = top
    if isinstance(_cdy_t101, core__TDeftSum):
        name = _cdy_t101.name
        variants = _cdy_t101.variants
        return (cdy_rt.primitives.to_list(name) + emit__variant_list_names(variants))
    else:
        if (emit__top_name(top) == ''):
            return ()
        else:
            return cdy_rt.primitives.to_list(emit__top_name(top))

def emit__variant_list_names(variants: tuple[core__Variant, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda v: v.name), variants)

def emit__top_name(top: core__Top) -> str:
    _cdy_t102: object = top
    if isinstance(_cdy_t102, core__TDeft):
        name = _cdy_t102.name
        return name
    elif isinstance(_cdy_t102, core__TDef):
        _cdy_name_50 = _cdy_t102.name
        return _cdy_name_50
    elif isinstance(_cdy_t102, core__TDefn):
        _cdy_name_51 = _cdy_t102.name
        return _cdy_name_51
    else:
        return ''

def emit__generic_variants(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, tuple[str, ...]]:
    return cdy_rt.primitives.list_fold((lambda m, top: emit__generic_sum(top, m)), {}, tops)

def emit__generic_sum(top: core__Top, acc: _cdy_Mapping[str, tuple[str, ...]]) -> _cdy_Mapping[str, tuple[str, ...]]:
    _cdy_t103: object = top
    if isinstance(_cdy_t103, core__TDeftSum):
        tvars = _cdy_t103.tvars
        variants = _cdy_t103.variants
        if (len(tvars) == 0):
            return acc
        else:
            return cdy_rt.primitives.list_fold((lambda m, v: cdy_rt.primitives.map_set(m, v.name, emit__generic_fields(v.fields))), acc, variants)
    else:
        return acc

def emit__deft_field_types(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, tuple[core__CType, ...]]:
    return cdy_rt.primitives.list_fold((lambda m, top: emit__top_field_types(top, m)), {}, tops)

def emit__top_field_types(top: core__Top, acc: _cdy_Mapping[str, tuple[core__CType, ...]]) -> _cdy_Mapping[str, tuple[core__CType, ...]]:
    _cdy_t104: object = top
    if isinstance(_cdy_t104, core__TDeft):
        name = _cdy_t104.name
        fields = _cdy_t104.fields
        return cdy_rt.primitives.map_set(acc, name, emit__field_types(fields))
    elif isinstance(_cdy_t104, core__TDeftSum):
        _cdy_name_68 = _cdy_t104.name
        variants = _cdy_t104.variants
        return cdy_rt.primitives.list_fold((lambda m, v: cdy_rt.primitives.map_set(m, v.name, emit__field_types(v.fields))), cdy_rt.primitives.map_set(acc, _cdy_name_68, cdy_rt.primitives.list_map((lambda v: core__TCon(v.name, ())), variants)), variants)
    else:
        return acc

def emit__generic_fields(fields: tuple[tuple[str, core__CType], ...]) -> tuple[str, ...]:
    def _cdy_t105(f: tuple[str, core__CType]) -> str:
        _tup = f
        name = _tup[0]
        _t = _tup[1]
        return name
    def _cdy_t106(f: tuple[str, core__CType]) -> bool:
        _tup = f
        _name = _tup[0]
        t = _tup[1]
        return (len(emit__type_vars(cdy_rt.primitives.to_list(t), ())) > 0)
    return cdy_rt.primitives.list_map(_cdy_t105, cdy_rt.primitives.list_filter(_cdy_t106, fields))

def emit__local_py(name: str, id_: int, env: emit__Env) -> str:
    if cdy_rt.primitives.map_has(env.locals_, id_):
        return cdy_rt.primitives.map_get(env.locals_, id_)
    else:
        return cdy_rt.primitives.fail(('internal error: emit: local ' + name + ' has no Python name'))

def emit__bind_locals(locs: tuple[core__Expr, ...], start: emit__Env) -> emit__Env:
    def _cdy_t108(env: emit__Env, loc: core__Expr) -> emit__Env:
        _cdy_t107: object = loc
        if isinstance(_cdy_t107, core__Local):
            name = _cdy_t107.name
            id_ = _cdy_t107.id_
            if cdy_rt.primitives.map_has(env.locals_, id_):
                return env
            else:
                base = emit__py_mangle(name)
                py = (('_cdy_' + base + '_' + str(id_)) if cdy_rt.primitives.map_has(env.taken, base) else base)
                return env._replace(locals_=cdy_rt.primitives.map_set(env.locals_, id_, py), taken=cdy_rt.primitives.map_set(env.taken, py, True))
        else:
            return env
    return cdy_rt.primitives.list_fold(_cdy_t108, start, locs)

def emit__bound_locals(stmts: tuple[lower__Stmt, ...], start: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    def _cdy_t111(acc: tuple[core__Expr, ...], stmt: lower__Stmt) -> tuple[core__Expr, ...]:
        _cdy_t109: object = stmt
        if isinstance(_cdy_t109, lower__SAssign):
            target = _cdy_t109.target
            _cdy_t110: object = target
            if isinstance(_cdy_t110, core__Local):
                return (acc + cdy_rt.primitives.to_list(target))
            else:
                return acc
        elif isinstance(_cdy_t109, lower__SIf):
            then = _cdy_t109.then
            other = _cdy_t109.other
            return emit__bound_locals(other, emit__bound_locals(then, acc))
        elif isinstance(_cdy_t109, lower__SMatch):
            cases = _cdy_t109.cases
            default = _cdy_t109.default
            return emit__bound_in_cases(cases, emit__bound_in_lists(default, acc))
        elif isinstance(_cdy_t109, lower__SLoop):
            body = _cdy_t109.body
            return emit__bound_locals(body, acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t111, start, stmts)

def emit__bound_in_cases(cases: tuple[lower__Case, ...], start: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    return cdy_rt.primitives.list_fold((lambda acc, c: emit__bound_locals(c.body, (acc + emit__bind_locs(c.binds)))), start, cases)

def emit__bind_locs(binds: tuple[tuple[str, core__Expr], ...]) -> tuple[core__Expr, ...]:
    def _cdy_t112(b: tuple[str, core__Expr]) -> core__Expr:
        _tup = b
        _ = _tup[0]
        loc = _tup[1]
        return loc
    return cdy_rt.primitives.list_map(_cdy_t112, binds)

def emit__bound_in_lists(lists: tuple[tuple[lower__Stmt, ...], ...], start: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    return cdy_rt.primitives.list_fold((lambda acc, stmts: emit__bound_locals(stmts, acc)), start, lists)

def emit__emit_expr(e: core__Expr, env: emit__Env) -> str:
    while True:
        _cdy_t113: object = e
        if isinstance(_cdy_t113, core__Lit):
            form = _cdy_t113.form
            return emit__emit_lit(form)
        elif isinstance(_cdy_t113, core__Local):
            name = _cdy_t113.name
            id_ = _cdy_t113.id_
            return emit__local_py(name, id_, env)
        elif isinstance(_cdy_t113, core__Global):
            _cdy_name_121 = _cdy_t113.name
            return cdy_rt.primitives.map_get(env.globals_, _cdy_name_121)
        elif isinstance(_cdy_t113, core__Prim):
            _cdy_name_122 = _cdy_t113.name
            pos = _cdy_t113.pos
            t = _cdy_t113.t
            return emit__emit_prim(_cdy_name_122, pos, t, env)
        elif isinstance(_cdy_t113, core__Call):
            callee = _cdy_t113.callee
            args = _cdy_t113.args
            return emit__emit_call(callee, args, env)
        elif isinstance(_cdy_t113, core__If):
            test = _cdy_t113.test
            then = _cdy_t113.then
            other = _cdy_t113.other
            return ('(' + emit__emit_expr(then, env) + ' if ' + emit__emit_expr(test, env) + ' else ' + emit__emit_expr(other, env) + ')')
        elif isinstance(_cdy_t113, core__Do):
            return cdy_rt.primitives.fail('internal error: emit: a do inside an expression (lower should have removed it)')
        elif isinstance(_cdy_t113, core__MatchE):
            return cdy_rt.primitives.fail('internal error: emit: a match inside an expression (lower should have removed it)')
        elif isinstance(_cdy_t113, core__Lambda):
            params = _cdy_t113.params
            body = _cdy_t113.body
            inner = emit__bind_locals(params, env)
            return ('(lambda ' + emit__comma_join(emit__emit_exprs(params, inner)) + ': ' + emit__emit_expr(body, inner) + ')')
        elif isinstance(_cdy_t113, core__Tuple):
            items = _cdy_t113.items
            strs = emit__emit_exprs(items, env)
            if (len(strs) == 1):
                return ('(' + strs[0] + ',)')
            else:
                return ('(' + emit__comma_join(strs) + ')')
        elif isinstance(_cdy_t113, core__ListOf):
            _cdy_items_135 = _cdy_t113.items
            _cdy_pos_136 = _cdy_t113.pos
            _cdy_t_137 = _cdy_t113.t
            e = core__Tuple(_cdy_items_135, _cdy_pos_136, _cdy_t_137)
            continue
        elif isinstance(_cdy_t113, core__Fmt):
            parts = _cdy_t113.parts
            _cdy_pos_139 = _cdy_t113.pos
            return emit__emit_format(parts, _cdy_pos_139, env)
        elif isinstance(_cdy_t113, core__Field):
            obj = _cdy_t113.obj
            field = _cdy_t113.field
            _cdy_t_142 = _cdy_t113.t
            return emit__emit_get(obj, field, _cdy_t_142, env)
        elif isinstance(_cdy_t113, core__Assoc):
            _cdy_obj_143 = _cdy_t113.obj
            fields = _cdy_t113.fields
            return (emit__emit_obj(_cdy_obj_143, env) + '._replace(' + emit__comma_join(emit__emit_fields(fields, env)) + ')')
        else:
            assert isinstance(_cdy_t113, core__Temp)
            _cdy_id__145 = _cdy_t113.id_
            return ('_cdy_t' + str(_cdy_id__145))

def emit__emit_obj(obj: core__Expr, env: emit__Env) -> str:
    _cdy_t114: object = obj
    if isinstance(_cdy_t114, core__Local):
        id_ = _cdy_t114.id_
        if cdy_rt.primitives.map_has(env.narrowed, id_):
            _tup = cdy_rt.primitives.map_get(env.narrowed, id_)
            tmp = _tup[0]
            _fields = _tup[1]
            return tmp
        else:
            return emit__emit_expr(obj, env)
    else:
        return emit__emit_expr(obj, env)

def emit__emit_get(obj: core__Expr, field: str, t: core__CType, env: emit__Env) -> str:
    text = (emit__emit_obj(obj, env) + '.' + emit__py_mangle(field))
    _cdy_t115: object = obj
    if isinstance(_cdy_t115, core__Local):
        id_ = _cdy_t115.id_
        _cdy_t116 = cdy_rt.primitives.map_has(env.narrowed, id_)
        if _cdy_t116:
            _tup = cdy_rt.primitives.map_get(env.narrowed, id_)
            _tmp = _tup[0]
            fields = _tup[1]
            _cdy_t116 = cdy_rt.primitives.list_contains(field, fields)
        if _cdy_t116:
            return ("_cdy_cast('" + emit__emit_type(t, env) + "', " + text + ')')
        else:
            return text
    else:
        return text

def emit__emit_format(parts: tuple[core__FPart, ...], pos: form__Pos, env: emit__Env) -> str:
    if (len(parts) == 0):
        return "''"
    else:
        return ('(' + cdy_rt.primitives.join(emit__emit_parts(parts, pos, env), ' + ') + ')')

def emit__emit_parts(parts: tuple[core__FPart, ...], pos: form__Pos, env: emit__Env) -> tuple[str, ...]:
    def _cdy_t118(p: core__FPart) -> str:
        _cdy_t117: object = p
        if isinstance(_cdy_t117, core__FText):
            text = _cdy_t117.text
            return emit__py_str(text)
        else:
            assert isinstance(_cdy_t117, core__FHole)
            e = _cdy_t117.expr
            return emit__emit_text(e, pos, env)
    return cdy_rt.primitives.list_map(_cdy_t118, parts)

def emit__emit_text(e: core__Expr, pos: form__Pos, env: emit__Env) -> str:
    return emit__text_of(emit__emit_expr(e, env), e.t, pos, env)

def emit__text_of(x: str, t: core__CType, pos: form__Pos, env: emit__Env) -> str:
    _cdy_t120: object = t
    if isinstance(_cdy_t120, core__TCon):
        name = _cdy_t120.name
        _cdy_t119 = name
    else:
        _cdy_t119 = ''
    _cdy_name_178 = _cdy_t119
    if cdy_rt.primitives.list_contains(_cdy_name_178, ('String', 'Char')):
        return x
    elif (_cdy_name_178 == 'Int'):
        return ('str(' + x + ')')
    elif (_cdy_name_178 == 'Any'):
        return ('cdy_rt.primitives.text_any(' + x + ')')
    else:
        return emit__show_call(x, t, pos, env)

def emit__show_call(x: str, t: core__CType, pos: form__Pos, env: emit__Env) -> str:
    return ('cdy_rt.primitives.show(' + x + ', ' + emit__show_type(t, pos, env) + ')')

def emit__show_type(t: core__CType, pos: form__Pos, env: emit__Env) -> str:
    _cdy_t121: object = t
    if isinstance(_cdy_t121, core__TCon):
        name = _cdy_t121.name
        args = _cdy_t121.args
        if emit__holds_fn(name, env, (name,)):
            return cdy_rt.primitives.fail((form__pos_text(pos) + ("show: a function can't be shown, and " + name + ' holds one')))
        elif (len(args) == 0):
            return emit__py_str(name)
        else:
            return ('(' + emit__comma_join((cdy_rt.primitives.to_list(emit__py_str(name)) + cdy_rt.primitives.list_map((lambda a: emit__show_type(a, pos, env)), args))) + ')')
    elif isinstance(_cdy_t121, core__TFn):
        return cdy_rt.primitives.fail((form__pos_text(pos) + "show: a function can't be shown"))
    else:
        assert isinstance(_cdy_t121, core__TVar)
        _cdy_name_189 = _cdy_t121.name
        shown = (('t' + cdy_rt.primitives.substring(_cdy_name_189, 1, len(_cdy_name_189))) if cdy_rt.primitives.starts_with(_cdy_name_189, '?') else _cdy_name_189)
        return cdy_rt.primitives.fail((form__pos_text(pos) + ("show: can't show a value of type " + shown + ', a type variable')))

def emit__holds_fn(name: str, env: emit__Env, seen: tuple[str, ...]) -> bool:
    return (cdy_rt.primitives.map_has(env.fields, name) and cdy_rt.primitives.list_any((lambda t: emit__field_holds_fn(t, env, seen)), cdy_rt.primitives.map_get(env.fields, name)))

def emit__field_holds_fn(t: core__CType, env: emit__Env, seen: tuple[str, ...]) -> bool:
    _cdy_t122: object = t
    if isinstance(_cdy_t122, core__TFn):
        return True
    elif isinstance(_cdy_t122, core__TCon):
        name = _cdy_t122.name
        args = _cdy_t122.args
        return (cdy_rt.primitives.list_any((lambda a: emit__field_holds_fn(a, env, seen)), args) or ((not cdy_rt.primitives.list_contains(name, seen)) and emit__holds_fn(name, env, (seen + (name,)))))
    else:
        return False

def emit__field_show_type(t: core__CType) -> str:
    _cdy_t123: object = t
    if isinstance(_cdy_t123, core__TCon):
        name = _cdy_t123.name
        args = _cdy_t123.args
        if (len(args) == 0):
            return emit__py_str(name)
        else:
            return ('(' + emit__comma_join((cdy_rt.primitives.to_list(emit__py_str(name)) + cdy_rt.primitives.list_map(emit__field_show_type, args))) + ')')
    elif isinstance(_cdy_t123, core__TFn):
        return emit__py_str('Fn')
    else:
        assert isinstance(_cdy_t123, core__TVar)
        _cdy_name_204 = _cdy_t123.name
        return emit__py_str(("'" + _cdy_name_204))

def emit__register_line(name: str, shown: str, tvars: tuple[str, ...], fields: tuple[tuple[str, core__CType], ...], level: int, env: emit__Env) -> str:
    _cdy_t125 = cdy_rt.primitives.map_get(env.globals_, name)
    _cdy_t126 = emit__py_str(shown)
    _cdy_t127 = emit__py_tuple(cdy_rt.primitives.list_map(emit__py_str, tvars))
    def _cdy_t124(f: tuple[str, core__CType]) -> str:
        _tup = f
        _name = _tup[0]
        t = _tup[1]
        return emit__field_show_type(t)
    return emit__line(level, ('cdy_rt.primitives.register_type(' + _cdy_t125 + ', ' + _cdy_t126 + ', ' + _cdy_t127 + ', ' + emit__py_tuple(cdy_rt.primitives.list_map(_cdy_t124, fields)) + ')'))

def emit__py_tuple(items: tuple[str, ...]) -> str:
    if (len(items) == 1):
        return ('(' + items[0] + ',)')
    else:
        return ('(' + emit__comma_join(items) + ')')

def emit__emit_fields(fields: tuple[tuple[str, core__Expr], ...], env: emit__Env) -> tuple[str, ...]:
    def _cdy_t128(fv: tuple[str, core__Expr]) -> str:
        _tup = fv
        f = _tup[0]
        v = _tup[1]
        return (emit__py_mangle(f) + '=' + emit__emit_expr(v, env))
    return cdy_rt.primitives.list_map(_cdy_t128, fields)

def emit__emit_exprs(exprs: tuple[core__Expr, ...], env: emit__Env) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda e: emit__emit_expr(e, env)), exprs)

def emit__emit_lit(form: form__Form) -> str:
    _cdy_t129: object = form
    if isinstance(_cdy_t129, form__Txt):
        v = _cdy_t129.val
        return emit__py_str(v)
    elif isinstance(_cdy_t129, form__CharLit):
        _cdy_v_227 = _cdy_t129.val
        return emit__py_str((_cdy_v_227))
    elif isinstance(_cdy_t129, form__IntLit):
        _cdy_v_228 = _cdy_t129.val
        return (str(_cdy_v_228))
    elif isinstance(_cdy_t129, form__LongLit):
        _cdy_v_229 = _cdy_t129.val
        return (str(_cdy_v_229))
    elif isinstance(_cdy_t129, form__ByteLit):
        _cdy_v_230 = _cdy_t129.val
        return (str(_cdy_v_230))
    elif isinstance(_cdy_t129, form__FloatLit):
        _cdy_v_231 = _cdy_t129.val
        return (cdy_rt.primitives.show(_cdy_v_231, 'Double'))
    elif isinstance(_cdy_t129, form__DoubleLit):
        _cdy_v_232 = _cdy_t129.val
        return (cdy_rt.primitives.show(_cdy_v_232, 'Double'))
    elif isinstance(_cdy_t129, form__BoolLit):
        _cdy_v_233 = _cdy_t129.val
        if _cdy_v_233:
            return 'True'
        else:
            return 'False'
    else:
        return cdy_rt.primitives.fail('internal error: emit: not a literal')

def emit__emit_prim(name: str, pos: form__Pos, t: core__CType, env: emit__Env) -> str:
    if (name == 'show'):
        _cdy_t130: object = t
        if isinstance(_cdy_t130, core__TFn):
            params = _cdy_t130.params
            return ('(lambda _cdy_x: ' + emit__show_call('_cdy_x', params[0], pos, env) + ')')
        else:
            return cdy_rt.primitives.fail((form__pos_text(pos) + "show: its type isn't known here"))
    elif (name == 'text'):
        _cdy_t131: object = t
        if isinstance(_cdy_t131, core__TFn):
            _cdy_params_239 = _cdy_t131.params
            return ('(lambda _cdy_x: ' + emit__text_of('_cdy_x', _cdy_params_239[0], pos, env) + ')')
        else:
            return cdy_rt.primitives.fail((form__pos_text(pos) + "text: its type isn't known here"))
    elif cdy_rt.primitives.list_contains(core__spelling_kind(env.spellings, name), core__TYPED_KINDS):
        return core__spelling_py(env.spellings, name)
    elif (core__spelling_value(env.spellings, name) != ''):
        return core__spelling_value(env.spellings, name)
    else:
        return cdy_rt.primitives.fail((form__pos_text(pos) + ('the operator ' + name + " can't be used as a value, for now; wrap it in a fn")))

def emit__emit_call(callee: core__Expr, args: tuple[core__Expr, ...], env: emit__Env) -> str:
    strs = emit__emit_exprs(args, env)
    _cdy_t132: object = callee
    if isinstance(_cdy_t132, core__Prim):
        name = _cdy_t132.name
        pos = _cdy_t132.pos
        if (name == 'text'):
            return emit__emit_text(args[0], pos, env)
        elif (name == 'show'):
            return emit__show_call(strs[0], args[0].t, pos, env)
        else:
            return emit__emit_prim_call(name, args, strs, env)
    else:
        return (emit__emit_expr(callee, env) + '(' + emit__comma_join(strs) + ')')

def emit__is_index_literal(e: core__Expr) -> bool:
    _cdy_t133: object = e
    if isinstance(_cdy_t133, core__Lit):
        form = _cdy_t133.form
        _cdy_t134: object = form
        if isinstance(_cdy_t134, form__IntLit):
            v = _cdy_t134.val
            return (v >= 0)
        else:
            return False
    else:
        return False

def emit__emit_prim_call(name: str, args: tuple[core__Expr, ...], strs: tuple[str, ...], env: emit__Env) -> str:
    kind = core__spelling_kind(env.spellings, name)
    py = core__spelling_py(env.spellings, name)
    op = (' ' + py + ' ')
    if cdy_rt.primitives.list_contains(kind, ('binop', 'compare', 'boolop')):
        return ('(' + cdy_rt.primitives.join(strs, op) + ')')
    elif (kind == 'unary'):
        return ('(' + py + ' ' + strs[0] + ')')
    elif ((kind == 'index') and emit__is_index_literal(args[1])):
        return (strs[0] + '[' + strs[1] + ']')
    else:
        return (py + '(' + emit__comma_join(strs) + ')')

def emit__emit_type(t: core__CType, env: emit__Env) -> str:
    _cdy_t135: object = t
    if isinstance(_cdy_t135, core__TVar):
        name = _cdy_t135.name
        if cdy_rt.primitives.starts_with(name, '?'):
            return '_cdy_Any'
        elif (core__constraint_of(name) == 'integer'):
            return 'int'
        elif (core__constraint_of(name) == 'float'):
            return 'float'
        else:
            return emit__py_mangle(name)
    elif isinstance(_cdy_t135, core__TFn):
        params = _cdy_t135.params
        ret = _cdy_t135.ret
        return ('_cdy_Callable[[' + emit__comma_join(emit__emit_types(params, env)) + '], ' + emit__emit_type(ret, env) + ']')
    else:
        assert isinstance(_cdy_t135, core__TCon)
        _cdy_name_261 = _cdy_t135.name
        args = _cdy_t135.args
        return emit__emit_tcon(_cdy_name_261, emit__emit_types(args, env), env.spellings)

def emit__emit_types(types: tuple[core__CType, ...], env: emit__Env) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda t: emit__emit_type(t, env)), types)

def emit__emit_tcon(name: str, args: tuple[str, ...], spellings: _cdy_Mapping[str, tuple[str, str, str]]) -> str:
    if (core__spelling_kind(spellings, name) == 'type'):
        return cdy_rt.primitives.replace(core__spelling_py(spellings, name), '{}', emit__comma_join(args))
    elif (name == 'Tup'):
        return ('tuple[' + emit__comma_join(args) + ']')
    elif (len(args) == 0):
        return emit__py_mangle(name)
    else:
        return (emit__py_mangle(name) + '[' + emit__comma_join(args) + ']')

def emit__type_vars(types: tuple[core__CType, ...], start: tuple[str, ...]) -> tuple[str, ...]:
    def _cdy_t137(acc: tuple[str, ...], t: core__CType) -> tuple[str, ...]:
        _cdy_t136: object = t
        if isinstance(_cdy_t136, core__TVar):
            name = _cdy_t136.name
            if cdy_rt.primitives.list_contains(name, acc):
                return acc
            else:
                return (acc + cdy_rt.primitives.to_list(name))
        elif isinstance(_cdy_t136, core__TCon):
            args = _cdy_t136.args
            return emit__type_vars(args, acc)
        else:
            assert isinstance(_cdy_t136, core__TFn)
            params = _cdy_t136.params
            ret = _cdy_t136.ret
            return emit__type_vars((params + cdy_rt.primitives.to_list(ret)), acc)
    return cdy_rt.primitives.list_fold(_cdy_t137, start, types)

def emit__emit_stmt(s: lower__Stmt, level: int, env: emit__Env) -> str:
    _cdy_t138: object = s
    if isinstance(_cdy_t138, lower__SRecord):
        name = _cdy_t138.name
        tvars = _cdy_t138.tvars
        fields = _cdy_t138.fields
        checked = emit__check_py_fields(('deft ' + emit__candy_name(name)), fields, {})
        return ('\n' + emit__line(level, ('class ' + cdy_rt.primitives.map_get(env.globals_, name) + emit__type_params(tvars) + '(_cdy_NamedTuple):')) + emit__emit_record_fields(fields, (level + 1), env) + emit__eq_methods((level + 1)) + emit__register_line(name, emit__own_name(name), tvars, fields, level, env))
    elif isinstance(_cdy_t138, lower__SSum):
        _cdy_name_284 = _cdy_t138.name
        _cdy_tvars_285 = _cdy_t138.tvars
        variants = _cdy_t138.variants
        return (emit__emit_variants(_cdy_name_284, variants, _cdy_tvars_285, level, env) + emit__line(level, ('type ' + cdy_rt.primitives.map_get(env.globals_, _cdy_name_284) + emit__type_params(_cdy_tvars_285) + ' = ' + cdy_rt.primitives.join(emit__variant_refs(variants, _cdy_tvars_285, env), ' | '))))
    elif isinstance(_cdy_t138, lower__SMatch):
        temp = _cdy_t138.temp
        subject = _cdy_t138.subject
        cases = _cdy_t138.cases
        default = _cdy_t138.default
        t = emit__emit_expr(temp, env)
        val = emit__emit_expr(subject, env)
        generic = cdy_rt.primitives.map_has(env.generic, cases[0].variant)
        return (emit__line(level, ((t + ' = ' + val) if generic else (t + ': object = ' + val))) + emit__emit_match(t, cases, default, ((not generic) and (len(default) == 0)), 'if', level, env, subject))
    elif isinstance(_cdy_t138, lower__SLoop):
        body = _cdy_t138.body
        return (emit__line(level, 'while True:') + emit__emit_block(body, (level + 1), env))
    elif isinstance(_cdy_t138, lower__SRebind):
        targets = _cdy_t138.targets
        vals = _cdy_t138.vals
        return emit__line(level, ((emit__emit_expr(targets[0], env) + ' = ' + emit__emit_expr(vals[0], env)) if (len(targets) == 1) else (emit__comma_join(emit__emit_exprs(targets, env)) + ' = (' + emit__comma_join(emit__emit_exprs(vals, env)) + ')')))
    elif isinstance(_cdy_t138, lower__SContinue):
        return emit__line(level, 'continue')
    elif isinstance(_cdy_t138, lower__SAssign):
        target = _cdy_t138.target
        _cdy_val_298 = _cdy_t138.val
        return emit__line(level, (emit__emit_expr(target, env) + emit__lambda_annotation(target, _cdy_val_298, env) + ' = ' + emit__emit_expr(_cdy_val_298, env)))
    elif isinstance(_cdy_t138, lower__SDefAssign):
        _cdy_name_299 = _cdy_t138.name
        _cdy_val_300 = _cdy_t138.val
        _cdy_t_301 = _cdy_t138.t
        return emit__line(level, (cdy_rt.primitives.map_get(env.globals_, _cdy_name_299) + ': ' + emit__emit_type(_cdy_t_301, env) + ' = ' + emit__emit_expr(_cdy_val_300, env)))
    elif isinstance(_cdy_t138, lower__SExpr):
        e = _cdy_t138.expr
        return emit__line(level, emit__emit_expr(e, env))
    elif isinstance(_cdy_t138, lower__SReturn):
        _cdy_e_303 = _cdy_t138.val
        return emit__line(level, ('return ' + emit__emit_expr(_cdy_e_303, env)))
    elif isinstance(_cdy_t138, lower__SIf):
        test = _cdy_t138.test
        then = _cdy_t138.then
        other = _cdy_t138.other
        return emit__emit_if('if', test, then, other, level, env)
    elif isinstance(_cdy_t138, lower__SFunc):
        _cdy_name_307 = _cdy_t138.name
        params = _cdy_t138.params
        _cdy_body_309 = _cdy_t138.body
        _cdy_t_310 = _cdy_t138.t
        return emit__emit_func(_cdy_name_307, params, _cdy_body_309, _cdy_t_310, level, env)
    else:
        assert isinstance(_cdy_t138, lower__SLocalFunc)
        _cdy_target_311 = _cdy_t138.target
        _cdy_params_312 = _cdy_t138.params
        _cdy_body_313 = _cdy_t138.body
        _cdy_t_314 = _cdy_t138.t
        inner = emit__bind_locals((_cdy_params_312 + emit__bound_locals(_cdy_body_313, ())), env)
        _cdy_t139: object = _cdy_t_314
        if isinstance(_cdy_t139, core__TFn):
            types = _cdy_t139.params
            ret = _cdy_t139.ret
            return (emit__line(level, ('def ' + emit__emit_expr(_cdy_target_311, env) + '(' + emit__comma_join(emit__emit_params(_cdy_params_312, types, inner, ())) + ') -> ' + emit__emit_type(ret, env) + ':')) + emit__emit_block(_cdy_body_313, (level + 1), inner))
        else:
            return (emit__line(level, ('def ' + emit__emit_expr(_cdy_target_311, env) + '(' + emit__comma_join(emit__emit_any_params(_cdy_params_312, inner)) + ') -> _cdy_Any:')) + emit__emit_block(_cdy_body_313, (level + 1), inner))

def emit__lambda_annotation(target: core__Expr, val: core__Expr, env: emit__Env) -> str:
    _cdy_t140: object = target
    if isinstance(_cdy_t140, core__Local):
        _cdy_t141: object = val
        if isinstance(_cdy_t141, core__Lambda):
            t = _cdy_t141.t
            _cdy_t142: object = t
            if isinstance(_cdy_t142, core__TFn):
                return (': ' + emit__emit_type(t, env))
            else:
                return ''
        else:
            return ''
    else:
        return ''

def emit__emit_if(keyword: str, test: core__Expr, then: tuple[lower__Stmt, ...], other: tuple[lower__Stmt, ...], level: int, env: emit__Env) -> str:
    _cdy_t146 = emit__line(level, (keyword + ' ' + emit__emit_expr(test, env) + ':'))
    _cdy_t147 = emit__emit_block(then, (level + 1), env)
    if (len(other) == 0):
        _cdy_t145 = ''
    elif (len(other) == 1):
        _cdy_t144: object = other[0]
        if isinstance(_cdy_t144, lower__SIf):
            test2 = _cdy_t144.test
            then2 = _cdy_t144.then
            other2 = _cdy_t144.other
            _cdy_t143 = emit__emit_if('elif', test2, then2, other2, level, env)
        else:
            _cdy_t143 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
        _cdy_t145 = _cdy_t143
    else:
        _cdy_t145 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
    return (_cdy_t146 + _cdy_t147 + _cdy_t145)

def emit__emit_any_params(params: tuple[core__Expr, ...], env: emit__Env) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda p: (emit__emit_expr(p, env) + ': _cdy_Any')), params)

def emit__type_params(tvars: tuple[str, ...]) -> str:
    params = cdy_rt.primitives.list_filter((lambda v: (not cdy_rt.primitives.list_contains(core__constraint_of(v), ('integer', 'float')))), tvars)
    if (len(params) == 0):
        return ''
    else:
        return ('[' + emit__comma_join(cdy_rt.primitives.list_map(emit__type_param, params)) + ']')

def emit__type_param(v: str) -> str:
    c = core__constraint_of(v)
    takes = ('(int, float)' if (c == 'number') else ('(int, float, str)' if (c == 'comparable') else ('(str, tuple[_cdy_Any, ...])' if (c == 'appendable') else '')))
    if (takes == ''):
        return emit__py_mangle(v)
    else:
        return (emit__py_mangle(v) + ': ' + takes)

def emit__eq_methods(level: int) -> str:
    return (emit__line(level, 'def __eq__(self, other: object) -> bool:') + emit__line((level + 1), 'return type(self) is type(other) and tuple.__eq__(self, other)') + emit__line(level, 'def __ne__(self, other: object) -> bool:') + emit__line((level + 1), 'return not self == other') + emit__line(level, 'def __hash__(self) -> int:') + emit__line((level + 1), 'return hash((type(self), tuple(self)))'))

def emit__emit_record_fields(fields: tuple[tuple[str, core__CType], ...], level: int, env: emit__Env) -> str:
    def _cdy_t148(ft: tuple[str, core__CType]) -> str:
        _tup = ft
        f = _tup[0]
        t = _tup[1]
        return emit__line(level, (emit__py_mangle(f) + ': ' + emit__emit_type(t, env)))
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map(_cdy_t148, fields), '')

def emit__check_py_fields(owner: str, fields: tuple[tuple[str, core__CType], ...], start: _cdy_Mapping[str, str]) -> bool:
    def _cdy_t149(seen: _cdy_Mapping[str, str], ft: tuple[str, core__CType]) -> _cdy_Mapping[str, str]:
        _tup = ft
        f = _tup[0]
        _t = _tup[1]
        py = emit__py_mangle(f)
        if cdy_rt.primitives.map_has(seen, py):
            return cdy_rt.primitives.fail((owner + ': fields ' + cdy_rt.primitives.map_get(seen, py) + ' and ' + f + ' are one name in Python (' + py + ')'))
        elif (cdy_rt.primitives.substring(py, 0, 1) == '_'):
            return cdy_rt.primitives.fail((owner + ': field ' + f + " can't start with _ in Python (" + py + ')'))
        else:
            return cdy_rt.primitives.map_set(seen, py, f)
    _seen = cdy_rt.primitives.list_fold(_cdy_t149, start, fields)
    return True

def emit__used_tvars(tvars: tuple[str, ...], used: tuple[str, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_filter((lambda v: cdy_rt.primitives.list_contains(v, used)), tvars)

def emit__field_types(fields: tuple[tuple[str, core__CType], ...]) -> tuple[core__CType, ...]:
    def _cdy_t150(f: tuple[str, core__CType]) -> core__CType:
        _tup = f
        _ = _tup[0]
        t = _tup[1]
        return t
    return cdy_rt.primitives.list_map(_cdy_t150, fields)

def emit__variant_tvars(v: core__Variant, tvars: tuple[str, ...]) -> tuple[str, ...]:
    return emit__used_tvars(tvars, emit__type_vars(emit__field_types(v.fields), ()))

def emit__emit_variants(sum_: str, variants: tuple[core__Variant, ...], tvars: tuple[str, ...], level: int, env: emit__Env) -> str:
    def _cdy_t151(v: core__Variant) -> str:
        checked = emit__check_py_fields(('deft ' + emit__candy_name(sum_) + ', variant ' + emit__own_name(v.name)), v.fields, {})
        head = ('class ' + cdy_rt.primitives.map_get(env.globals_, v.name) + emit__type_params(emit__variant_tvars(v, tvars)) + '(_cdy_NamedTuple):')
        body = (emit__emit_record_fields(v.fields, (level + 1), env) + emit__eq_methods((level + 1)))
        register = emit__register_line(v.name, emit__own_name(v.name), tvars, v.fields, level, env)
        return ('\n' + emit__line(level, head) + body + register)
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map(_cdy_t151, variants), '')

def emit__variant_refs(variants: tuple[core__Variant, ...], tvars: tuple[str, ...], env: emit__Env) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda v: (cdy_rt.primitives.map_get(env.globals_, v.name) + emit__type_params(emit__variant_tvars(v, tvars)))), variants)

def emit__emit_match(subj: str, cases: tuple[lower__Case, ...], default: tuple[tuple[lower__Stmt, ...], ...], assert_last: bool, keyword: str, level: int, env: emit__Env, subject: core__Expr) -> str:
    if (len(cases) == 0):
        if (len(default) == 0):
            return ''
        else:
            return (emit__line(level, 'else:') + emit__emit_block(default[0], (level + 1), env))
    elif (assert_last and (len(cases) == 1)):
        c = cases[0]
        cenv = emit__case_env(subject, subj, c.variant, env)
        inner = (level if (keyword == 'if') else (level + 1))
        return (('' if (keyword == 'if') else emit__line(level, 'else:')) + emit__line(inner, ('assert isinstance(' + subj + ', ' + cdy_rt.primitives.map_get(env.globals_, c.variant) + ')')) + emit__emit_binds(c.binds, c.variant, subj, inner, cenv) + emit__emit_stmts(c.body, inner, cenv))
    else:
        _cdy_c_393 = cases[0]
        _cdy_cenv_394 = emit__case_env(subject, subj, _cdy_c_393.variant, env)
        test = (keyword + ' isinstance(' + subj + ', ' + cdy_rt.primitives.map_get(env.globals_, _cdy_c_393.variant) + '):')
        binds = emit__emit_binds(_cdy_c_393.binds, _cdy_c_393.variant, subj, (level + 1), _cdy_cenv_394)
        body = ((emit__line((level + 1), 'pass') if (binds == '') else '') if (len(_cdy_c_393.body) == 0) else emit__emit_stmts(_cdy_c_393.body, (level + 1), _cdy_cenv_394))
        return (emit__line(level, test) + binds + body + emit__emit_match(subj, prelude__rest(cases), default, assert_last, 'elif', level, env, subject))

def emit__case_env(subject: core__Expr, subj: str, variant: str, env: emit__Env) -> emit__Env:
    _cdy_t152: object = subject
    if isinstance(_cdy_t152, core__Local):
        id_ = _cdy_t152.id_
        fields = (cdy_rt.primitives.map_get(env.generic, variant) if cdy_rt.primitives.map_has(env.generic, variant) else ())
        return env._replace(narrowed=cdy_rt.primitives.map_set(env.narrowed, id_, (subj, fields)))
    else:
        return env

def emit__emit_binds(binds: tuple[tuple[str, core__Expr], ...], variant: str, subj: str, level: int, env: emit__Env) -> str:
    def _cdy_t153(b: tuple[str, core__Expr]) -> str:
        _tup = b
        f = _tup[0]
        loc = _tup[1]
        note = ((': ' + emit__emit_type(loc.t, env)) if cdy_rt.primitives.map_has(env.generic, variant) else '')
        return emit__line(level, (emit__emit_expr(loc, env) + note + ' = ' + subj + '.' + emit__py_mangle(f)))
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map(_cdy_t153, binds), '')

def emit__emit_stmts(stmts: tuple[lower__Stmt, ...], level: int, env: emit__Env) -> str:
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda st: emit__emit_stmt(st, level, env)), stmts), '')

def emit__emit_block(stmts: tuple[lower__Stmt, ...], level: int, env: emit__Env) -> str:
    if (len(stmts) == 0):
        return emit__line(level, 'pass')
    else:
        return emit__emit_stmts(stmts, level, env)

def emit__emit_params(params: tuple[core__Expr, ...], types: tuple[core__CType, ...], env: emit__Env, acc: tuple[str, ...]) -> tuple[str, ...]:
    while True:
        if (len(params) == 0):
            return acc
        else:
            params, types, acc = (prelude__rest(params), prelude__rest(types), (acc + cdy_rt.primitives.to_list(emit__emit_param(params[0], types[0], env))))
            continue

def emit__emit_param(param: core__Expr, t: core__CType, env: emit__Env) -> str:
    if core__is_rest(t):
        return ('*' + emit__emit_expr(param, env) + ': ' + emit__emit_type(core__rest_item(t)[0], env))
    else:
        return (emit__emit_expr(param, env) + ': ' + emit__emit_type(t, env))

def emit__emit_func(name: str, params: tuple[core__Expr, ...], body: tuple[lower__Stmt, ...], t: core__CType, level: int, env: emit__Env) -> str:
    _cdy_t154: object = t
    if isinstance(_cdy_t154, core__TFn):
        types = _cdy_t154.params
        ret = _cdy_t154.ret
        inner = emit__bind_locals((params + emit__bound_locals(body, ())), env._replace(locals_={}))
        tvars = emit__type_vars((types + cdy_rt.primitives.to_list(ret)), ())
        tparams = emit__type_params(tvars)
        args = emit__comma_join(emit__emit_params(params, types, inner, ()))
        return ('\n' + emit__line(level, ('def ' + cdy_rt.primitives.map_get(env.globals_, name) + tparams + '(' + args + ') -> ' + emit__emit_type(ret, env) + ':')) + emit__emit_block(body, (level + 1), inner))
    else:
        return cdy_rt.primitives.fail(('defn ' + name + ': its sig must be a function type'))

def emit__emit_imports(modules: tuple[str, ...]) -> str:
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda m: ('import ' + m + '\n')), modules), '')

def emit__emit_main(env: emit__Env) -> str:
    name = cdy_rt.primitives.map_get(env.globals_, 'main')
    return ('\n\nif __name__ == "__main__":\n' + emit__indent(1) + 'cdy_rt.primitives.run_main(' + name + ')\n')

class expand__Imports(_cdy_NamedTuple):
    macros: tuple[form__Macro, ...]
    helpers: tuple[tuple[str, tuple[form__Form, ...]], ...]
    seen: _cdy_Mapping[str, bool]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__Imports, 'Imports', (), (('List', 'form__Macro'), ('List', ('Tup', 'String', ('List', 'form__Form'))), ('Map', 'String', 'Bool')))

class expand__Expanded(_cdy_NamedTuple):
    forms: tuple[form__Form, ...]
    macros: _cdy_Mapping[str, form__Macro]
    own: tuple[form__Macro, ...]
    helpers: tuple[tuple[str, tuple[form__Form, ...]], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__Expanded, 'Expanded', (), (('List', 'form__Form'), ('Map', 'String', 'form__Macro'), ('List', 'form__Macro'), ('List', ('Tup', 'String', ('List', 'form__Form')))))

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
    if cdy_rt.primitives.list_contains(cdy_rt.primitives.path_resolve(path), loading):
        return ()
    else:
        return cdy_rt.primitives.to_list(form__Lst((form__Sym('import-macros', form__NOWHERE), form__Txt(path, form__NOWHERE)), form__NOWHERE))

def expand__pick_forms(forms: tuple[form__Form, ...], heads: tuple[str, ...], keep: bool, acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(forms) == 0):
            return acc
        else:
            form = forms[0]
            items = form__list_items(form)
            picked = ((len(items) > 0) and cdy_rt.primitives.list_contains(form__sym_name(items[0]), heads))
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
                return cdy_rt.primitives.fail((form__pos_text(macro.pos) + 'defmacro: ' + name + ' is already a macro'))
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
    elif cdy_rt.primitives.list_contains(key, loading):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'import-macros: ' + path + ' imports itself'))
    else:
        done = expand__expand_file(include__read_program(path), True, compile_, (loading + cdy_rt.primitives.to_list(key)))
        return expand__Imports((acc.macros + done.own), expand__add_helpers((done.helpers + cdy_rt.primitives.to_list((key, done.forms))), acc.helpers), cdy_rt.primitives.map_set(acc.seen, key, True))

def expand__macro_path(form: form__Form) -> str:
    _cdy_t155: object = form__list_items(form)[1]
    if isinstance(_cdy_t155, form__Txt):
        path = _cdy_t155.val
        return path
    else:
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'import-macros: expected (import-macros name)'))

def expand__add_helpers(groups: tuple[tuple[str, tuple[form__Form, ...]], ...], acc: tuple[tuple[str, tuple[form__Form, ...]], ...]) -> tuple[tuple[str, tuple[form__Form, ...]], ...]:
    while True:
        if (len(groups) == 0):
            return acc
        else:
            _cdy_t156 = prelude__rest(groups)
            _tup = groups[0]
            key = _tup[0]
            _forms = _tup[1]
            groups, acc = (_cdy_t156, (acc if expand__has_helpers(key, acc) else (acc + cdy_rt.primitives.to_list(groups[0]))))
            continue

def expand__has_helpers(key: str, groups: tuple[tuple[str, tuple[form__Form, ...]], ...]) -> bool:
    def _cdy_t157(g: tuple[str, tuple[form__Form, ...]]) -> bool:
        _tup = g
        k = _tup[0]
        _forms = _tup[1]
        return (k == key)
    return cdy_rt.primitives.list_any(_cdy_t157, groups)

def expand__helper_forms(groups: tuple[tuple[str, tuple[form__Form, ...]], ...], acc: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    while True:
        if (len(groups) == 0):
            return acc
        else:
            _tup = groups[0]
            _key = _tup[0]
            forms = _tup[1]
            groups, acc = (prelude__rest(groups), (acc + forms))
            continue

def expand__load_defs(defs: tuple[form__Form, ...], helpers: tuple[form__Form, ...], compile_: _cdy_Callable[[tuple[form__Form, ...]], str]) -> tuple[form__Macro, ...]:
    builtins = expand__library_builtins(None)
    checked = expand__unique_names(defs, builtins, {})
    form_forms = expand__form_defs(None)
    python = compile_((form_forms + helpers + expand__macro_program(defs, builtins, ())))
    loaded = cdy_rt.primitives.load_macros(python, form__sym_name, expand__mangled_names(cdy_rt.primitives.map_keys(core__top_names(form_forms)), {}))
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
        return cdy_rt.primitives.fail((where + 'defmacro: ' + form__sym_name(items[1]) + ' is a special form'))
    elif (not expand__params_ok(items[2])):
        return cdy_rt.primitives.fail((where + 'defmacro: a parameter must be a name'))
    else:
        return items

def expand__params_ok(params: form__Form) -> bool:
    _cdy_t158: object = params
    if isinstance(_cdy_t158, form__Sym):
        return True
    elif isinstance(_cdy_t158, form__Lst):
        items = _cdy_t158.items
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
            params, i, acc = (prelude__rest(params), (i + 1), (acc + cdy_rt.primitives.to_list(form__Lst((params[0], form__Lst((form__Sym('at', pos), args, form__IntLit(i, pos)), pos)), pos))))
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
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(defs[0])) + 'defmacro: ' + name + ' is defined twice'))
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
        _cdy_t159: object = form
        if isinstance(_cdy_t159, form__Lst):
            items = _cdy_t159.items
            pos = _cdy_t159.pos
            head = ('' if (len(items) == 0) else form__sym_name(items[0]))
            if cdy_rt.primitives.map_has(macros, head):
                form = expand__expand_call(cdy_rt.primitives.map_get(macros, head), prelude__rest(items), pos)
                continue
            elif cdy_rt.primitives.list_contains(head, ('sig', 'deft', 'import', 'import-macros', 'quo', 'quasi')):
                return form
            elif (head == 'defn'):
                return form__Lst(expand__expand_after(items, 3, macros), pos)
            elif (head == 'fn'):
                return form__Lst(expand__expand_after(items, 2, macros), pos)
            elif cdy_rt.primitives.list_contains(head, ('let', 'match')):
                return form__Lst(expand__expand_clauses(head, items, macros), pos)
            else:
                return form__Lst(expand__expand_all(items, macros, ()), pos)
        else:
            return form

def expand__expand_after(items: tuple[form__Form, ...], n: int, macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    if (len(items) < n):
        return items
    else:
        return (cdy_rt.primitives.list_take(n, items) + expand__expand_all(cdy_rt.primitives.list_drop(n, items), macros, ()))

def expand__expand_clauses(head: str, items: tuple[form__Form, ...], macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    if ((head == 'let') and (len(items) == 3)):
        _cdy_t160: object = items[1]
        if isinstance(_cdy_t160, form__Lst):
            binds = _cdy_t160.items
            p = _cdy_t160.pos
            return (items[0], form__Lst(expand__each_clause(binds, 1, macros, ()), p), expand__expand_form(items[2], macros))
        else:
            return expand__expand_all(items, macros, ())
    elif ((head == 'match') and (len(items) > 1)):
        return ((items[0], expand__expand_form(items[1], macros)) + expand__each_clause(cdy_rt.primitives.list_drop(2, items), 1, macros, ()))
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
    _cdy_t161: object = clause
    if isinstance(_cdy_t161, form__Lst):
        items = _cdy_t161.items
        p = _cdy_t161.pos
        return form__Lst(expand__expand_after(items, n, macros), p)
    else:
        return expand__expand_form(clause, macros)

def expand__expand_call(macro: form__Macro, args: tuple[form__Form, ...], pos: form__Pos) -> form__Form:
    arity = macro.arity
    where = (form__pos_text(pos) + macro.name + ': ')
    if ((arity >= 0) and (arity != len(args))):
        return cdy_rt.primitives.fail((where + 'expected ' + str(arity) + ' argument(s), got ' + str(len(args))))
    else:
        return expand__stamp(cdy_rt.primitives.call_macro(macro.run, args, where), pos)

def expand__stamp(form: form__Form, pos: form__Pos) -> form__Form:
    _cdy_t162: object = form
    if isinstance(_cdy_t162, form__Lst):
        items = _cdy_t162.items
        p = _cdy_t162.pos
        return form__Lst(expand__stamp_all(items, pos, ()), (pos if (p.line == 0) else p))
    else:
        if (form__form_pos(form).line == 0):
            return expand__form_at(form, pos)
        else:
            return form

def expand__form_at(form: form__Form, pos: form__Pos) -> form__Form:
    _cdy_t163: object = form
    if isinstance(_cdy_t163, form__Sym):
        v = _cdy_t163.name
        return form__Sym(v, pos)
    elif isinstance(_cdy_t163, form__Txt):
        _cdy_v_148 = _cdy_t163.val
        return form__Txt(_cdy_v_148, pos)
    elif isinstance(_cdy_t163, form__IntLit):
        _cdy_v_149 = _cdy_t163.val
        return form__IntLit(_cdy_v_149, pos)
    elif isinstance(_cdy_t163, form__LongLit):
        _cdy_v_150 = _cdy_t163.val
        return form__LongLit(_cdy_v_150, pos)
    elif isinstance(_cdy_t163, form__ByteLit):
        _cdy_v_151 = _cdy_t163.val
        return form__ByteLit(_cdy_v_151, pos)
    elif isinstance(_cdy_t163, form__FloatLit):
        _cdy_v_152 = _cdy_t163.val
        return form__FloatLit(_cdy_v_152, pos)
    elif isinstance(_cdy_t163, form__DoubleLit):
        _cdy_v_153 = _cdy_t163.val
        return form__DoubleLit(_cdy_v_153, pos)
    elif isinstance(_cdy_t163, form__CharLit):
        _cdy_v_154 = _cdy_t163.val
        return form__CharLit(_cdy_v_154, pos)
    elif isinstance(_cdy_t163, form__BoolLit):
        _cdy_v_155 = _cdy_t163.val
        return form__BoolLit(_cdy_v_155, pos)
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
    here: form__Pos
    env: _cdy_Mapping[str, core__CType]
    narrowed: _cdy_Mapping[str, str]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__Ctx, 'Ctx', (), (('Map', 'String', 'core__CType'), ('Map', 'String', 'check__Shape'), ('Map', 'String', 'check__Shape'), ('Map', 'String', 'core__Builtin'), 'form__Pos', ('Map', 'String', 'core__CType'), ('Map', 'String', 'String')))

class check__Shape(_cdy_NamedTuple):
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]
    sum_: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__Shape, 'Shape', (), (('List', 'String'), ('List', ('Tup', 'String', 'core__CType')), 'String'))

class check__St(_cdy_NamedTuple):
    subst: _cdy_Mapping[str, core__CType]
    n: int
    errors: tuple[str, ...]
    types: _cdy_Mapping[str, core__CType]
    pending: tuple[check__Pending, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__St, 'St', (), (('Map', 'String', 'core__CType'), 'Int', ('List', 'String'), ('Map', 'String', 'core__CType'), ('List', 'check__Pending')))

class check__Pending(_cdy_NamedTuple):
    obj: core__Expr
    field: str
    what: str
    on: core__CType
    t: core__CType
    here: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__Pending, 'Pending', (), ('core__Expr', 'String', 'String', 'core__CType', 'core__CType', 'form__Pos'))

class check__Res(_cdy_NamedTuple):
    t: core__CType
    st: check__St
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__Res, 'Res', (), ('core__CType', 'check__St'))

def check__tcon(name: str) -> core__CType:
    return core__TCon(name, ())

def check__type_check(tops: tuple[core__Top, ...], builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[core__Top, ...]:
    _tup = check__check_program(tops, builtins)
    typed_tops = _tup[0]
    errors = _tup[1]
    order_errors = (check__check_order(tops, check__order_of(tops), {}) if (len(errors) == 0) else ())
    if (len(errors) > 0):
        return cdy_rt.primitives.fail(errors[0])
    elif (len(order_errors) > 0):
        return cdy_rt.primitives.fail(order_errors[0])
    else:
        return typed_tops

def check__check_program(tops: tuple[core__Top, ...], builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[tuple[core__Top, ...], tuple[str, ...]]:
    ctx = check__Ctx(check__top_types(tops), check__top_shapes(tops), check__top_sums(tops), builtins, form__NOWHERE, {}, {})
    return check__check_tops(tops, ctx, check__St({}, 0, (), {}, ()))

def check__check_tops(tops: tuple[core__Top, ...], ctx: check__Ctx, st: check__St) -> tuple[tuple[core__Top, ...], tuple[str, ...]]:
    def _cdy_t164(s: check__St, top: core__Top) -> tuple[check__St, core__Top]:
        named = check__retype_top(top, (lambda t, k: core__TVar(('?e' + str(k)))))
        s1 = check__solve_pending(ctx, check__check_top(named, ctx, s._replace(subst={})._replace(types={})))
        return (s1, check__retype_top(named, (lambda t, k: check__node_type(t, s1))))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t164, st, tops)
    st1 = _tup[0]
    done = _tup[1]
    return (done, st1.errors)

def check__check_top(top: core__Top, ctx: check__Ctx, st: check__St) -> check__St:
    _cdy_t165: object = top
    if isinstance(_cdy_t165, core__TDef):
        name = _cdy_t165.name
        init = _cdy_t165.init
        t = _cdy_t165.t
        pos = _cdy_t165.pos
        return check__check_expr(init, t, ('def ' + check__shown_name(name)), ctx._replace(here=pos), st)
    elif isinstance(_cdy_t165, core__TDefn):
        _cdy_name_31 = _cdy_t165.name
        params = _cdy_t165.params
        body = _cdy_t165.body
        _cdy_t_34 = _cdy_t165.t
        _cdy_pos_35 = _cdy_t165.pos
        c = ctx._replace(here=_cdy_pos_35)
        _cdy_t166: object = _cdy_t_34
        if isinstance(_cdy_t166, core__TFn):
            ptypes = _cdy_t166.params
            ret = _cdy_t166.ret
            inside = check__body_types(ptypes)
            return check__check_expr(body, ret, ('defn ' + check__shown_name(_cdy_name_31)), c._replace(env=check__bind_all(params, inside, c.env, 0)), check__typed_all(params, inside, st))
        else:
            return st
    elif isinstance(_cdy_t165, core__TExpr):
        e = _cdy_t165.expr
        return check__infer(e, ctx, st).st
    else:
        return st

def check__body_types(ptypes: tuple[core__CType, ...]) -> tuple[core__CType, ...]:
    def _cdy_t167(p: core__CType) -> core__CType:
        if core__is_rest(p):
            return core__TCon('List', core__rest_item(p))
        else:
            return p
    return cdy_rt.primitives.list_map(_cdy_t167, ptypes)

def check__bind_all(params: tuple[core__Expr, ...], types: tuple[core__CType, ...], env: _cdy_Mapping[str, core__CType], i: int) -> _cdy_Mapping[str, core__CType]:
    while True:
        if ((i == len(params)) or (i == len(types))):
            return env
        else:
            env, i = (cdy_rt.primitives.map_set(env, check__local_key(cdy_rt.primitives.at(params, i)), cdy_rt.primitives.at(types, i)), (i + 1))
            continue

def check__local_key(e: core__Expr) -> str:
    _cdy_t168: object = e
    if isinstance(_cdy_t168, core__Local):
        name = _cdy_t168.name
        id_ = _cdy_t168.id_
        return (name + '#' + str(id_))
    else:
        return ''

def check__top_types(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, core__CType]:
    def _cdy_t170(acc: _cdy_Mapping[str, core__CType], top: core__Top) -> _cdy_Mapping[str, core__CType]:
        _cdy_t169: object = top
        if isinstance(_cdy_t169, core__TDef):
            name = _cdy_t169.name
            t = _cdy_t169.t
            return cdy_rt.primitives.map_set(acc, name, t)
        elif isinstance(_cdy_t169, core__TDefn):
            _cdy_name_55 = _cdy_t169.name
            _cdy_t_56 = _cdy_t169.t
            return cdy_rt.primitives.map_set(acc, _cdy_name_55, _cdy_t_56)
        elif isinstance(_cdy_t169, core__TDeft):
            _cdy_name_57 = _cdy_t169.name
            tvars = _cdy_t169.tvars
            fields = _cdy_t169.fields
            return cdy_rt.primitives.map_set(acc, _cdy_name_57, core__TFn(check__fields_types(fields), core__TCon(_cdy_name_57, check__tvar_types(tvars))))
        elif isinstance(_cdy_t169, core__TDeftSum):
            _cdy_name_60 = _cdy_t169.name
            _cdy_tvars_61 = _cdy_t169.tvars
            variants = _cdy_t169.variants
            return check__variant_types(variants, core__TCon(_cdy_name_60, check__tvar_types(_cdy_tvars_61)), acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t170, {}, tops)

def check__variant_types(variants: tuple[core__Variant, ...], sum_: core__CType, start: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    return cdy_rt.primitives.list_fold((lambda acc, v: cdy_rt.primitives.map_set(acc, v.name, core__TFn(check__fields_types(v.fields), sum_))), start, variants)

def check__fields_types(fields: tuple[tuple[str, core__CType], ...]) -> tuple[core__CType, ...]:
    def _cdy_t171(f: tuple[str, core__CType]) -> core__CType:
        _tup = f
        _name = _tup[0]
        t = _tup[1]
        return t
    return cdy_rt.primitives.list_map(_cdy_t171, fields)

def check__tvar_types(names: tuple[str, ...]) -> tuple[core__CType, ...]:
    return cdy_rt.primitives.list_map((lambda name: core__TVar(name)), names)

def check__top_shapes(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, check__Shape]:
    def _cdy_t173(acc: _cdy_Mapping[str, check__Shape], top: core__Top) -> _cdy_Mapping[str, check__Shape]:
        _cdy_t172: object = top
        if isinstance(_cdy_t172, core__TDeft):
            name = _cdy_t172.name
            tvars = _cdy_t172.tvars
            fields = _cdy_t172.fields
            return cdy_rt.primitives.map_set(acc, name, check__Shape(tvars, fields, ''))
        elif isinstance(_cdy_t172, core__TDeftSum):
            _cdy_name_81 = _cdy_t172.name
            _cdy_tvars_82 = _cdy_t172.tvars
            variants = _cdy_t172.variants
            return check__variant_shapes(variants, _cdy_tvars_82, _cdy_name_81, acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t173, {}, tops)

def check__variant_shapes(variants: tuple[core__Variant, ...], tvars: tuple[str, ...], sum_: str, start: _cdy_Mapping[str, check__Shape]) -> _cdy_Mapping[str, check__Shape]:
    return cdy_rt.primitives.list_fold((lambda acc, v: cdy_rt.primitives.map_set(acc, v.name, check__Shape(tvars, v.fields, sum_))), start, variants)

def check__top_sums(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, check__Shape]:
    def _cdy_t175(acc: _cdy_Mapping[str, check__Shape], top: core__Top) -> _cdy_Mapping[str, check__Shape]:
        _cdy_t174: object = top
        if isinstance(_cdy_t174, core__TDeftSum):
            name = _cdy_t174.name
            tvars = _cdy_t174.tvars
            variants = _cdy_t174.variants
            return cdy_rt.primitives.map_set(acc, name, check__Shape(tvars, cdy_rt.primitives.list_map((lambda v: (v.name, core__ANY)), variants), ''))
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t175, {}, tops)

def check__check_expr(e: core__Expr, want: core__CType, what: str, outer: check__Ctx, st: check__St) -> check__St:
    while True:
        ctx = check__at_node(e, outer)
        _cdy_t176: object = e
        if isinstance(_cdy_t176, core__If):
            test = _cdy_t176.test
            then = _cdy_t176.then
            other = _cdy_t176.other
            if check__is_var(check__prune(want, st.subst)):
                return check__infer_expect(e, want, what, ctx, st)
            else:
                rt = check__infer(test, ctx, st)
                st1 = check__expect_is(check__tcon('Bool'), rt.t, 'if: the test', ctx, rt.st)
                return check__typed(e, want, check__check_expr(other, want, what, ctx, check__check_expr(then, want, what, ctx, st1)))
        elif isinstance(_cdy_t176, core__Do):
            body = _cdy_t176.body
            return check__typed(e, want, (check__expect(want, check__tcon('Unit'), what, ctx, st) if (len(body) == 0) else check__check_expr(cdy_rt.primitives.at(body, (len(body) - 1)), want, what, ctx, check__infer_do(cdy_rt.primitives.slice_(body, 0, (len(body) - 1)), ctx, check__Res(core__ANY, st)).st)))
        elif isinstance(_cdy_t176, core__Call):
            callee = _cdy_t176.callee
            args = _cdy_t176.args
            _cdy_t177: object = callee
            if isinstance(_cdy_t177, core__Lambda):
                params = _cdy_t177.params
                _cdy_body_112 = _cdy_t177.body
                if (len(params) == len(args)):
                    _tup = check__infer_all(args, ctx, st)
                    ts = _tup[0]
                    st0 = _tup[1]
                    _cdy_st1_116 = check__typed_all(params, ts, check__typed(callee, core__TFn(ts, want), check__typed(e, want, st0)))
                    e, outer, st = (_cdy_body_112, ctx._replace(env=check__bind_all(params, ts, ctx.env, 0)), _cdy_st1_116)
                    continue
                else:
                    return check__infer_expect(e, want, what, ctx, st)
            else:
                return check__infer_expect(e, want, what, ctx, st)
        elif isinstance(_cdy_t176, core__Lambda):
            return check__check_lambda(e, want, what, ctx, st)
        elif isinstance(_cdy_t176, core__MatchE):
            subject = _cdy_t176.subject
            clauses = _cdy_t176.clauses
            default = _cdy_t176.default
            if check__is_any(check__prune(want, st.subst)):
                return check__infer(e, ctx, st).st
            else:
                return check__infer_expect(e, want, what, ctx, st)
        else:
            return check__infer_expect(e, want, what, ctx, st)

def check__at_node(e: core__Expr, ctx: check__Ctx) -> check__Ctx:
    pos = check__node_pos(e)
    if (pos.line == 0):
        return ctx
    else:
        return ctx._replace(here=pos)

def check__node_pos(e: core__Expr) -> form__Pos:
    _cdy_t178: object = e
    if isinstance(_cdy_t178, core__Lit):
        form = _cdy_t178.form
        return form__form_pos(form)
    elif isinstance(_cdy_t178, core__Local):
        pos = _cdy_t178.pos
        return pos
    elif isinstance(_cdy_t178, core__Global):
        _cdy_pos_126 = _cdy_t178.pos
        return _cdy_pos_126
    elif isinstance(_cdy_t178, core__Prim):
        _cdy_pos_127 = _cdy_t178.pos
        return _cdy_pos_127
    elif isinstance(_cdy_t178, core__Do):
        _cdy_pos_128 = _cdy_t178.pos
        return _cdy_pos_128
    elif isinstance(_cdy_t178, core__Call):
        _cdy_pos_129 = _cdy_t178.pos
        return _cdy_pos_129
    elif isinstance(_cdy_t178, core__If):
        _cdy_pos_130 = _cdy_t178.pos
        return _cdy_pos_130
    elif isinstance(_cdy_t178, core__Lambda):
        _cdy_pos_131 = _cdy_t178.pos
        return _cdy_pos_131
    elif isinstance(_cdy_t178, core__Tuple):
        _cdy_pos_132 = _cdy_t178.pos
        return _cdy_pos_132
    elif isinstance(_cdy_t178, core__ListOf):
        _cdy_pos_133 = _cdy_t178.pos
        return _cdy_pos_133
    elif isinstance(_cdy_t178, core__Fmt):
        _cdy_pos_134 = _cdy_t178.pos
        return _cdy_pos_134
    elif isinstance(_cdy_t178, core__Field):
        _cdy_pos_135 = _cdy_t178.pos
        return _cdy_pos_135
    elif isinstance(_cdy_t178, core__Assoc):
        _cdy_pos_136 = _cdy_t178.pos
        return _cdy_pos_136
    elif isinstance(_cdy_t178, core__MatchE):
        _cdy_pos_137 = _cdy_t178.pos
        return _cdy_pos_137
    else:
        return form__NOWHERE

def check__is_missing_else(e: core__Expr) -> bool:
    _cdy_t179: object = e
    if isinstance(_cdy_t179, core__Prim):
        name = _cdy_t179.name
        pos = _cdy_t179.pos
        return ((name == 'nil') and (pos == form__NOWHERE))
    else:
        return False

def check__infer_expect(e: core__Expr, want: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    r = check__infer(e, ctx, st)
    return check__expect(want, r.t, what, ctx, r.st)

def check__infer(e: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer_node(e, ctx, st)
    return check__Res(r.t, check__typed(e, r.t, r.st))

def check__infer_node(e: core__Expr, outer: check__Ctx, st: check__St) -> check__Res:
    ctx = check__at_node(e, outer)
    _cdy_t180: object = e
    if isinstance(_cdy_t180, core__Lit):
        form = _cdy_t180.form
        return check__Res(check__literal_type(form), st)
    elif isinstance(_cdy_t180, core__Local):
        name = _cdy_t180.name
        key = check__local_key(e)
        return check__Res((cdy_rt.primitives.map_get(ctx.env, key) if cdy_rt.primitives.map_has(ctx.env, key) else core__ANY), st)
    elif isinstance(_cdy_t180, core__Global):
        return check__as_value(check__name_type(e, ctx, st))
    elif isinstance(_cdy_t180, core__Prim):
        return check__as_value(check__name_type(e, ctx, st))
    elif isinstance(_cdy_t180, core__Call):
        callee = _cdy_t180.callee
        args = _cdy_t180.args
        return check__infer_call(callee, args, ctx, st)
    elif isinstance(_cdy_t180, core__If):
        test = _cdy_t180.test
        then = _cdy_t180.then
        other = _cdy_t180.other
        rt = check__infer(test, ctx, st)
        st1 = check__expect_is(check__tcon('Bool'), rt.t, 'if: the test', ctx, rt.st)
        ra = check__infer(then, ctx, st1)
        rb = check__infer(other, ctx, ra.st)
        if check__is_missing_else(other):
            return check__Res(check__tcon('Unit'), check__expect_is(check__tcon('Unit'), ra.t, 'if: with no else, the then', ctx, rb.st))
        else:
            return check__join_types(ra.t, rb.t, 'if: the branches', ctx, rb.st)
    elif isinstance(_cdy_t180, core__Do):
        body = _cdy_t180.body
        return check__infer_do(body, ctx, check__Res(check__tcon('Unit'), st))
    elif isinstance(_cdy_t180, core__Lambda):
        params = _cdy_t180.params
        _cdy_body_169 = _cdy_t180.body
        return check__infer_lambda(params, _cdy_body_169, ctx, st)
    elif isinstance(_cdy_t180, core__Tuple):
        items = _cdy_t180.items
        _tup = check__infer_all(items, ctx, st)
        ts = _tup[0]
        _cdy_st1_173 = _tup[1]
        return check__Res(core__TCon('Tup', ts), _cdy_st1_173)
    elif isinstance(_cdy_t180, core__ListOf):
        _cdy_items_174 = _cdy_t180.items
        return check__infer_list_of(_cdy_items_174, ctx, st)
    elif isinstance(_cdy_t180, core__Fmt):
        parts = _cdy_t180.parts
        return check__Res(check__tcon('String'), check__infer_holes(parts, ctx, st))
    elif isinstance(_cdy_t180, core__Field):
        obj = _cdy_t180.obj
        field = _cdy_t180.field
        return check__infer_field(obj, field, ctx, st)
    elif isinstance(_cdy_t180, core__Assoc):
        _cdy_obj_178 = _cdy_t180.obj
        fields = _cdy_t180.fields
        return check__infer_assoc(_cdy_obj_178, fields, ctx, st)
    elif isinstance(_cdy_t180, core__MatchE):
        subject = _cdy_t180.subject
        clauses = _cdy_t180.clauses
        default = _cdy_t180.default
        return check__infer_match(subject, clauses, default, ctx, st)
    else:
        return check__Res(core__ANY, st)

def check__literal_type(form: form__Form) -> core__CType:
    _cdy_t181: object = form
    if isinstance(_cdy_t181, form__Txt):
        return check__tcon('String')
    elif isinstance(_cdy_t181, form__IntLit):
        return check__tcon('Int')
    elif isinstance(_cdy_t181, form__LongLit):
        return check__tcon('Long')
    elif isinstance(_cdy_t181, form__ByteLit):
        return check__tcon('Byte')
    elif isinstance(_cdy_t181, form__FloatLit):
        return check__tcon('Float')
    elif isinstance(_cdy_t181, form__DoubleLit):
        return check__tcon('Double')
    elif isinstance(_cdy_t181, form__CharLit):
        return check__tcon('Char')
    elif isinstance(_cdy_t181, form__BoolLit):
        return check__tcon('Bool')
    else:
        return core__ANY

def check__name_type(e: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t182: object = e
    if isinstance(_cdy_t182, core__Global):
        name = _cdy_t182.name
        if cdy_rt.primitives.map_has(ctx.globals_, name):
            return check__instantiate(cdy_rt.primitives.map_get(ctx.globals_, name), st)
        else:
            return check__Res(core__ANY, st)
    elif isinstance(_cdy_t182, core__Prim):
        _cdy_name_188 = _cdy_t182.name
        return check__prim_type(_cdy_name_188, ctx, st)
    else:
        return check__Res(core__ANY, st)

def check__as_value(r: check__Res) -> check__Res:
    _cdy_t183: object = r.t
    if isinstance(_cdy_t183, core__TFn):
        params = _cdy_t183.params
        ret = _cdy_t183.ret
        if core__is_variadic(r.t):
            return check__Res(core__TFn(cdy_rt.primitives.slice_(params, 0, (len(params) - 1)), ret), r.st)
        else:
            return r
    else:
        return r

def check__infer_callee(callee: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t184: object = callee
    if isinstance(_cdy_t184, core__Global):
        return check__callee_typed(callee, check__name_type(callee, ctx, st))
    elif isinstance(_cdy_t184, core__Prim):
        return check__callee_typed(callee, check__name_type(callee, ctx, st))
    else:
        return check__infer(callee, ctx, st)

def check__callee_typed(callee: core__Expr, r: check__Res) -> check__Res:
    return check__Res(r.t, check__typed(callee, check__as_value(r).t, r.st))

def check__prim_type(name: str, ctx: check__Ctx, st: check__St) -> check__Res:
    if cdy_rt.primitives.map_has(ctx.builtins, name):
        _cdy_t185: object = cdy_rt.primitives.map_get(ctx.builtins, name)
        if isinstance(_cdy_t185, core__Typed):
            type_ = _cdy_t185.type_
            return check__instantiate(type_, st)
        else:
            return check__Res(core__ANY, st)
    else:
        return check__Res(core__ANY, st)

def check__infer_all(es: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> tuple[tuple[core__CType, ...], check__St]:
    def _cdy_t186(s: check__St, e: core__Expr) -> tuple[check__St, core__CType]:
        r = check__infer(e, ctx, s)
        return (r.st, r.t)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t186, st, es)
    st1 = _tup[0]
    ts = _tup[1]
    return (ts, st1)

def check__infer_list_of(items: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    rv = check__fresh(st)
    st1 = cdy_rt.primitives.list_fold((lambda s, e: check__infer_expect(e, rv.t, 'List: an item', ctx, s)), rv.st, items)
    return check__Res(core__TCon('List', cdy_rt.primitives.to_list(rv.t)), st1)

def check__infer_do(body: tuple[core__Expr, ...], ctx: check__Ctx, start: check__Res) -> check__Res:
    return cdy_rt.primitives.list_fold((lambda last, e: check__infer(e, ctx, last.st)), start, body)

def check__infer_holes(parts: tuple[core__FPart, ...], ctx: check__Ctx, start: check__St) -> check__St:
    def _cdy_t188(st: check__St, p: core__FPart) -> check__St:
        _cdy_t187: object = p
        if isinstance(_cdy_t187, core__FHole):
            e = _cdy_t187.expr
            return check__infer(e, ctx, st).st
        else:
            return st
    return cdy_rt.primitives.list_fold(_cdy_t188, start, parts)

def check__infer_lambda(params: tuple[core__Expr, ...], body: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    _tup = check__fresh_types(len(params), st, ())
    ptypes = _tup[0]
    st1 = _tup[1]
    inner = ctx._replace(env=check__bind_all(params, ptypes, ctx.env, 0))
    r = check__infer(body, inner, check__typed_all(params, ptypes, st1))
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
    _cdy_t189: object = callee
    if isinstance(_cdy_t189, core__Lambda):
        params = _cdy_t189.params
        body = _cdy_t189.body
        if (len(params) == len(args)):
            return check__typed_callee(callee, args, check__infer_applied(params, body, args, ctx, st))
        else:
            return check__infer_called(callee, args, ctx, st)
    elif isinstance(_cdy_t189, core__Prim):
        name = _cdy_t189.name
        if cdy_rt.primitives.list_contains(name, ('=', '!=')):
            return check__infer_compare(name, callee, args, ctx, st)
        elif ((name == 'at') and check__is_tup_item(args)):
            return check__typed_callee(callee, args, check__infer_tup_item(args, ctx, st))
        else:
            return check__infer_called(callee, args, ctx, st)
    else:
        return check__infer_called(callee, args, ctx, st)

def check__infer_applied(params: tuple[core__Expr, ...], body: core__Expr, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    _tup = check__infer_all(args, ctx, st)
    ts = _tup[0]
    st1 = _tup[1]
    inner = ctx._replace(env=check__bind_all(params, ts, ctx.env, 0))
    return check__infer(body, inner, check__typed_all(params, ts, st1))

def check__infer_called(callee: core__Expr, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    rc = check__infer_callee(callee, ctx, st)
    ct = check__prune(rc.t, rc.st.subst)
    name = check__callee_name(callee)
    _cdy_t190: object = ct
    if isinstance(_cdy_t190, core__TFn):
        params = _cdy_t190.params
        ret = _cdy_t190.ret
        if core__is_variadic(ct):
            if (len(args) < (len(params) - 1)):
                st1 = check__report(('(' + name + ' ...) takes at least ' + str((len(params) - 1)) + ' argument(s), got ' + str(len(args))), ctx, rc.st)
                return check__Res(ret, check__args_st(args, ctx, st1))
            else:
                return check__Res(ret, check__check_args(args, check__spread_rest(params, len(args)), name, ctx, rc.st))
        elif (len(params) != len(args)):
            unit = ('field(s)' if cdy_rt.primitives.map_has(ctx.shapes, check__global_of(callee)) else 'argument(s)')
            _cdy_st1_268 = check__report(('(' + name + ' ...) takes ' + str(len(params)) + ' ' + unit + ', got ' + str(len(args))), ctx, rc.st)
            return check__Res(ret, check__args_st(args, ctx, _cdy_st1_268))
        else:
            return check__Res(ret, check__check_args(args, params, name, ctx, rc.st))
    elif isinstance(_cdy_t190, core__TVar):
        v = _cdy_t190.name
        if check__is_flexible(v):
            _tup = check__infer_all(args, ctx, rc.st)
            ts = _tup[0]
            _cdy_st1_272 = _tup[1]
            rr = check__fresh(_cdy_st1_272)
            _cdy__tup_274 = check__unify(ct, core__TFn(ts, rr.t), rr.st.subst)
            _ok = _cdy__tup_274[0]
            s = _cdy__tup_274[1]
            return check__Res(rr.t, rr.st._replace(subst=s))
        else:
            return check__Res(core__ANY, check__report(('expected a function, got ' + check__show(ct, rc.st.subst)), ctx, rc.st))
    else:
        if check__is_any(ct):
            return check__Res(core__ANY, check__args_st(args, ctx, rc.st))
        else:
            return check__Res(core__ANY, check__report(('expected a function, got ' + check__show(ct, rc.st.subst)), ctx, rc.st))

def check__args_st(args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__St:
    _tup = check__infer_all(args, ctx, st)
    _ts = _tup[0]
    st1 = _tup[1]
    return st1

def check__spread_rest(params: tuple[core__CType, ...], count: int) -> tuple[core__CType, ...]:
    fixed = cdy_rt.primitives.slice_(params, 0, (len(params) - 1))
    item = core__rest_item(cdy_rt.primitives.at(params, (len(params) - 1)))[0]
    return (fixed + cdy_rt.primitives.list_map((lambda _: item), cdy_rt.primitives.list_range(0, (count - len(fixed)))))

def check__check_args(args: tuple[core__Expr, ...], params: tuple[core__CType, ...], name: str, ctx: check__Ctx, st: check__St) -> check__St:
    return check__check_fn_args(args, params, name, ctx, check__check_plain_args(args, params, name, ctx, st, 0), 0)

def check__check_plain_args(args: tuple[core__Expr, ...], params: tuple[core__CType, ...], name: str, ctx: check__Ctx, st: check__St, i: int) -> check__St:
    while True:
        if (i == len(args)):
            return st
        elif check__is_lambda(cdy_rt.primitives.at(args, i)):
            i = (i + 1)
            continue
        else:
            st, i = (check__check_expr(cdy_rt.primitives.at(args, i), cdy_rt.primitives.at(params, i), check__arg_what(i, name), ctx, st), (i + 1))
            continue

def check__check_fn_args(args: tuple[core__Expr, ...], params: tuple[core__CType, ...], name: str, ctx: check__Ctx, st: check__St, i: int) -> check__St:
    while True:
        if (i == len(args)):
            return st
        elif check__is_lambda(cdy_rt.primitives.at(args, i)):
            st, i = (check__check_lambda(cdy_rt.primitives.at(args, i), cdy_rt.primitives.at(params, i), check__arg_what(i, name), ctx, st), (i + 1))
            continue
        else:
            i = (i + 1)
            continue

def check__arg_what(i: int, name: str) -> str:
    return ('argument ' + str((i + 1)) + ' of ' + name)

def check__is_lambda(e: core__Expr) -> bool:
    _cdy_t191: object = e
    if isinstance(_cdy_t191, core__Lambda):
        return True
    else:
        return False

def check__check_lambda(lam: core__Expr, expected: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    _cdy_t192: object = lam
    if isinstance(_cdy_t192, core__Lambda):
        params = _cdy_t192.params
        body = _cdy_t192.body
        _cdy_t193: object = check__prune(expected, st.subst)
        if isinstance(_cdy_t193, core__TFn):
            ptypes = _cdy_t193.params
            ret = _cdy_t193.ret
            if (len(ptypes) == len(params)):
                return check__check_expr(body, ret, (what + "'s result"), ctx._replace(env=check__bind_all(params, ptypes, ctx.env, 0)), check__typed_all(params, ptypes, check__typed(lam, expected, st)))
            else:
                _cdy_r_317 = check__infer(lam, ctx, st)
                return check__expect(expected, _cdy_r_317.t, what, ctx, _cdy_r_317.st)
        else:
            r = check__infer(lam, ctx, st)
            return check__expect(expected, r.t, what, ctx, r.st)
    else:
        return st

def check__global_of(e: core__Expr) -> str:
    _cdy_t194: object = e
    if isinstance(_cdy_t194, core__Global):
        name = _cdy_t194.name
        return name
    else:
        return ''

def check__callee_name(e: core__Expr) -> str:
    _cdy_t195: object = e
    if isinstance(_cdy_t195, core__Global):
        name = _cdy_t195.name
        return check__shown_name(name)
    elif isinstance(_cdy_t195, core__Prim):
        _cdy_name_323 = _cdy_t195.name
        return _cdy_name_323
    elif isinstance(_cdy_t195, core__Local):
        _cdy_name_324 = _cdy_t195.name
        return _cdy_name_324
    else:
        return 'the function'

def check__is_tup_item(args: tuple[core__Expr, ...]) -> bool:
    return ((len(args) == 2) and (check__tup_name(args[0]) == '_tup') and (check__int_lit(args[1]) >= 0))

def check__tup_name(e: core__Expr) -> str:
    _cdy_t196: object = e
    if isinstance(_cdy_t196, core__Local):
        name = _cdy_t196.name
        return name
    else:
        return ''

def check__int_lit(e: core__Expr) -> int:
    _cdy_t197: object = e
    if isinstance(_cdy_t197, core__Lit):
        form = _cdy_t197.form
        _cdy_t198: object = form
        if isinstance(_cdy_t198, form__IntLit):
            k = _cdy_t198.val
            return k
        else:
            return -1
    else:
        return -1

def check__infer_tup_item(args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(args[0], ctx, check__typed(args[1], check__tcon('Int'), st))
    i = check__int_lit(args[1])
    tt = check__prune(r.t, r.st.subst)
    items = check__tup_items(tt)
    if (check__is_any(tt) or check__is_var(tt)):
        return check__Res(core__ANY, r.st)
    elif (check__tcon_name(tt) != 'Tup'):
        return check__Res(core__ANY, (check__report(('a Tup pattern takes a tuple, not a ' + check__show(tt, r.st.subst)), ctx, r.st) if (i == 0) else r.st))
    elif (i < len(items)):
        return check__Res(cdy_rt.primitives.at(items, i), r.st)
    else:
        return check__Res(core__ANY, check__report(('a ' + check__show(tt, r.st.subst) + ' has ' + str(len(items)) + ' items, not ' + str((i + 1))), ctx, r.st))

def check__tup_items(t: core__CType) -> tuple[core__CType, ...]:
    _cdy_t199: object = t
    if isinstance(_cdy_t199, core__TCon):
        args = _cdy_t199.args
        return args
    else:
        return ()

def check__infer_compare(name: str, callee: core__Expr, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer_called(callee, args, ctx, st)
    subst = r.st.subst
    t1 = (core__ANY if (len(args) == 0) else check__resolve_type(check__recorded(args[0], r.st), subst))
    if check__has_fn(t1, subst, ctx, ()):
        return check__Res(r.t, check__report((name + ": a function can't be compared, got " + check__show(t1, subst)), ctx, r.st))
    else:
        return r

def check__has_fn(t: core__CType, subst: _cdy_Mapping[str, core__CType], ctx: check__Ctx, seen: tuple[str, ...]) -> bool:
    _cdy_t200: object = check__prune(t, subst)
    if isinstance(_cdy_t200, core__TFn):
        return True
    elif isinstance(_cdy_t200, core__TCon):
        name = _cdy_t200.name
        args = _cdy_t200.args
        return (cdy_rt.primitives.list_any((lambda a: check__has_fn(a, subst, ctx, seen)), args) or ((not cdy_rt.primitives.list_contains(name, seen)) and check__fields_have_fn(name, subst, ctx, (seen + (name,)))))
    else:
        return False

def check__fields_have_fn(name: str, subst: _cdy_Mapping[str, core__CType], ctx: check__Ctx, seen: tuple[str, ...]) -> bool:
    if cdy_rt.primitives.map_has(ctx.shapes, name):
        def _cdy_t201(f: tuple[str, core__CType]) -> bool:
            _tup = f
            _name = _tup[0]
            t = _tup[1]
            return check__has_fn(t, subst, ctx, seen)
        return cdy_rt.primitives.list_any(_cdy_t201, cdy_rt.primitives.map_get(ctx.shapes, name).fields)
    elif cdy_rt.primitives.map_has(ctx.sums, name):
        def _cdy_t202(v: tuple[str, core__CType]) -> bool:
            _tup = v
            variant = _tup[0]
            _t = _tup[1]
            return check__has_fn(core__TCon(variant, ()), subst, ctx, seen)
        return cdy_rt.primitives.list_any(_cdy_t202, cdy_rt.primitives.map_get(ctx.sums, name).fields)
    else:
        return False

def check__join_all(types: tuple[core__CType, ...], what: str, ctx: check__Ctx, start: check__Res) -> check__Res:
    return cdy_rt.primitives.list_fold((lambda r, ty: check__join_types(r.t, ty, what, ctx, r.st)), start, prelude__rest(types))

def check__field_of(t: core__CType, field: str, ctx: check__Ctx) -> tuple[bool, core__CType]:
    _cdy_t203: object = t
    if isinstance(_cdy_t203, core__TCon):
        name = _cdy_t203.name
        args = _cdy_t203.args
        if cdy_rt.primitives.map_has(ctx.shapes, name):
            s = cdy_rt.primitives.map_get(ctx.shapes, name)
            return check__find_field(s.fields, field, check__zip_map(s.tvars, args, {}))
        elif cdy_rt.primitives.map_has(ctx.sums, name):
            return check__sum_field(cdy_rt.primitives.map_get(ctx.sums, name), args, field, ctx)
        else:
            return (False, core__ANY)
    else:
        return (False, core__ANY)

def check__sum_field(sum_: check__Shape, args: tuple[core__CType, ...], field: str, ctx: check__Ctx) -> tuple[bool, core__CType]:
    def _cdy_t204(v: tuple[str, core__CType]) -> tuple[bool, core__CType]:
        _cdy__tup_384 = v
        variant = _cdy__tup_384[0]
        _t = _cdy__tup_384[1]
        return check__field_of(core__TCon(variant, args), field, ctx)
    found = cdy_rt.primitives.list_map(_cdy_t204, sum_.fields)
    if (len(found) == 0):
        return (False, core__ANY)
    else:
        _tup = found[0]
        _ok = _tup[0]
        first = _tup[1]
        def _cdy_t205(f: tuple[bool, core__CType]) -> bool:
            _cdy__tup_392 = f
            ok = _cdy__tup_392[0]
            t = _cdy__tup_392[1]
            return (ok and (t == first))
        if cdy_rt.primitives.list_all(_cdy_t205, found):
            return found[0]
        else:
            return (False, core__ANY)

def check__in_every_variant(name: str, field: str, ctx: check__Ctx) -> bool:
    _cdy_t207 = cdy_rt.primitives.map_has(ctx.sums, name)
    if _cdy_t207:
        def _cdy_t206(v: tuple[str, core__CType]) -> bool:
            _tup = v
            variant = _tup[0]
            _t = _tup[1]
            _cdy__tup_402 = check__field_of(core__TCon(variant, ()), field, ctx)
            ok = _cdy__tup_402[0]
            _ft = _cdy__tup_402[1]
            return ok
        _cdy_t207 = cdy_rt.primitives.list_all(_cdy_t206, cdy_rt.primitives.map_get(ctx.sums, name).fields)
    return _cdy_t207

def check__find_field(fields: tuple[tuple[str, core__CType], ...], field: str, vars_: _cdy_Mapping[str, core__CType]) -> tuple[bool, core__CType]:
    while True:
        if (len(fields) == 0):
            return (False, core__ANY)
        else:
            _tup = fields[0]
            name = _tup[0]
            t = _tup[1]
            if (name == field):
                return (True, check__put_vars(t, vars_))
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
    _cdy_t208: object = t
    if isinstance(_cdy_t208, core__TVar):
        name = _cdy_t208.name
        if cdy_rt.primitives.map_has(vars_, name):
            return cdy_rt.primitives.map_get(vars_, name)
        else:
            return t
    elif isinstance(_cdy_t208, core__TCon):
        _cdy_name_417 = _cdy_t208.name
        args = _cdy_t208.args
        return core__TCon(_cdy_name_417, cdy_rt.primitives.list_map((lambda a: check__put_vars(a, vars_)), args))
    else:
        assert isinstance(_cdy_t208, core__TFn)
        params = _cdy_t208.params
        ret = _cdy_t208.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__put_vars(p, vars_)), params), check__put_vars(ret, vars_))

def check__infer_field(obj: core__Expr, field: str, ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(obj, ctx, st)
    ot = check__prune(r.t, r.st.subst)
    return check__field_type(ot, obj, field, 'get', ctx, r.st)

def check__field_type(ot0: core__CType, obj: core__Expr, field: str, what: str, ctx: check__Ctx, st: check__St) -> check__Res:
    ot = check__narrow(ot0, obj, ctx)
    _cdy_t209: object = ot
    if isinstance(_cdy_t209, core__TVar):
        v = _cdy_t209.name
        if check__is_flexible(v):
            r = check__fresh(st)
            p = check__Pending(obj, field, what, ot, r.t, ctx.here)
            return check__Res(r.t, r.st._replace(pending=(r.st.pending + cdy_rt.primitives.to_list(p))))
        else:
            return check__Res(core__ANY, check__report((what + ': ' + v + ' has no fields'), ctx, st))
    else:
        _tup = check__field_of(ot, field, ctx)
        found = _tup[0]
        ft = _tup[1]
        if check__is_any(ot):
            return check__Res(core__ANY, st)
        elif found:
            return check__Res(ft, st)
        else:
            return check__Res(core__ANY, check__report(((what + ': field ' + field + ' of ' + check__show(ot, st.subst) + ' has different types in its variants') if check__in_every_variant(check__tcon_name(ot), field, ctx) else ((what + ': ' + check__show(ot, st.subst) + ' has no field ' + field) if (cdy_rt.primitives.map_has(ctx.shapes, check__tcon_name(ot)) or cdy_rt.primitives.map_has(ctx.sums, check__tcon_name(ot))) else (what + ': ' + check__show(ot, st.subst) + ' has no fields'))), ctx, st))

def check__narrow(ot: core__CType, obj: core__Expr, ctx: check__Ctx) -> core__CType:
    _cdy_t211: object = obj
    if isinstance(_cdy_t211, core__Local):
        _cdy_t210 = check__local_key(obj)
    else:
        _cdy_t210 = ''
    key = _cdy_t210
    if cdy_rt.primitives.map_has(ctx.narrowed, key):
        variant = cdy_rt.primitives.map_get(ctx.narrowed, key)
        _cdy_t212: object = ot
        if isinstance(_cdy_t212, core__TCon):
            name = _cdy_t212.name
            args = _cdy_t212.args
            if (name == cdy_rt.primitives.map_get(ctx.shapes, variant).sum_):
                return core__TCon(variant, args)
            else:
                return ot
        else:
            return ot
    else:
        return ot

def check__solve_pending(ctx: check__Ctx, st: check__St) -> check__St:
    while True:
        ps = st.pending
        _tup = check__solve_each(ps, ctx, st._replace(pending=()), ())
        st1 = _tup[0]
        left = _tup[1]
        if (len(left) == 0):
            return st1
        elif (len(left) < len(ps)):
            st = st1._replace(pending=(st1.pending + left))
            continue
        else:
            return check__report_pending(left, ctx, st1)

def check__solve_each(ps: tuple[check__Pending, ...], ctx: check__Ctx, start: check__St, left: tuple[check__Pending, ...]) -> tuple[check__St, tuple[check__Pending, ...]]:
    def _cdy_t213(acc: tuple[check__St, tuple[check__Pending, ...]], p: check__Pending) -> tuple[check__St, tuple[check__Pending, ...]]:
        _tup = acc
        st = _tup[0]
        _cdy_left_463 = _tup[1]
        on = check__prune(p.on, st.subst)
        if cdy_rt.primitives.map_has(st.subst, ('any' + check__tvar_name(on))):
            return (st._replace(subst=check__mark_any(p.t, st.subst)), _cdy_left_463)
        elif check__is_var(on):
            return (st, (_cdy_left_463 + cdy_rt.primitives.to_list(p)))
        else:
            c = ctx._replace(here=p.here)
            r = check__field_type(on, p.obj, p.field, p.what, c, st)
            what = (p.what + ': field ' + p.field + ' of ' + check__show(on, r.st.subst))
            return (check__expect_is(p.t, r.t, what, c, r.st), _cdy_left_463)
    return cdy_rt.primitives.list_fold(_cdy_t213, (start, left), ps)

def check__report_pending(ps: tuple[check__Pending, ...], ctx: check__Ctx, start: check__St) -> check__St:
    return cdy_rt.primitives.list_fold((lambda st, p: check__report((p.what + ': the type of ' + check__callee_name(p.obj) + " isn't known here (" + p.field + ')'), ctx._replace(here=p.here), st)), start, ps)

def check__tcon_name(t: core__CType) -> str:
    _cdy_t214: object = t
    if isinstance(_cdy_t214, core__TCon):
        name = _cdy_t214.name
        return name
    else:
        return ''

def check__infer_assoc(obj: core__Expr, fields: tuple[tuple[str, core__Expr], ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(obj, ctx, st)
    ot = check__prune(r.t, r.st.subst)
    return check__Res(r.t, check__assoc_values(ot, obj, fields, ctx, r.st))

def check__assoc_values(ot: core__CType, obj: core__Expr, fields: tuple[tuple[str, core__Expr], ...], ctx: check__Ctx, start: check__St) -> check__St:
    def _cdy_t215(st: check__St, f: tuple[str, core__Expr]) -> check__St:
        _tup = f
        field = _tup[0]
        val = _tup[1]
        ft = check__field_type(ot, obj, field, 'assoc', ctx, st)
        return check__check_expr(val, ft.t, ('assoc: field ' + field + ' of ' + check__show(ot, st.subst)), ctx, ft.st)
    return cdy_rt.primitives.list_fold(_cdy_t215, start, fields)

def check__infer_match(subject: core__Expr, clauses: tuple[core__Clause, ...], default: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    rs = check__infer(subject, ctx, st)
    variant = clauses[0].variant
    sum_ = (cdy_rt.primitives.map_get(ctx.shapes, variant).sum_ if cdy_rt.primitives.map_has(ctx.shapes, variant) else '')
    tvars = (cdy_rt.primitives.map_get(ctx.sums, sum_).tvars if cdy_rt.primitives.map_has(ctx.sums, sum_) else ())
    _tup = check__fresh_types(len(tvars), rs.st, ())
    ftypes = _tup[0]
    st0 = _tup[1]
    vars_ = check__zip_map(tvars, ftypes, {})
    want = core__TCon(sum_, ftypes)
    st1 = check__expect_is(want, rs.t, 'match: the subject', ctx, st0)
    _cdy__tup_507 = check__infer_clauses(subject, clauses, vars_, ctx, st1)
    ctypes = _cdy__tup_507[0]
    st2 = _cdy__tup_507[1]
    if (len(default) == 0):
        return check__join_all(ctypes, 'match: the clauses', ctx, check__Res(ctypes[0], st2))
    else:
        rd = check__infer(default[0], ctx, st2)
        return check__join_all((ctypes + cdy_rt.primitives.to_list(rd.t)), 'match: the clauses', ctx, check__Res(ctypes[0], rd.st))

def check__infer_clauses(subject: core__Expr, clauses: tuple[core__Clause, ...], vars_: _cdy_Mapping[str, core__CType], ctx: check__Ctx, st: check__St) -> tuple[tuple[core__CType, ...], check__St]:
    def _cdy_t218(s: check__St, c: core__Clause) -> tuple[check__St, core__CType]:
        shape = (cdy_rt.primitives.map_get(ctx.shapes, c.variant) if cdy_rt.primitives.map_has(ctx.shapes, c.variant) else check__Shape((), (), ''))
        bound = ctx._replace(env=check__bind_fields(c.binds, shape.fields, vars_, ctx.env))
        _cdy_t217: object = subject
        if isinstance(_cdy_t217, core__Local):
            _cdy_t216 = bound._replace(narrowed=cdy_rt.primitives.map_set(ctx.narrowed, check__local_key(subject), c.variant))
        else:
            _cdy_t216 = bound
        inner = _cdy_t216
        r = check__infer(c.body, inner, check__typed_binds(c.binds, inner.env, s))
        return (r.st, r.t)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t218, st, clauses)
    st1 = _tup[0]
    ts = _tup[1]
    return (ts, st1)

def check__bind_fields(binds: tuple[tuple[str, core__Expr], ...], fields: tuple[tuple[str, core__CType], ...], vars_: _cdy_Mapping[str, core__CType], start: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    def _cdy_t219(env: _cdy_Mapping[str, core__CType], b: tuple[str, core__Expr]) -> _cdy_Mapping[str, core__CType]:
        _tup = b
        field = _tup[0]
        loc = _tup[1]
        _cdy__tup_534 = check__find_field(fields, field, vars_)
        found = _cdy__tup_534[0]
        ft = _cdy__tup_534[1]
        return cdy_rt.primitives.map_set(env, check__local_key(loc), (ft if found else core__ANY))
    return cdy_rt.primitives.list_fold(_cdy_t219, start, binds)

def check__typed(e: core__Expr, t: core__CType, st: check__St) -> check__St:
    key = check__tvar_name(e.t)
    if cdy_rt.primitives.starts_with(key, '?e'):
        return st._replace(types=cdy_rt.primitives.map_set(st.types, key, t))
    else:
        return st

def check__typed_all(es: tuple[core__Expr, ...], ts: tuple[core__CType, ...], st: check__St) -> check__St:
    while True:
        if ((len(es) == 0) or (len(ts) == 0)):
            return st
        else:
            es, ts, st = (prelude__rest(es), prelude__rest(ts), check__typed(es[0], ts[0], st))
            continue

def check__typed_binds(binds: tuple[tuple[str, core__Expr], ...], env: _cdy_Mapping[str, core__CType], start: check__St) -> check__St:
    def _cdy_t220(st: check__St, b: tuple[str, core__Expr]) -> check__St:
        _tup = b
        _field = _tup[0]
        loc = _tup[1]
        return check__typed(loc, (cdy_rt.primitives.map_get(env, check__local_key(loc)) if cdy_rt.primitives.map_has(env, check__local_key(loc)) else core__ANY), st)
    return cdy_rt.primitives.list_fold(_cdy_t220, start, binds)

def check__typed_callee(callee: core__Expr, args: tuple[core__Expr, ...], r: check__Res) -> check__Res:
    return check__Res(r.t, check__typed(callee, core__TFn(cdy_rt.primitives.list_map((lambda a: check__recorded(a, r.st)), args), r.t), r.st))

def check__recorded(e: core__Expr, st: check__St) -> core__CType:
    key = check__tvar_name(e.t)
    if cdy_rt.primitives.map_has(st.types, key):
        return cdy_rt.primitives.map_get(st.types, key)
    else:
        return core__ANY

def check__node_type(t: core__CType, st: check__St) -> core__CType:
    key = check__tvar_name(t)
    if cdy_rt.primitives.map_has(st.types, key):
        return check__final_type(cdy_rt.primitives.map_get(st.types, key), st.subst)
    else:
        return t

def check__final_type(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> core__CType:
    _cdy_t221: object = check__prune(t, subst)
    if isinstance(_cdy_t221, core__TCon):
        name = _cdy_t221.name
        args = _cdy_t221.args
        return core__TCon(name, cdy_rt.primitives.list_map((lambda a: check__final_type(a, subst)), args))
    elif isinstance(_cdy_t221, core__TFn):
        params = _cdy_t221.params
        ret = _cdy_t221.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__final_type(p, subst)), params), check__final_type(ret, subst))
    else:
        assert isinstance(_cdy_t221, core__TVar)
        _cdy_name_570 = _cdy_t221.name
        if cdy_rt.primitives.map_has(subst, ('any' + _cdy_name_570)):
            return core__ANY
        else:
            return core__TVar(_cdy_name_570)

def check__retype_top(top: core__Top, f: _cdy_Callable[[core__CType, int], core__CType]) -> core__Top:
    _cdy_t222: object = top
    if isinstance(_cdy_t222, core__TDef):
        name = _cdy_t222.name
        init = _cdy_t222.init
        t = _cdy_t222.t
        pos = _cdy_t222.pos
        _tup = check__retype(init, f, 0)
        e = _tup[0]
        _n = _tup[1]
        return core__TDef(name, e, t, pos)
    elif isinstance(_cdy_t222, core__TDefn):
        _cdy_name_580 = _cdy_t222.name
        params = _cdy_t222.params
        body = _cdy_t222.body
        _cdy_t_583 = _cdy_t222.t
        _cdy_pos_584 = _cdy_t222.pos
        _cdy__tup_585 = check__retype_all(params, f, 0)
        ps = _cdy__tup_585[0]
        n1 = _cdy__tup_585[1]
        _cdy__tup_588 = check__retype(body, f, n1)
        b = _cdy__tup_588[0]
        _ = _cdy__tup_588[1]
        return core__TDefn(_cdy_name_580, ps, b, _cdy_t_583, _cdy_pos_584)
    elif isinstance(_cdy_t222, core__TExpr):
        _cdy_e_591 = _cdy_t222.expr
        _cdy__tup_592 = check__retype(_cdy_e_591, f, 0)
        e1 = _cdy__tup_592[0]
        _cdy__n_594 = _cdy__tup_592[1]
        return core__TExpr(e1)
    else:
        return top

def check__retype(e: core__Expr, f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[core__Expr, int]:
    k = (n + 1)
    _cdy_t223: object = e
    if isinstance(_cdy_t223, core__Lit):
        form = _cdy_t223.form
        t = _cdy_t223.t
        return (core__Lit(form, f(t, n)), k)
    elif isinstance(_cdy_t223, core__Local):
        name = _cdy_t223.name
        id_ = _cdy_t223.id_
        pos = _cdy_t223.pos
        _cdy_t_604 = _cdy_t223.t
        return (core__Local(name, id_, pos, f(_cdy_t_604, n)), k)
    elif isinstance(_cdy_t223, core__Global):
        _cdy_name_605 = _cdy_t223.name
        _cdy_pos_606 = _cdy_t223.pos
        _cdy_t_607 = _cdy_t223.t
        return (core__Global(_cdy_name_605, _cdy_pos_606, f(_cdy_t_607, n)), k)
    elif isinstance(_cdy_t223, core__Prim):
        _cdy_name_608 = _cdy_t223.name
        _cdy_pos_609 = _cdy_t223.pos
        _cdy_t_610 = _cdy_t223.t
        return (core__Prim(_cdy_name_608, _cdy_pos_609, f(_cdy_t_610, n)), k)
    elif isinstance(_cdy_t223, core__Temp):
        _cdy_id__611 = _cdy_t223.id_
        _cdy_t_612 = _cdy_t223.t
        return (core__Temp(_cdy_id__611, f(_cdy_t_612, n)), k)
    elif isinstance(_cdy_t223, core__Call):
        callee = _cdy_t223.callee
        args = _cdy_t223.args
        _cdy_pos_615 = _cdy_t223.pos
        _cdy_t_616 = _cdy_t223.t
        _tup = check__retype(callee, f, k)
        c = _tup[0]
        n1 = _tup[1]
        _cdy__tup_620 = check__retype_all(args, f, n1)
        xs = _cdy__tup_620[0]
        n2 = _cdy__tup_620[1]
        return (core__Call(c, xs, _cdy_pos_615, f(_cdy_t_616, n)), n2)
    elif isinstance(_cdy_t223, core__If):
        test = _cdy_t223.test
        then = _cdy_t223.then
        other = _cdy_t223.other
        _cdy_pos_626 = _cdy_t223.pos
        _cdy_t_627 = _cdy_t223.t
        _cdy__tup_628 = check__retype(test, f, k)
        a = _cdy__tup_628[0]
        _cdy_n1_630 = _cdy__tup_628[1]
        _cdy__tup_631 = check__retype(then, f, _cdy_n1_630)
        b = _cdy__tup_631[0]
        _cdy_n2_633 = _cdy__tup_631[1]
        _cdy__tup_634 = check__retype(other, f, _cdy_n2_633)
        _cdy_c_635 = _cdy__tup_634[0]
        n3 = _cdy__tup_634[1]
        return (core__If(a, b, _cdy_c_635, _cdy_pos_626, f(_cdy_t_627, n)), n3)
    elif isinstance(_cdy_t223, core__Do):
        body = _cdy_t223.body
        _cdy_pos_638 = _cdy_t223.pos
        _cdy_t_639 = _cdy_t223.t
        _cdy__tup_640 = check__retype_all(body, f, k)
        _cdy_xs_641 = _cdy__tup_640[0]
        _cdy_n1_642 = _cdy__tup_640[1]
        return (core__Do(_cdy_xs_641, _cdy_pos_638, f(_cdy_t_639, n)), _cdy_n1_642)
    elif isinstance(_cdy_t223, core__Lambda):
        params = _cdy_t223.params
        _cdy_body_644 = _cdy_t223.body
        _cdy_pos_645 = _cdy_t223.pos
        _cdy_t_646 = _cdy_t223.t
        _cdy__tup_647 = check__retype_all(params, f, k)
        ps = _cdy__tup_647[0]
        _cdy_n1_649 = _cdy__tup_647[1]
        _cdy__tup_650 = check__retype(_cdy_body_644, f, _cdy_n1_649)
        _cdy_b_651 = _cdy__tup_650[0]
        _cdy_n2_652 = _cdy__tup_650[1]
        return (core__Lambda(ps, _cdy_b_651, _cdy_pos_645, f(_cdy_t_646, n)), _cdy_n2_652)
    elif isinstance(_cdy_t223, core__Tuple):
        items = _cdy_t223.items
        _cdy_pos_654 = _cdy_t223.pos
        _cdy_t_655 = _cdy_t223.t
        _cdy__tup_656 = check__retype_all(items, f, k)
        _cdy_xs_657 = _cdy__tup_656[0]
        _cdy_n1_658 = _cdy__tup_656[1]
        return (core__Tuple(_cdy_xs_657, _cdy_pos_654, f(_cdy_t_655, n)), _cdy_n1_658)
    elif isinstance(_cdy_t223, core__ListOf):
        _cdy_items_659 = _cdy_t223.items
        _cdy_pos_660 = _cdy_t223.pos
        _cdy_t_661 = _cdy_t223.t
        _cdy__tup_662 = check__retype_all(_cdy_items_659, f, k)
        _cdy_xs_663 = _cdy__tup_662[0]
        _cdy_n1_664 = _cdy__tup_662[1]
        return (core__ListOf(_cdy_xs_663, _cdy_pos_660, f(_cdy_t_661, n)), _cdy_n1_664)
    elif isinstance(_cdy_t223, core__Fmt):
        parts = _cdy_t223.parts
        _cdy_pos_666 = _cdy_t223.pos
        _cdy_t_667 = _cdy_t223.t
        _cdy__tup_668 = check__retype_parts(parts, f, k)
        _cdy_ps_669 = _cdy__tup_668[0]
        _cdy_n1_670 = _cdy__tup_668[1]
        return (core__Fmt(_cdy_ps_669, _cdy_pos_666, f(_cdy_t_667, n)), _cdy_n1_670)
    elif isinstance(_cdy_t223, core__Field):
        obj = _cdy_t223.obj
        field = _cdy_t223.field
        _cdy_pos_673 = _cdy_t223.pos
        _cdy_t_674 = _cdy_t223.t
        _cdy__tup_675 = check__retype(obj, f, k)
        o = _cdy__tup_675[0]
        _cdy_n1_677 = _cdy__tup_675[1]
        return (core__Field(o, field, _cdy_pos_673, f(_cdy_t_674, n)), _cdy_n1_677)
    elif isinstance(_cdy_t223, core__Assoc):
        _cdy_obj_678 = _cdy_t223.obj
        fields = _cdy_t223.fields
        _cdy_pos_680 = _cdy_t223.pos
        _cdy_t_681 = _cdy_t223.t
        _cdy__tup_682 = check__retype(_cdy_obj_678, f, k)
        _cdy_o_683 = _cdy__tup_682[0]
        _cdy_n1_684 = _cdy__tup_682[1]
        _cdy__tup_685 = check__retype_pairs(fields, f, _cdy_n1_684)
        fs = _cdy__tup_685[0]
        _cdy_n2_687 = _cdy__tup_685[1]
        return (core__Assoc(_cdy_o_683, fs, _cdy_pos_680, f(_cdy_t_681, n)), _cdy_n2_687)
    else:
        assert isinstance(_cdy_t223, core__MatchE)
        subject = _cdy_t223.subject
        clauses = _cdy_t223.clauses
        default = _cdy_t223.default
        _cdy_pos_691 = _cdy_t223.pos
        _cdy_t_692 = _cdy_t223.t
        _cdy__tup_693 = check__retype(subject, f, k)
        s = _cdy__tup_693[0]
        _cdy_n1_695 = _cdy__tup_693[1]
        _cdy__tup_696 = check__retype_clauses(clauses, f, _cdy_n1_695)
        cs = _cdy__tup_696[0]
        _cdy_n2_698 = _cdy__tup_696[1]
        _cdy__tup_699 = check__retype_all(default, f, _cdy_n2_698)
        d = _cdy__tup_699[0]
        _cdy_n3_701 = _cdy__tup_699[1]
        return (core__MatchE(s, cs, d, _cdy_pos_691, f(_cdy_t_692, n)), _cdy_n3_701)

def check__retype_all(es: tuple[core__Expr, ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[core__Expr, ...], int]:
    def _cdy_t224(k: int, e: core__Expr) -> tuple[int, core__Expr]:
        _cdy__tup_707 = check__retype(e, f, k)
        e1 = _cdy__tup_707[0]
        k1 = _cdy__tup_707[1]
        return (k1, e1)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t224, n, es)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__retype_pairs(pairs: tuple[tuple[str, core__Expr], ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[tuple[str, core__Expr], ...], int]:
    def _cdy_t225(k: int, pair: tuple[str, core__Expr]) -> tuple[int, tuple[str, core__Expr]]:
        _cdy__tup_718 = pair
        name = _cdy__tup_718[0]
        e = _cdy__tup_718[1]
        _cdy__tup_721 = check__retype(e, f, k)
        e1 = _cdy__tup_721[0]
        k1 = _cdy__tup_721[1]
        return (k1, (name, e1))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t225, n, pairs)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__retype_parts(parts: tuple[core__FPart, ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[core__FPart, ...], int]:
    def _cdy_t227(k: int, part: core__FPart) -> tuple[int, core__FPart]:
        _cdy_t226: object = part
        if isinstance(_cdy_t226, core__FHole):
            e = _cdy_t226.expr
            _cdy__tup_733 = check__retype(e, f, k)
            e1 = _cdy__tup_733[0]
            k1 = _cdy__tup_733[1]
            return (k1, core__FHole(e1))
        else:
            return (k, part)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t227, n, parts)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__retype_clauses(clauses: tuple[core__Clause, ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[core__Clause, ...], int]:
    def _cdy_t228(k: int, c: core__Clause) -> tuple[int, core__Clause]:
        _cdy__tup_744 = check__retype_pairs(c.binds, f, k)
        bs = _cdy__tup_744[0]
        k1 = _cdy__tup_744[1]
        _cdy__tup_747 = check__retype(c.body, f, k1)
        b = _cdy__tup_747[0]
        k2 = _cdy__tup_747[1]
        return (k2, core__Clause(c.variant, bs, b))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t228, n, clauses)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__is_flexible(name: str) -> bool:
    return cdy_rt.primitives.starts_with(name, '?')

def check__prune(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> core__CType:
    while True:
        _cdy_t229: object = t
        if isinstance(_cdy_t229, core__TVar):
            name = _cdy_t229.name
            if cdy_rt.primitives.map_has(subst, name):
                t = cdy_rt.primitives.map_get(subst, name)
                continue
            else:
                return t
        else:
            return t

def check__resolve_type(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> core__CType:
    _cdy_t230: object = check__prune(t, subst)
    if isinstance(_cdy_t230, core__TCon):
        name = _cdy_t230.name
        args = _cdy_t230.args
        return core__TCon(name, cdy_rt.primitives.list_map((lambda a: check__resolve_type(a, subst)), args))
    elif isinstance(_cdy_t230, core__TFn):
        params = _cdy_t230.params
        ret = _cdy_t230.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__resolve_type(p, subst)), params), check__resolve_type(ret, subst))
    else:
        return check__prune(t, subst)

def check__occurs(v: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> bool:
    _cdy_t231: object = check__prune(t, subst)
    if isinstance(_cdy_t231, core__TVar):
        name = _cdy_t231.name
        return (name == v)
    elif isinstance(_cdy_t231, core__TCon):
        args = _cdy_t231.args
        return cdy_rt.primitives.list_any((lambda a: check__occurs(v, a, subst)), args)
    else:
        assert isinstance(_cdy_t231, core__TFn)
        params = _cdy_t231.params
        ret = _cdy_t231.ret
        return (cdy_rt.primitives.list_any((lambda p: check__occurs(v, p, subst)), params) or check__occurs(v, ret, subst))

def check__unify(a: core__CType, b: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    while True:
        pa = check__prune(a, subst)
        pb = check__prune(b, subst)
        if check__is_any(pa):
            return (True, check__mark_any(pb, subst))
        elif check__is_any(pb):
            return (True, check__mark_any(pa, subst))
        elif check__is_var(pa):
            return check__bind_var(check__tvar_name(pa), pb, subst)
        elif check__is_var(pb):
            return check__bind_var(check__tvar_name(pb), pa, subst)
        else:
            _cdy_t232: object = pa
            if isinstance(_cdy_t232, core__TVar):
                name = _cdy_t232.name
                _cdy_t234: object = pb
                if isinstance(_cdy_t234, core__TVar):
                    other = _cdy_t234.name
                    _cdy_t233 = (name == other)
                else:
                    _cdy_t233 = False
                return (_cdy_t233, subst)
            elif isinstance(_cdy_t232, core__TCon):
                _cdy_name_781 = _cdy_t232.name
                args = _cdy_t232.args
                _cdy_t235: object = pb
                if isinstance(_cdy_t235, core__TCon):
                    _cdy_other_783 = _cdy_t235.name
                    bargs = _cdy_t235.args
                    if ((_cdy_name_781 == _cdy_other_783) and (len(args) == len(bargs))):
                        return check__unify_all(args, bargs, subst)
                    else:
                        return (False, subst)
                else:
                    return (False, subst)
            else:
                assert isinstance(_cdy_t232, core__TFn)
                params = _cdy_t232.params
                ret = _cdy_t232.ret
                _cdy_t236: object = pb
                if isinstance(_cdy_t236, core__TFn):
                    bparams = _cdy_t236.params
                    bret = _cdy_t236.ret
                    if (len(params) == len(bparams)):
                        _tup = check__unify_all(params, bparams, subst)
                        ok = _tup[0]
                        s = _tup[1]
                        if ok:
                            a, b, subst = (ret, bret, s)
                            continue
                        else:
                            return (False, s)
                    else:
                        return (False, subst)
                else:
                    return (False, subst)

def check__mark_any(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    _cdy_t237: object = check__prune(t, subst)
    if isinstance(_cdy_t237, core__TVar):
        name = _cdy_t237.name
        if check__is_flexible(name):
            return cdy_rt.primitives.map_set(subst, ('any' + name), core__ANY)
        else:
            return subst
    elif isinstance(_cdy_t237, core__TCon):
        args = _cdy_t237.args
        return cdy_rt.primitives.list_fold((lambda s, a: check__mark_any(a, s)), subst, args)
    else:
        assert isinstance(_cdy_t237, core__TFn)
        params = _cdy_t237.params
        ret = _cdy_t237.ret
        return check__mark_any(ret, cdy_rt.primitives.list_fold((lambda s, p: check__mark_any(p, s)), subst, params))

def check__unify_all(xs: tuple[core__CType, ...], ys: tuple[core__CType, ...], subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    while True:
        if (len(xs) == 0):
            return (True, subst)
        else:
            _tup = check__unify(xs[0], ys[0], subst)
            ok = _tup[0]
            s = _tup[1]
            if ok:
                xs, ys, subst = (prelude__rest(xs), prelude__rest(ys), s)
                continue
            else:
                return (False, s)

def check__bind_var(v: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    _cdy_t239: object = t
    if isinstance(_cdy_t239, core__TVar):
        other = _cdy_t239.name
        _cdy_t238 = (other == v)
    else:
        _cdy_t238 = False
    if _cdy_t238:
        return (True, subst)
    elif check__occurs(v, t, subst):
        return (False, subst)
    elif (core__constraint_of(v) == ''):
        return (True, cdy_rt.primitives.map_set(subst, v, t))
    else:
        return check__bind_constrained(v, core__constraint_of(v), t, subst)

def check__bind_constrained(v: str, c: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    takes = cdy_rt.primitives.map_get(core__CONSTRAINTS, c)
    _cdy_t240: object = t
    if isinstance(_cdy_t240, core__TCon):
        name = _cdy_t240.name
        if cdy_rt.primitives.list_contains(name, takes):
            return (True, cdy_rt.primitives.map_set(subst, v, t))
        else:
            return (False, subst)
    elif isinstance(_cdy_t240, core__TVar):
        other = _cdy_t240.name
        oc = core__constraint_of(other)
        if (not check__is_flexible(other)):
            if ((oc != '') and check__within(oc, c)):
                return (True, cdy_rt.primitives.map_set(subst, v, t))
            else:
                return (False, subst)
        elif (oc == ''):
            return (True, cdy_rt.primitives.map_set(subst, other, core__TVar(v)))
        elif check__within(c, oc):
            return (True, cdy_rt.primitives.map_set(subst, other, core__TVar(v)))
        elif check__within(oc, c):
            return (True, cdy_rt.primitives.map_set(subst, v, t))
        else:
            both = cdy_rt.primitives.list_filter((lambda x: cdy_rt.primitives.list_contains(x, cdy_rt.primitives.map_get(core__CONSTRAINTS, oc))), takes)
            if ((len(both) == 1) and (both[0] != 'List')):
                return (True, cdy_rt.primitives.map_set(cdy_rt.primitives.map_set(subst, v, check__tcon(both[0])), other, check__tcon(both[0])))
            else:
                return (False, subst)
    else:
        return (False, subst)

def check__within(a: str, b: str) -> bool:
    return cdy_rt.primitives.list_all((lambda x: cdy_rt.primitives.list_contains(x, cdy_rt.primitives.map_get(core__CONSTRAINTS, b))), cdy_rt.primitives.map_get(core__CONSTRAINTS, a))

def check__is_any(t: core__CType) -> bool:
    _cdy_t241: object = t
    if isinstance(_cdy_t241, core__TCon):
        name = _cdy_t241.name
        return (name == 'Any')
    else:
        return False

def check__is_var(t: core__CType) -> bool:
    _cdy_t242: object = t
    if isinstance(_cdy_t242, core__TVar):
        name = _cdy_t242.name
        return check__is_flexible(name)
    else:
        return False

def check__tvar_name(t: core__CType) -> str:
    _cdy_t243: object = t
    if isinstance(_cdy_t243, core__TVar):
        name = _cdy_t243.name
        return name
    else:
        return ''

def check__accepts(want: core__CType, actual: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    return check__unify(want, actual, subst)

def check__expect(want: core__CType, actual: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    _tup = check__accepts(want, actual, st.subst)
    ok = _tup[0]
    s = _tup[1]
    if ok:
        return st._replace(subst=s)
    else:
        lead = ('' if (what == '') else (what + ': '))
        return check__report((lead + 'expected ' + check__show(want, st.subst) + ', got ' + check__show(actual, st.subst)), ctx, st)

def check__expect_is(want: core__CType, actual: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    _tup = check__accepts(want, actual, st.subst)
    ok = _tup[0]
    s = _tup[1]
    if ok:
        return st._replace(subst=s)
    else:
        return check__report((what + ' is ' + check__show(actual, st.subst) + ', not ' + check__show(want, st.subst)), ctx, st)

def check__join_types(a: core__CType, b: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__Res:
    pa = check__prune(a, st.subst)
    pb = check__prune(b, st.subst)
    _tup = check__unify(pa, pb, st.subst)
    ok = _tup[0]
    s = _tup[1]
    if ok:
        return check__Res(pa, st._replace(subst=s))
    else:
        return check__Res(core__ANY, check__report(check__mismatch(what, check__show(pa, st.subst), check__show(pb, st.subst), ctx), ctx, st))

def check__mismatch(what: str, a: str, b: str, ctx: check__Ctx) -> str:
    return (what + ' are ' + a + ' and ' + b)

def check__instantiate(t: core__CType, st: check__St) -> check__Res:
    names = check__rigid_vars(t, ())
    if (len(names) == 0):
        return check__Res(t, st)
    else:
        _tup = check__fresh_types(len(names), st, ())
        ftypes = _tup[0]
        st1 = _tup[1]
        vars_ = cdy_rt.primitives.list_map((lambda i: check__keep_constraint(cdy_rt.primitives.at(names, i), cdy_rt.primitives.at(ftypes, i))), cdy_rt.primitives.list_range(0, len(names)))
        return check__Res(check__put_vars(t, check__zip_map(names, vars_, {})), st1)

def check__keep_constraint(name: str, fresh_var: core__CType) -> core__CType:
    c = core__constraint_of(name)
    if (c == ''):
        return fresh_var
    else:
        return core__TVar((check__tvar_name(fresh_var) + ':' + c))

def check__rigid_vars(t: core__CType, acc: tuple[str, ...]) -> tuple[str, ...]:
    _cdy_t244: object = t
    if isinstance(_cdy_t244, core__TVar):
        name = _cdy_t244.name
        if (check__is_flexible(name) or cdy_rt.primitives.list_contains(name, acc)):
            return acc
        else:
            return (acc + cdy_rt.primitives.to_list(name))
    elif isinstance(_cdy_t244, core__TCon):
        args = _cdy_t244.args
        return cdy_rt.primitives.list_fold((lambda a, x: check__rigid_vars(x, a)), acc, args)
    else:
        assert isinstance(_cdy_t244, core__TFn)
        params = _cdy_t244.params
        ret = _cdy_t244.ret
        return check__rigid_vars(ret, cdy_rt.primitives.list_fold((lambda a, x: check__rigid_vars(x, a)), acc, params))

class check__Order(_cdy_NamedTuple):
    kinds: _cdy_Mapping[str, str]
    bodies: _cdy_Mapping[str, core__Expr]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__Order, 'Order', (), (('Map', 'String', 'String'), ('Map', 'String', 'core__Expr')))

def check__order_of(tops: tuple[core__Top, ...]) -> check__Order:
    def _cdy_t246(o: check__Order, top: core__Top) -> check__Order:
        _cdy_t245: object = top
        if isinstance(_cdy_t245, core__TDef):
            name = _cdy_t245.name
            return o._replace(kinds=cdy_rt.primitives.map_set(o.kinds, name, 'def'))
        elif isinstance(_cdy_t245, core__TDefn):
            _cdy_name_890 = _cdy_t245.name
            body = _cdy_t245.body
            return check__Order(cdy_rt.primitives.map_set(o.kinds, _cdy_name_890, 'defn'), cdy_rt.primitives.map_set(o.bodies, _cdy_name_890, body))
        else:
            return cdy_rt.primitives.list_fold((lambda o2, n: o2._replace(kinds=cdy_rt.primitives.map_set(o2.kinds, n, 'deft'))), o, check__defined_by(top))
    return cdy_rt.primitives.list_fold(_cdy_t246, check__Order({}, {}), tops)

def check__defined_by(top: core__Top) -> tuple[str, ...]:
    _cdy_t247: object = top
    if isinstance(_cdy_t247, core__TDeft):
        name = _cdy_t247.name
        return (name,)
    elif isinstance(_cdy_t247, core__TDeftSum):
        variants = _cdy_t247.variants
        return cdy_rt.primitives.list_map((lambda v: v.name), variants)
    elif isinstance(_cdy_t247, core__TDef):
        _cdy_name_898 = _cdy_t247.name
        return (_cdy_name_898,)
    elif isinstance(_cdy_t247, core__TDefn):
        _cdy_name_899 = _cdy_t247.name
        return (_cdy_name_899,)
    else:
        assert isinstance(_cdy_t247, core__TExpr)
        return ()

def check__check_order(tops: tuple[core__Top, ...], order: check__Order, start: _cdy_Mapping[str, bool]) -> tuple[str, ...]:
    def _cdy_t251(defined: _cdy_Mapping[str, bool], top: core__Top) -> tuple[_cdy_Mapping[str, bool], tuple[str, ...]]:
        _cdy_t250 = cdy_rt.primitives.list_fold((lambda d, n: cdy_rt.primitives.map_set(d, n, True)), defined, check__defined_by(top))
        _cdy_t249: object = top
        if isinstance(_cdy_t249, core__TDef):
            init = _cdy_t249.init
            _cdy_t248 = check__order_errors(init, order, defined)
        elif isinstance(_cdy_t249, core__TExpr):
            e = _cdy_t249.expr
            _cdy_t248 = check__order_errors(e, order, defined)
        else:
            _cdy_t248 = ()
        return (_cdy_t250, _cdy_t248)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t251, start, tops)
    _defined = _tup[0]
    errors = _tup[1]
    return cdy_rt.primitives.list_concat(errors)

def check__order_errors(e: core__Expr, order: check__Order, defined: _cdy_Mapping[str, bool]) -> tuple[str, ...]:
    def _cdy_t252(u: tuple[str, form__Pos]) -> tuple[str, ...]:
        _tup = u
        name = _tup[0]
        pos = _tup[1]
        reached = check__reach((name,), order, cdy_rt.primitives.map_from(((name, True),)))
        return cdy_rt.primitives.list_map((lambda n: (form__pos_text(pos) + check__used_early(n, name, order))), cdy_rt.primitives.list_filter((lambda n: (cdy_rt.primitives.map_has(order.kinds, n) and (not cdy_rt.primitives.map_has(defined, n)))), cdy_rt.primitives.map_keys(reached)))
    return cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(_cdy_t252, check__uses(e, ())))

def check__used_early(n: str, name: str, order: check__Order) -> str:
    through = ('' if (n == name) else (', through ' + check__shown_name(name)))
    return (check__shown_name(n) + ' is used before its ' + cdy_rt.primitives.map_get(order.kinds, n) + through)

def check__reach(todo: tuple[str, ...], order: check__Order, seen: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    if (len(todo) == 0):
        return seen
    else:
        name = todo[0]
        if cdy_rt.primitives.map_has(order.bodies, name):
            _cdy_t254 = (lambda n: (not cdy_rt.primitives.map_has(seen, n)))
            def _cdy_t253(u: tuple[str, form__Pos]) -> str:
                _tup = u
                n = _tup[0]
                _pos = _tup[1]
                return n
            _cdy_t255 = cdy_rt.primitives.list_filter(_cdy_t254, cdy_rt.primitives.list_map(_cdy_t253, check__uses(cdy_rt.primitives.map_get(order.bodies, name), ())))
        else:
            _cdy_t255 = ()
        found = _cdy_t255
        return check__reach((prelude__rest(todo) + found), order, cdy_rt.primitives.list_fold((lambda m, n: cdy_rt.primitives.map_set(m, n, True)), seen, found))

def check__uses(e: core__Expr, acc: tuple[tuple[str, form__Pos], ...]) -> tuple[tuple[str, form__Pos], ...]:
    _cdy_t256: object = e
    if isinstance(_cdy_t256, core__Global):
        name = _cdy_t256.name
        pos = _cdy_t256.pos
        return (acc + ((name, pos),))
    elif isinstance(_cdy_t256, core__Call):
        callee = _cdy_t256.callee
        args = _cdy_t256.args
        return check__uses_all(args, check__uses(callee, acc))
    elif isinstance(_cdy_t256, core__If):
        test = _cdy_t256.test
        then = _cdy_t256.then
        other = _cdy_t256.other
        return check__uses(other, check__uses(then, check__uses(test, acc)))
    elif isinstance(_cdy_t256, core__Do):
        body = _cdy_t256.body
        return check__uses_all(body, acc)
    elif isinstance(_cdy_t256, core__Lambda):
        _cdy_body_948 = _cdy_t256.body
        return check__uses(_cdy_body_948, acc)
    elif isinstance(_cdy_t256, core__Tuple):
        items = _cdy_t256.items
        return check__uses_all(items, acc)
    elif isinstance(_cdy_t256, core__ListOf):
        _cdy_items_950 = _cdy_t256.items
        return check__uses_all(_cdy_items_950, acc)
    elif isinstance(_cdy_t256, core__Fmt):
        parts = _cdy_t256.parts
        def _cdy_t258(a: tuple[tuple[str, form__Pos], ...], p: core__FPart) -> tuple[tuple[str, form__Pos], ...]:
            _cdy_t257: object = p
            if isinstance(_cdy_t257, core__FHole):
                x = _cdy_t257.expr
                return check__uses(x, a)
            else:
                return a
        return cdy_rt.primitives.list_fold(_cdy_t258, acc, parts)
    elif isinstance(_cdy_t256, core__Field):
        obj = _cdy_t256.obj
        return check__uses(obj, acc)
    elif isinstance(_cdy_t256, core__Assoc):
        _cdy_obj_956 = _cdy_t256.obj
        fields = _cdy_t256.fields
        def _cdy_t259(f: tuple[str, core__Expr]) -> core__Expr:
            _tup = f
            _name = _tup[0]
            v = _tup[1]
            return v
        return check__uses_all(cdy_rt.primitives.list_map(_cdy_t259, fields), check__uses(_cdy_obj_956, acc))
    elif isinstance(_cdy_t256, core__MatchE):
        subject = _cdy_t256.subject
        clauses = _cdy_t256.clauses
        default = _cdy_t256.default
        return check__uses_all(default, check__uses_all(cdy_rt.primitives.list_map((lambda c: c.body), clauses), check__uses(subject, acc)))
    else:
        return acc

def check__uses_all(es: tuple[core__Expr, ...], acc: tuple[tuple[str, form__Pos], ...]) -> tuple[tuple[str, form__Pos], ...]:
    return cdy_rt.primitives.list_fold((lambda a, x: check__uses(x, a)), acc, es)

def check__report(msg: str, ctx: check__Ctx, st: check__St) -> check__St:
    return st._replace(errors=(st.errors + cdy_rt.primitives.to_list((form__pos_text(ctx.here) + msg))))

def check__show(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> str:
    _cdy_t260: object = check__resolve_type(t, subst)
    if isinstance(_cdy_t260, core__TCon):
        name = _cdy_t260.name
        args = _cdy_t260.args
        if (len(args) == 0):
            return check__shown_name(name)
        else:
            return ('(' + check__shown_name(name) + ' ' + cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda a: check__show(a, subst)), args), ' ') + ')')
    elif isinstance(_cdy_t260, core__TFn):
        params = _cdy_t260.params
        ret = _cdy_t260.ret
        return ('(Fn (' + cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda p: check__show(p, subst)), params), ' ') + ') ' + check__show(ret, subst) + ')')
    else:
        assert isinstance(_cdy_t260, core__TVar)
        _cdy_name_981 = _cdy_t260.name
        if (not check__is_flexible(_cdy_name_981)):
            return _cdy_name_981
        elif (core__constraint_of(_cdy_name_981) != ''):
            return core__constraint_of(_cdy_name_981)
        else:
            return ('t' + cdy_rt.primitives.substring(_cdy_name_981, 1, len(_cdy_name_981)))

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
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(Ready, 'Ready', (), ('include__Module', ('List', 'form__Form'), ('Map', 'String', 'form__Macro'), 'core__Exports'))

def translate_modules(modules: tuple[include__Module, ...], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]]) -> str:
    builtins = expand__library_builtins(None)
    return python_of(check__type_check(program_tops(modules, parse, builtins), builtins))

def program_tops(modules: tuple[include__Module, ...], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[core__Top, ...]:
    ready = expand_modules(modules, (len(modules) - 1), ())
    by_key = exports_by_key(ready, {})
    elsewhere = core__elsewhere_names(exports_of(ready, ()))
    return analyse_modules(ready, by_key, elsewhere, builtins, parse, ())

def expand_modules(modules: tuple[include__Module, ...], top: int, acc: tuple[Ready, ...]) -> tuple[Ready, ...]:
    while True:
        if (len(acc) == len(modules)):
            return acc
        else:
            m = cdy_rt.primitives.at(modules, len(acc))
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

def analyse_modules(ready: tuple[Ready, ...], by_key: _cdy_Mapping[str, core__Exports], elsewhere: _cdy_Mapping[str, str], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], acc: tuple[core__Top, ...]) -> tuple[core__Top, ...]:
    if (len(ready) == 0):
        return acc
    else:
        r = ready[0]
        macros = r.macros
        tops = core__analyse_module(r.forms, r.exports, imported(r.module.imports, by_key, ()), elsewhere, builtins, (lambda text, where: expand__expand_all(parse(text, where), macros, ())), macros, False)
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
    return translate_expanded(forms, read__read_hole, {}, True)

def translate_expanded(forms: tuple[form__Form, ...], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> str:
    return python_of(core__analyse_program(forms, expand__library_builtins(None), parse, macros, quoting))

def python_of(tops: tuple[core__Top, ...]) -> str:
    stmts = lower__lower_program(tops, 0)
    globals_ = emit__global_names(tops, emit__Env({}, {}, {}, emit__generic_variants(tops), cdy_rt.spelling.SPELLINGS, {}, emit__deft_field_types(tops)))
    env = emit__bind_locals(emit__bound_locals(stmts, ()), globals_)
    return (emit__HEADER + emit__emit_imports(emit__PY_IMPORTS) + '\ncdy_rt.primitives.stop_on_panic()\n' + emit__emit_stmts(stmts, 0, env) + (emit__emit_main(env) if core__has_main(tops) else ''))

def translate_text(text: str) -> str:
    return translate_modules(include__text_modules(text), read__read_hole)

def translate_file(path: str) -> str:
    return translate_modules(include__read_modules(path), read__read_hole)
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
        cdy_rt.primitives.put_err(('candy: ' + src + ' -> ' + out))
        return 0


if __name__ == "__main__":
    cdy_rt.primitives.run_main(main)
