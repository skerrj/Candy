from __future__ import annotations

from collections.abc import Callable as _cdy_Callable, Mapping as _cdy_Mapping
from typing import Any as _cdy_Any, NamedTuple as _cdy_NamedTuple, cast as _cdy_cast
import math
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

def prelude__index_of[equatable](x: equatable, xs: tuple[equatable, ...]) -> prelude__Maybe[int]:
    i = cdy_rt.primitives.list_find_index((lambda y: (y == x)), xs)
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

def translator__catch_panic[a](f: _cdy_Callable[[None], a]) -> prelude__Result[a, str]:
    _tup = cdy_rt.primitives.run_caught(f)
    done = _tup[0]
    msg = _tup[1]
    if (len(done) == 1):
        return prelude__Ok(done[0])
    else:
        return prelude__Err(msg)

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
cdy_rt.primitives.register_type(form__Sym, 'Sym', (), ('String', 'form.Pos'))

class form__Lst(_cdy_NamedTuple):
    items: tuple[form__Form, ...]
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Lst, 'Lst', (), (('List', 'form.Form'), 'form.Pos'))

class form__Txt(_cdy_NamedTuple):
    val: str
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Txt, 'Txt', (), ('String', 'form.Pos'))

class form__IntLit(_cdy_NamedTuple):
    val: int
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__IntLit, 'IntLit', (), ('Int', 'form.Pos'))

class form__LongLit(_cdy_NamedTuple):
    val: int
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__LongLit, 'LongLit', (), ('Int', 'form.Pos'))

class form__ByteLit(_cdy_NamedTuple):
    val: int
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__ByteLit, 'ByteLit', (), ('Int', 'form.Pos'))

class form__FloatLit(_cdy_NamedTuple):
    val: float
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__FloatLit, 'FloatLit', (), ('Double', 'form.Pos'))

class form__DoubleLit(_cdy_NamedTuple):
    val: float
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__DoubleLit, 'DoubleLit', (), ('Double', 'form.Pos'))

class form__CharLit(_cdy_NamedTuple):
    val: str
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__CharLit, 'CharLit', (), ('Char', 'form.Pos'))

class form__BoolLit(_cdy_NamedTuple):
    val: bool
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__BoolLit, 'BoolLit', (), ('Bool', 'form.Pos'))
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

def form__form_pos(form: form__Form) -> form__Pos:
    _cdy_t3: object = form
    if isinstance(_cdy_t3, form__Sym):
        pos = _cdy_t3.pos
        return pos
    elif isinstance(_cdy_t3, form__Lst):
        _cdy_pos_6 = _cdy_t3.pos
        return _cdy_pos_6
    elif isinstance(_cdy_t3, form__Txt):
        _cdy_pos_7 = _cdy_t3.pos
        return _cdy_pos_7
    elif isinstance(_cdy_t3, form__IntLit):
        _cdy_pos_8 = _cdy_t3.pos
        return _cdy_pos_8
    elif isinstance(_cdy_t3, form__LongLit):
        _cdy_pos_9 = _cdy_t3.pos
        return _cdy_pos_9
    elif isinstance(_cdy_t3, form__ByteLit):
        _cdy_pos_10 = _cdy_t3.pos
        return _cdy_pos_10
    elif isinstance(_cdy_t3, form__FloatLit):
        _cdy_pos_11 = _cdy_t3.pos
        return _cdy_pos_11
    elif isinstance(_cdy_t3, form__DoubleLit):
        _cdy_pos_12 = _cdy_t3.pos
        return _cdy_pos_12
    elif isinstance(_cdy_t3, form__CharLit):
        _cdy_pos_13 = _cdy_t3.pos
        return _cdy_pos_13
    else:
        assert isinstance(_cdy_t3, form__BoolLit)
        _cdy_pos_14 = _cdy_t3.pos
        return _cdy_pos_14

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
    run: _cdy_Callable[[tuple[form__Form, ...]], form__Form]
    pos: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(form__Macro, 'Macro', (), ('String', 'Int', 'Fn', 'form.Pos'))

def string__trim(s: str) -> str:
    start = string__skip_space(s, 0, 1, len(s))
    end = string__skip_space(s, (len(s) - 1), -1, -1)
    if (start > end):
        return ''
    else:
        return cdy_rt.primitives.substring(s, start, (end + 1))

def string__skip_space(s: str, i: int, step: int, stop: int) -> int:
    while True:
        if ((i != stop) and string__space_at(s, i)):
            i = (i + step)
            continue
        else:
            return i

def string__space_at(s: str, i: int) -> bool:
    return cdy_rt.primitives.isspace(cdy_rt.primitives.substring(s, i, (i + 1)))

def string__lines(s: str) -> tuple[str, ...]:
    if (s == ''):
        return ()
    elif cdy_rt.primitives.ends_with(s, '\n'):
        return cdy_rt.primitives.split(cdy_rt.primitives.substring(s, 0, (len(s) - 1)), '\n')
    else:
        return cdy_rt.primitives.split(s, '\n')

def read__read_forms(text: str) -> tuple[form__Form, ...]:
    return read__read_all(read__Source('', (), form__NOWHERE), text, read__skip(text, 0), ())

def read__read_source(file: str, text: str) -> tuple[form__Form, ...]:
    return read__read_all(read__Source(file, read__line_starts(text, 0, (0,)), form__Pos(file, 1, 1)), text, read__skip(text, 0), ())

def read__read_hole(text: str, where: form__Pos) -> tuple[form__Form, ...]:
    if (where.line == 0):
        return read__read_forms(text)
    else:
        return read__read_all(read__Source(where.file, read__line_starts(text, 0, (0,)), where), text, read__skip(text, 0), ())

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
cdy_rt.primitives.register_type(read__Source, 'Source', (), ('String', ('List', 'Int'), 'form.Pos'))

def read__line_starts(text: str, pos: int, acc: tuple[int, ...]) -> tuple[int, ...]:
    while True:
        if (pos >= len(text)):
            return acc
        elif (read__char_text(text, pos) == '\n'):
            pos, acc = ((pos + 1), (acc + ((pos + 1),)))
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
            pos, acc = (read__skip(text, next_), (acc + (form,)))
            continue

def read__skip(text: str, pos: int) -> int:
    while True:
        if (pos >= len(text)):
            return pos
        elif cdy_rt.primitives.isspace(read__char_text(text, pos)):
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
    return ((pos >= len(text)) or cdy_rt.primitives.isspace(read__char_text(text, pos)) or cdy_rt.primitives.str_contains(read__char_text(text, pos), '();'))

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
            pos, acc = (read__skip(text, next_), (acc + (form,)))
            continue

def read__read_char(src: read__Source, text: str, pos: int) -> tuple[form__Form, int]:
    if (((pos + 1) < len(text)) and (not cdy_rt.primitives.isspace(read__char_text(text, (pos + 1)))) and read__ends_at(text, (pos + 2))):
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
        if ((pos >= len(text)) or cdy_rt.primitives.isspace(read__char_text(text, pos)) or cdy_rt.primitives.str_contains(read__char_text(text, pos), '()\'";\\')):
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

class syntax__SynName(_cdy_NamedTuple):
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(syntax__SynName, 'SynName', (), ())

class syntax__SynModName(_cdy_NamedTuple):
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(syntax__SynModName, 'SynModName', (), ())

class syntax__SynList(_cdy_NamedTuple):
    item: syntax__Syntax
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(syntax__SynList, 'SynList', (), ('syntax.Syntax',))

class syntax__SynOpt(_cdy_NamedTuple):
    item: syntax__Syntax
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(syntax__SynOpt, 'SynOpt', (), ('syntax.Syntax',))
type syntax__Syntax = syntax__SynName | syntax__SynModName | syntax__SynList | syntax__SynOpt

def syntax__read_shape(form: form__Form, where: str) -> tuple[syntax__Syntax, ...]:
    _cdy_t5: object = form
    if isinstance(_cdy_t5, form__Lst):
        items = _cdy_t5.items
        shape = cdy_rt.primitives.list_map((lambda item: syntax__read_syntax(item, where)), items)
        last = (len(shape) - 1)
        if cdy_rt.primitives.list_any((lambda i: (syntax__is_opt(cdy_rt.primitives.at(shape, i)) and (i < last))), cdy_rt.primitives.list_range(0, len(shape))):
            return cdy_rt.primitives.fail((where + 'special.cdy: (Opt c) may only be last'))
        else:
            return shape
    else:
        return cdy_rt.primitives.fail((where + 'special.cdy: a shape is a list of syntax categories, (ModName (Opt (List Name)))'))

def syntax__is_opt(c: syntax__Syntax) -> bool:
    _cdy_t6: object = c
    if isinstance(_cdy_t6, syntax__SynOpt):
        return True
    else:
        return False

def syntax__read_syntax(form: form__Form, where: str) -> syntax__Syntax:
    items = form__list_items(form)
    head = (form__sym_name(items[0]) if (len(items) > 0) else '')
    if (form__sym_name(form) == 'Name'):
        return syntax__SynName()
    elif (form__sym_name(form) == 'ModName'):
        return syntax__SynModName()
    elif ((head == 'List') and (len(items) == 2)):
        return syntax__SynList(syntax__read_syntax(items[1], where))
    elif ((head == 'Opt') and (len(items) == 2)):
        return syntax__SynOpt(syntax__read_syntax(items[1], where))
    else:
        return cdy_rt.primitives.fail((where + 'special.cdy: a syntax category is Name, ModName, (List c) or (Opt c)'))

def syntax__fits_shape(shape: tuple[syntax__Syntax, ...], args: tuple[form__Form, ...]) -> bool:
    if (len(shape) == 0):
        return (len(args) == 0)
    else:
        _cdy_t7: object = shape[0]
        if isinstance(_cdy_t7, syntax__SynOpt):
            item = _cdy_t7.item
            return ((len(args) == 0) or syntax__fits_shape(((item,) + prelude__rest(shape)), args))
        else:
            return ((len(args) > 0) and syntax__fits_syntax(shape[0], args[0]) and syntax__fits_shape(prelude__rest(shape), prelude__rest(args)))

def syntax__fits_syntax(c: syntax__Syntax, form: form__Form) -> bool:
    _cdy_t8: object = c
    if isinstance(_cdy_t8, syntax__SynName):
        return (form__sym_name(form) != '')
    elif isinstance(_cdy_t8, syntax__SynModName):
        return (form__sym_name(form) != '')
    elif isinstance(_cdy_t8, syntax__SynList):
        item = _cdy_t8.item
        _cdy_t9: object = form
        if isinstance(_cdy_t9, form__Lst):
            items = _cdy_t9.items
            return cdy_rt.primitives.list_all((lambda f: syntax__fits_syntax(item, f)), items)
        else:
            return False
    else:
        assert isinstance(_cdy_t8, syntax__SynOpt)
        _cdy_item_20 = _cdy_t8.item
        return syntax__fits_syntax(_cdy_item_20, form)

def syntax__shape_text(name: str, shape: tuple[syntax__Syntax, ...]) -> str:
    return ('(' + cdy_rt.primitives.join(((name,) + cdy_rt.primitives.list_map(syntax__syntax_text, shape)), ' ') + ')')

def syntax__syntax_text(c: syntax__Syntax) -> str:
    _cdy_t10: object = c
    if isinstance(_cdy_t10, syntax__SynName):
        return 'Name'
    elif isinstance(_cdy_t10, syntax__SynModName):
        return 'ModName'
    elif isinstance(_cdy_t10, syntax__SynList):
        item = _cdy_t10.item
        return ('(' + syntax__syntax_text(item) + '*)')
    else:
        assert isinstance(_cdy_t10, syntax__SynOpt)
        _cdy_item_25 = _cdy_t10.item
        return ('[' + syntax__syntax_text(_cdy_item_25) + ']')

def syntax__declared_shape(decls: tuple[form__Form, ...], name: str) -> tuple[syntax__Syntax, ...]:
    def _cdy_t11(_cdy_form_28: form__Form) -> bool:
        items = form__list_items(_cdy_form_28)
        return ((len(items) == 3) and (form__sym_name(items[0]) == 'special') and (form__sym_name(items[1]) == name))
    found = cdy_rt.primitives.list_filter(_cdy_t11, decls)
    if (len(found) == 0):
        return ()
    else:
        form = found[0]
        return syntax__read_shape(form__list_items(form)[2], form__pos_text(form__form_pos(form)))

def map__update[k, v](m: _cdy_Mapping[k, v], key: k, f: _cdy_Callable[[v], v]) -> _cdy_Mapping[k, v]:
    return cdy_rt.primitives.map_set(m, key, f(cdy_rt.primitives.map_get(m, key)))

def map__values[k, v](m: _cdy_Mapping[k, v]) -> tuple[v, ...]:
    return cdy_rt.primitives.list_map((lambda key: cdy_rt.primitives.map_get(m, key)), cdy_rt.primitives.map_keys(m))

def map__at_or[k, v](m: _cdy_Mapping[k, v], key: k, fallback: v) -> v:
    if cdy_rt.primitives.map_has(m, key):
        return cdy_rt.primitives.map_get(m, key)
    else:
        return fallback

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
cdy_rt.primitives.register_type(include__Module, 'Module', (), ('String', 'String', 'String', ('List', 'form.Form'), ('List', 'include.Imp')))

class include__Imp(_cdy_NamedTuple):
    key: str
    pos: form__Pos
    only: prelude__Maybe[tuple[form__Form, ...]]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(include__Imp, 'Imp', (), ('String', 'form.Pos', ('prelude.Maybe', ('List', 'form.Form'))))

class include__Mods(_cdy_NamedTuple):
    done: tuple[include__Module, ...]
    seen: _cdy_Mapping[str, bool]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(include__Mods, 'Mods', (), (('List', 'include.Module'), ('Map', 'String', 'Bool')))

def include__read_modules(path: str) -> tuple[include__Module, ...]:
    return include__checked_stems(include__add_module(path, cdy_rt.primitives.path_resolve(path), read__read_source(path, cdy_rt.primitives.slurp(path)), cdy_rt.primitives.path_dir(path), (), include__Mods((), {})))

def include__text_modules(text: str) -> tuple[include__Module, ...]:
    return include__checked_stems(include__add_module('', '', read__read_source('', text), '.', (), include__Mods((), {})))

def include__add_module(path: str, key: str, forms: tuple[form__Form, ...], dir_: str, stack: tuple[str, ...], acc: include__Mods) -> include__Mods:
    imports = (include__prelude_module(key) + include__module_imports(forms, dir_))
    inner = include__load_imports(imports, (stack + (key,)), acc._replace(seen=cdy_rt.primitives.map_set(acc.seen, key, True)))
    return inner._replace(done=(inner.done + (include__Module(path, key, cdy_rt.primitives.path_stem(path), include__other_forms(forms, dir_), include__imp_list(imports)),)))

def include__prelude_module(key: str) -> tuple[tuple[str, include__Imp], ...]:
    path = include__library_path('prelude.cdy')
    prelude = cdy_rt.primitives.path_resolve(path)
    if ((prelude == key) or include__is_declaration(key)):
        return ()
    else:
        return ((path, include__Imp(prelude, form__NOWHERE, prelude__None())),)

def include__library_dir(_: None) -> str:
    return cdy_rt.primitives.module_dir(form__sym_name)

def include__library_path(name: str) -> str:
    dir_ = include__library_dir(None)
    path = cdy_rt.primitives.path_join(dir_, name)
    if cdy_rt.primitives.file_exists(path):
        return path
    else:
        return cdy_rt.primitives.fail(('the translator needs ' + name + ' next to it, in ' + dir_))

def include__module_imports(forms: tuple[form__Form, ...], dir_: str) -> tuple[tuple[str, include__Imp], ...]:
    shape = include__import_shape(None)
    def _cdy_t12(form: form__Form) -> tuple[str, include__Imp]:
        _tup = include__import_parts(shape, form)
        name = _tup[0]
        only = _tup[1]
        path = include__import_path('import', dir_, name, form__form_pos(form))
        return (path, include__Imp(cdy_rt.primitives.path_resolve(path), form__form_pos(form), only))
    return cdy_rt.primitives.list_map(_cdy_t12, cdy_rt.primitives.list_filter(include__is_import, forms))

def include__imp_list(imports: tuple[tuple[str, include__Imp], ...]) -> tuple[include__Imp, ...]:
    def _cdy_t13(i: tuple[str, include__Imp]) -> include__Imp:
        _tup = i
        _name = _tup[0]
        imp = _tup[1]
        return imp
    return cdy_rt.primitives.list_map(_cdy_t13, imports)

def include__load_imports(imports: tuple[tuple[str, include__Imp], ...], stack: tuple[str, ...], start: include__Mods) -> include__Mods:
    def _cdy_t14(acc: include__Mods, i: tuple[str, include__Imp]) -> include__Mods:
        _tup = i
        path = _tup[0]
        imp = _tup[1]
        key = imp.key
        if cdy_rt.primitives.list_contains(key, stack):
            return cdy_rt.primitives.fail((form__pos_text(imp.pos) + 'import: cycle ' + include__cycle_text(stack, key)))
        elif cdy_rt.primitives.map_has(acc.seen, key):
            return acc
        else:
            return include__add_module(path, key, read__read_source(path, cdy_rt.primitives.slurp(path)), cdy_rt.primitives.path_dir(path), stack, acc)
    return cdy_rt.primitives.list_fold(_cdy_t14, start, imports)

def include__cycle_text(stack: tuple[str, ...], key: str) -> str:
    cycle = cdy_rt.primitives.list_drop(cdy_rt.primitives.list_find_index((lambda k: (k == key)), stack), stack)
    return (cdy_rt.primitives.join(cdy_rt.primitives.list_map(cdy_rt.primitives.path_stem, cycle), ' -> ') + ' -> ' + cdy_rt.primitives.path_stem(key))

def include__other_forms(forms: tuple[form__Form, ...], dir_: str) -> tuple[form__Form, ...]:
    return cdy_rt.primitives.list_map((lambda form: include__macro_import(form, dir_)), cdy_rt.primitives.list_filter((lambda form: (not include__is_import(form))), forms))

def include__checked_stems(mods: include__Mods) -> tuple[include__Module, ...]:
    modules = mods.done
    checked = include__unique_stems(cdy_rt.primitives.slice_(modules, 0, (len(modules) - 1)), {})
    return modules

def include__unique_stems(modules: tuple[include__Module, ...], start: _cdy_Mapping[str, str]) -> bool:
    def _cdy_t15(seen: _cdy_Mapping[str, str], m: include__Module) -> _cdy_Mapping[str, str]:
        stem = m.stem
        if cdy_rt.primitives.map_has(seen, stem):
            return cdy_rt.primitives.fail(('import: two modules are named ' + stem + ': ' + cdy_rt.primitives.map_get(seen, stem) + ' and ' + m.path))
        else:
            return cdy_rt.primitives.map_set(seen, stem, m.path)
    _seen = cdy_rt.primitives.list_fold(_cdy_t15, start, modules)
    return True

def include__macro_import(form: form__Form, dir_: str) -> form__Form:
    items = form__list_items(form)
    pos = form__form_pos(form)
    if ((len(items) == 0) or (form__sym_name(items[0]) != 'import-macros')):
        return form
    elif ((len(items) == 2) and (form__sym_name(items[1]) != '')):
        return form__Lst((items[0], form__Txt(include__import_path('import-macros', dir_, form__sym_name(items[1]), pos), pos)), pos)
    else:
        return cdy_rt.primitives.fail((form__pos_text(pos) + 'import-macros: expected (import-macros name)'))

def include__is_import(form: form__Form) -> bool:
    items = form__list_items(form)
    return ((len(items) > 0) and (form__sym_name(items[0]) == 'import'))

def include__import_shape(_: None) -> tuple[syntax__Syntax, ...]:
    path = include__library_path('special.cdy')
    return syntax__declared_shape(read__read_source(path, cdy_rt.primitives.slurp(path)), 'import')

def include__import_parts(shape: tuple[syntax__Syntax, ...], form: form__Form) -> tuple[str, prelude__Maybe[tuple[form__Form, ...]]]:
    args = prelude__rest(form__list_items(form))
    if (not syntax__fits_shape(shape, args)):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'import: expected ' + syntax__shape_text('import', shape)))
    elif (len(args) == 1):
        return (form__sym_name(args[0]), prelude__None())
    else:
        return (form__sym_name(args[0]), prelude__Some(form__list_items(args[1])))

def include__declaration_modules(_: None) -> tuple[str, ...]:
    def _cdy_t16(acc: tuple[str, ...], key: str) -> tuple[str, ...]:
        parts = cdy_rt.primitives.split(key, '.')
        if ((len(parts) != 2) or (parts[0] == '') or cdy_rt.primitives.list_contains(parts[0], acc)):
            return acc
        else:
            return (acc + (parts[0],))
    return cdy_rt.primitives.list_fold(_cdy_t16, (), cdy_rt.primitives.map_keys(cdy_rt.spelling.SPELLINGS))

def include__is_declaration_name(name: str) -> bool:
    return cdy_rt.primitives.list_contains(name, include__declaration_modules(None))

def include__is_declaration(key: str) -> bool:
    return cdy_rt.primitives.list_any((lambda name: (key == cdy_rt.primitives.path_resolve(include__library_path((name + '.cdy'))))), include__declaration_modules(None))
include__NOT_MODULES: tuple[str, ...] = ('special', 'prelude_macros')

def include__import_path(what: str, dir_: str, name: str, pos: form__Pos) -> str:
    file = (name + '.cdy')
    path = cdy_rt.primitives.path_join(dir_, file)
    lib = cdy_rt.primitives.path_join(include__library_dir(None), file)
    if (cdy_rt.primitives.path_stem(name) == 'system'):
        return cdy_rt.primitives.fail((form__pos_text(pos) + what + ': every file imports system, implicitly'))
    elif include__is_declaration_name(name):
        return include__library_path(file)
    elif cdy_rt.primitives.file_exists(path):
        return path
    elif cdy_rt.primitives.list_contains(name, include__NOT_MODULES):
        return cdy_rt.primitives.fail((form__pos_text(pos) + what + ': ' + name + " is the translator's, not a module"))
    elif cdy_rt.primitives.file_exists(lib):
        return lib
    else:
        return cdy_rt.primitives.fail((form__pos_text(pos) + what + ": can't find " + file + ' in ' + dir_ + ' or the library'))

class core__TCon(_cdy_NamedTuple):
    module: str
    name: str
    args: tuple[core__CType, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TCon, 'TCon', (), ('String', 'String', ('List', 'core.CType')))

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
cdy_rt.primitives.register_type(core__TFn, 'TFn', (), (('List', 'core.CType'), 'core.CType'))
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
cdy_rt.primitives.register_type(core__Lit, 'Lit', (), ('form.Form', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Local, 'Local', (), ('String', 'Int', 'form.Pos', 'core.CType'))

class core__Global(_cdy_NamedTuple):
    module: str
    name: str
    pos: form__Pos
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Global, 'Global', (), ('String', 'String', 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Prim, 'Prim', (), ('String', 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Call, 'Call', (), ('core.Expr', ('List', 'core.Expr'), 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__If, 'If', (), ('core.Expr', 'core.Expr', 'core.Expr', 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Do, 'Do', (), (('List', 'core.Expr'), 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Lambda, 'Lambda', (), (('List', 'core.Expr'), 'core.Expr', 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Tuple, 'Tuple', (), (('List', 'core.Expr'), 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__ListOf, 'ListOf', (), (('List', 'core.Expr'), 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Fmt, 'Fmt', (), (('List', 'core.FPart'), 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Field, 'Field', (), ('core.Expr', 'String', 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__Assoc, 'Assoc', (), ('core.Expr', ('List', ('Tup', 'String', 'core.Expr')), 'form.Pos', 'core.CType'))

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
cdy_rt.primitives.register_type(core__MatchE, 'MatchE', (), ('core.Expr', ('List', 'core.Clause'), ('List', 'core.Expr'), 'form.Pos', 'core.CType'))

class core__Temp(_cdy_NamedTuple):
    id_: int
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Temp, 'Temp', (), ('Int', 'core.CType'))
type core__Expr = core__Lit | core__Local | core__Global | core__Prim | core__Call | core__If | core__Do | core__Lambda | core__Tuple | core__ListOf | core__Fmt | core__Field | core__Assoc | core__MatchE | core__Temp
core__SYSTEM: str = 'system'
core__ANY: core__CType = core__TCon(core__SYSTEM, 'Any', ())

class core__Clause(_cdy_NamedTuple):
    module: str
    variant: str
    binds: tuple[tuple[str, core__Expr], ...]
    body: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Clause, 'Clause', (), ('String', 'String', ('List', ('Tup', 'String', 'core.Expr')), 'core.Expr'))

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
cdy_rt.primitives.register_type(core__FHole, 'FHole', (), ('core.Expr',))
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
cdy_rt.primitives.register_type(core__Variant, 'Variant', (), ('String', ('List', ('Tup', 'String', 'core.CType'))))

class core__TDeft(_cdy_NamedTuple):
    module: str
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TDeft, 'TDeft', (), ('String', 'String', ('List', 'String'), ('List', ('Tup', 'String', 'core.CType'))))

class core__TDeftSum(_cdy_NamedTuple):
    module: str
    name: str
    tvars: tuple[str, ...]
    variants: tuple[core__Variant, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TDeftSum, 'TDeftSum', (), ('String', 'String', ('List', 'String'), ('List', 'core.Variant')))

class core__TDef(_cdy_NamedTuple):
    module: str
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
cdy_rt.primitives.register_type(core__TDef, 'TDef', (), ('String', 'String', 'core.Expr', 'core.CType', 'form.Pos'))

class core__TDefn(_cdy_NamedTuple):
    module: str
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
cdy_rt.primitives.register_type(core__TDefn, 'TDefn', (), ('String', 'String', ('List', 'core.Expr'), 'core.Expr', 'core.CType', 'form.Pos'))

class core__TExpr(_cdy_NamedTuple):
    expr: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__TExpr, 'TExpr', (), ('core.Expr',))
type core__Top = core__TDeft | core__TDeftSum | core__TDef | core__TDefn | core__TExpr
core__NIL: core__Expr = core__Prim('nil', form__NOWHERE, core__ANY)

class core__Scope(_cdy_NamedTuple):
    env: _cdy_Mapping[str, core__Expr]
    parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]]
    here: form__Pos
    macros: _cdy_Mapping[str, form__Macro]
    quoting: bool
    names: _cdy_Mapping[str, core__Entry]
    qualifiers: _cdy_Mapping[str, bool]
    builtins: _cdy_Mapping[str, core__Builtin]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Scope, 'Scope', (), (('Map', 'String', 'core.Expr'), 'Fn', 'form.Pos', ('Map', 'String', 'form.Macro'), 'Bool', ('Map', 'String', 'core.Entry'), ('Map', 'String', 'Bool'), ('Map', 'String', 'core.Builtin')))

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
    elif (core__name_error(name) != ''):
        return cdy_rt.primitives.fail(core__located(scope, core__name_error(name)))
    else:
        return scope._replace(env=cdy_rt.primitives.map_set(scope.env, name, loc))

def core__has_dot(name: str) -> bool:
    return cdy_rt.primitives.str_contains('.', name)

def core__name_error(name: str) -> str:
    if core__has_dot(name):
        return (name + ": a name can't hold a ., which qualifies a name with its module (m.name)")
    elif ((name != '/') and cdy_rt.primitives.str_contains('/', name)):
        return (name + ": a name can't hold a /, which is reserved")
    else:
        return ''

def core__bare_name(name: str) -> str:
    parts = cdy_rt.primitives.split(name, '.')
    if (core__has_dot(name) and (len(parts) == 2)):
        return parts[1]
    else:
        return name

def core__qualified_error(name: str, scope: core__Scope) -> str:
    parts = cdy_rt.primitives.split(name, '.')
    if (not core__has_dot(name)):
        return ''
    elif (core__number_hint(name) != ''):
        return (name + ': a number needs a digit before its . (' + core__number_hint(name) + ')')
    elif ((len(parts) != 2) or (parts[0] == '') or (parts[1] == '')):
        return (name + ': a qualified name is m.name, one . between a module (its file name, without its path) and a name')
    elif (not cdy_rt.primitives.map_has(scope.qualifiers, parts[0])):
        return (name + ": this file doesn't import a module " + parts[0])
    else:
        return (name + ': ' + parts[0] + " doesn't define " + parts[1])

def core__number_hint(name: str) -> str:
    sign = ('-' if cdy_rt.primitives.starts_with(name, '-') else '')
    body = cdy_rt.primitives.substring(name, len(sign), len(name))
    if (cdy_rt.primitives.starts_with(body, '.') and (len(body) > 1) and cdy_rt.primitives.str_contains(cdy_rt.primitives.substring(body, 1, 2), '0123456789')):
        return (sign + ('0' + body))
    else:
        return ''

def core__use_error(name: str, scope: core__Scope) -> str:
    if (cdy_rt.primitives.map_has(scope.names, name) and (not core__gives_way(name, scope))):
        _cdy_t17: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t17, core__Clash):
            modules = _cdy_t17.modules
            qualified = cdy_rt.primitives.list_map((lambda _cdy_m_20: (_cdy_m_20 + ('.' + name))), modules)
            return (name + ' is defined by ' + cdy_rt.primitives.join(modules, ' and ') + ': write ' + cdy_rt.primitives.join(qualified, ' or '))
        elif isinstance(_cdy_t17, core__Unlisted):
            m = _cdy_t17.module
            return (name + ': the import of ' + m + " doesn't list it: write " + m + '.' + name)
        elif isinstance(_cdy_t17, core__Private):
            _cdy_m_23 = _cdy_t17.module
            if core__has_dot(name):
                return (name + ': ' + core__bare_name(name) + ' is private to ' + _cdy_m_23)
            else:
                return (name + ' is private to ' + _cdy_m_23)
        else:
            return ''
    else:
        return ''

def core__gives_way(name: str, scope: core__Scope) -> bool:
    builtins = scope.builtins
    _cdy_t20 = (core__is_everyones(name, builtins) or core__is_builtin_type(name, builtins))
    if _cdy_t20:
        _cdy_t19: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t19, core__Unlisted):
            _cdy_t18 = True
        elif isinstance(_cdy_t19, core__Private):
            _cdy_t18 = True
        else:
            _cdy_t18 = False
        _cdy_t20 = _cdy_t18
    return _cdy_t20

class core__Value(_cdy_NamedTuple):
    module: str
    name: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Value, 'Value', (), ('String', 'String'))

class core__Declared(_cdy_NamedTuple):
    module: str
    name: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Declared, 'Declared', (), ('String', 'String'))

class core__Record(_cdy_NamedTuple):
    module: str
    name: str
    arity: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Record, 'Record', (), ('String', 'String', 'Int'))

class core__Sum(_cdy_NamedTuple):
    module: str
    name: str
    arity: int
    variants: tuple[str, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Sum, 'Sum', (), ('String', 'String', 'Int', ('List', 'String')))

class core__VariantOf(_cdy_NamedTuple):
    module: str
    name: str
    sum_: str
    fields: tuple[str, ...]
    all_: tuple[str, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__VariantOf, 'VariantOf', (), ('String', 'String', 'String', ('List', 'String'), ('List', 'String')))

class core__Elsewhere(_cdy_NamedTuple):
    module: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Elsewhere, 'Elsewhere', (), ('String',))

class core__Unlisted(_cdy_NamedTuple):
    module: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Unlisted, 'Unlisted', (), ('String',))

class core__Private(_cdy_NamedTuple):
    module: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Private, 'Private', (), ('String',))

class core__Clash(_cdy_NamedTuple):
    modules: tuple[str, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Clash, 'Clash', (), (('List', 'String'),))
type core__Entry = core__Value | core__Declared | core__Record | core__Sum | core__VariantOf | core__Elsewhere | core__Unlisted | core__Private | core__Clash

def core__entry_name(e: core__Entry) -> str:
    _cdy_t21: object = e
    if isinstance(_cdy_t21, core__Value):
        g = _cdy_t21.name
        return g
    elif isinstance(_cdy_t21, core__Declared):
        _cdy_g_29 = _cdy_t21.name
        return _cdy_g_29
    elif isinstance(_cdy_t21, core__Record):
        _cdy_g_30 = _cdy_t21.name
        return _cdy_g_30
    elif isinstance(_cdy_t21, core__Sum):
        _cdy_g_31 = _cdy_t21.name
        return _cdy_g_31
    elif isinstance(_cdy_t21, core__VariantOf):
        _cdy_g_32 = _cdy_t21.name
        return _cdy_g_32
    else:
        return ''

def core__entry_module(e: core__Entry) -> str:
    _cdy_t22: object = e
    if isinstance(_cdy_t22, core__Value):
        m = _cdy_t22.module
        return m
    elif isinstance(_cdy_t22, core__Declared):
        _cdy_m_35 = _cdy_t22.module
        return _cdy_m_35
    elif isinstance(_cdy_t22, core__Record):
        _cdy_m_36 = _cdy_t22.module
        return _cdy_m_36
    elif isinstance(_cdy_t22, core__Sum):
        _cdy_m_37 = _cdy_t22.module
        return _cdy_m_37
    elif isinstance(_cdy_t22, core__VariantOf):
        _cdy_m_38 = _cdy_t22.module
        return _cdy_m_38
    elif isinstance(_cdy_t22, core__Elsewhere):
        _cdy_m_39 = _cdy_t22.module
        return _cdy_m_39
    elif isinstance(_cdy_t22, core__Unlisted):
        _cdy_m_40 = _cdy_t22.module
        return _cdy_m_40
    elif isinstance(_cdy_t22, core__Private):
        _cdy_m_41 = _cdy_t22.module
        return _cdy_m_41
    else:
        assert isinstance(_cdy_t22, core__Clash)
        return ''

def core__is_top_value(name: str, scope: core__Scope) -> bool:
    _cdy_t25 = cdy_rt.primitives.map_has(scope.names, name)
    if _cdy_t25:
        _cdy_t24: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t24, core__Value):
            _cdy_t23 = True
        elif isinstance(_cdy_t24, core__Record):
            _cdy_t23 = True
        elif isinstance(_cdy_t24, core__VariantOf):
            _cdy_t23 = True
        else:
            _cdy_t23 = False
        _cdy_t25 = _cdy_t23
    return _cdy_t25

def core__is_sum(name: str, scope: core__Scope) -> bool:
    _cdy_t28 = cdy_rt.primitives.map_has(scope.names, name)
    if _cdy_t28:
        _cdy_t27: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t27, core__Sum):
            _cdy_t26 = True
        else:
            _cdy_t26 = False
        _cdy_t28 = _cdy_t26
    return _cdy_t28

def core__type_arity(name: str, scope: core__Scope) -> int:
    if cdy_rt.primitives.map_has(scope.names, name):
        _cdy_t29: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t29, core__Record):
            arity = _cdy_t29.arity
            return arity
        elif isinstance(_cdy_t29, core__Sum):
            _cdy_arity_49 = _cdy_t29.arity
            return _cdy_arity_49
        else:
            return -1
    else:
        return -1

def core__declared_name(name: str, scope: core__Scope) -> str:
    if cdy_rt.primitives.map_has(scope.names, name):
        _cdy_t30: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t30, core__Declared):
            m = _cdy_t30.module
            g = _cdy_t30.name
            return core__builtin_key(m, g)
        else:
            return ''
    else:
        return ''

def core__elsewhere_module(name: str, scope: core__Scope) -> str:
    if cdy_rt.primitives.map_has(scope.names, name):
        _cdy_t31: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t31, core__Elsewhere):
            stem = _cdy_t31.module
            return stem
        else:
            return ''
    else:
        return ''

def core__is_variant(name: str, scope: core__Scope) -> bool:
    _cdy_t34 = cdy_rt.primitives.map_has(scope.names, name)
    if _cdy_t34:
        _cdy_t34 = (not cdy_rt.primitives.map_has(scope.env, name))
        if _cdy_t34:
            _cdy_t33: object = cdy_rt.primitives.map_get(scope.names, name)
            if isinstance(_cdy_t33, core__VariantOf):
                _cdy_t32 = True
            else:
                _cdy_t32 = False
            _cdy_t34 = _cdy_t32
    return _cdy_t34

def core__variant_fields(name: str, scope: core__Scope) -> tuple[str, ...]:
    if cdy_rt.primitives.map_has(scope.names, name):
        _cdy_t35: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t35, core__VariantOf):
            fields = _cdy_t35.fields
            return fields
        else:
            return ()
    else:
        return ()

def core__variant_sum(name: str, scope: core__Scope) -> str:
    if cdy_rt.primitives.map_has(scope.names, name):
        _cdy_t36: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t36, core__VariantOf):
            sum_ = _cdy_t36.sum_
            return sum_
        else:
            return ''
    else:
        return ''

def core__sibling_variants(name: str, scope: core__Scope) -> tuple[str, ...]:
    if cdy_rt.primitives.map_has(scope.names, name):
        _cdy_t37: object = cdy_rt.primitives.map_get(scope.names, name)
        if isinstance(_cdy_t37, core__VariantOf):
            all_ = _cdy_t37.all_
            return all_
        else:
            return ()
    else:
        return ()

def core__analyse_expr(form: form__Form, scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    _cdy_t38: object = form
    if isinstance(_cdy_t38, form__Sym):
        name = _cdy_t38.name
        pos = _cdy_t38.pos
        return (core__resolve(name, core__at_pos(scope, pos)), n)
    elif isinstance(_cdy_t38, form__Lst):
        items = _cdy_t38.items
        _cdy_pos_74 = _cdy_t38.pos
        return core__analyse_list(items, core__at_pos(scope, _cdy_pos_74), n)
    else:
        return (core__Lit(form, core__ANY), n)

def core__analyse_all(forms: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[tuple[core__Expr, ...], int]:
    def _cdy_t39(k: int, form: form__Form) -> tuple[int, core__Expr]:
        _cdy__tup_80 = core__analyse_expr(form, scope, k)
        e = _cdy__tup_80[0]
        k1 = _cdy__tup_80[1]
        return (k1, e)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t39, n, forms)
    n1 = _tup[0]
    es = _tup[1]
    return (es, n1)

def core__resolve(name: str, scope: core__Scope) -> core__Expr:
    if cdy_rt.primitives.map_has(scope.env, name):
        return core__at_use(cdy_rt.primitives.map_get(scope.env, name), scope.here)
    elif (core__use_error(name, scope) != ''):
        return cdy_rt.primitives.fail(core__located(scope, core__use_error(name, scope)))
    elif core__is_builtin_type(core__declared_name(name, scope), scope.builtins):
        return cdy_rt.primitives.fail(core__located(scope, (name + ' is a type, not a value')))
    elif (core__declared_name(name, scope) != ''):
        return core__Prim(core__declared_name(name, scope), scope.here, core__ANY)
    elif (core__is_variant(name, scope) and (len(core__variant_fields(name, scope)) == 0)):
        return core__Call(core__global_of(name, scope), (), scope.here, core__ANY)
    elif core__is_top_value(name, scope):
        return core__global_of(name, scope)
    elif core__is_sum(name, scope):
        return cdy_rt.primitives.fail(core__located(scope, (name + ' is a type, not a value')))
    elif core__is_special(name, scope.builtins):
        return cdy_rt.primitives.fail(core__located(scope, (name + ' is a special form, not a value')))
    elif core__is_everyones(name, scope.builtins):
        return core__Prim(name, scope.here, core__ANY)
    elif (core__declaring_module(name, scope.builtins) != ''):
        m = core__declaring_module(name, scope.builtins)
        return cdy_rt.primitives.fail(core__located(scope, (name + ' is declared by ' + m + ", which this file doesn't import: (import " + m + ')')))
    elif (core__elsewhere_module(name, scope) != ''):
        stem = core__elsewhere_module(name, scope)
        return cdy_rt.primitives.fail(core__located(scope, (name + ' is not defined here; ' + stem + " defines it, but this file doesn't import " + stem)))
    elif core__has_dot(name):
        return cdy_rt.primitives.fail(core__located(scope, core__qualified_error(name, scope)))
    else:
        return cdy_rt.primitives.fail(core__located(scope, ('unknown name ' + name)))

def core__at_use(e: core__Expr, pos: form__Pos) -> core__Expr:
    _cdy_t40: object = e
    if isinstance(_cdy_t40, core__Local):
        name = _cdy_t40.name
        id_ = _cdy_t40.id_
        return core__Local(name, id_, pos, core__ANY)
    else:
        return e

def core__global_of(name: str, scope: core__Scope) -> core__Expr:
    _tup = core__global_ref(name, scope.names)
    module = _tup[0]
    own = _tup[1]
    return core__Global(module, own, scope.here, core__ANY)

def core__global_ref(name: str, names: _cdy_Mapping[str, core__Entry]) -> tuple[str, str]:
    e = (cdy_rt.primitives.map_get(names, name) if cdy_rt.primitives.map_has(names, name) else core__Clash(()))
    if (core__entry_name(e) == ''):
        return (core__SYSTEM, name)
    else:
        return (core__entry_module(e), core__entry_name(e))

def core__global_key(module: str, name: str) -> str:
    if (module == ''):
        return name
    else:
        return (module + '.' + name)

def core__builtin_key(module: str, name: str) -> str:
    if (module == core__SYSTEM):
        return name
    else:
        return core__global_key(module, name)

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
            _cdy__tup_116 = core__analyse_all(prelude__rest(items), scope, n1)
            args = _cdy__tup_116[0]
            n2 = _cdy__tup_116[1]
            arity_ok = core__check_call(callee, len(args), scope)
            return (core__Call(callee, args, scope.here, core__ANY), n2)

def core__check_call(callee: core__Expr, count: int, scope: core__Scope) -> bool:
    _cdy_t41: object = callee
    if isinstance(_cdy_t41, core__Prim):
        name = _cdy_t41.name
        builtin = cdy_rt.primitives.map_get(scope.builtins, name)
        _cdy_t43: object = builtin
        if isinstance(_cdy_t43, core__Typed):
            type_ = _cdy_t43.type_
            _cdy_t42 = core__is_variadic(type_)
        else:
            _cdy_t42 = False
        rest_of_type = _cdy_t42
        _cdy_t45: object = builtin
        if isinstance(_cdy_t45, core__Typed):
            _cdy_type__127 = _cdy_t45.type_
            _cdy_t44 = core__fn_arity(_cdy_type__127)
        else:
            _cdy_t44 = -1
        arity = _cdy_t44
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
    elif cdy_rt.primitives.list_contains(head, ('def', 'defn', 'deft', 'sig', 'private', 'import', 'import-macros', 'defmacro')):
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
        _cdy__tup_156 = core__analyse_expr(args[1], inner, n1)
        body = _cdy__tup_156[0]
        n2 = _cdy__tup_156[1]
        return (core__nest(pairs, body, scope.here), n2)

def core__is_list_form(form: form__Form) -> bool:
    _cdy_t46: object = form
    if isinstance(_cdy_t46, form__Lst):
        return True
    else:
        return False

def core__let_bindings(bindings: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    _tup = cdy_rt.primitives.list_map_acc(core__let_binding, (scope, n), bindings)
    last = _tup[0]
    pairs = _tup[1]
    _cdy__tup_166 = last
    sc = _cdy__tup_166[0]
    k = _cdy__tup_166[1]
    return (cdy_rt.primitives.list_concat(pairs), sc, k)

def core__let_binding(state: tuple[core__Scope, int], binding: form__Form) -> tuple[tuple[core__Scope, int], tuple[tuple[core__Expr, core__Expr], ...]]:
    _tup = state
    scope = _tup[0]
    n = _tup[1]
    items = form__list_items(binding)
    if (len(items) != 2):
        return cdy_rt.primitives.fail(core__located(scope, 'let: binding must be (name init)'))
    else:
        _cdy__tup_175 = core__analyse_expr(items[1], scope, n)
        init = _cdy__tup_175[0]
        n1 = _cdy__tup_175[1]
        target = items[0]
        _cdy_t47: object = target
        if isinstance(_cdy_t47, form__Lst):
            names = _cdy_t47.items
            tmp = core__Local('_tup', n1, scope.here, core__ANY)
            _cdy__tup_181 = core__destructure(names, tmp, scope, (n1 + 1))
            more = _cdy__tup_181[0]
            inner = _cdy__tup_181[1]
            n2 = _cdy__tup_181[2]
            return ((inner, n2), (((tmp, init),) + more))
        else:
            name = form__sym_name(target)
            loc = core__Local(name, n1, form__form_pos(target), core__ANY)
            if ((name == '') or core__is_special(name, scope.builtins)):
                return cdy_rt.primitives.fail(core__located(scope, 'let name must be a name, not a special form'))
            else:
                return ((core__bind_local(scope, name, loc), (n1 + 1)), ((loc, init),))

def core__destructure(names: tuple[form__Form, ...], tmp: core__Expr, scope: core__Scope, n: int) -> tuple[tuple[tuple[core__Expr, core__Expr], ...], core__Scope, int]:
    def _cdy_t48(state: tuple[core__Scope, int], item: tuple[int, form__Form]) -> tuple[tuple[core__Scope, int], tuple[core__Expr, core__Expr]]:
        _cdy__tup_193 = state
        _cdy_sc_194 = _cdy__tup_193[0]
        _cdy_k_195 = _cdy__tup_193[1]
        _cdy__tup_196 = item
        i = _cdy__tup_196[0]
        form = _cdy__tup_196[1]
        name = form__sym_name(form)
        loc = core__Local(name, _cdy_k_195, form__form_pos(form), core__ANY)
        read = core__Call(core__Prim('at', _cdy_sc_194.here, core__ANY), (tmp, core__Lit(form__IntLit(i, _cdy_sc_194.here), core__ANY)), _cdy_sc_194.here, core__ANY)
        if (name == ''):
            return cdy_rt.primitives.fail(core__located(_cdy_sc_194, 'let name must be a name'))
        else:
            return ((core__bind_local(_cdy_sc_194, name, loc), (_cdy_k_195 + 1)), (loc, read))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t48, (scope, n), cdy_rt.primitives.list_zip(cdy_rt.primitives.list_range(0, len(names)), names))
    last = _tup[0]
    pairs = _tup[1]
    _cdy__tup_205 = last
    sc = _cdy__tup_205[0]
    k = _cdy__tup_205[1]
    return (pairs, sc, k)

def core__nest(pairs: tuple[tuple[core__Expr, core__Expr], ...], body: core__Expr, pos: form__Pos) -> core__Expr:
    if (len(pairs) == 0):
        return body
    else:
        _tup = pairs[0]
        loc = _tup[0]
        init = _tup[1]
        return core__Call(core__Lambda((loc,), core__nest(prelude__rest(pairs), body, pos), pos, core__ANY), (init,), pos, core__ANY)

def core__an_fn(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) != 2):
        return cdy_rt.primitives.fail(core__located(scope, 'fn: expected (fn (args+) body), with exactly one body form'))
    else:
        _tup = core__bind_params(form__list_items(args[0]), scope, n)
        params = _tup[0]
        inner = _tup[1]
        n1 = _tup[2]
        _cdy__tup_221 = core__analyse_expr(args[1], inner, n1)
        body = _cdy__tup_221[0]
        n2 = _cdy__tup_221[1]
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
        _cdy__tup_248 = core__assoc_fields(prelude__rest(args), scope, n1, ())
        fields = _cdy__tup_248[0]
        n2 = _cdy__tup_248[1]
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
                forms, n, acc = (cdy_rt.primitives.list_drop(2, forms), n1, (acc + ((field, val),)))
                continue

def core__an_format(args: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[core__Expr, int]:
    if (len(args) != 1):
        return cdy_rt.primitives.fail(core__located(scope, 'format: expected one string literal'))
    else:
        _cdy_t49: object = args[0]
        if isinstance(_cdy_t49, form__Txt):
            text = _cdy_t49.val
            where = _cdy_t49.pos
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
                pos, acc, n, parts = ((end + 1), '', n1, (core__add_text(parts, acc) + (core__FHole(e),)))
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
        return (parts + (core__FText(text),))

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
    _cdy__tup_301 = core__match_clauses(prelude__rest(args), scope, n1, core__MatchE(subject, (), (), scope.here, core__ANY), '')
    m = _cdy__tup_301[0]
    n2 = _cdy__tup_301[1]
    sum_ = (core__match_sum(core__match_clause_list(m), scope) if (len(core__match_clause_list(m)) > 0) else '')
    return (core__global_clauses(core__check_exhaustive(m, sum_, scope), scope.names), n2)

def core__global_clauses(m: core__Expr, names: _cdy_Mapping[str, core__Entry]) -> core__Expr:
    _cdy_t50: object = m
    if isinstance(_cdy_t50, core__MatchE):
        subject = _cdy_t50.subject
        clauses = _cdy_t50.clauses
        default = _cdy_t50.default
        pos = _cdy_t50.pos
        return core__MatchE(subject, core__rename_clauses(clauses, names), default, pos, core__ANY)
    else:
        return m

def core__rename_clauses(clauses: tuple[core__Clause, ...], names: _cdy_Mapping[str, core__Entry]) -> tuple[core__Clause, ...]:
    def _cdy_t51(c: core__Clause) -> core__Clause:
        _tup = core__global_ref(c.variant, names)
        module = _tup[0]
        own = _tup[1]
        return c._replace(module=module, variant=own)
    return cdy_rt.primitives.list_map(_cdy_t51, clauses)

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
        _cdy__tup_327 = core__tup_binds(names, tmp, 0, scope, (n1 + 1), ())
        pairs = _cdy__tup_327[0]
        inner = _cdy__tup_327[1]
        n2 = _cdy__tup_327[2]
        _cdy__tup_331 = core__analyse_expr(items[1], inner, n2)
        body = _cdy__tup_331[0]
        n3 = _cdy__tup_331[1]
        return (core__nest((((tmp, subject),) + pairs), body, scope.here), n3)

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
                names, i, scope, n, acc = (prelude__rest(names), (i + 1), core__bind_local(scope, name, loc), (n + 1), (acc + ((loc, item),)))
                continue

def core__bound_in_pairs(name: str, pairs: tuple[tuple[core__Expr, core__Expr], ...]) -> bool:
    while True:
        if (len(pairs) == 0):
            return False
        else:
            _tup = pairs[0]
            loc = _tup[0]
            _ = _tup[1]
            _cdy_t52: object = loc
            if isinstance(_cdy_t52, core__Local):
                other = _cdy_t52.name
                return ((other == name) or core__bound_in_pairs(name, prelude__rest(pairs)))
            else:
                pairs = prelude__rest(pairs)
                continue

def core__match_sum(clauses: tuple[core__Clause, ...], scope: core__Scope) -> str:
    return core__variant_sum(clauses[0].variant, scope)

def core__check_exhaustive(m: core__Expr, sum_: str, scope: core__Scope) -> core__Expr:
    _cdy_t53: object = m
    if isinstance(_cdy_t53, core__MatchE):
        clauses = _cdy_t53.clauses
        default = _cdy_t53.default
        missing = core__missing_variants(core__sibling_variants(clauses[0].variant, scope), clauses)
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
        elif (core__bare_name(clauses[0].variant) == core__bare_name(name)):
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
                _cdy__tup_374 = core__pattern_binds(core__variant_fields(variant, scope), prelude__rest(pattern), scope, n, ())
                binds = _cdy__tup_374[0]
                inner = _cdy__tup_374[1]
                _cdy_n1_377 = _cdy__tup_374[2]
                _cdy__tup_378 = core__analyse_expr(items[1], inner, _cdy_n1_377)
                body = _cdy__tup_378[0]
                n2 = _cdy__tup_378[1]
                forms, n, m, sum_ = (prelude__rest(forms), n2, core__add_clause(m, core__Clause('', variant, binds, body)), core__variant_sum(variant, scope))
                continue

def core__check_pattern(variant: str, pattern: tuple[form__Form, ...], sum_: str, m: core__Expr, scope: core__Scope) -> bool:
    if (variant == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'match: pattern must be (Variant name*) or else'))
    elif (variant == 'Tup'):
        return cdy_rt.primitives.fail(core__located(scope, 'match: a (Tup name+) pattern must be the only clause, with no else'))
    elif (core__use_error(variant, scope) != ''):
        return cdy_rt.primitives.fail(core__located(scope, core__use_error(variant, scope)))
    elif (not core__is_variant(variant, scope)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: ' + variant + ' is not a variant of a sum type')))
    elif core__has_clause(variant, core__match_clause_list(m)):
        return cdy_rt.primitives.fail(core__located(scope, ('match: more than one clause for ' + variant)))
    elif ((sum_ != '') and (sum_ != core__variant_sum(variant, scope))):
        return cdy_rt.primitives.fail(core__located(scope, ('match: clauses mix variants of ' + sum_ + ' and ' + core__variant_sum(variant, scope))))
    elif ((len(pattern) - 1) != len(core__variant_fields(variant, scope))):
        return cdy_rt.primitives.fail(core__located(scope, ('match: ' + variant + ' has ' + str(len(core__variant_fields(variant, scope))) + ' field(s), so the pattern needs that many names')))
    else:
        return True

def core__match_clause_list(m: core__Expr) -> tuple[core__Clause, ...]:
    _cdy_t54: object = m
    if isinstance(_cdy_t54, core__MatchE):
        clauses = _cdy_t54.clauses
        return clauses
    else:
        return ()

def core__add_clause(m: core__Expr, clause: core__Clause) -> core__Expr:
    _cdy_t55: object = m
    if isinstance(_cdy_t55, core__MatchE):
        subject = _cdy_t55.subject
        clauses = _cdy_t55.clauses
        default = _cdy_t55.default
        pos = _cdy_t55.pos
        return core__MatchE(subject, (clauses + (clause,)), default, pos, core__ANY)
    else:
        return m

def core__set_default(m: core__Expr, e: core__Expr) -> core__Expr:
    _cdy_t56: object = m
    if isinstance(_cdy_t56, core__MatchE):
        subject = _cdy_t56.subject
        clauses = _cdy_t56.clauses
        pos = _cdy_t56.pos
        return core__MatchE(subject, clauses, (e,), pos, core__ANY)
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
                fields, names, scope, n, acc = (prelude__rest(fields), prelude__rest(names), core__bind_local(scope, name, loc), (n + 1), (acc + ((fields[0], loc),)))
                continue

def core__bound_in(name: str, binds: tuple[tuple[str, core__Expr], ...]) -> bool:
    while True:
        if (len(binds) == 0):
            return False
        else:
            _tup = binds[0]
            _ = _tup[0]
            loc = _tup[1]
            _cdy_t57: object = loc
            if isinstance(_cdy_t57, core__Local):
                other = _cdy_t57.name
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
core__FORM: str = 'form'

def core__quoted(form: form__Form) -> core__Expr:
    _cdy_t58: object = form
    if isinstance(_cdy_t58, form__Sym):
        name = _cdy_t58.name
        return core__Call(core__Global(core__FORM, 'Sym', form__NOWHERE, core__ANY), (core__Lit(form__Txt(name, form__NOWHERE), core__ANY), core__Global(core__FORM, 'NOWHERE', form__NOWHERE, core__ANY)), form__NOWHERE, core__ANY)
    elif isinstance(_cdy_t58, form__Lst):
        items = _cdy_t58.items
        return core__Call(core__Global(core__FORM, 'Lst', form__NOWHERE, core__ANY), (core__form_list(cdy_rt.primitives.list_map(core__quoted, items)), core__Global(core__FORM, 'NOWHERE', form__NOWHERE, core__ANY)), form__NOWHERE, core__ANY)
    else:
        return core__Call(core__Global(core__FORM, core__literal_variant(form), form__NOWHERE, core__ANY), (core__Lit(core__field_literal(form), core__ANY), core__Global(core__FORM, 'NOWHERE', form__NOWHERE, core__ANY)), form__NOWHERE, core__ANY)

def core__field_literal(form: form__Form) -> form__Form:
    _cdy_t59: object = form
    if isinstance(_cdy_t59, form__LongLit):
        n = _cdy_t59.val
        pos = _cdy_t59.pos
        return form__IntLit(n, pos)
    elif isinstance(_cdy_t59, form__ByteLit):
        _cdy_n_428 = _cdy_t59.val
        _cdy_pos_429 = _cdy_t59.pos
        return form__IntLit(_cdy_n_428, _cdy_pos_429)
    elif isinstance(_cdy_t59, form__FloatLit):
        x = _cdy_t59.val
        _cdy_pos_431 = _cdy_t59.pos
        return form__DoubleLit(x, _cdy_pos_431)
    else:
        return form

def core__form_list(items: tuple[core__Expr, ...]) -> core__Expr:
    if (len(items) == 0):
        return core__Prim('empty-list', form__NOWHERE, core__ANY)
    else:
        return core__ListOf(items, form__NOWHERE, core__ANY)

def core__literal_variant(form: form__Form) -> str:
    _cdy_t60: object = form
    if isinstance(_cdy_t60, form__Txt):
        return 'Txt'
    elif isinstance(_cdy_t60, form__IntLit):
        return 'IntLit'
    elif isinstance(_cdy_t60, form__LongLit):
        return 'LongLit'
    elif isinstance(_cdy_t60, form__ByteLit):
        return 'ByteLit'
    elif isinstance(_cdy_t60, form__FloatLit):
        return 'FloatLit'
    elif isinstance(_cdy_t60, form__DoubleLit):
        return 'DoubleLit'
    elif isinstance(_cdy_t60, form__CharLit):
        return 'CharLit'
    elif isinstance(_cdy_t60, form__BoolLit):
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
        return (core__quoted(core__hygienic(form, scope)), n)

def core__hygienic(form: form__Form, scope: core__Scope) -> form__Form:
    _cdy_t61: object = form
    if isinstance(_cdy_t61, form__Sym):
        name = _cdy_t61.name
        pos = _cdy_t61.pos
        names = scope.names
        if core__names_own(name, names):
            if core__is_prelude_value(cdy_rt.primitives.map_get(names, name)):
                return form__Sym(('prelude.' + name), pos)
            else:
                return form
        elif (core__is_everyones(name, scope.builtins) and (not cdy_rt.primitives.map_has(scope.macros, name))):
            return form__Sym(('system.' + name), pos)
        else:
            return form
    else:
        return form

def core__names_own(name: str, names: _cdy_Mapping[str, core__Entry]) -> bool:
    _cdy_t64 = cdy_rt.primitives.map_has(names, name)
    if _cdy_t64:
        _cdy_t63: object = cdy_rt.primitives.map_get(names, name)
        if isinstance(_cdy_t63, core__Unlisted):
            _cdy_t62 = False
        elif isinstance(_cdy_t63, core__Elsewhere):
            _cdy_t62 = False
        else:
            _cdy_t62 = True
        _cdy_t64 = _cdy_t62
    return _cdy_t64

def core__is_prelude_value(e: core__Entry) -> bool:
    _cdy_t65: object = e
    if isinstance(_cdy_t65, core__Value):
        m = _cdy_t65.module
        return (m == core__PRELUDE)
    else:
        return False
core__PRELUDE: str = 'prelude'

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
    here = scope.here
    return (core__Call(core__Global(core__FORM, 'Lst', form__NOWHERE, core__ANY), (core__join_parts(parts, here), core__Global(core__FORM, 'NOWHERE', form__NOWHERE, core__ANY)), here, core__ANY), n1)

def core__quasi_parts(items: tuple[form__Form, ...], scope: core__Scope, n: int, run: tuple[core__Expr, ...], parts: tuple[core__Expr, ...]) -> tuple[tuple[core__Expr, ...], int]:
    while True:
        if (len(items) == 0):
            return (core__close_run(run, parts, scope.here), n)
        else:
            item = items[0]
            if (core__head_name(item) == 'unq-sp'):
                _tup = core__unq_arg(item, core__at_pos(scope, form__form_pos(item)), n)
                e = _tup[0]
                n1 = _tup[1]
                items, n, run, parts = (prelude__rest(items), n1, (), (core__close_run(run, parts, scope.here) + (e,)))
                continue
            else:
                _cdy__tup_469 = core__quasi_form(item, scope, n)
                _cdy_e_470 = _cdy__tup_469[0]
                _cdy_n1_471 = _cdy__tup_469[1]
                items, n, run = (prelude__rest(items), _cdy_n1_471, (run + (_cdy_e_470,)))
                continue

def core__close_run(run: tuple[core__Expr, ...], parts: tuple[core__Expr, ...], pos: form__Pos) -> tuple[core__Expr, ...]:
    if (len(run) == 0):
        return parts
    else:
        return (parts + (core__ListOf(run, pos, core__ANY),))

def core__join_parts(parts: tuple[core__Expr, ...], pos: form__Pos) -> core__Expr:
    if (len(parts) == 0):
        return core__Prim('empty-list', pos, core__ANY)
    elif (len(parts) == 1):
        return parts[0]
    else:
        return core__Call(core__Prim('++', pos, core__ANY), parts, pos, core__ANY)

def core__is_lower(name: str) -> bool:
    return ((len(name) > 0) and (cdy_rt.primitives.substring(name, 0, 1) >= 'a') and (cdy_rt.primitives.substring(name, 0, 1) <= 'z'))

def core__analyse_type(form: form__Form) -> core__CType:
    _cdy_t66: object = form
    if isinstance(_cdy_t66, form__Sym):
        name = _cdy_t66.name
        if (core__is_lower(name) and (not core__has_dot(name))):
            return core__TVar(name)
        else:
            return core__TCon(core__SYSTEM, name, ())
    elif isinstance(_cdy_t66, form__Lst):
        items = _cdy_t66.items
        if (len(items) == 0):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad type ()'))
        elif (form__sym_name(items[0]) == 'Fn'):
            if (len(items) == 3):
                return core__TFn(cdy_rt.primitives.list_map(core__analyse_type, form__list_items(items[1])), core__analyse_type(items[2]))
            else:
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad function type: expected (Fn (Arg+) Ret)'))
        elif (form__sym_name(items[0]) == 'Rest'):
            if (len(items) == 2):
                return core__TCon(core__SYSTEM, 'Rest', (core__analyse_type(items[1]),))
            else:
                return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad rest type: expected (Rest Type)'))
        else:
            return core__TCon(core__SYSTEM, form__sym_name(items[0]), cdy_rt.primitives.list_map(core__analyse_type, prelude__rest(items)))
    else:
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'bad type'))
core__CONSTRAINTS: _cdy_Mapping[str, tuple[str, ...]] = cdy_rt.primitives.map_from((('number', ('Int', 'Long', 'Byte', 'Float', 'Double')), ('integer', ('Int', 'Long', 'Byte')), ('float', ('Float', 'Double')), ('comparable', ('Int', 'Long', 'Byte', 'Float', 'Double', 'String', 'Char')), ('appendable', ('String', 'List')), ('equatable', ())))

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
cdy_rt.primitives.register_type(core__Prog, 'Prog', (), (('List', 'core.Top'), ('Map', 'String', 'core.CType'), 'Int', ('Map', 'String', 'Bool'), ('Map', 'String', 'Bool')))

def core__top_names(forms: tuple[form__Form, ...]) -> _cdy_Mapping[str, bool]:
    def _cdy_t67(acc: _cdy_Mapping[str, bool], form: form__Form) -> _cdy_Mapping[str, bool]:
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
    return cdy_rt.primitives.list_fold(_cdy_t67, {}, forms)

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

def core__field_names(fields: tuple[form__Form, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda field: form__sym_name(core__first_item(field))), fields)

def core__deft_name(form: form__Form) -> str:
    _cdy_t68: object = form
    if isinstance(_cdy_t68, form__Lst):
        items = _cdy_t68.items
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
    module: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Typed, 'Typed', (), ('core.CType', 'String'))

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

def core__is_everyones(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t71 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t71:
        _cdy_t70: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t70, core__Typed):
            m = _cdy_t70.module
            _cdy_t69 = (m == 'system')
        else:
            _cdy_t69 = False
        _cdy_t71 = _cdy_t69
    return _cdy_t71

def core__declaring_module(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> str:
    def _cdy_t73(_cdy_key_513: str) -> str:
        _cdy_t72: object = cdy_rt.primitives.map_get(builtins, _cdy_key_513)
        if isinstance(_cdy_t72, core__Typed):
            m = _cdy_t72.module
            return m
        else:
            return core__SYSTEM
    owner = _cdy_t73
    found = prelude__find((lambda _cdy_key_516: ((owner(_cdy_key_516) != core__SYSTEM) and (_cdy_key_516 == core__global_key(owner(_cdy_key_516), name)))), cdy_rt.primitives.map_keys(builtins))
    _cdy_t74 = found
    if isinstance(_cdy_t74, prelude__Some):
        key: str = _cdy_t74.v
        return owner(key)
    elif isinstance(_cdy_t74, prelude__None):
        return ''

def core__is_builtin_type(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t77 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t77:
        _cdy_t76: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t76, core__BType):
            _cdy_t75 = True
        else:
            _cdy_t75 = False
        _cdy_t77 = _cdy_t75
    return _cdy_t77

def core__is_special(name: str, builtins: _cdy_Mapping[str, core__Builtin]) -> bool:
    _cdy_t80 = cdy_rt.primitives.map_has(builtins, name)
    if _cdy_t80:
        _cdy_t79: object = cdy_rt.primitives.map_get(builtins, name)
        if isinstance(_cdy_t79, core__Special):
            _cdy_t78 = True
        else:
            _cdy_t78 = False
        _cdy_t80 = _cdy_t78
    return _cdy_t80

def core__read_builtins(decls: tuple[form__Form, ...], files: tuple[tuple[str, tuple[form__Form, ...]], ...], spellings: _cdy_Mapping[str, tuple[str, str, str]]) -> _cdy_Mapping[str, core__Builtin]:
    def _cdy_t81(acc: _cdy_Mapping[str, core__Builtin], file: tuple[str, tuple[form__Form, ...]]) -> _cdy_Mapping[str, core__Builtin]:
        _tup = file
        name = _tup[0]
        forms = _tup[1]
        return core__read_sigs(name, forms, spellings, acc)
    builtins = cdy_rt.primitives.list_fold(_cdy_t81, core__read_decls(decls, spellings), files)
    _cdy_t83 = cdy_rt.primitives.map_keys(spellings)
    def _cdy_t82(f: tuple[str, tuple[form__Form, ...]]) -> str:
        _tup = f
        name = _tup[0]
        _ = _tup[1]
        return name
    checked = core__all_declared(_cdy_t83, builtins, cdy_rt.primitives.list_map(_cdy_t82, files))
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
    def _cdy_t84(acc: _cdy_Mapping[str, core__Builtin], form: form__Form) -> _cdy_Mapping[str, core__Builtin]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 0) else '')
        name = (form__sym_name(items[1]) if (len(items) > 1) else '')
        where = form__pos_text(form__form_pos(form))
        decl = (('', core__Special()) if (name == '') else (('special', core__Special()) if ((head == 'special') and (len(items) == 2)) else (('special', core__Special()) if ((head == 'special') and (len(items) == 3) and core__shape_read(items[2], where)) else ('', core__Special()))))
        _tup = decl
        class_ = _tup[0]
        kind = _tup[1]
        if (class_ == ''):
            return cdy_rt.primitives.fail((where + 'special.cdy: expected (special name) or (special name shape)'))
        elif cdy_rt.primitives.map_has(acc, name):
            return cdy_rt.primitives.fail((where + 'special.cdy: ' + name + ' is declared more than once'))
        elif (not cdy_rt.primitives.list_contains(core__spelling_kind(spellings, name), core__kinds_of(class_))):
            return cdy_rt.primitives.fail(((where + 'special.cdy: ' + name + " is a special form, so spelling.py can't spell it") if (class_ == 'special') else (where + 'special.cdy: ' + name + ' has no ' + class_ + ' entry in spelling.py')))
        else:
            return cdy_rt.primitives.map_set(acc, name, kind)
    return cdy_rt.primitives.list_fold(_cdy_t84, {}, forms)

def core__shape_read(form: form__Form, where: str) -> bool:
    return (len(syntax__read_shape(form, where)) >= 0)

def core__kinds_of(class_: str) -> tuple[str, ...]:
    if (class_ == 'special'):
        return core__SPECIAL_KINDS
    else:
        return core__TYPED_KINDS

def core__read_sigs(file: str, all_: tuple[form__Form, ...], spellings: _cdy_Mapping[str, tuple[str, str, str]], start: _cdy_Mapping[str, core__Builtin]) -> _cdy_Mapping[str, core__Builtin]:
    def _cdy_t85(acc: _cdy_Mapping[str, core__Builtin], form: form__Form) -> _cdy_Mapping[str, core__Builtin]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 0) else '')
        name = (form__sym_name(items[1]) if ((len(items) == 3) and (head == 'sig')) else '')
        key = core__builtin_key(cdy_rt.primitives.path_stem(file), name)
        where = (form__pos_text(form__form_pos(form)) + file)
        if ((head == 'deft') and (file == 'system.cdy')):
            return core__read_type(form, items, where, spellings, acc)
        elif (head == 'deft'):
            return cdy_rt.primitives.fail((where + ': only system.cdy declares types'))
        elif ((name == '') and (file == 'system.cdy')):
            return cdy_rt.primitives.fail((where + ': expected (sig name Type) or (deft Name)'))
        elif (name == ''):
            return cdy_rt.primitives.fail((where + ': expected (sig name Type)'))
        elif cdy_rt.primitives.map_has(acc, key):
            return cdy_rt.primitives.fail((where + ': ' + name + ' is already declared'))
        elif (not cdy_rt.primitives.list_contains(core__spelling_kind(spellings, key), (core__TYPED_KINDS + core__OPERATOR_KINDS))):
            return cdy_rt.primitives.fail((where + ': ' + key + ' has no Python mapping in spelling.py'))
        else:
            return cdy_rt.primitives.map_set(acc, key, core__Typed(core__analyse_type(items[2]), cdy_rt.primitives.path_stem(file)))
    return cdy_rt.primitives.list_fold(_cdy_t85, start, (all_ if (file == 'system.cdy') else core__declarations(all_)))

def core__declarations(forms: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    defined = core__def_names(forms)
    return cdy_rt.primitives.list_filter((lambda form: core__is_declaration_form(form, defined)), forms)

def core__definitions(forms: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    defined = core__def_names(forms)
    return cdy_rt.primitives.list_filter((lambda form: (not core__is_declaration_form(form, defined))), forms)

def core__is_declaration_form(form: form__Form, defined: _cdy_Mapping[str, bool]) -> bool:
    items = form__list_items(form)
    head = (form__sym_name(items[0]) if (len(items) > 0) else '')
    if (head == 'sig'):
        return (not ((len(items) == 3) and cdy_rt.primitives.map_has(defined, form__sym_name(items[1]))))
    elif (head == 'deft'):
        return (len(items) == 2)
    else:
        return False

def core__read_type(form: form__Form, items: tuple[form__Form, ...], where: str, spellings: _cdy_Mapping[str, tuple[str, str, str]], acc: _cdy_Mapping[str, core__Builtin]) -> _cdy_Mapping[str, core__Builtin]:
    header = (items[1] if (len(items) == 2) else form)
    _cdy_t87: object = header
    if isinstance(_cdy_t87, form__Lst):
        xs = _cdy_t87.items
        _cdy_t86 = xs
    elif isinstance(_cdy_t87, form__Sym):
        _cdy_t86 = (header,)
    else:
        _cdy_t86 = ()
    parts = _cdy_t86
    name = (form__sym_name(parts[0]) if (len(parts) > 0) else '')
    tvars = (prelude__rest(parts) if (len(parts) > 0) else ())
    if ((name == '') or core__is_lower(name) or (not core__all_lower(tvars))):
        return cdy_rt.primitives.fail((where + ': expected (deft Name) or (deft (Name a ...))'))
    elif cdy_rt.primitives.map_has(acc, name):
        return cdy_rt.primitives.fail((where + ': ' + name + ' is already declared'))
    elif (not cdy_rt.primitives.list_contains(core__spelling_kind(spellings, name), core__TYPE_KINDS)):
        return cdy_rt.primitives.fail((where + ': ' + name + ' has no Python type in spelling.py'))
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

def core__all_declared(names: tuple[str, ...], builtins: _cdy_Mapping[str, core__Builtin], files: tuple[str, ...]) -> bool:
    while True:
        if (len(names) == 0):
            return True
        elif (not cdy_rt.primitives.map_has(builtins, names[0])):
            return cdy_rt.primitives.fail(('spelling.py: ' + names[0] + ' is declared in none of special.cdy, ' + cdy_rt.primitives.join(files, ', ')))
        else:
            names = prelude__rest(names)
            continue

class core__Exports(_cdy_NamedTuple):
    stem: str
    names: _cdy_Mapping[str, core__Entry]
    privates: _cdy_Mapping[str, bool]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Exports, 'Exports', (), ('String', ('Map', 'String', 'core.Entry'), ('Map', 'String', 'Bool')))

def core__module_exports(forms: tuple[form__Form, ...], stem: str) -> core__Exports:
    names = core__module_names(forms, stem)
    return core__Exports(stem, names, core__private_names(forms, names, {}))

def core__declared_exports(forms: tuple[form__Form, ...], stem: str) -> core__Exports:
    return core__Exports(stem, core__declared_names(core__declarations(forms), stem, {}), {})

def core__with_declared(own: core__Exports, forms: tuple[form__Form, ...], stem: str) -> core__Exports:
    return own._replace(names=core__declared_names(core__declarations(forms), stem, own.names))

def core__declared_names(forms: tuple[form__Form, ...], stem: str, start: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    def _cdy_t88(acc: _cdy_Mapping[str, core__Entry], form: form__Form) -> _cdy_Mapping[str, core__Entry]:
        name = form__sym_name(form__list_items(form)[1])
        return cdy_rt.primitives.map_set(acc, name, core__Declared(stem, name))
    return cdy_rt.primitives.list_fold(_cdy_t88, start, forms)

def core__private_names(forms: tuple[form__Form, ...], names: _cdy_Mapping[str, core__Entry], start: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    def _cdy_t89(acc: _cdy_Mapping[str, bool], form: form__Form) -> _cdy_Mapping[str, bool]:
        items = form__list_items(form)
        if ((len(items) > 0) and (form__sym_name(items[0]) == 'private')):
            return cdy_rt.primitives.list_fold((lambda acc1, item: core__add_private(item, names, acc1)), acc, prelude__rest(items))
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t89, start, forms)

def core__add_private(item: form__Form, names: _cdy_Mapping[str, core__Entry], acc: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    name = form__sym_name(item)
    where = form__pos_text(form__form_pos(item))
    if (name == ''):
        return cdy_rt.primitives.fail((where + 'private: expected (private name ...)'))
    elif (not cdy_rt.primitives.map_has(names, name)):
        return cdy_rt.primitives.fail((where + 'private: ' + name + " isn't defined in this file"))
    elif cdy_rt.primitives.map_has(acc, name):
        return cdy_rt.primitives.fail((where + 'private: ' + name + ' is listed twice'))
    else:
        _cdy_t90: object = cdy_rt.primitives.map_get(names, name)
        if isinstance(_cdy_t90, core__VariantOf):
            sum_ = _cdy_t90.sum_
            return cdy_rt.primitives.fail((where + 'private: ' + name + ' is a variant, private only with its type: (private ' + sum_ + ')'))
        elif isinstance(_cdy_t90, core__Sum):
            variants = _cdy_t90.variants
            return cdy_rt.primitives.list_fold((lambda a, v: cdy_rt.primitives.map_set(a, v, True)), cdy_rt.primitives.map_set(acc, name, True), variants)
        else:
            return cdy_rt.primitives.map_set(acc, name, True)

def core__module_names(forms: tuple[form__Form, ...], stem: str) -> _cdy_Mapping[str, core__Entry]:
    def _cdy_t91(acc: _cdy_Mapping[str, core__Entry], form: form__Form) -> _cdy_Mapping[str, core__Entry]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 1) else '')
        if ((head == 'def') or (head == 'defn')):
            name = form__sym_name(items[1])
            return core__add_entry(name, form__form_pos(items[1]), core__Value(stem, name), acc)
        elif (head == 'deft'):
            return core__add_deft(items, stem, acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t91, {}, forms)

def core__add_deft(items: tuple[form__Form, ...], stem: str, acc: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    name = core__deft_name(items[1])
    pos = form__form_pos(items[1])
    _cdy_t93: object = items[1]
    if isinstance(_cdy_t93, form__Lst):
        xs = _cdy_t93.items
        _cdy_t92 = (len(xs) - 1)
    else:
        _cdy_t92 = 0
    arity = _cdy_t92
    body = cdy_rt.primitives.list_drop(2, items)
    if core__is_sum_body(body):
        def _cdy_t94(acc1: _cdy_Mapping[str, core__Entry], v: form__Form) -> _cdy_Mapping[str, core__Entry]:
            v_items = form__list_items(v)
            vname = form__sym_name(v_items[0])
            fields = (core__field_names(form__list_items(v_items[1])) if (len(v_items) == 2) else ())
            return core__add_entry(vname, pos, core__VariantOf(stem, vname, name, fields, core__variant_names(body)), acc1)
        return cdy_rt.primitives.list_fold(_cdy_t94, core__add_entry(name, pos, core__Sum(stem, name, arity, core__variant_names(body)), acc), body)
    else:
        return core__add_entry(name, pos, core__Record(stem, name, arity), acc)

def core__add_entry(name: str, pos: form__Pos, e: core__Entry, acc: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    if (core__name_error(name) != ''):
        return cdy_rt.primitives.fail((form__pos_text(pos) + core__name_error(name)))
    elif cdy_rt.primitives.map_has(acc, name):
        return cdy_rt.primitives.fail((form__pos_text(pos) + ('defined more than once: ' + name)))
    else:
        return cdy_rt.primitives.map_set(acc, name, e)

def core__analyse_program(forms: tuple[form__Form, ...], imports: tuple[core__Import, ...], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    return core__analyse_module(forms, core__module_exports(forms, ''), imports, {}, builtins, parse, macros, quoting)

class core__Import(_cdy_NamedTuple):
    exports: core__Exports
    pos: form__Pos
    only: prelude__Maybe[tuple[form__Form, ...]]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(core__Import, 'Import', (), ('core.Exports', 'form.Pos', ('prelude.Maybe', ('List', 'form.Form'))))

def core__analyse_module(forms: tuple[form__Form, ...], own: core__Exports, imports: tuple[core__Import, ...], elsewhere: _cdy_Mapping[str, str], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], macros: _cdy_Mapping[str, form__Macro], quoting: bool) -> tuple[core__Top, ...]:
    names = core__with_own(core__with_imports(imports, core__with_system(builtins, core__elsewhere_entries(elsewhere))), own)
    qualifiers = core__qualifiers_of(imports, cdy_rt.primitives.map_set({}, core__SYSTEM, True))
    scope = core__Scope({}, parse, form__NOWHERE, macros, quoting, names, qualifiers, builtins)
    prog = core__analyse_tops(forms, scope, core__Prog((), {}, 0, core__def_names(forms), {}))
    return core__rename_tops(prog.out, names)

def core__qualifiers_of(imports: tuple[core__Import, ...], start: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    return cdy_rt.primitives.list_fold((lambda acc, imp: cdy_rt.primitives.map_set(acc, imp.exports.stem, True)), start, imports)

def core__with_system(builtins: _cdy_Mapping[str, core__Builtin], names: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    def _cdy_t95(acc: _cdy_Mapping[str, core__Entry], name: str) -> _cdy_Mapping[str, core__Entry]:
        if (core__is_everyones(name, builtins) or core__is_builtin_type(name, builtins)):
            return cdy_rt.primitives.map_set(acc, (core__SYSTEM + ('.' + name)), core__Declared(core__SYSTEM, name))
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t95, names, cdy_rt.primitives.map_keys(builtins))

def core__elsewhere_entries(elsewhere: _cdy_Mapping[str, str]) -> _cdy_Mapping[str, core__Entry]:
    return cdy_rt.primitives.list_fold((lambda acc, name: cdy_rt.primitives.map_set(acc, name, core__Elsewhere(cdy_rt.primitives.map_get(elsewhere, name)))), {}, cdy_rt.primitives.map_keys(elsewhere))

def core__with_imports(imports: tuple[core__Import, ...], names: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    return cdy_rt.primitives.list_fold((lambda acc, imp: core__import_names(imp, acc)), names, imports)

def core__import_names(imp: core__Import, start: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    ex = imp.exports
    stem = ex.stem
    listed = core__listed_names(imp)
    qualified = cdy_rt.primitives.list_fold((lambda acc, name: cdy_rt.primitives.map_set(acc, (stem + ('.' + name)), (core__Private(stem) if cdy_rt.primitives.map_has(ex.privates, name) else cdy_rt.primitives.map_get(ex.names, name)))), start, cdy_rt.primitives.map_keys(ex.names))
    def _cdy_t96(acc: _cdy_Mapping[str, core__Entry], name: str) -> _cdy_Mapping[str, core__Entry]:
        if cdy_rt.primitives.map_has(ex.privates, name):
            return core__hidden_entry(name, core__Private(stem), acc)
        elif cdy_rt.primitives.list_contains(name, listed):
            return core__import_entry(name, cdy_rt.primitives.map_get(ex.names, name), stem, acc)
        else:
            return core__hidden_entry(name, core__Unlisted(stem), acc)
    return cdy_rt.primitives.list_fold(_cdy_t96, qualified, cdy_rt.primitives.map_keys(ex.names))

def core__listed_names(imp: core__Import) -> tuple[str, ...]:
    ex = imp.exports
    _cdy_t97 = imp.only
    if isinstance(_cdy_t97, prelude__Some):
        forms: tuple[form__Form, ...] = _cdy_t97.v
        def _cdy_t98(acc: tuple[str, ...], form: form__Form) -> tuple[str, ...]:
            name = form__sym_name(form)
            where = form__pos_text(form__form_pos(form))
            if (not cdy_rt.primitives.map_has(ex.names, name)):
                return cdy_rt.primitives.fail((where + 'import: ' + ex.stem + " doesn't define " + name))
            elif cdy_rt.primitives.map_has(ex.privates, name):
                return cdy_rt.primitives.fail((where + 'import: ' + name + ' is private to ' + ex.stem))
            elif cdy_rt.primitives.list_contains(name, acc):
                return cdy_rt.primitives.fail((where + 'import: ' + name + ' is listed twice'))
            else:
                return (acc + (name,))
        return cdy_rt.primitives.list_fold(_cdy_t98, (), forms)
    elif isinstance(_cdy_t97, prelude__None):
        return cdy_rt.primitives.list_filter((lambda name: (not cdy_rt.primitives.map_has(ex.privates, name))), cdy_rt.primitives.map_keys(ex.names))

def core__hidden_entry(name: str, e: core__Entry, acc: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    if cdy_rt.primitives.map_has(acc, name):
        _cdy_t99: object = cdy_rt.primitives.map_get(acc, name)
        if isinstance(_cdy_t99, core__Elsewhere):
            return cdy_rt.primitives.map_set(acc, name, e)
        else:
            return acc
    else:
        return cdy_rt.primitives.map_set(acc, name, e)

def core__import_entry(name: str, e: core__Entry, stem: str, acc: _cdy_Mapping[str, core__Entry]) -> _cdy_Mapping[str, core__Entry]:
    if cdy_rt.primitives.map_has(acc, name):
        old = cdy_rt.primitives.map_get(acc, name)
        _cdy_t100: object = old
        if isinstance(_cdy_t100, core__Elsewhere):
            return cdy_rt.primitives.map_set(acc, name, e)
        elif isinstance(_cdy_t100, core__Unlisted):
            return cdy_rt.primitives.map_set(acc, name, e)
        elif isinstance(_cdy_t100, core__Private):
            return cdy_rt.primitives.map_set(acc, name, e)
        elif isinstance(_cdy_t100, core__Clash):
            modules = _cdy_t100.modules
            return cdy_rt.primitives.map_set(acc, name, (old if cdy_rt.primitives.list_contains(stem, modules) else core__Clash((modules + (stem,)))))
        else:
            return cdy_rt.primitives.map_set(acc, name, (e if (core__entry_module(old) == stem) else core__Clash((core__entry_module(old), stem))))
    else:
        return cdy_rt.primitives.map_set(acc, name, e)

def core__with_own(names: _cdy_Mapping[str, core__Entry], own: core__Exports) -> _cdy_Mapping[str, core__Entry]:
    return core__put_all(own.names, cdy_rt.primitives.map_keys(own.names), names)

def core__put_all[a](m: _cdy_Mapping[str, a], keys: tuple[str, ...], start: _cdy_Mapping[str, a]) -> _cdy_Mapping[str, a]:
    return cdy_rt.primitives.list_fold((lambda acc, key: cdy_rt.primitives.map_set(acc, key, cdy_rt.primitives.map_get(m, key))), start, keys)

def core__elsewhere_names(exports: tuple[core__Exports, ...]) -> _cdy_Mapping[str, str]:
    def _cdy_t101(acc: _cdy_Mapping[str, str], ex: core__Exports) -> _cdy_Mapping[str, str]:
        public = cdy_rt.primitives.list_filter((lambda name: (not cdy_rt.primitives.map_has(ex.privates, name))), cdy_rt.primitives.map_keys(ex.names))
        return core__put_all(core__stems_for(public, ex.stem), public, acc)
    return cdy_rt.primitives.list_fold(_cdy_t101, {}, exports)

def core__stems_for(names: tuple[str, ...], stem: str) -> _cdy_Mapping[str, str]:
    return cdy_rt.primitives.list_fold((lambda acc, name: cdy_rt.primitives.map_set(acc, name, stem)), {}, names)

def core__rename_tops(tops: tuple[core__Top, ...], names: _cdy_Mapping[str, core__Entry]) -> tuple[core__Top, ...]:
    return cdy_rt.primitives.list_map((lambda top: core__rename_top(top, names)), tops)

def core__rename_top(top: core__Top, names: _cdy_Mapping[str, core__Entry]) -> core__Top:
    _cdy_t102: object = top
    if isinstance(_cdy_t102, core__TDeft):
        name = _cdy_t102.name
        tvars = _cdy_t102.tvars
        fields = _cdy_t102.fields
        return core__TDeft(core__top_module(name, names), name, tvars, core__rename_fields(fields, names))
    elif isinstance(_cdy_t102, core__TDeftSum):
        _cdy_name_744 = _cdy_t102.name
        _cdy_tvars_745 = _cdy_t102.tvars
        variants = _cdy_t102.variants
        return core__TDeftSum(core__top_module(_cdy_name_744, names), _cdy_name_744, _cdy_tvars_745, core__rename_variants(variants, names))
    elif isinstance(_cdy_t102, core__TDef):
        _cdy_name_747 = _cdy_t102.name
        init = _cdy_t102.init
        t = _cdy_t102.t
        pos = _cdy_t102.pos
        return core__TDef(core__top_module(_cdy_name_747, names), _cdy_name_747, init, core__rename_type(t, names), pos)
    elif isinstance(_cdy_t102, core__TDefn):
        _cdy_name_751 = _cdy_t102.name
        params = _cdy_t102.params
        body = _cdy_t102.body
        _cdy_t_754 = _cdy_t102.t
        _cdy_pos_755 = _cdy_t102.pos
        return core__TDefn(core__top_module(_cdy_name_751, names), _cdy_name_751, params, body, core__rename_type(_cdy_t_754, names), _cdy_pos_755)
    else:
        assert isinstance(_cdy_t102, core__TExpr)
        return top

def core__rename_variants(variants: tuple[core__Variant, ...], names: _cdy_Mapping[str, core__Entry]) -> tuple[core__Variant, ...]:
    return cdy_rt.primitives.list_map((lambda v: core__Variant(v.name, core__rename_fields(v.fields, names))), variants)

def core__top_module(name: str, names: _cdy_Mapping[str, core__Entry]) -> str:
    _tup = core__global_ref(name, names)
    module = _tup[0]
    _own = _tup[1]
    return module

def core__rename_fields(fields: tuple[tuple[str, core__CType], ...], names: _cdy_Mapping[str, core__Entry]) -> tuple[tuple[str, core__CType], ...]:
    def _cdy_t103(field: tuple[str, core__CType]) -> tuple[str, core__CType]:
        _tup = field
        name = _tup[0]
        t = _tup[1]
        return (name, core__rename_type(t, names))
    return cdy_rt.primitives.list_map(_cdy_t103, fields)

def core__rename_type(t: core__CType, names: _cdy_Mapping[str, core__Entry]) -> core__CType:
    _cdy_t104: object = t
    if isinstance(_cdy_t104, core__TCon):
        name = _cdy_t104.name
        args = _cdy_t104.args
        _tup = core__global_ref(name, names)
        module = _tup[0]
        own = _tup[1]
        return core__TCon(module, own, core__rename_types(args, names))
    elif isinstance(_cdy_t104, core__TVar):
        return t
    else:
        assert isinstance(_cdy_t104, core__TFn)
        params = _cdy_t104.params
        ret = _cdy_t104.ret
        return core__TFn(core__rename_types(params, names), core__rename_type(ret, names))

def core__rename_types(types: tuple[core__CType, ...], names: _cdy_Mapping[str, core__Entry]) -> tuple[core__CType, ...]:
    return cdy_rt.primitives.list_map((lambda t: core__rename_type(t, names)), types)

def core__def_names(forms: tuple[form__Form, ...]) -> _cdy_Mapping[str, bool]:
    def _cdy_t105(acc: _cdy_Mapping[str, bool], form: form__Form) -> _cdy_Mapping[str, bool]:
        items = form__list_items(form)
        head = (form__sym_name(items[0]) if (len(items) > 1) else '')
        if ((head == 'def') or (head == 'defn')):
            return cdy_rt.primitives.map_set(acc, form__sym_name(items[1]), True)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t105, {}, forms)

def core__analyse_tops(forms: tuple[form__Form, ...], scope: core__Scope, prog: core__Prog) -> core__Prog:
    while True:
        if (len(forms) == 0):
            return prog
        else:
            forms, prog = (prelude__rest(forms), core__analyse_top(forms[0], scope, prog))
            continue

def core__add_top(prog: core__Prog, top: core__Top, n: int) -> core__Prog:
    return prog._replace(out=(prog.out + (top,)), n=n)

def core__mark_defined(prog: core__Prog, name: str) -> core__Prog:
    return prog._replace(defined=cdy_rt.primitives.map_set(prog.defined, name, True))

def core__analyse_top(form: form__Form, scope: core__Scope, prog: core__Prog) -> core__Prog:
    items = form__list_items(form)
    head = (form__sym_name(items[0]) if (len(items) > 0) else '')
    here = core__at_pos(scope, form__form_pos(form))
    if (cdy_rt.primitives.list_contains(head, ('def', 'defn')) and (len(items) > 1) and cdy_rt.primitives.map_has(scope.macros, form__sym_name(items[1]))):
        return cdy_rt.primitives.fail(core__located(here, (form__sym_name(items[1]) + " is a macro, so it can't be defined")))
    elif ((head == 'deft') and (len(items) > 1) and (core__macro_named(core__deft_names(items), scope) != '')):
        return cdy_rt.primitives.fail(core__located(here, (core__macro_named(core__deft_names(items), scope) + " is a macro, so it can't be defined")))
    elif (head == 'sig'):
        return core__top_sig(items, here, prog)
    elif (head == 'def'):
        return core__top_def(items, here, prog)
    elif (head == 'defn'):
        return core__top_defn(items, here, prog)
    elif (head == 'deft'):
        return core__top_deft(items, here, prog)
    elif (head == 'private'):
        return prog
    else:
        _tup = core__analyse_expr(form, here, prog.n)
        e = _tup[0]
        n = _tup[1]
        return core__add_top(prog, core__TExpr(e), n)

def core__deft_names(items: tuple[form__Form, ...]) -> tuple[str, ...]:
    body = cdy_rt.primitives.list_drop(2, items)
    return ((core__deft_name(items[1]),) + (core__variant_names(body) if core__is_sum_body(body) else ()))

def core__macro_named(names: tuple[str, ...], scope: core__Scope) -> str:
    found = cdy_rt.primitives.list_filter((lambda name: cdy_rt.primitives.map_has(scope.macros, name)), names)
    if (len(found) == 0):
        return ''
    else:
        return found[0]

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
        _cdy_t106: object = t
        if isinstance(_cdy_t106, core__TFn):
            params = _cdy_t106.params
            ret = _cdy_t106.ret
            last = cdy_rt.primitives.at(params, (len(params) - 1))
            return (core__check_types(cdy_rt.primitives.slice_(params, 0, (len(params) - 1)), scope) and core__check_types(core__rest_item(last), scope) and core__check_type(ret, scope))
        else:
            return core__check_type(t, scope)
    else:
        return core__check_type(t, scope)

def core__check_type(t: core__CType, scope: core__Scope) -> bool:
    _cdy_t107: object = t
    if isinstance(_cdy_t107, core__TVar):
        return True
    elif isinstance(_cdy_t107, core__TFn):
        params = _cdy_t107.params
        ret = _cdy_t107.ret
        return (core__check_types(params, scope) and core__check_type(ret, scope))
    else:
        assert isinstance(_cdy_t107, core__TCon)
        name = _cdy_t107.name
        args = _cdy_t107.args
        builtins = scope.builtins
        if (name == 'Tup'):
            _cdy_t112 = len(args)
        elif (core__use_error(name, scope) != ''):
            _cdy_t112 = cdy_rt.primitives.fail(core__located(scope, core__use_error(name, scope)))
        elif (name == 'Rest'):
            _cdy_t112 = cdy_rt.primitives.fail(core__located(scope, "(Rest t) is only for the last argument of a sig's function type"))
        elif (core__type_arity(name, scope) >= 0):
            _cdy_t112 = core__type_arity(name, scope)
        elif core__is_builtin_type(core__declared_name(name, scope), builtins):
            _cdy_t109: object = cdy_rt.primitives.map_get(builtins, core__declared_name(name, scope))
            if isinstance(_cdy_t109, core__BType):
                n = _cdy_t109.arity
                _cdy_t108 = n
            else:
                _cdy_t108 = 0
            _cdy_t112 = _cdy_t108
        elif (core__declared_name(name, scope) != ''):
            _cdy_t112 = cdy_rt.primitives.fail(core__located(scope, (name + ' is a value, not a type')))
        elif core__is_builtin_type(name, builtins):
            _cdy_t111: object = cdy_rt.primitives.map_get(builtins, name)
            if isinstance(_cdy_t111, core__BType):
                _cdy_n_829 = _cdy_t111.arity
                _cdy_t110 = _cdy_n_829
            else:
                _cdy_t110 = 0
            _cdy_t112 = _cdy_t110
        elif (core__variant_sum(name, scope) != ''):
            _cdy_t112 = cdy_rt.primitives.fail(core__located(scope, (name + ' is a variant of ' + core__variant_sum(name, scope) + ', not a type')))
        elif core__is_top_value(name, scope):
            _cdy_t112 = cdy_rt.primitives.fail(core__located(scope, (name + ' is a value, not a type')))
        elif (core__elsewhere_module(name, scope) != ''):
            stem = core__elsewhere_module(name, scope)
            _cdy_t112 = cdy_rt.primitives.fail(core__located(scope, (name + ' is not defined here; ' + stem + " defines it, but this file doesn't import " + stem)))
        else:
            _cdy_t112 = (cdy_rt.primitives.fail(core__located(scope, core__qualified_error(name, scope))) if core__has_dot(name) else cdy_rt.primitives.fail(core__located(scope, ('unknown type ' + name))))
        arity = _cdy_t112
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
    constrained = cdy_rt.primitives.list_find_index((lambda v: (core__constraint_of(v) != '')), tvars)
    body = cdy_rt.primitives.list_drop(2, items)
    field_forms = (form__list_items(items[2]) if (len(items) == 3) else ())
    if (name == ''):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+)) or (deft Name variant+)'))
    elif (dup >= 0):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(cdy_rt.primitives.at(tvar_forms, dup))) + ('deft ' + name + ': type variables must be different (' + cdy_rt.primitives.at(tvars, dup) + ')')))
    elif (constrained >= 0):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(cdy_rt.primitives.at(tvar_forms, constrained))) + ('deft ' + name + ": a type variable can't be a constraint (" + cdy_rt.primitives.at(tvars, constrained) + ')')))
    elif core__is_sum_body(body):
        variants = core__deft_variants(name, body)
        checked = core__check_variants(variants, scope)
        return core__add_top(prog, core__TDeftSum('', name, tvars, variants), prog.n)
    elif (len(field_forms) == 0):
        return cdy_rt.primitives.fail(core__located(scope, 'deft: expected (deft Name ((field Type)+))'))
    else:
        fields = core__deft_fields(('deft ' + name), field_forms)
        _cdy_checked_848 = core__check_fields(fields, scope)
        return core__add_top(prog, core__TDeft('', name, tvars, fields), prog.n)

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
    def _cdy_t113(form: form__Form) -> core__Variant:
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
    return cdy_rt.primitives.list_map(_cdy_t113, body)

def core__is_upper(name: str) -> bool:
    return ((len(name) > 0) and (cdy_rt.primitives.substring(name, 0, 1) >= 'A') and (cdy_rt.primitives.substring(name, 0, 1) <= 'Z'))

def core__deft_fields(owner: str, forms: tuple[form__Form, ...]) -> tuple[tuple[str, core__CType], ...]:
    def _cdy_t114(acc: tuple[tuple[str, core__CType], ...], form: form__Form) -> tuple[tuple[str, core__CType], ...]:
        items = form__list_items(form)
        if ((len(items) != 2) or (form__sym_name(items[0]) == '')):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'deft: field must be (name Type)'))
        elif (core__name_error(form__sym_name(items[0])) != ''):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + (owner + ': ' + core__name_error(form__sym_name(items[0])))))
        elif core__has_field(form__sym_name(items[0]), acc):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + (owner + ': field names must be different (' + form__sym_name(items[0]) + ')')))
        else:
            return (acc + ((form__sym_name(items[0]), core__analyse_type(items[1])),))
    return cdy_rt.primitives.list_fold(_cdy_t114, (), forms)

def core__has_field(name: str, fields: tuple[tuple[str, core__CType], ...]) -> bool:
    def _cdy_t115(f: tuple[str, core__CType]) -> bool:
        _tup = f
        field = _tup[0]
        _t = _tup[1]
        return (field == name)
    return cdy_rt.primitives.list_any(_cdy_t115, fields)

def core__repeated(forms: tuple[form__Form, ...], seen: tuple[str, ...], i: int) -> int:
    while True:
        if (i == len(forms)):
            return -1
        elif cdy_rt.primitives.list_contains(form__sym_name(cdy_rt.primitives.at(forms, i)), seen):
            return i
        else:
            seen, i = ((seen + (form__sym_name(cdy_rt.primitives.at(forms, i)),)), (i + 1))
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
            return core__mark_defined(core__add_top(prog, core__TDef('', name, init, t, scope.here), n), name)

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
        _cdy__tup_897 = core__analyse_expr(items[3], inner, n1)
        body = _cdy__tup_897[0]
        n2 = _cdy__tup_897[1]
        if (len(params) == 0):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + name + ': at least one argument is needed')))
        elif (len(params) != core__fn_arity(t)):
            return cdy_rt.primitives.fail(core__located(scope, ('defn ' + name + ': its sig must be a function type with one type per argument')))
        else:
            return core__mark_defined(core__add_top(prog, core__TDefn('', name, params, body, t, scope.here), n2), name)

def core__fn_arity(t: core__CType) -> int:
    _cdy_t116: object = t
    if isinstance(_cdy_t116, core__TFn):
        params = _cdy_t116.params
        return len(params)
    else:
        return -1

def core__is_variadic(t: core__CType) -> bool:
    _cdy_t117: object = t
    if isinstance(_cdy_t117, core__TFn):
        params = _cdy_t117.params
        return ((len(params) > 0) and core__is_rest(cdy_rt.primitives.at(params, (len(params) - 1))))
    else:
        return False

def core__is_rest(t: core__CType) -> bool:
    _cdy_t118: object = t
    if isinstance(_cdy_t118, core__TCon):
        module = _cdy_t118.module
        name = _cdy_t118.name
        return ((module == core__SYSTEM) and (name == 'Rest'))
    else:
        return False

def core__rest_item(t: core__CType) -> tuple[core__CType, ...]:
    _cdy_t119: object = t
    if isinstance(_cdy_t119, core__TCon):
        module = _cdy_t119.module
        name = _cdy_t119.name
        args = _cdy_t119.args
        if ((module == core__SYSTEM) and (name == 'Rest')):
            return args
        else:
            return ()
    else:
        return ()

def core__bind_params(forms: tuple[form__Form, ...], scope: core__Scope, n: int) -> tuple[tuple[core__Expr, ...], core__Scope, int]:
    def _cdy_t120(s: tuple[core__Scope, int], form: form__Form) -> tuple[tuple[core__Scope, int], core__Expr]:
        _cdy__tup_916 = s
        _cdy_sc_917 = _cdy__tup_916[0]
        _cdy_k_918 = _cdy__tup_916[1]
        name = form__sym_name(form)
        loc = core__Local(name, _cdy_k_918, form__form_pos(form), core__ANY)
        if (name == ''):
            return cdy_rt.primitives.fail(core__located(_cdy_sc_917, 'a parameter must be a name'))
        else:
            return ((core__bind_local(_cdy_sc_917, name, loc), (_cdy_k_918 + 1)), loc)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t120, (scope, n), forms)
    last = _tup[0]
    locs = _tup[1]
    _cdy__tup_924 = last
    sc = _cdy__tup_924[0]
    k = _cdy__tup_924[1]
    return (locs, sc, k)
core__MAIN_TYPE: core__CType = core__TFn((core__TCon(core__SYSTEM, 'List', (core__TCon(core__SYSTEM, 'String', ()),)),), core__TCon(core__SYSTEM, 'Int', ()))

def core__has_main(tops: tuple[core__Top, ...], top: str) -> bool:
    while True:
        if (len(tops) == 0):
            return False
        elif core__is_main(tops[0], top):
            return True
        else:
            tops = prelude__rest(tops)
            continue

def core__is_main(t0: core__Top, top: str) -> bool:
    _cdy_t121: object = t0
    if isinstance(_cdy_t121, core__TDefn):
        module = _cdy_t121.module
        name = _cdy_t121.name
        t = _cdy_t121.t
        pos = _cdy_t121.pos
        if ((module != top) or (name != 'main')):
            return False
        elif (t == core__MAIN_TYPE):
            return True
        else:
            return cdy_rt.primitives.fail((form__pos_text(pos) + 'main must be typed (Fn ((List String)) Int)'))
    elif isinstance(_cdy_t121, core__TDef):
        _cdy_module_935 = _cdy_t121.module
        _cdy_name_936 = _cdy_t121.name
        _cdy_pos_937 = _cdy_t121.pos
        if ((_cdy_module_935 == top) and (_cdy_name_936 == 'main')):
            return cdy_rt.primitives.fail((form__pos_text(_cdy_pos_937) + 'main must be a defn'))
        else:
            return False
    else:
        return False

class lower__SRecord(_cdy_NamedTuple):
    module: str
    name: str
    tvars: tuple[str, ...]
    fields: tuple[tuple[str, core__CType], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SRecord, 'SRecord', (), ('String', 'String', ('List', 'String'), ('List', ('Tup', 'String', 'core.CType'))))

class lower__SSum(_cdy_NamedTuple):
    module: str
    name: str
    tvars: tuple[str, ...]
    variants: tuple[core__Variant, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SSum, 'SSum', (), ('String', 'String', ('List', 'String'), ('List', 'core.Variant')))

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
cdy_rt.primitives.register_type(lower__SMatch, 'SMatch', (), ('core.Expr', 'core.Expr', ('List', 'lower.Case'), ('List', ('List', 'lower.Stmt'))))

class lower__SAssign(_cdy_NamedTuple):
    target: core__Expr
    val: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SAssign, 'SAssign', (), ('core.Expr', 'core.Expr'))

class lower__SDefAssign(_cdy_NamedTuple):
    module: str
    name: str
    val: core__Expr
    t: core__CType
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SDefAssign, 'SDefAssign', (), ('String', 'String', 'core.Expr', 'core.CType'))

class lower__SExpr(_cdy_NamedTuple):
    expr: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SExpr, 'SExpr', (), ('core.Expr',))

class lower__SReturn(_cdy_NamedTuple):
    val: core__Expr
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SReturn, 'SReturn', (), ('core.Expr',))

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
cdy_rt.primitives.register_type(lower__SIf, 'SIf', (), ('core.Expr', ('List', 'lower.Stmt'), ('List', 'lower.Stmt')))

class lower__SFunc(_cdy_NamedTuple):
    module: str
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
cdy_rt.primitives.register_type(lower__SFunc, 'SFunc', (), ('String', 'String', ('List', 'core.Expr'), ('List', 'lower.Stmt'), 'core.CType'))

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
cdy_rt.primitives.register_type(lower__SLocalFunc, 'SLocalFunc', (), ('core.Expr', ('List', 'core.Expr'), ('List', 'lower.Stmt'), 'core.CType'))

class lower__SLoop(_cdy_NamedTuple):
    body: tuple[lower__Stmt, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SLoop, 'SLoop', (), (('List', 'lower.Stmt'),))

class lower__SRebind(_cdy_NamedTuple):
    targets: tuple[core__Expr, ...]
    vals: tuple[core__Expr, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__SRebind, 'SRebind', (), (('List', 'core.Expr'), ('List', 'core.Expr')))

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
    module: str
    variant: str
    binds: tuple[tuple[str, core__Expr], ...]
    body: tuple[lower__Stmt, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(lower__Case, 'Case', (), ('String', 'String', ('List', ('Tup', 'String', 'core.Expr')), ('List', 'lower.Stmt')))

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
cdy_rt.primitives.register_type(lower__Low, 'Low', (), (('List', 'lower.Stmt'), 'core.Expr', 'Int'))

def lower__is_simple(e: core__Expr) -> bool:
    _cdy_t122: object = e
    if isinstance(_cdy_t122, core__Lit):
        return True
    elif isinstance(_cdy_t122, core__Local):
        return True
    elif isinstance(_cdy_t122, core__Global):
        return True
    elif isinstance(_cdy_t122, core__Prim):
        return True
    elif isinstance(_cdy_t122, core__Temp):
        return True
    else:
        return False

def lower__is_applied(e: core__Expr) -> bool:
    _cdy_t123: object = e
    if isinstance(_cdy_t123, core__Call):
        callee = _cdy_t123.callee
        args = _cdy_t123.args
        _cdy_t124: object = callee
        if isinstance(_cdy_t124, core__Lambda):
            params = _cdy_t124.params
            return (len(params) == len(args))
        else:
            return False
    else:
        return False

def lower__bind_applied(e: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], core__Expr, int]:
    _cdy_t125: object = e
    if isinstance(_cdy_t125, core__Call):
        callee = _cdy_t125.callee
        args = _cdy_t125.args
        _cdy_t126: object = callee
        if isinstance(_cdy_t126, core__Lambda):
            params = _cdy_t126.params
            body = _cdy_t126.body
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
            targets, vals, acc = (prelude__rest(targets), prelude__rest(vals), (acc + (lower__SAssign(targets[0], vals[0]),)))
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
        _cdy_t127: object = e
        if isinstance(_cdy_t127, core__Call):
            callee = _cdy_t127.callee
            args = _cdy_t127.args
            pos = _cdy_t127.pos
            ty = _cdy_t127.t
            return lower__value_call(callee, args, pos, ty, n)
        elif isinstance(_cdy_t127, core__If):
            test = _cdy_t127.test
            then = _cdy_t127.then
            other = _cdy_t127.other
            _cdy_pos_32 = _cdy_t127.pos
            _cdy_ty_33 = _cdy_t127.t
            return lower__value_if(test, then, other, _cdy_pos_32, _cdy_ty_33, n)
        elif isinstance(_cdy_t127, core__Do):
            _cdy_body_34 = _cdy_t127.body
            return lower__value_do(_cdy_body_34, n)
        elif isinstance(_cdy_t127, core__Lambda):
            params = _cdy_t127.params
            _cdy_body_36 = _cdy_t127.body
            _cdy_pos_37 = _cdy_t127.pos
            _cdy_ty_38 = _cdy_t127.t
            return lower__value_fn(params, _cdy_body_36, _cdy_pos_37, _cdy_ty_38, n)
        elif isinstance(_cdy_t127, core__Tuple):
            items = _cdy_t127.items
            _cdy_pos_40 = _cdy_t127.pos
            _cdy_ty_41 = _cdy_t127.t
            _cdy__tup_42 = lower__value_seq(items, n)
            _cdy_stmts_43 = _cdy__tup_42[0]
            vals = _cdy__tup_42[1]
            _cdy_n1_45 = _cdy__tup_42[2]
            return lower__Low(_cdy_stmts_43, core__Tuple(vals, _cdy_pos_40, _cdy_ty_41), _cdy_n1_45)
        elif isinstance(_cdy_t127, core__ListOf):
            _cdy_items_46 = _cdy_t127.items
            _cdy_pos_47 = _cdy_t127.pos
            _cdy_ty_48 = _cdy_t127.t
            _cdy__tup_49 = lower__value_seq(_cdy_items_46, n)
            _cdy_stmts_50 = _cdy__tup_49[0]
            _cdy_vals_51 = _cdy__tup_49[1]
            _cdy_n1_52 = _cdy__tup_49[2]
            return lower__Low(_cdy_stmts_50, core__Tuple(_cdy_vals_51, _cdy_pos_47, _cdy_ty_48), _cdy_n1_52)
        elif isinstance(_cdy_t127, core__Fmt):
            parts = _cdy_t127.parts
            _cdy_pos_54 = _cdy_t127.pos
            _cdy_ty_55 = _cdy_t127.t
            _cdy__tup_56 = lower__value_seq(lower__holes(parts), n)
            _cdy_stmts_57 = _cdy__tup_56[0]
            _cdy_vals_58 = _cdy__tup_56[1]
            _cdy_n1_59 = _cdy__tup_56[2]
            return lower__Low(_cdy_stmts_57, core__Fmt(lower__fill_holes(parts, _cdy_vals_58, ()), _cdy_pos_54, _cdy_ty_55), _cdy_n1_59)
        elif isinstance(_cdy_t127, core__Field):
            obj = _cdy_t127.obj
            field = _cdy_t127.field
            _cdy_pos_62 = _cdy_t127.pos
            _cdy_ty_63 = _cdy_t127.t
            _cdy_low_64 = lower__value(obj, n)
            return lower__Low(_cdy_low_64.stmts, core__Field(_cdy_low_64.expr, field, _cdy_pos_62, _cdy_ty_63), _cdy_low_64.n)
        elif isinstance(_cdy_t127, core__Assoc):
            _cdy_obj_65 = _cdy_t127.obj
            fields = _cdy_t127.fields
            _cdy_pos_67 = _cdy_t127.pos
            _cdy_ty_68 = _cdy_t127.t
            _cdy__tup_69 = lower__value_seq(((_cdy_obj_65,) + lower__field_vals(fields)), n)
            _cdy_stmts_70 = _cdy__tup_69[0]
            _cdy_vals_71 = _cdy__tup_69[1]
            _cdy_n1_72 = _cdy__tup_69[2]
            return lower__Low(_cdy_stmts_70, core__Assoc(_cdy_vals_71[0], lower__refill(fields, prelude__rest(_cdy_vals_71), ()), _cdy_pos_67, _cdy_ty_68), _cdy_n1_72)
        elif isinstance(_cdy_t127, core__MatchE):
            _cdy_ty_73 = _cdy_t127.t
            tmp = core__Temp(n, _cdy_ty_73)
            _cdy__tup_75 = lower__lower_match(e, 'value', tmp, (n + 1))
            _cdy_stmts_76 = _cdy__tup_75[0]
            _cdy_n1_77 = _cdy__tup_75[1]
            return lower__Low(_cdy_stmts_76, tmp, _cdy_n1_77)
        else:
            return lower__Low((), e, n)

def lower__lower_match(e: core__Expr, mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t128: object = e
    if isinstance(_cdy_t128, core__MatchE):
        subject = _cdy_t128.subject
        clauses = _cdy_t128.clauses
        default = _cdy_t128.default
        low = lower__value(subject, n)
        temp = core__Temp(low.n, core__ANY)
        _tup = lower__lower_cases(clauses, mode, tmp, (low.n + 1))
        cases = _tup[0]
        n2 = _tup[1]
        _cdy__tup_90 = lower__lower_default(default, mode, tmp, n2)
        default_stmts = _cdy__tup_90[0]
        n3 = _cdy__tup_90[1]
        return ((low.stmts + (lower__SMatch(temp, low.expr, cases, default_stmts),)), n3)
    else:
        return cdy_rt.primitives.fail('internal error: lower: not a match')

def lower__lower_default(default: tuple[core__Expr, ...], mode: str, tmp: core__Expr, n: int) -> tuple[tuple[tuple[lower__Stmt, ...], ...], int]:
    if (len(default) == 0):
        return ((), n)
    else:
        _tup = lower__lower_body(default[0], mode, tmp, n)
        stmts = _tup[0]
        n1 = _tup[1]
        return ((stmts,), n1)

def lower__lower_cases(clauses: tuple[core__Clause, ...], mode: str, tmp: core__Expr, n: int) -> tuple[tuple[lower__Case, ...], int]:
    def _cdy_t129(k: int, clause: core__Clause) -> tuple[int, lower__Case]:
        _cdy__tup_106 = lower__lower_body(clause.body, mode, tmp, k)
        body = _cdy__tup_106[0]
        k1 = _cdy__tup_106[1]
        return (k1, lower__Case(clause.module, clause.variant, clause.binds, body))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t129, n, clauses)
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
        return ((low.stmts + (lower__SAssign(tmp, low.expr),)), low.n)

def lower__value_fn(params: tuple[core__Expr, ...], body: core__Expr, pos: form__Pos, ty: core__CType, n: int) -> lower__Low:
    _tup = lower__tail(body, n)
    stmts = _tup[0]
    n1 = _tup[1]
    _cdy_t130: object = (stmts[0] if (len(stmts) == 1) else lower__SExpr(core__NIL))
    if isinstance(_cdy_t130, lower__SReturn):
        result = _cdy_t130.val
        return lower__Low((), core__Lambda(params, result, pos, ty), n1)
    else:
        return lower__Low((lower__SLocalFunc(core__Temp(n1, ty), params, stmts, ty),), core__Temp(n1, ty), (n1 + 1))

def lower__holes(parts: tuple[core__FPart, ...]) -> tuple[core__Expr, ...]:
    def _cdy_t132(acc: tuple[core__Expr, ...], part: core__FPart) -> tuple[core__Expr, ...]:
        _cdy_t131: object = part
        if isinstance(_cdy_t131, core__FHole):
            e = _cdy_t131.expr
            return (acc + (e,))
        else:
            assert isinstance(_cdy_t131, core__FText)
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t132, (), parts)

def lower__fill_holes(parts: tuple[core__FPart, ...], vals: tuple[core__Expr, ...], acc: tuple[core__FPart, ...]) -> tuple[core__FPart, ...]:
    while True:
        if (len(parts) == 0):
            return acc
        else:
            _cdy_t133: object = parts[0]
            if isinstance(_cdy_t133, core__FHole):
                parts, vals, acc = (prelude__rest(parts), prelude__rest(vals), (acc + (core__FHole(vals[0]),)))
                continue
            else:
                assert isinstance(_cdy_t133, core__FText)
                text = _cdy_t133.text
                parts, acc = (prelude__rest(parts), (acc + (core__FText(text),)))
                continue

def lower__field_vals(fields: tuple[tuple[str, core__Expr], ...]) -> tuple[core__Expr, ...]:
    def _cdy_t134(field: tuple[str, core__Expr]) -> core__Expr:
        _tup = field
        _ = _tup[0]
        v = _tup[1]
        return v
    return cdy_rt.primitives.list_map(_cdy_t134, fields)

def lower__refill(fields: tuple[tuple[str, core__Expr], ...], vals: tuple[core__Expr, ...], acc: tuple[tuple[str, core__Expr], ...]) -> tuple[tuple[str, core__Expr], ...]:
    while True:
        if (len(fields) == 0):
            return acc
        else:
            _tup = fields[0]
            f = _tup[0]
            _ = _tup[1]
            fields, vals, acc = (prelude__rest(fields), prelude__rest(vals), (acc + ((f, vals[0]),)))
            continue

def lower__value_call(callee: core__Expr, args: tuple[core__Expr, ...], pos: form__Pos, ty: core__CType, n: int) -> lower__Low:
    if cdy_rt.primitives.list_contains(lower__prim_name(callee), ('and', 'or')):
        return lower__value_boolop(callee, args, pos, ty, n)
    else:
        _tup = lower__value_seq(((callee,) + args), n)
        stmts = _tup[0]
        items = _tup[1]
        n1 = _tup[2]
        return lower__Low(stmts, core__Call(items[0], prelude__rest(items), pos, ty), n1)

def lower__prim_name(e: core__Expr) -> str:
    _cdy_t135: object = e
    if isinstance(_cdy_t135, core__Prim):
        name = _cdy_t135.name
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
        return lower__Low((first.stmts + (lower__SAssign(tmp, first.expr),) + (lower__guard(op, tmp, lower__guarded(op, later, tmp)),)), tmp, (n1 + 1))
    else:
        return lower__Low(first.stmts, core__Call(op, lower__low_exprs(lows), pos, ty), n1)

def lower__guarded(op: core__Expr, lows: tuple[lower__Low, ...], tmp: core__Expr) -> tuple[lower__Stmt, ...]:
    low = lows[0]
    assign = (low.stmts + (lower__SAssign(tmp, low.expr),))
    if (len(lows) == 1):
        return assign
    else:
        return (assign + (lower__guard(op, tmp, lower__guarded(op, prelude__rest(lows), tmp)),))

def lower__guard(op: core__Expr, tmp: core__Expr, body: tuple[lower__Stmt, ...]) -> lower__Stmt:
    return lower__SIf((tmp if (lower__prim_name(op) == 'and') else core__Call(core__Prim('not', form__NOWHERE, core__ANY), (tmp,), form__NOWHERE, core__ANY)), body, ())

def lower__low_exprs(lows: tuple[lower__Low, ...]) -> tuple[core__Expr, ...]:
    return cdy_rt.primitives.list_map((lambda low: low.expr), lows)

def lower__value_seq(exprs: tuple[core__Expr, ...], n: int) -> tuple[tuple[lower__Stmt, ...], tuple[core__Expr, ...], int]:
    _tup = lower__low_all(exprs, n)
    lows = _tup[0]
    n1 = _tup[1]
    return lower__seq_build(lows, n1, (), ())

def lower__low_all(exprs: tuple[core__Expr, ...], n: int) -> tuple[tuple[lower__Low, ...], int]:
    def _cdy_t136(k: int, e: core__Expr) -> tuple[int, lower__Low]:
        low = lower__value(e, k)
        return (low.n, low)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t136, n, exprs)
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
                lows, n, stmts, out = (later, (n + 1), (stmts + low.stmts + (lower__SAssign(core__Temp(n, low.expr.t), low.expr),)), (out + (core__Temp(n, low.expr.t),)))
                continue
            else:
                lows, stmts, out = (later, (stmts + low.stmts), (out + (low.expr,)))
                continue

def lower__value_if(test: core__Expr, then: core__Expr, other: core__Expr, pos: form__Pos, ty: core__CType, n: int) -> lower__Low:
    t = lower__value(test, n)
    a = lower__value(then, t.n)
    b = lower__value(other, a.n)
    if ((len(a.stmts) == 0) and (len(b.stmts) == 0)):
        return lower__Low(t.stmts, core__If(t.expr, a.expr, b.expr, pos, ty), b.n)
    elif lower__is_if_into(b.stmts, b.expr):
        tmp = b.expr
        return lower__Low((t.stmts + (lower__SIf(t.expr, (a.stmts + (lower__SAssign(tmp, a.expr),)), b.stmts),)), tmp, b.n)
    else:
        _cdy_tmp_207 = core__Temp(b.n, ty)
        return lower__Low((t.stmts + (lower__SIf(t.expr, (a.stmts + (lower__SAssign(_cdy_tmp_207, a.expr),)), (b.stmts + (lower__SAssign(_cdy_tmp_207, b.expr),))),)), _cdy_tmp_207, (b.n + 1))

def lower__is_if_into(stmts: tuple[lower__Stmt, ...], e: core__Expr) -> bool:
    _cdy_t141 = (len(stmts) == 1)
    if _cdy_t141:
        _cdy_t138: object = stmts[0]
        if isinstance(_cdy_t138, lower__SIf):
            _cdy_t137 = True
        else:
            _cdy_t137 = False
        _cdy_t141 = _cdy_t137
        if _cdy_t141:
            _cdy_t140: object = e
            if isinstance(_cdy_t140, core__Temp):
                _cdy_t139 = True
            else:
                _cdy_t139 = False
            _cdy_t141 = _cdy_t139
    return _cdy_t141

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
    _cdy_t142: object = e
    if isinstance(_cdy_t142, core__If):
        test = _cdy_t142.test
        then = _cdy_t142.then
        other = _cdy_t142.other
        t = lower__value(test, n)
        _tup = lower__tail(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_236 = lower__tail(other, n1)
        b = _cdy__tup_236[0]
        n2 = _cdy__tup_236[1]
        return ((t.stmts + (lower__SIf(t.expr, a, b),)), n2)
    elif isinstance(_cdy_t142, core__Do):
        body = _cdy_t142.body
        _cdy__tup_240 = lower__effect_all(lower__all_but_last(body), n)
        stmts = _cdy__tup_240[0]
        _cdy_n1_242 = _cdy__tup_240[1]
        _cdy__tup_243 = lower__tail(lower__last_of(body), _cdy_n1_242)
        last = _cdy__tup_243[0]
        _cdy_n2_245 = _cdy__tup_243[1]
        return ((stmts + last), _cdy_n2_245)
    elif isinstance(_cdy_t142, core__MatchE):
        return lower__lower_match(e, 'tail', core__NIL, n)
    else:
        low = lower__value(e, n)
        return ((low.stmts + (lower__SReturn(low.expr),)), low.n)

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
    _cdy_t143: object = e
    if isinstance(_cdy_t143, core__If):
        test = _cdy_t143.test
        then = _cdy_t143.then
        other = _cdy_t143.other
        t = lower__value(test, n)
        _tup = lower__effect(then, t.n)
        a = _tup[0]
        n1 = _tup[1]
        _cdy__tup_265 = lower__effect(other, n1)
        b = _cdy__tup_265[0]
        n2 = _cdy__tup_265[1]
        return ((t.stmts + (lower__SIf(t.expr, a, b),)), n2)
    elif isinstance(_cdy_t143, core__Do):
        body = _cdy_t143.body
        return lower__effect_all(body, n)
    elif isinstance(_cdy_t143, core__MatchE):
        return lower__lower_match(e, 'effect', core__NIL, n)
    else:
        if lower__is_simple(e):
            return ((), n)
        else:
            low = lower__value(e, n)
            return ((low.stmts + (lower__SExpr(low.expr),)), low.n)

def lower__effect_all(exprs: tuple[core__Expr, ...], n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    def _cdy_t144(k: int, e: core__Expr) -> tuple[int, tuple[lower__Stmt, ...]]:
        _cdy__tup_274 = lower__effect(e, k)
        stmts = _cdy__tup_274[0]
        k1 = _cdy__tup_274[1]
        return (k1, stmts)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t144, n, exprs)
    n1 = _tup[0]
    parts = _tup[1]
    return (cdy_rt.primitives.list_concat(parts), n1)

def lower__returns_unit(t: core__CType) -> bool:
    _cdy_t145: object = t
    if isinstance(_cdy_t145, core__TFn):
        ret = _cdy_t145.ret
        _cdy_t146: object = ret
        if isinstance(_cdy_t146, core__TCon):
            m = _cdy_t146.module
            name = _cdy_t146.name
            return ((m == core__SYSTEM) and (name == 'Unit'))
        else:
            return False
    else:
        return False

def lower__lower_top(top: core__Top, n: int) -> tuple[tuple[lower__Stmt, ...], int]:
    _cdy_t147: object = top
    if isinstance(_cdy_t147, core__TDeft):
        m = _cdy_t147.module
        name = _cdy_t147.name
        tvars = _cdy_t147.tvars
        fields = _cdy_t147.fields
        return ((lower__SRecord(m, name, tvars, fields),), n)
    elif isinstance(_cdy_t147, core__TDeftSum):
        _cdy_m_290 = _cdy_t147.module
        _cdy_name_291 = _cdy_t147.name
        _cdy_tvars_292 = _cdy_t147.tvars
        variants = _cdy_t147.variants
        return ((lower__SSum(_cdy_m_290, _cdy_name_291, _cdy_tvars_292, variants),), n)
    elif isinstance(_cdy_t147, core__TDef):
        _cdy_m_294 = _cdy_t147.module
        _cdy_name_295 = _cdy_t147.name
        init = _cdy_t147.init
        t = _cdy_t147.t
        low = lower__value(init, n)
        return ((low.stmts + (lower__SDefAssign(_cdy_m_294, _cdy_name_295, low.expr, t),)), low.n)
    elif isinstance(_cdy_t147, core__TDefn):
        _cdy_m_299 = _cdy_t147.module
        _cdy_name_300 = _cdy_t147.name
        params = _cdy_t147.params
        body = _cdy_t147.body
        _cdy_t_303 = _cdy_t147.t
        _tup = (lower__effect(body, n) if lower__returns_unit(_cdy_t_303) else lower__tail(body, n))
        stmts = _tup[0]
        n1 = _tup[1]
        return ((lower__SFunc(_cdy_m_299, _cdy_name_300, params, (stmts if core__is_variadic(_cdy_t_303) else lower__loop_tail_calls(core__global_key(_cdy_m_299, _cdy_name_300), params, stmts, lower__returns_unit(_cdy_t_303))), _cdy_t_303),), n1)
    else:
        assert isinstance(_cdy_t147, core__TExpr)
        e = _cdy_t147.expr
        return lower__effect(e, n)

def lower__loop_tail_calls(name: str, params: tuple[core__Expr, ...], body: tuple[lower__Stmt, ...], unit: bool) -> tuple[lower__Stmt, ...]:
    if lower__stmts_have_closure(body):
        return body
    else:
        looped = lower__retail_all(body, name, params)
        if (looped == body):
            return body
        else:
            return (lower__SLoop(((looped + (lower__SReturn(core__NIL),)) if unit else looped)),)

def lower__retail_all(stmts: tuple[lower__Stmt, ...], name: str, params: tuple[core__Expr, ...]) -> tuple[lower__Stmt, ...]:
    if (len(stmts) == 0):
        return stmts
    else:
        return (cdy_rt.primitives.slice_(stmts, 0, (len(stmts) - 1)) + lower__retail(cdy_rt.primitives.at(stmts, (len(stmts) - 1)), name, params))

def lower__retail(s: lower__Stmt, name: str, params: tuple[core__Expr, ...]) -> tuple[lower__Stmt, ...]:
    _cdy_t148: object = s
    if isinstance(_cdy_t148, lower__SReturn):
        val = _cdy_t148.val
        if lower__is_self_call(val, name, params):
            return lower__jump(params, lower__call_args(val))
        else:
            return (s,)
    elif isinstance(_cdy_t148, lower__SExpr):
        e = _cdy_t148.expr
        if lower__is_self_call(e, name, params):
            return lower__jump(params, lower__call_args(e))
        else:
            return (s,)
    elif isinstance(_cdy_t148, lower__SIf):
        test = _cdy_t148.test
        then = _cdy_t148.then
        other = _cdy_t148.other
        return (lower__SIf(test, lower__retail_all(then, name, params), lower__retail_all(other, name, params)),)
    elif isinstance(_cdy_t148, lower__SMatch):
        temp = _cdy_t148.temp
        subject = _cdy_t148.subject
        cases = _cdy_t148.cases
        default = _cdy_t148.default
        return (lower__SMatch(temp, subject, lower__retail_cases(cases, name, params), lower__retail_lists(default, name, params)),)
    else:
        return (s,)

def lower__retail_cases(cases: tuple[lower__Case, ...], name: str, params: tuple[core__Expr, ...]) -> tuple[lower__Case, ...]:
    return cdy_rt.primitives.list_map((lambda c: c._replace(body=lower__retail_all(c.body, name, params))), cases)

def lower__retail_lists(lists: tuple[tuple[lower__Stmt, ...], ...], name: str, params: tuple[core__Expr, ...]) -> tuple[tuple[lower__Stmt, ...], ...]:
    return cdy_rt.primitives.list_map((lambda stmts: lower__retail_all(stmts, name, params)), lists)

def lower__is_self_call(e: core__Expr, name: str, params: tuple[core__Expr, ...]) -> bool:
    _cdy_t149: object = e
    if isinstance(_cdy_t149, core__Call):
        callee = _cdy_t149.callee
        args = _cdy_t149.args
        _cdy_t150: object = callee
        if isinstance(_cdy_t150, core__Global):
            m = _cdy_t150.module
            g = _cdy_t150.name
            return ((core__global_key(m, g) == name) and (len(args) == len(params)))
        else:
            return False
    else:
        return False

def lower__call_args(e: core__Expr) -> tuple[core__Expr, ...]:
    _cdy_t151: object = e
    if isinstance(_cdy_t151, core__Call):
        args = _cdy_t151.args
        return args
    else:
        return ()

def lower__jump(params: tuple[core__Expr, ...], args: tuple[core__Expr, ...]) -> tuple[lower__Stmt, ...]:
    _tup = lower__changed(params, args, (), ())
    targets = _tup[0]
    vals = _tup[1]
    if (len(targets) == 0):
        return (lower__SContinue(),)
    else:
        return ((lower__SRebind(targets, vals),) + (lower__SContinue(),))

def lower__same_local(param: core__Expr, e: core__Expr) -> bool:
    _cdy_t152: object = param
    if isinstance(_cdy_t152, core__Local):
        name = _cdy_t152.name
        id_ = _cdy_t152.id_
        _cdy_t153: object = e
        if isinstance(_cdy_t153, core__Local):
            other = _cdy_t153.name
            oid = _cdy_t153.id_
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
            params, args, targets, vals = (prelude__rest(params), prelude__rest(args), (targets + (params[0],)), (vals + (args[0],)))
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
    _cdy_t154: object = s
    if isinstance(_cdy_t154, lower__SLocalFunc):
        return True
    elif isinstance(_cdy_t154, lower__SAssign):
        target = _cdy_t154.target
        val = _cdy_t154.val
        return (lower__has_lambda(target) or lower__has_lambda(val))
    elif isinstance(_cdy_t154, lower__SDefAssign):
        _cdy_val_364 = _cdy_t154.val
        return lower__has_lambda(_cdy_val_364)
    elif isinstance(_cdy_t154, lower__SExpr):
        e = _cdy_t154.expr
        return lower__has_lambda(e)
    elif isinstance(_cdy_t154, lower__SReturn):
        _cdy_val_366 = _cdy_t154.val
        return lower__has_lambda(_cdy_val_366)
    elif isinstance(_cdy_t154, lower__SIf):
        test = _cdy_t154.test
        then = _cdy_t154.then
        other = _cdy_t154.other
        return (lower__has_lambda(test) or lower__stmts_have_closure(then) or lower__stmts_have_closure(other))
    elif isinstance(_cdy_t154, lower__SMatch):
        subject = _cdy_t154.subject
        cases = _cdy_t154.cases
        default = _cdy_t154.default
        return (lower__has_lambda(subject) or lower__cases_have_closure(cases) or lower__lists_have_closure(default))
    elif isinstance(_cdy_t154, lower__SLoop):
        body = _cdy_t154.body
        return lower__stmts_have_closure(body)
    elif isinstance(_cdy_t154, lower__SRebind):
        vals = _cdy_t154.vals
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
        _cdy_t155: object = e
        if isinstance(_cdy_t155, core__Lambda):
            return True
        elif isinstance(_cdy_t155, core__Call):
            callee = _cdy_t155.callee
            args = _cdy_t155.args
            return (lower__has_lambda(callee) or lower__any_lambda(args))
        elif isinstance(_cdy_t155, core__If):
            test = _cdy_t155.test
            then = _cdy_t155.then
            other = _cdy_t155.other
            return (lower__has_lambda(test) or lower__has_lambda(then) or lower__has_lambda(other))
        elif isinstance(_cdy_t155, core__Do):
            body = _cdy_t155.body
            return lower__any_lambda(body)
        elif isinstance(_cdy_t155, core__Tuple):
            items = _cdy_t155.items
            return lower__any_lambda(items)
        elif isinstance(_cdy_t155, core__ListOf):
            _cdy_items_386 = _cdy_t155.items
            return lower__any_lambda(_cdy_items_386)
        elif isinstance(_cdy_t155, core__Fmt):
            parts = _cdy_t155.parts
            return lower__any_lambda(lower__holes(parts))
        elif isinstance(_cdy_t155, core__Field):
            obj = _cdy_t155.obj
            e = obj
            continue
        elif isinstance(_cdy_t155, core__Assoc):
            _cdy_obj_389 = _cdy_t155.obj
            fields = _cdy_t155.fields
            return (lower__has_lambda(_cdy_obj_389) or lower__any_lambda(lower__field_vals(fields)))
        elif isinstance(_cdy_t155, core__MatchE):
            subject = _cdy_t155.subject
            e = subject
            continue
        else:
            return False

def lower__lower_program(tops: tuple[core__Top, ...], n: int) -> tuple[lower__Stmt, ...]:
    def _cdy_t156(k: int, top: core__Top) -> tuple[int, tuple[lower__Stmt, ...]]:
        _cdy__tup_396 = lower__lower_top(top, k)
        stmts = _cdy__tup_396[0]
        k1 = _cdy__tup_396[1]
        return (k1, stmts)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t156, n, tops)
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
    top: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(emit__Env, 'Env', (), (('Map', 'String', 'String'), ('Map', 'Int', 'String'), ('Map', 'String', 'Bool'), ('Map', 'String', ('List', 'String')), ('Map', 'String', ('Tup', 'String', 'String', 'String')), ('Map', 'Int', ('Tup', 'String', ('List', 'String'))), ('Map', 'String', ('List', 'core.CType')), 'String'))
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
emit__PY_IMPORTS: tuple[str, ...] = ('math', 'cdy_rt.spelling', 'cdy_rt.primitives')

def emit__name_set(names: tuple[str, ...]) -> _cdy_Mapping[str, bool]:
    return cdy_rt.primitives.list_fold((lambda acc, n: cdy_rt.primitives.map_set(acc, n, True)), {}, names)
emit__PY_RESERVED: _cdy_Mapping[str, bool] = emit__name_set((('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'PythonFinalizationError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '_IncompleteInputError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'and', 'anext', 'any', 'as', 'ascii', 'assert', 'async', 'await', 'bin', 'bool', 'break', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'class', 'classmethod', 'compile', 'complex', 'continue', 'copyright', 'credits', 'def', 'del', 'delattr', 'dict', 'dir', 'divmod', 'elif', 'else', 'enumerate', 'eval', 'except', 'exec', 'exit', 'filter', 'finally', 'float', 'for', 'format', 'from', 'frozenset', 'getattr', 'global', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'if', 'import', 'in', 'input', 'int', 'is', 'isinstance', 'issubclass', 'iter', 'lambda', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'nonlocal', 'not', 'object', 'oct', 'open', 'or', 'ord', 'pass', 'pow', 'print', 'property', 'quit', 'raise', 'range', 'repr', 'return', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'try', 'tuple', 'type', 'vars', 'while', 'with', 'yield', 'zip') + ('math', 'cdy_rt')))
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

def emit__spelled_in(module: str, name: str, top: str) -> str:
    if ((module == '') or (module == top)):
        return name
    else:
        return (module + '__' + name)

def emit__spelled(module: str, name: str, env: emit__Env) -> str:
    return emit__spelled_in(module, name, env.top)

def emit__py_global_name(module: str, name: str, top: str) -> str:
    return emit__py_mangle(emit__spelled_in(module, name, top))

def emit__global_py(module: str, name: str, env: emit__Env) -> str:
    return cdy_rt.primitives.map_get(env.globals_, core__global_key(module, name))

def emit__global_names(tops: tuple[core__Top, ...], start: emit__Env) -> emit__Env:
    return cdy_rt.primitives.list_fold((lambda env, top: emit__add_globals(emit__top_module_of(top), emit__top_names_of(top), env)), start, tops)

def emit__add_globals(module: str, names: tuple[str, ...], start: emit__Env) -> emit__Env:
    def _cdy_t157(env: emit__Env, name: str) -> emit__Env:
        key = core__global_key(module, name)
        py = emit__py_global_name(module, name, env.top)
        if (cdy_rt.primitives.map_has(env.taken, py) and (not cdy_rt.primitives.map_has(env.globals_, key))):
            return cdy_rt.primitives.fail((emit__candy_name(emit__holder(py, cdy_rt.primitives.map_keys(env.globals_), env.globals_), env) + ' and ' + emit__candy_name(key, env) + ' are one name in Python (' + py + ')'))
        else:
            return env._replace(globals_=cdy_rt.primitives.map_set(env.globals_, key, py), taken=cdy_rt.primitives.map_set(env.taken, py, True))
    return cdy_rt.primitives.list_fold(_cdy_t157, start, names)

def emit__holder(py: str, names: tuple[str, ...], globals_: _cdy_Mapping[str, str]) -> str:
    return prelude__with_default(py, prelude__find((lambda n: (cdy_rt.primitives.map_get(globals_, n) == py)), names))

def emit__candy_name(key: str, env: emit__Env) -> str:
    parts = cdy_rt.primitives.split(key, '.')
    name = cdy_rt.primitives.at(parts, (len(parts) - 1))
    if ((len(parts) == 1) or (parts[0] == env.top)):
        return name
    else:
        return (name + ' (from module ' + parts[0] + ')')

def emit__top_names_of(top: core__Top) -> tuple[str, ...]:
    _cdy_t158: object = top
    if isinstance(_cdy_t158, core__TDeftSum):
        name = _cdy_t158.name
        variants = _cdy_t158.variants
        return ((name,) + emit__variant_list_names(variants))
    else:
        if (emit__top_name(top) == ''):
            return ()
        else:
            return (emit__top_name(top),)

def emit__variant_list_names(variants: tuple[core__Variant, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda v: v.name), variants)

def emit__top_name(top: core__Top) -> str:
    _cdy_t159: object = top
    if isinstance(_cdy_t159, core__TDeft):
        name = _cdy_t159.name
        return name
    elif isinstance(_cdy_t159, core__TDef):
        _cdy_name_63 = _cdy_t159.name
        return _cdy_name_63
    elif isinstance(_cdy_t159, core__TDefn):
        _cdy_name_64 = _cdy_t159.name
        return _cdy_name_64
    else:
        return ''

def emit__top_module_of(top: core__Top) -> str:
    _cdy_t160: object = top
    if isinstance(_cdy_t160, core__TDeft):
        m = _cdy_t160.module
        return m
    elif isinstance(_cdy_t160, core__TDeftSum):
        _cdy_m_67 = _cdy_t160.module
        return _cdy_m_67
    elif isinstance(_cdy_t160, core__TDef):
        _cdy_m_68 = _cdy_t160.module
        return _cdy_m_68
    elif isinstance(_cdy_t160, core__TDefn):
        _cdy_m_69 = _cdy_t160.module
        return _cdy_m_69
    else:
        return ''

def emit__generic_variants(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, tuple[str, ...]]:
    return cdy_rt.primitives.list_fold((lambda m, top: emit__generic_sum(top, m)), {}, tops)

def emit__generic_sum(top: core__Top, acc: _cdy_Mapping[str, tuple[str, ...]]) -> _cdy_Mapping[str, tuple[str, ...]]:
    _cdy_t161: object = top
    if isinstance(_cdy_t161, core__TDeftSum):
        module = _cdy_t161.module
        tvars = _cdy_t161.tvars
        variants = _cdy_t161.variants
        if (len(tvars) == 0):
            return acc
        else:
            return cdy_rt.primitives.list_fold((lambda m, v: cdy_rt.primitives.map_set(m, core__global_key(module, v.name), emit__generic_fields(v.fields))), acc, variants)
    else:
        return acc

def emit__deft_field_types(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, tuple[core__CType, ...]]:
    return cdy_rt.primitives.list_fold((lambda m, top: emit__top_field_types(top, m)), {}, tops)

def emit__top_field_types(top: core__Top, acc: _cdy_Mapping[str, tuple[core__CType, ...]]) -> _cdy_Mapping[str, tuple[core__CType, ...]]:
    _cdy_t162: object = top
    if isinstance(_cdy_t162, core__TDeft):
        module = _cdy_t162.module
        name = _cdy_t162.name
        fields = _cdy_t162.fields
        return cdy_rt.primitives.map_set(acc, core__global_key(module, name), emit__field_types(fields))
    elif isinstance(_cdy_t162, core__TDeftSum):
        _cdy_module_88 = _cdy_t162.module
        _cdy_name_89 = _cdy_t162.name
        variants = _cdy_t162.variants
        return cdy_rt.primitives.list_fold((lambda m, v: cdy_rt.primitives.map_set(m, core__global_key(_cdy_module_88, v.name), emit__field_types(v.fields))), cdy_rt.primitives.map_set(acc, core__global_key(_cdy_module_88, _cdy_name_89), cdy_rt.primitives.list_map((lambda v: core__TCon(_cdy_module_88, v.name, ())), variants)), variants)
    else:
        return acc

def emit__generic_fields(fields: tuple[tuple[str, core__CType], ...]) -> tuple[str, ...]:
    def _cdy_t163(f: tuple[str, core__CType]) -> str:
        _tup = f
        name = _tup[0]
        _t = _tup[1]
        return name
    def _cdy_t164(f: tuple[str, core__CType]) -> bool:
        _tup = f
        _name = _tup[0]
        t = _tup[1]
        return (len(emit__type_vars((t,), ())) > 0)
    return cdy_rt.primitives.list_map(_cdy_t163, cdy_rt.primitives.list_filter(_cdy_t164, fields))

def emit__local_py(name: str, id_: int, env: emit__Env) -> str:
    if cdy_rt.primitives.map_has(env.locals_, id_):
        return cdy_rt.primitives.map_get(env.locals_, id_)
    else:
        return cdy_rt.primitives.fail(('internal error: emit: local ' + name + ' has no Python name'))

def emit__bind_locals(locs: tuple[core__Expr, ...], start: emit__Env) -> emit__Env:
    def _cdy_t166(env: emit__Env, loc: core__Expr) -> emit__Env:
        _cdy_t165: object = loc
        if isinstance(_cdy_t165, core__Local):
            name = _cdy_t165.name
            id_ = _cdy_t165.id_
            if cdy_rt.primitives.map_has(env.locals_, id_):
                return env
            else:
                base = emit__py_mangle(name)
                py = (('_cdy_' + base + '_' + str(id_)) if cdy_rt.primitives.map_has(env.taken, base) else base)
                return env._replace(locals_=cdy_rt.primitives.map_set(env.locals_, id_, py), taken=cdy_rt.primitives.map_set(env.taken, py, True))
        else:
            return env
    return cdy_rt.primitives.list_fold(_cdy_t166, start, locs)

def emit__bound_locals(stmts: tuple[lower__Stmt, ...], start: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    def _cdy_t169(acc: tuple[core__Expr, ...], stmt: lower__Stmt) -> tuple[core__Expr, ...]:
        _cdy_t167: object = stmt
        if isinstance(_cdy_t167, lower__SAssign):
            target = _cdy_t167.target
            _cdy_t168: object = target
            if isinstance(_cdy_t168, core__Local):
                return (acc + (target,))
            else:
                return acc
        elif isinstance(_cdy_t167, lower__SIf):
            then = _cdy_t167.then
            other = _cdy_t167.other
            return emit__bound_locals(other, emit__bound_locals(then, acc))
        elif isinstance(_cdy_t167, lower__SMatch):
            cases = _cdy_t167.cases
            default = _cdy_t167.default
            return emit__bound_in_cases(cases, emit__bound_in_lists(default, acc))
        elif isinstance(_cdy_t167, lower__SLoop):
            body = _cdy_t167.body
            return emit__bound_locals(body, acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t169, start, stmts)

def emit__bound_in_cases(cases: tuple[lower__Case, ...], start: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    return cdy_rt.primitives.list_fold((lambda acc, c: emit__bound_locals(c.body, (acc + emit__bind_locs(c.binds)))), start, cases)

def emit__bind_locs(binds: tuple[tuple[str, core__Expr], ...]) -> tuple[core__Expr, ...]:
    def _cdy_t170(b: tuple[str, core__Expr]) -> core__Expr:
        _tup = b
        _ = _tup[0]
        loc = _tup[1]
        return loc
    return cdy_rt.primitives.list_map(_cdy_t170, binds)

def emit__bound_in_lists(lists: tuple[tuple[lower__Stmt, ...], ...], start: tuple[core__Expr, ...]) -> tuple[core__Expr, ...]:
    return cdy_rt.primitives.list_fold((lambda acc, stmts: emit__bound_locals(stmts, acc)), start, lists)

def emit__emit_expr(e: core__Expr, env: emit__Env) -> str:
    while True:
        _cdy_t171: object = e
        if isinstance(_cdy_t171, core__Lit):
            form = _cdy_t171.form
            return emit__emit_lit(form)
        elif isinstance(_cdy_t171, core__Local):
            name = _cdy_t171.name
            id_ = _cdy_t171.id_
            return emit__local_py(name, id_, env)
        elif isinstance(_cdy_t171, core__Global):
            module = _cdy_t171.module
            _cdy_name_143 = _cdy_t171.name
            return emit__global_py(module, _cdy_name_143, env)
        elif isinstance(_cdy_t171, core__Prim):
            _cdy_name_144 = _cdy_t171.name
            pos = _cdy_t171.pos
            t = _cdy_t171.t
            return emit__emit_prim(_cdy_name_144, pos, t, env)
        elif isinstance(_cdy_t171, core__Call):
            callee = _cdy_t171.callee
            args = _cdy_t171.args
            return emit__emit_call(callee, args, env)
        elif isinstance(_cdy_t171, core__If):
            test = _cdy_t171.test
            then = _cdy_t171.then
            other = _cdy_t171.other
            return ('(' + emit__emit_expr(then, env) + ' if ' + emit__emit_expr(test, env) + ' else ' + emit__emit_expr(other, env) + ')')
        elif isinstance(_cdy_t171, core__Do):
            return cdy_rt.primitives.fail('internal error: emit: a do inside an expression (lower should have removed it)')
        elif isinstance(_cdy_t171, core__MatchE):
            return cdy_rt.primitives.fail('internal error: emit: a match inside an expression (lower should have removed it)')
        elif isinstance(_cdy_t171, core__Lambda):
            params = _cdy_t171.params
            body = _cdy_t171.body
            inner = emit__bind_locals(params, env)
            return ('(lambda ' + emit__comma_join(emit__emit_exprs(params, inner)) + ': ' + emit__emit_expr(body, inner) + ')')
        elif isinstance(_cdy_t171, core__Tuple):
            items = _cdy_t171.items
            strs = emit__emit_exprs(items, env)
            if (len(strs) == 1):
                return ('(' + strs[0] + ',)')
            else:
                return ('(' + emit__comma_join(strs) + ')')
        elif isinstance(_cdy_t171, core__ListOf):
            _cdy_items_157 = _cdy_t171.items
            _cdy_pos_158 = _cdy_t171.pos
            _cdy_t_159 = _cdy_t171.t
            e = core__Tuple(_cdy_items_157, _cdy_pos_158, _cdy_t_159)
            continue
        elif isinstance(_cdy_t171, core__Fmt):
            parts = _cdy_t171.parts
            _cdy_pos_161 = _cdy_t171.pos
            return emit__emit_format(parts, _cdy_pos_161, env)
        elif isinstance(_cdy_t171, core__Field):
            obj = _cdy_t171.obj
            field = _cdy_t171.field
            _cdy_t_164 = _cdy_t171.t
            return emit__emit_get(obj, field, _cdy_t_164, env)
        elif isinstance(_cdy_t171, core__Assoc):
            _cdy_obj_165 = _cdy_t171.obj
            fields = _cdy_t171.fields
            return (emit__emit_obj(_cdy_obj_165, env) + '._replace(' + emit__comma_join(emit__emit_fields(fields, env)) + ')')
        else:
            assert isinstance(_cdy_t171, core__Temp)
            _cdy_id__167 = _cdy_t171.id_
            return ('_cdy_t' + str(_cdy_id__167))

def emit__emit_obj(obj: core__Expr, env: emit__Env) -> str:
    _cdy_t172: object = obj
    if isinstance(_cdy_t172, core__Local):
        id_ = _cdy_t172.id_
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
    _cdy_t173: object = obj
    if isinstance(_cdy_t173, core__Local):
        id_ = _cdy_t173.id_
        _cdy_t174 = cdy_rt.primitives.map_has(env.narrowed, id_)
        if _cdy_t174:
            _tup = cdy_rt.primitives.map_get(env.narrowed, id_)
            _tmp = _tup[0]
            fields = _tup[1]
            _cdy_t174 = cdy_rt.primitives.list_contains(field, fields)
        if _cdy_t174:
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
    def _cdy_t176(p: core__FPart) -> str:
        _cdy_t175: object = p
        if isinstance(_cdy_t175, core__FText):
            text = _cdy_t175.text
            return emit__py_str(text)
        else:
            assert isinstance(_cdy_t175, core__FHole)
            e = _cdy_t175.expr
            return emit__emit_text(e, pos, env)
    return cdy_rt.primitives.list_map(_cdy_t176, parts)

def emit__emit_text(e: core__Expr, pos: form__Pos, env: emit__Env) -> str:
    return emit__text_of(emit__emit_expr(e, env), e.t, pos, env)

def emit__text_of(x: str, t: core__CType, pos: form__Pos, env: emit__Env) -> str:
    _cdy_t178: object = t
    if isinstance(_cdy_t178, core__TCon):
        m = _cdy_t178.module
        name = _cdy_t178.name
        _cdy_t177 = (name if (m == core__SYSTEM) else '')
    else:
        _cdy_t177 = ''
    _cdy_name_201 = _cdy_t177
    if cdy_rt.primitives.list_contains(_cdy_name_201, ('String', 'Char')):
        return x
    elif (_cdy_name_201 == 'Int'):
        return ('str(' + x + ')')
    elif (_cdy_name_201 == 'Any'):
        return ('cdy_rt.primitives.text_any(' + x + ')')
    else:
        return emit__show_call(x, t, pos, env)

def emit__show_call(x: str, t: core__CType, pos: form__Pos, env: emit__Env) -> str:
    return ('cdy_rt.primitives.show(' + x + ', ' + emit__show_type(t, pos, env) + ')')

def emit__show_type(t: core__CType, pos: form__Pos, env: emit__Env) -> str:
    _cdy_t179: object = t
    if isinstance(_cdy_t179, core__TCon):
        m = _cdy_t179.module
        name = _cdy_t179.name
        args = _cdy_t179.args
        key = core__global_key(m, name)
        shown = emit__py_str(emit__show_name(m, name))
        if emit__holds_fn(key, env, (key,)):
            return cdy_rt.primitives.fail((form__pos_text(pos) + ("show: a function can't be shown, and " + name + ' holds one')))
        elif (len(args) == 0):
            return shown
        else:
            return ('(' + emit__comma_join(((shown,) + cdy_rt.primitives.list_map((lambda a: emit__show_type(a, pos, env)), args))) + ')')
    elif isinstance(_cdy_t179, core__TFn):
        return cdy_rt.primitives.fail((form__pos_text(pos) + "show: a function can't be shown"))
    else:
        assert isinstance(_cdy_t179, core__TVar)
        _cdy_name_215 = _cdy_t179.name
        _cdy_shown_216 = (('t' + cdy_rt.primitives.substring(_cdy_name_215, 1, len(_cdy_name_215))) if cdy_rt.primitives.starts_with(_cdy_name_215, '?') else _cdy_name_215)
        return cdy_rt.primitives.fail((form__pos_text(pos) + ("show: can't show a value of type " + _cdy_shown_216 + ', a type variable')))

def emit__show_name(m: str, name: str) -> str:
    if (m == core__SYSTEM):
        return name
    else:
        return (m + ('.' + name))

def emit__holds_fn(name: str, env: emit__Env, seen: tuple[str, ...]) -> bool:
    return (cdy_rt.primitives.map_has(env.fields, name) and cdy_rt.primitives.list_any((lambda t: emit__field_holds_fn(t, env, seen)), cdy_rt.primitives.map_get(env.fields, name)))

def emit__field_holds_fn(t: core__CType, env: emit__Env, seen: tuple[str, ...]) -> bool:
    _cdy_t180: object = t
    if isinstance(_cdy_t180, core__TFn):
        return True
    elif isinstance(_cdy_t180, core__TCon):
        m = _cdy_t180.module
        n = _cdy_t180.name
        args = _cdy_t180.args
        key = core__global_key(m, n)
        return (cdy_rt.primitives.list_any((lambda a: emit__field_holds_fn(a, env, seen)), args) or ((not cdy_rt.primitives.list_contains(key, seen)) and emit__holds_fn(key, env, (seen + (key,)))))
    else:
        return False

def emit__field_show_type(t: core__CType, env: emit__Env) -> str:
    _cdy_t181: object = t
    if isinstance(_cdy_t181, core__TCon):
        m = _cdy_t181.module
        name = _cdy_t181.name
        args = _cdy_t181.args
        shown = emit__py_str(emit__show_name(m, name))
        if (len(args) == 0):
            return shown
        else:
            return ('(' + emit__comma_join(((shown,) + cdy_rt.primitives.list_map((lambda a: emit__field_show_type(a, env)), args))) + ')')
    elif isinstance(_cdy_t181, core__TFn):
        return emit__py_str('Fn')
    else:
        assert isinstance(_cdy_t181, core__TVar)
        _cdy_name_238 = _cdy_t181.name
        return emit__py_str(("'" + _cdy_name_238))

def emit__register_line(module: str, name: str, tvars: tuple[str, ...], fields: tuple[tuple[str, core__CType], ...], level: int, env: emit__Env) -> str:
    _cdy_t183 = emit__global_py(module, name, env)
    _cdy_t184 = emit__py_str(name)
    _cdy_t185 = emit__py_tuple(cdy_rt.primitives.list_map(emit__py_str, tvars))
    def _cdy_t182(f: tuple[str, core__CType]) -> str:
        _tup = f
        _name = _tup[0]
        t = _tup[1]
        return emit__field_show_type(t, env)
    return emit__line(level, ('cdy_rt.primitives.register_type(' + _cdy_t183 + ', ' + _cdy_t184 + ', ' + _cdy_t185 + ', ' + emit__py_tuple(cdy_rt.primitives.list_map(_cdy_t182, fields)) + ')'))

def emit__py_tuple(items: tuple[str, ...]) -> str:
    if (len(items) == 1):
        return ('(' + items[0] + ',)')
    else:
        return ('(' + emit__comma_join(items) + ')')

def emit__emit_fields(fields: tuple[tuple[str, core__Expr], ...], env: emit__Env) -> tuple[str, ...]:
    def _cdy_t186(fv: tuple[str, core__Expr]) -> str:
        _tup = fv
        f = _tup[0]
        v = _tup[1]
        return (emit__py_mangle(f) + '=' + emit__emit_expr(v, env))
    return cdy_rt.primitives.list_map(_cdy_t186, fields)

def emit__emit_exprs(exprs: tuple[core__Expr, ...], env: emit__Env) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda e: emit__emit_expr(e, env)), exprs)

def emit__emit_lit(form: form__Form) -> str:
    _cdy_t187: object = form
    if isinstance(_cdy_t187, form__Txt):
        v = _cdy_t187.val
        return emit__py_str(v)
    elif isinstance(_cdy_t187, form__CharLit):
        _cdy_v_261 = _cdy_t187.val
        return emit__py_str((_cdy_v_261))
    elif isinstance(_cdy_t187, form__IntLit):
        _cdy_v_262 = _cdy_t187.val
        return (str(_cdy_v_262))
    elif isinstance(_cdy_t187, form__LongLit):
        _cdy_v_263 = _cdy_t187.val
        return (str(_cdy_v_263))
    elif isinstance(_cdy_t187, form__ByteLit):
        _cdy_v_264 = _cdy_t187.val
        return (str(_cdy_v_264))
    elif isinstance(_cdy_t187, form__FloatLit):
        _cdy_v_265 = _cdy_t187.val
        return (cdy_rt.primitives.show(_cdy_v_265, 'Double'))
    elif isinstance(_cdy_t187, form__DoubleLit):
        _cdy_v_266 = _cdy_t187.val
        return (cdy_rt.primitives.show(_cdy_v_266, 'Double'))
    elif isinstance(_cdy_t187, form__BoolLit):
        _cdy_v_267 = _cdy_t187.val
        if _cdy_v_267:
            return 'True'
        else:
            return 'False'
    else:
        return cdy_rt.primitives.fail('internal error: emit: not a literal')

def emit__emit_prim(name: str, pos: form__Pos, t: core__CType, env: emit__Env) -> str:
    if (name == 'show'):
        _cdy_t188: object = t
        if isinstance(_cdy_t188, core__TFn):
            params = _cdy_t188.params
            return ('(lambda _cdy_x: ' + emit__show_call('_cdy_x', params[0], pos, env) + ')')
        else:
            return cdy_rt.primitives.fail((form__pos_text(pos) + "show: its type isn't known here"))
    elif (name == 'text'):
        _cdy_t189: object = t
        if isinstance(_cdy_t189, core__TFn):
            _cdy_params_273 = _cdy_t189.params
            return ('(lambda _cdy_x: ' + emit__text_of('_cdy_x', _cdy_params_273[0], pos, env) + ')')
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
    _cdy_t190: object = callee
    if isinstance(_cdy_t190, core__Prim):
        name = _cdy_t190.name
        pos = _cdy_t190.pos
        if (name == 'text'):
            return emit__emit_text(args[0], pos, env)
        elif (name == 'show'):
            return emit__show_call(strs[0], args[0].t, pos, env)
        else:
            return emit__emit_prim_call(name, args, strs, env)
    else:
        return (emit__emit_expr(callee, env) + '(' + emit__comma_join(strs) + ')')

def emit__is_index_literal(e: core__Expr) -> bool:
    _cdy_t191: object = e
    if isinstance(_cdy_t191, core__Lit):
        form = _cdy_t191.form
        _cdy_t192: object = form
        if isinstance(_cdy_t192, form__IntLit):
            v = _cdy_t192.val
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
    _cdy_t193: object = t
    if isinstance(_cdy_t193, core__TVar):
        name = _cdy_t193.name
        if cdy_rt.primitives.starts_with(name, '?'):
            return '_cdy_Any'
        elif (core__constraint_of(name) == 'integer'):
            return 'int'
        elif (core__constraint_of(name) == 'float'):
            return 'float'
        else:
            return emit__py_mangle(name)
    elif isinstance(_cdy_t193, core__TFn):
        params = _cdy_t193.params
        ret = _cdy_t193.ret
        return ('_cdy_Callable[[' + emit__comma_join(emit__emit_types(params, env)) + '], ' + emit__emit_type(ret, env) + ']')
    else:
        assert isinstance(_cdy_t193, core__TCon)
        m = _cdy_t193.module
        _cdy_name_296 = _cdy_t193.name
        args = _cdy_t193.args
        if (m == core__SYSTEM):
            return emit__emit_tcon(_cdy_name_296, emit__emit_types(args, env), env.spellings)
        else:
            return emit__emit_tcon(emit__spelled(m, _cdy_name_296, env), emit__emit_types(args, env), {})

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
    def _cdy_t195(acc: tuple[str, ...], t: core__CType) -> tuple[str, ...]:
        _cdy_t194: object = t
        if isinstance(_cdy_t194, core__TVar):
            name = _cdy_t194.name
            if cdy_rt.primitives.list_contains(name, acc):
                return acc
            else:
                return (acc + (name,))
        elif isinstance(_cdy_t194, core__TCon):
            args = _cdy_t194.args
            return emit__type_vars(args, acc)
        else:
            assert isinstance(_cdy_t194, core__TFn)
            params = _cdy_t194.params
            ret = _cdy_t194.ret
            return emit__type_vars((params + (ret,)), acc)
    return cdy_rt.primitives.list_fold(_cdy_t195, start, types)

def emit__emit_stmt(s: lower__Stmt, level: int, env: emit__Env) -> str:
    _cdy_t196: object = s
    if isinstance(_cdy_t196, lower__SRecord):
        m = _cdy_t196.module
        name = _cdy_t196.name
        tvars = _cdy_t196.tvars
        fields = _cdy_t196.fields
        checked = emit__check_py_fields(('deft ' + emit__candy_name(core__global_key(m, name), env)), fields, {})
        return ('\n' + emit__line(level, ('class ' + emit__global_py(m, name, env) + emit__type_params(tvars) + '(_cdy_NamedTuple):')) + emit__emit_record_fields(fields, (level + 1), env) + emit__eq_methods((level + 1)) + emit__register_line(m, name, tvars, fields, level, env))
    elif isinstance(_cdy_t196, lower__SSum):
        _cdy_m_320 = _cdy_t196.module
        _cdy_name_321 = _cdy_t196.name
        _cdy_tvars_322 = _cdy_t196.tvars
        variants = _cdy_t196.variants
        return (emit__emit_variants(_cdy_m_320, _cdy_name_321, variants, _cdy_tvars_322, level, env) + emit__line(level, ('type ' + emit__global_py(_cdy_m_320, _cdy_name_321, env) + emit__type_params(_cdy_tvars_322) + ' = ' + cdy_rt.primitives.join(emit__variant_refs(_cdy_m_320, variants, _cdy_tvars_322, env), ' | '))))
    elif isinstance(_cdy_t196, lower__SMatch):
        temp = _cdy_t196.temp
        subject = _cdy_t196.subject
        cases = _cdy_t196.cases
        default = _cdy_t196.default
        t = emit__emit_expr(temp, env)
        val = emit__emit_expr(subject, env)
        generic = cdy_rt.primitives.map_has(env.generic, emit__case_key(cases[0]))
        return (emit__line(level, ((t + ' = ' + val) if generic else (t + ': object = ' + val))) + emit__emit_match(t, cases, default, ((not generic) and (len(default) == 0)), 'if', level, env, subject))
    elif isinstance(_cdy_t196, lower__SLoop):
        body = _cdy_t196.body
        return (emit__line(level, 'while True:') + emit__emit_block(body, (level + 1), env))
    elif isinstance(_cdy_t196, lower__SRebind):
        targets = _cdy_t196.targets
        vals = _cdy_t196.vals
        return emit__line(level, ((emit__emit_expr(targets[0], env) + ' = ' + emit__emit_expr(vals[0], env)) if (len(targets) == 1) else (emit__comma_join(emit__emit_exprs(targets, env)) + ' = (' + emit__comma_join(emit__emit_exprs(vals, env)) + ')')))
    elif isinstance(_cdy_t196, lower__SContinue):
        return emit__line(level, 'continue')
    elif isinstance(_cdy_t196, lower__SAssign):
        target = _cdy_t196.target
        _cdy_val_335 = _cdy_t196.val
        return emit__line(level, (emit__emit_expr(target, env) + emit__lambda_annotation(target, _cdy_val_335, env) + ' = ' + emit__emit_expr(_cdy_val_335, env)))
    elif isinstance(_cdy_t196, lower__SDefAssign):
        _cdy_m_336 = _cdy_t196.module
        _cdy_name_337 = _cdy_t196.name
        _cdy_val_338 = _cdy_t196.val
        _cdy_t_339 = _cdy_t196.t
        return emit__line(level, (emit__global_py(_cdy_m_336, _cdy_name_337, env) + ': ' + emit__emit_type(_cdy_t_339, env) + ' = ' + emit__emit_expr(_cdy_val_338, env)))
    elif isinstance(_cdy_t196, lower__SExpr):
        e = _cdy_t196.expr
        return emit__line(level, emit__emit_expr(e, env))
    elif isinstance(_cdy_t196, lower__SReturn):
        _cdy_e_341 = _cdy_t196.val
        return emit__line(level, ('return ' + emit__emit_expr(_cdy_e_341, env)))
    elif isinstance(_cdy_t196, lower__SIf):
        test = _cdy_t196.test
        then = _cdy_t196.then
        other = _cdy_t196.other
        return emit__emit_if('if', test, then, other, level, env)
    elif isinstance(_cdy_t196, lower__SFunc):
        _cdy_m_345 = _cdy_t196.module
        _cdy_name_346 = _cdy_t196.name
        params = _cdy_t196.params
        _cdy_body_348 = _cdy_t196.body
        _cdy_t_349 = _cdy_t196.t
        return emit__emit_func(_cdy_m_345, _cdy_name_346, params, _cdy_body_348, _cdy_t_349, level, env)
    else:
        assert isinstance(_cdy_t196, lower__SLocalFunc)
        _cdy_target_350 = _cdy_t196.target
        _cdy_params_351 = _cdy_t196.params
        _cdy_body_352 = _cdy_t196.body
        _cdy_t_353 = _cdy_t196.t
        inner = emit__bind_locals((_cdy_params_351 + emit__bound_locals(_cdy_body_352, ())), env)
        _cdy_t197: object = _cdy_t_353
        if isinstance(_cdy_t197, core__TFn):
            types = _cdy_t197.params
            ret = _cdy_t197.ret
            return (emit__line(level, ('def ' + emit__emit_expr(_cdy_target_350, env) + '(' + emit__comma_join(emit__emit_params(_cdy_params_351, types, inner, ())) + ') -> ' + emit__emit_type(ret, env) + ':')) + emit__emit_block(_cdy_body_352, (level + 1), inner))
        else:
            return (emit__line(level, ('def ' + emit__emit_expr(_cdy_target_350, env) + '(' + emit__comma_join(emit__emit_any_params(_cdy_params_351, inner)) + ') -> _cdy_Any:')) + emit__emit_block(_cdy_body_352, (level + 1), inner))

def emit__lambda_annotation(target: core__Expr, val: core__Expr, env: emit__Env) -> str:
    _cdy_t198: object = target
    if isinstance(_cdy_t198, core__Local):
        _cdy_t199: object = val
        if isinstance(_cdy_t199, core__Lambda):
            t = _cdy_t199.t
            _cdy_t200: object = t
            if isinstance(_cdy_t200, core__TFn):
                return (': ' + emit__emit_type(t, env))
            else:
                return ''
        else:
            return ''
    else:
        return ''

def emit__emit_if(keyword: str, test: core__Expr, then: tuple[lower__Stmt, ...], other: tuple[lower__Stmt, ...], level: int, env: emit__Env) -> str:
    _cdy_t204 = emit__line(level, (keyword + ' ' + emit__emit_expr(test, env) + ':'))
    _cdy_t205 = emit__emit_block(then, (level + 1), env)
    if (len(other) == 0):
        _cdy_t203 = ''
    elif (len(other) == 1):
        _cdy_t202: object = other[0]
        if isinstance(_cdy_t202, lower__SIf):
            test2 = _cdy_t202.test
            then2 = _cdy_t202.then
            other2 = _cdy_t202.other
            _cdy_t201 = emit__emit_if('elif', test2, then2, other2, level, env)
        else:
            _cdy_t201 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
        _cdy_t203 = _cdy_t201
    else:
        _cdy_t203 = (emit__line(level, 'else:') + emit__emit_block(other, (level + 1), env))
    return (_cdy_t204 + _cdy_t205 + _cdy_t203)

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
    def _cdy_t206(ft: tuple[str, core__CType]) -> str:
        _tup = ft
        f = _tup[0]
        t = _tup[1]
        return emit__line(level, (emit__py_mangle(f) + ': ' + emit__emit_type(t, env)))
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map(_cdy_t206, fields), '')

def emit__check_py_fields(owner: str, fields: tuple[tuple[str, core__CType], ...], start: _cdy_Mapping[str, str]) -> bool:
    def _cdy_t207(seen: _cdy_Mapping[str, str], ft: tuple[str, core__CType]) -> _cdy_Mapping[str, str]:
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
    _seen = cdy_rt.primitives.list_fold(_cdy_t207, start, fields)
    return True

def emit__used_tvars(tvars: tuple[str, ...], used: tuple[str, ...]) -> tuple[str, ...]:
    return cdy_rt.primitives.list_filter((lambda v: cdy_rt.primitives.list_contains(v, used)), tvars)

def emit__field_types(fields: tuple[tuple[str, core__CType], ...]) -> tuple[core__CType, ...]:
    def _cdy_t208(f: tuple[str, core__CType]) -> core__CType:
        _tup = f
        _ = _tup[0]
        t = _tup[1]
        return t
    return cdy_rt.primitives.list_map(_cdy_t208, fields)

def emit__variant_tvars(v: core__Variant, tvars: tuple[str, ...]) -> tuple[str, ...]:
    return emit__used_tvars(tvars, emit__type_vars(emit__field_types(v.fields), ()))

def emit__emit_variants(module: str, sum_: str, variants: tuple[core__Variant, ...], tvars: tuple[str, ...], level: int, env: emit__Env) -> str:
    def _cdy_t209(v: core__Variant) -> str:
        checked = emit__check_py_fields(('deft ' + emit__candy_name(core__global_key(module, sum_), env) + ', variant ' + v.name), v.fields, {})
        head = ('class ' + emit__global_py(module, v.name, env) + emit__type_params(emit__variant_tvars(v, tvars)) + '(_cdy_NamedTuple):')
        body = (emit__emit_record_fields(v.fields, (level + 1), env) + emit__eq_methods((level + 1)))
        register = emit__register_line(module, v.name, tvars, v.fields, level, env)
        return ('\n' + emit__line(level, head) + body + register)
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map(_cdy_t209, variants), '')

def emit__variant_refs(module: str, variants: tuple[core__Variant, ...], tvars: tuple[str, ...], env: emit__Env) -> tuple[str, ...]:
    return cdy_rt.primitives.list_map((lambda v: (emit__global_py(module, v.name, env) + emit__type_params(emit__variant_tvars(v, tvars)))), variants)

def emit__case_key(c: lower__Case) -> str:
    return core__global_key(c.module, c.variant)

def emit__emit_match(subj: str, cases: tuple[lower__Case, ...], default: tuple[tuple[lower__Stmt, ...], ...], assert_last: bool, keyword: str, level: int, env: emit__Env, subject: core__Expr) -> str:
    if (len(cases) == 0):
        if (len(default) == 0):
            return ''
        else:
            return (emit__line(level, 'else:') + emit__emit_block(default[0], (level + 1), env))
    elif (assert_last and (len(cases) == 1)):
        c = cases[0]
        cenv = emit__case_env(subject, subj, emit__case_key(c), env)
        inner = (level if (keyword == 'if') else (level + 1))
        return (('' if (keyword == 'if') else emit__line(level, 'else:')) + emit__line(inner, ('assert isinstance(' + subj + ', ' + emit__global_py(c.module, c.variant, env) + ')')) + emit__emit_binds(c.binds, emit__case_key(c), subj, inner, cenv) + emit__emit_stmts(c.body, inner, cenv))
    else:
        _cdy_c_435 = cases[0]
        _cdy_cenv_436 = emit__case_env(subject, subj, emit__case_key(_cdy_c_435), env)
        test = (keyword + ' isinstance(' + subj + ', ' + emit__global_py(_cdy_c_435.module, _cdy_c_435.variant, env) + '):')
        binds = emit__emit_binds(_cdy_c_435.binds, emit__case_key(_cdy_c_435), subj, (level + 1), _cdy_cenv_436)
        body = ((emit__line((level + 1), 'pass') if (binds == '') else '') if (len(_cdy_c_435.body) == 0) else emit__emit_stmts(_cdy_c_435.body, (level + 1), _cdy_cenv_436))
        return (emit__line(level, test) + binds + body + emit__emit_match(subj, prelude__rest(cases), default, assert_last, 'elif', level, env, subject))

def emit__case_env(subject: core__Expr, subj: str, variant: str, env: emit__Env) -> emit__Env:
    _cdy_t210: object = subject
    if isinstance(_cdy_t210, core__Local):
        id_ = _cdy_t210.id_
        fields = (cdy_rt.primitives.map_get(env.generic, variant) if cdy_rt.primitives.map_has(env.generic, variant) else ())
        return env._replace(narrowed=cdy_rt.primitives.map_set(env.narrowed, id_, (subj, fields)))
    else:
        return env

def emit__emit_binds(binds: tuple[tuple[str, core__Expr], ...], variant: str, subj: str, level: int, env: emit__Env) -> str:
    def _cdy_t211(b: tuple[str, core__Expr]) -> str:
        _tup = b
        f = _tup[0]
        loc = _tup[1]
        note = ((': ' + emit__emit_type(loc.t, env)) if cdy_rt.primitives.map_has(env.generic, variant) else '')
        return emit__line(level, (emit__emit_expr(loc, env) + note + ' = ' + subj + '.' + emit__py_mangle(f)))
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map(_cdy_t211, binds), '')

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
            params, types, acc = (prelude__rest(params), prelude__rest(types), (acc + (emit__emit_param(params[0], types[0], env),)))
            continue

def emit__emit_param(param: core__Expr, t: core__CType, env: emit__Env) -> str:
    if core__is_rest(t):
        return ('*' + emit__emit_expr(param, env) + ': ' + emit__emit_type(core__rest_item(t)[0], env))
    else:
        return (emit__emit_expr(param, env) + ': ' + emit__emit_type(t, env))

def emit__emit_func(module: str, name: str, params: tuple[core__Expr, ...], body: tuple[lower__Stmt, ...], t: core__CType, level: int, env: emit__Env) -> str:
    _cdy_t212: object = t
    if isinstance(_cdy_t212, core__TFn):
        types = _cdy_t212.params
        ret = _cdy_t212.ret
        inner = emit__bind_locals((params + emit__bound_locals(body, ())), env._replace(locals_={}))
        tvars = emit__type_vars((types + (ret,)), ())
        tparams = emit__type_params(tvars)
        args = emit__comma_join(emit__emit_params(params, types, inner, ()))
        return ('\n' + emit__line(level, ('def ' + emit__global_py(module, name, env) + tparams + '(' + args + ') -> ' + emit__emit_type(ret, env) + ':')) + emit__emit_block(body, (level + 1), inner))
    else:
        return cdy_rt.primitives.fail(('defn ' + name + ': its sig must be a function type'))

def emit__emit_imports(modules: tuple[str, ...]) -> str:
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda m: ('import ' + m + '\n')), modules), '')

def emit__emit_main(env: emit__Env) -> str:
    name = emit__global_py(env.top, 'main', env)
    return ('\n\nif __name__ == "__main__":\n' + emit__indent(1) + 'cdy_rt.primitives.run_main(' + name + ')\n')

class expand__Loaded(_cdy_NamedTuple):
    key: str
    exports: core__Exports
    tops: tuple[core__Top, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__Loaded, 'Loaded', (), ('String', 'core.Exports', ('List', 'core.Top')))

class expand__MacroFile(_cdy_NamedTuple):
    key: str
    macros: tuple[form__Macro, ...]
    modules: tuple[expand__Loaded, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__MacroFile, 'MacroFile', (), ('String', ('List', 'form.Macro'), ('List', 'expand.Loaded')))

class expand__Imports(_cdy_NamedTuple):
    macros: tuple[form__Macro, ...]
    files: tuple[expand__MacroFile, ...]
    seen: _cdy_Mapping[str, bool]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__Imports, 'Imports', (), (('List', 'form.Macro'), ('List', 'expand.MacroFile'), ('Map', 'String', 'Bool')))

class expand__Expanded(_cdy_NamedTuple):
    forms: tuple[form__Form, ...]
    macros: _cdy_Mapping[str, form__Macro]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__Expanded, 'Expanded', (), (('List', 'form.Form'), ('Map', 'String', 'form.Macro')))

class expand__MacroForms(_cdy_NamedTuple):
    forms: tuple[form__Form, ...]
    defs: tuple[form__Form, ...]
    macros: _cdy_Mapping[str, form__Macro]
    files: tuple[expand__MacroFile, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__MacroForms, 'MacroForms', (), (('List', 'form.Form'), ('List', 'form.Form'), ('Map', 'String', 'form.Macro'), ('List', 'expand.MacroFile')))

class expand__Expander(_cdy_NamedTuple):
    builtins: _cdy_Mapping[str, core__Builtin]
    load_file: _cdy_Callable[[str, expand__Expander, tuple[str, ...]], tuple[expand__MacroFile, expand__Expander]]
    load_own: _cdy_Callable[[tuple[form__Form, ...], tuple[expand__MacroFile, ...]], _cdy_Callable[[str], _cdy_Callable[[tuple[form__Form, ...]], form__Form]]]
    prelude: expand__Imports
    loaded: _cdy_Mapping[str, expand__MacroFile]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(expand__Expander, 'Expander', (), (('Map', 'String', 'core.Builtin'), 'Fn', 'Fn', 'expand.Imports', ('Map', 'String', 'expand.MacroFile')))

def expand__new_expander(builtins: _cdy_Mapping[str, core__Builtin], load_file: _cdy_Callable[[str, expand__Expander, tuple[str, ...]], tuple[expand__MacroFile, expand__Expander]], load_own: _cdy_Callable[[tuple[form__Form, ...], tuple[expand__MacroFile, ...]], _cdy_Callable[[str], _cdy_Callable[[tuple[form__Form, ...]], form__Form]]]) -> expand__Expander:
    bare = expand__Expander(builtins, load_file, load_own, expand__Imports((), (), {}), {})
    path = include__library_path('prelude_macros.cdy')
    form = form__Lst((form__Sym('import-macros', form__NOWHERE), form__Txt(path, form__NOWHERE)), form__NOWHERE)
    _tup = expand__import_file(form, bare, (), bare.prelude)
    imports = _tup[0]
    ex = _tup[1]
    return ex._replace(prelude=imports)

def expand__expand_program(forms: tuple[form__Form, ...], ex: expand__Expander) -> tuple[tuple[form__Form, ...], _cdy_Mapping[str, form__Macro], expand__Expander]:
    _tup = expand__expand_file(forms, ex, ())
    done = _tup[0]
    ex1 = _tup[1]
    return (done.forms, done.macros, ex1)
expand__MACRO_HEADS: tuple[str, ...] = ('defmacro', 'import-macros')

def expand__expand_file(forms: tuple[form__Form, ...], ex: expand__Expander, loading: tuple[str, ...]) -> tuple[expand__Expanded, expand__Expander]:
    _tup = expand__import_all(expand__pick_forms(forms, ('import-macros',), True), ex, loading, ex.prelude)
    imports = _tup[0]
    ex1 = _tup[1]
    _cdy_imported_20 = expand__macro_map(imports.macros, {})
    defs = expand__expand_defs(expand__pick_forms(forms, ('defmacro',), True), _cdy_imported_20)
    own = (() if (len(defs) == 0) else expand__load_own_defs(defs, imports.files, ex1))
    macros = expand__macro_map(own, _cdy_imported_20)
    return (expand__Expanded(expand__splice_dos(expand__expand_all(expand__pick_forms(forms, expand__MACRO_HEADS, False), macros)), macros), ex1)

def expand__expand_macro_file(forms: tuple[form__Form, ...], ex: expand__Expander, loading: tuple[str, ...]) -> tuple[expand__MacroForms, expand__Expander]:
    builtins = ex.builtins
    _tup = expand__import_all(expand__pick_forms(forms, ('import-macros',), True), ex, loading, ex.prelude)
    imports = _tup[0]
    ex1 = _tup[1]
    _cdy_imported_31 = expand__macro_map(imports.macros, {})
    defs = expand__expand_defs(expand__pick_forms(forms, ('defmacro',), True), _cdy_imported_31)
    checked = expand__unique_names(defs, builtins, {})
    helpers = expand__splice_dos(expand__expand_all(expand__pick_forms(forms, expand__MACRO_HEADS, False), _cdy_imported_31))
    return (expand__MacroForms((helpers + expand__macro_program(defs, builtins)), defs, _cdy_imported_31, imports.files), ex1)

def expand__splice_dos(forms: tuple[form__Form, ...]) -> tuple[form__Form, ...]:
    def _cdy_t213(form: form__Form) -> tuple[form__Form, ...]:
        items = form__list_items(form)
        if ((len(items) > 0) and (form__sym_name(items[0]) == 'do')):
            return expand__splice_dos(cdy_rt.primitives.list_map(expand__spliceable, prelude__rest(items)))
        else:
            return (form,)
    return cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(_cdy_t213, forms))

def expand__spliceable(form: form__Form) -> form__Form:
    items = form__list_items(form)
    head = (form__sym_name(items[0]) if (len(items) > 0) else '')
    if cdy_rt.primitives.list_contains(head, ('defmacro', 'import', 'import-macros')):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + head + " can't be in a top-level do: it is read before macros are expanded"))
    else:
        return form

def expand__pick_forms(forms: tuple[form__Form, ...], heads: tuple[str, ...], keep: bool) -> tuple[form__Form, ...]:
    def _cdy_t214(form: form__Form) -> bool:
        items = form__list_items(form)
        return (((len(items) > 0) and cdy_rt.primitives.list_contains(form__sym_name(items[0]), heads)) == keep)
    return cdy_rt.primitives.list_filter(_cdy_t214, forms)

def expand__expand_defs(defs: tuple[form__Form, ...], macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    return cdy_rt.primitives.list_map((lambda d: form__Lst(expand__expand_after(form__list_items(d), 3, macros), form__form_pos(d))), defs)

def expand__macro_map(macros: tuple[form__Macro, ...], start: _cdy_Mapping[str, form__Macro]) -> _cdy_Mapping[str, form__Macro]:
    def _cdy_t215(acc: _cdy_Mapping[str, form__Macro], macro: form__Macro) -> _cdy_Mapping[str, form__Macro]:
        name = macro.name
        if cdy_rt.primitives.map_has(acc, name):
            return cdy_rt.primitives.fail((form__pos_text(macro.pos) + 'defmacro: ' + name + ' is already a macro'))
        else:
            return cdy_rt.primitives.map_set(acc, name, macro)
    return cdy_rt.primitives.list_fold(_cdy_t215, start, macros)

def expand__import_all(forms: tuple[form__Form, ...], ex: expand__Expander, loading: tuple[str, ...], start: expand__Imports) -> tuple[expand__Imports, expand__Expander]:
    def _cdy_t216(acc: tuple[expand__Imports, expand__Expander], form: form__Form) -> tuple[expand__Imports, expand__Expander]:
        _tup = acc
        imports = _tup[0]
        e = _tup[1]
        return expand__import_file(form, e, loading, imports)
    return cdy_rt.primitives.list_fold(_cdy_t216, (start, ex), forms)

def expand__import_file(form: form__Form, ex: expand__Expander, loading: tuple[str, ...], acc: expand__Imports) -> tuple[expand__Imports, expand__Expander]:
    path = expand__macro_path(form)
    key = cdy_rt.primitives.path_resolve(path)
    if cdy_rt.primitives.map_has(acc.seen, key):
        return (acc, ex)
    elif cdy_rt.primitives.list_contains(key, loading):
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'import-macros: ' + path + ' imports itself'))
    else:
        _tup = ((cdy_rt.primitives.map_get(ex.loaded, key), ex) if cdy_rt.primitives.map_has(ex.loaded, key) else expand__load_new(path, key, ex, loading))
        file = _tup[0]
        ex1 = _tup[1]
        return (expand__Imports((acc.macros + file.macros), expand__add_files((file,), acc.files), cdy_rt.primitives.map_set(acc.seen, key, True)), ex1)

def expand__load_new(path: str, key: str, ex: expand__Expander, loading: tuple[str, ...]) -> tuple[expand__MacroFile, expand__Expander]:
    _tup = ex.load_file(path, ex, (loading + (key,)))
    file = _tup[0]
    ex1 = _tup[1]
    return (file, ex1._replace(loaded=cdy_rt.primitives.map_set(ex1.loaded, key, file)))

def expand__macro_path(form: form__Form) -> str:
    _cdy_t217: object = form__list_items(form)[1]
    if isinstance(_cdy_t217, form__Txt):
        path = _cdy_t217.val
        return path
    else:
        return cdy_rt.primitives.fail((form__pos_text(form__form_pos(form)) + 'import-macros: expected (import-macros name)'))

def expand__add_files(files: tuple[expand__MacroFile, ...], start: tuple[expand__MacroFile, ...]) -> tuple[expand__MacroFile, ...]:
    def _cdy_t218(acc: tuple[expand__MacroFile, ...], f: expand__MacroFile) -> tuple[expand__MacroFile, ...]:
        if cdy_rt.primitives.list_any((lambda g: (g.key == f.key)), acc):
            return acc
        else:
            return (acc + (f,))
    return cdy_rt.primitives.list_fold(_cdy_t218, start, files)

def expand__load_own_defs(defs: tuple[form__Form, ...], files: tuple[expand__MacroFile, ...], ex: expand__Expander) -> tuple[form__Macro, ...]:
    builtins = ex.builtins
    checked = expand__unique_names(defs, builtins, {})
    run = ex.load_own(expand__macro_program(defs, builtins), files)
    return expand__macro_list(defs, run)

def expand__library_builtins(_: None) -> _cdy_Mapping[str, core__Builtin]:
    decls = include__library_path('special.cdy')
    _cdy_t220 = read__read_source(decls, cdy_rt.primitives.slurp(decls))
    def _cdy_t219(file: str) -> tuple[str, tuple[form__Form, ...]]:
        path = include__library_path(file)
        return (file, read__read_source(path, cdy_rt.primitives.slurp(path)))
    return core__read_builtins(_cdy_t220, cdy_rt.primitives.list_map(_cdy_t219, (('system.cdy',) + cdy_rt.primitives.list_map((lambda name: (name + '.cdy')), include__declaration_modules(None)))), cdy_rt.spelling.SPELLINGS)

def expand__macro_program(defs: tuple[form__Form, ...], builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[form__Form, ...]:
    def _cdy_t221(d: form__Form) -> tuple[form__Form, ...]:
        items = expand__defmacro_items(d, builtins)
        pos = form__form_pos(d)
        fname = form__Sym(expand__macro_fn(form__sym_name(items[1])), pos)
        args = form__Sym('args__', pos)
        type_ = form__Lst((form__Sym('Fn', pos), form__Lst((form__Lst((form__Sym('List', pos), form__Sym('Form', pos)), pos),), pos), form__Sym('Form', pos)), pos)
        body = form__Lst((form__Sym('let', pos), form__Lst(expand__param_binds(items[2], args, pos), pos), items[3]), pos)
        return (form__Lst((form__Sym('sig', pos), fname, type_), pos), form__Lst((form__Sym('defn', pos), fname, form__Lst((args,), pos), body), pos))
    return cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(_cdy_t221, defs))

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
    _cdy_t222: object = params
    if isinstance(_cdy_t222, form__Sym):
        return True
    elif isinstance(_cdy_t222, form__Lst):
        items = _cdy_t222.items
        return expand__all_names(items)
    else:
        return False

def expand__all_names(forms: tuple[form__Form, ...]) -> bool:
    return cdy_rt.primitives.list_all((lambda f: (form__sym_name(f) != '')), forms)

def expand__param_binds(params: form__Form, args: form__Form, pos: form__Pos) -> tuple[form__Form, ...]:
    if (form__sym_name(params) == ''):
        return expand__arg_binds(form__list_items(params), args, pos)
    else:
        return (form__Lst((params, args), pos),)

def expand__arg_binds(params: tuple[form__Form, ...], args: form__Form, pos: form__Pos) -> tuple[form__Form, ...]:
    def _cdy_t223(ip: tuple[int, form__Form]) -> form__Form:
        _tup = ip
        i = _tup[0]
        p = _tup[1]
        return form__Lst((p, form__Lst((form__Sym('at', pos), args, form__IntLit(i, pos)), pos)), pos)
    return cdy_rt.primitives.list_map(_cdy_t223, cdy_rt.primitives.list_zip(cdy_rt.primitives.list_range(0, len(params)), params))

def expand__macro_fn(name: str) -> str:
    return ('macro__' + name)

def expand__unique_names(defs: tuple[form__Form, ...], builtins: _cdy_Mapping[str, core__Builtin], start: _cdy_Mapping[str, bool]) -> bool:
    def _cdy_t224(seen: _cdy_Mapping[str, bool], d: form__Form) -> _cdy_Mapping[str, bool]:
        name = form__sym_name(expand__defmacro_items(d, builtins)[1])
        if cdy_rt.primitives.map_has(seen, name):
            return cdy_rt.primitives.fail((form__pos_text(form__form_pos(d)) + 'defmacro: ' + name + ' is defined twice'))
        else:
            return cdy_rt.primitives.map_set(seen, name, True)
    _seen = cdy_rt.primitives.list_fold(_cdy_t224, start, defs)
    return True

def expand__macro_list(defs: tuple[form__Form, ...], run_of: _cdy_Callable[[str], _cdy_Callable[[tuple[form__Form, ...]], form__Form]]) -> tuple[form__Macro, ...]:
    def _cdy_t225(d: form__Form) -> form__Macro:
        items = form__list_items(d)
        name = form__sym_name(items[1])
        params = items[2]
        arity = (len(form__list_items(params)) if (form__sym_name(params) == '') else -1)
        run = run_of(expand__macro_fn(name))
        return form__Macro(name, arity, run, form__form_pos(d))
    return cdy_rt.primitives.list_map(_cdy_t225, defs)

def expand__expand_all(forms: tuple[form__Form, ...], macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    return cdy_rt.primitives.list_map((lambda f: expand__expand_form(f, macros)), forms)

def expand__expand_form(form: form__Form, macros: _cdy_Mapping[str, form__Macro]) -> form__Form:
    while True:
        _cdy_t226: object = form
        if isinstance(_cdy_t226, form__Lst):
            items = _cdy_t226.items
            pos = _cdy_t226.pos
            head = ('' if (len(items) == 0) else form__sym_name(items[0]))
            if cdy_rt.primitives.map_has(macros, head):
                form = expand__expand_call(cdy_rt.primitives.map_get(macros, head), prelude__rest(items), pos)
                continue
            elif cdy_rt.primitives.list_contains(head, ('sig', 'deft', 'private', 'import', 'import-macros', 'quo', 'quasi')):
                return form
            elif (head == 'defn'):
                return form__Lst(expand__expand_after(items, 3, macros), pos)
            elif (head == 'fn'):
                return form__Lst(expand__expand_after(items, 2, macros), pos)
            elif cdy_rt.primitives.list_contains(head, ('let', 'match')):
                return form__Lst(expand__expand_clauses(head, items, macros), pos)
            else:
                return form__Lst(expand__expand_all(items, macros), pos)
        else:
            return form

def expand__expand_after(items: tuple[form__Form, ...], n: int, macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    if (len(items) < n):
        return items
    else:
        return (cdy_rt.primitives.list_take(n, items) + expand__expand_all(cdy_rt.primitives.list_drop(n, items), macros))

def expand__expand_clauses(head: str, items: tuple[form__Form, ...], macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    if ((head == 'let') and (len(items) == 3)):
        _cdy_t227: object = items[1]
        if isinstance(_cdy_t227, form__Lst):
            binds = _cdy_t227.items
            p = _cdy_t227.pos
            return (items[0], form__Lst(expand__each_clause(binds, 1, macros), p), expand__expand_form(items[2], macros))
        else:
            return expand__expand_all(items, macros)
    elif ((head == 'match') and (len(items) > 1)):
        return ((items[0], expand__expand_form(items[1], macros)) + expand__each_clause(cdy_rt.primitives.list_drop(2, items), 1, macros))
    else:
        return expand__expand_all(items, macros)

def expand__each_clause(clauses: tuple[form__Form, ...], n: int, macros: _cdy_Mapping[str, form__Macro]) -> tuple[form__Form, ...]:
    return cdy_rt.primitives.list_map((lambda c: expand__expand_clause(c, n, macros)), clauses)

def expand__expand_clause(clause: form__Form, n: int, macros: _cdy_Mapping[str, form__Macro]) -> form__Form:
    _cdy_t228: object = clause
    if isinstance(_cdy_t228, form__Lst):
        items = _cdy_t228.items
        p = _cdy_t228.pos
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
    _cdy_t229: object = form
    if isinstance(_cdy_t229, form__Lst):
        items = _cdy_t229.items
        p = _cdy_t229.pos
        return form__Lst(expand__stamp_all(items, pos), (pos if (p.line == 0) else p))
    else:
        if (form__form_pos(form).line == 0):
            return expand__form_at(form, pos)
        else:
            return form

def expand__form_at(form: form__Form, pos: form__Pos) -> form__Form:
    _cdy_t230: object = form
    if isinstance(_cdy_t230, form__Sym):
        v = _cdy_t230.name
        return form__Sym(v, pos)
    elif isinstance(_cdy_t230, form__Txt):
        _cdy_v_177 = _cdy_t230.val
        return form__Txt(_cdy_v_177, pos)
    elif isinstance(_cdy_t230, form__IntLit):
        _cdy_v_178 = _cdy_t230.val
        return form__IntLit(_cdy_v_178, pos)
    elif isinstance(_cdy_t230, form__LongLit):
        _cdy_v_179 = _cdy_t230.val
        return form__LongLit(_cdy_v_179, pos)
    elif isinstance(_cdy_t230, form__ByteLit):
        _cdy_v_180 = _cdy_t230.val
        return form__ByteLit(_cdy_v_180, pos)
    elif isinstance(_cdy_t230, form__FloatLit):
        _cdy_v_181 = _cdy_t230.val
        return form__FloatLit(_cdy_v_181, pos)
    elif isinstance(_cdy_t230, form__DoubleLit):
        _cdy_v_182 = _cdy_t230.val
        return form__DoubleLit(_cdy_v_182, pos)
    elif isinstance(_cdy_t230, form__CharLit):
        _cdy_v_183 = _cdy_t230.val
        return form__CharLit(_cdy_v_183, pos)
    elif isinstance(_cdy_t230, form__BoolLit):
        _cdy_v_184 = _cdy_t230.val
        return form__BoolLit(_cdy_v_184, pos)
    else:
        return form

def expand__stamp_all(forms: tuple[form__Form, ...], pos: form__Pos) -> tuple[form__Form, ...]:
    return cdy_rt.primitives.list_map((lambda f: expand__stamp(f, pos)), forms)

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
cdy_rt.primitives.register_type(check__Ctx, 'Ctx', (), (('Map', 'String', 'core.CType'), ('Map', 'String', 'check.Shape'), ('Map', 'String', 'check.Shape'), ('Map', 'String', 'core.Builtin'), 'form.Pos', ('Map', 'String', 'core.CType'), ('Map', 'String', 'String')))

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
cdy_rt.primitives.register_type(check__Shape, 'Shape', (), (('List', 'String'), ('List', ('Tup', 'String', 'core.CType')), 'String'))

class check__St(_cdy_NamedTuple):
    subst: _cdy_Mapping[str, core__CType]
    n: int
    errors: tuple[str, ...]
    types: _cdy_Mapping[str, core__CType]
    pending: tuple[check__Pending, ...]
    compared: tuple[check__Compared, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__St, 'St', (), (('Map', 'String', 'core.CType'), 'Int', ('List', 'String'), ('Map', 'String', 'core.CType'), ('List', 'check.Pending'), ('List', 'check.Compared')))

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
cdy_rt.primitives.register_type(check__Pending, 'Pending', (), ('core.Expr', 'String', 'String', 'core.CType', 'core.CType', 'form.Pos'))

class check__Compared(_cdy_NamedTuple):
    var: str
    what: str
    here: form__Pos
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__Compared, 'Compared', (), ('String', 'String', 'form.Pos'))

class check__Res(_cdy_NamedTuple):
    t: core__CType
    st: check__St
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(check__Res, 'Res', (), ('core.CType', 'check.St'))

def check__tcon(name: str) -> core__CType:
    return core__TCon(core__SYSTEM, name, ())

def check__key_tcon(key: str, args: tuple[core__CType, ...]) -> core__CType:
    parts = cdy_rt.primitives.split(key, '.')
    if (len(parts) == 2):
        return core__TCon(parts[0], parts[1], args)
    else:
        return core__TCon('', key, args)

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
    return check__check_tops(tops, ctx, check__St({}, 0, (), {}, (), ()))

def check__defn_label(name: str) -> str:
    if ((len(name) > 7) and (cdy_rt.primitives.substring(name, 0, 7) == 'macro__')):
        return ('defmacro ' + cdy_rt.primitives.substring(name, 7, len(name)))
    else:
        return ('defn ' + name)

def check__check_tops(tops: tuple[core__Top, ...], ctx: check__Ctx, st: check__St) -> tuple[tuple[core__Top, ...], tuple[str, ...]]:
    def _cdy_t231(s: check__St, top: core__Top) -> tuple[check__St, core__Top]:
        named = check__retype_top(top, (lambda t, k: core__TVar(('?e' + str(k)))))
        fresh_st = s._replace(subst={}, types={}, compared=())
        s1 = check__check_compared(ctx, check__solve_pending(ctx, check__check_top(named, ctx, fresh_st)))
        return (s1, check__retype_top(named, (lambda t, k: check__node_type(t, s1))))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t231, st, tops)
    st1 = _tup[0]
    done = _tup[1]
    return (done, st1.errors)

def check__check_top(top: core__Top, ctx: check__Ctx, st: check__St) -> check__St:
    _cdy_t232: object = top
    if isinstance(_cdy_t232, core__TDef):
        name = _cdy_t232.name
        init = _cdy_t232.init
        t = _cdy_t232.t
        pos = _cdy_t232.pos
        return check__check_expr(init, t, ('def ' + name), ctx._replace(here=pos), st)
    elif isinstance(_cdy_t232, core__TDefn):
        _cdy_name_36 = _cdy_t232.name
        params = _cdy_t232.params
        body = _cdy_t232.body
        _cdy_t_39 = _cdy_t232.t
        _cdy_pos_40 = _cdy_t232.pos
        c = ctx._replace(here=_cdy_pos_40)
        _cdy_t233: object = _cdy_t_39
        if isinstance(_cdy_t233, core__TFn):
            ptypes = _cdy_t233.params
            ret = _cdy_t233.ret
            inside = check__body_types(ptypes)
            return check__check_expr(body, ret, check__defn_label(_cdy_name_36), c._replace(env=check__bind_all(params, inside, c.env, 0)), check__typed_all(params, inside, st))
        else:
            return st
    elif isinstance(_cdy_t232, core__TExpr):
        e = _cdy_t232.expr
        return check__infer(e, ctx, st).st
    else:
        return st

def check__body_types(ptypes: tuple[core__CType, ...]) -> tuple[core__CType, ...]:
    def _cdy_t234(p: core__CType) -> core__CType:
        if core__is_rest(p):
            return core__TCon(core__SYSTEM, 'List', core__rest_item(p))
        else:
            return p
    return cdy_rt.primitives.list_map(_cdy_t234, ptypes)

def check__bind_all(params: tuple[core__Expr, ...], types: tuple[core__CType, ...], env: _cdy_Mapping[str, core__CType], i: int) -> _cdy_Mapping[str, core__CType]:
    while True:
        if ((i == len(params)) or (i == len(types))):
            return env
        else:
            env, i = (cdy_rt.primitives.map_set(env, check__local_key(cdy_rt.primitives.at(params, i)), cdy_rt.primitives.at(types, i)), (i + 1))
            continue

def check__local_key(e: core__Expr) -> str:
    _cdy_t235: object = e
    if isinstance(_cdy_t235, core__Local):
        name = _cdy_t235.name
        id_ = _cdy_t235.id_
        return (name + '#' + str(id_))
    else:
        return ''

def check__top_types(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, core__CType]:
    def _cdy_t237(acc: _cdy_Mapping[str, core__CType], top: core__Top) -> _cdy_Mapping[str, core__CType]:
        _cdy_t236: object = top
        if isinstance(_cdy_t236, core__TDef):
            m = _cdy_t236.module
            name = _cdy_t236.name
            t = _cdy_t236.t
            return cdy_rt.primitives.map_set(acc, core__global_key(m, name), t)
        elif isinstance(_cdy_t236, core__TDefn):
            _cdy_m_61 = _cdy_t236.module
            _cdy_name_62 = _cdy_t236.name
            _cdy_t_63 = _cdy_t236.t
            return cdy_rt.primitives.map_set(acc, core__global_key(_cdy_m_61, _cdy_name_62), _cdy_t_63)
        elif isinstance(_cdy_t236, core__TDeft):
            _cdy_m_64 = _cdy_t236.module
            _cdy_name_65 = _cdy_t236.name
            tvars = _cdy_t236.tvars
            fields = _cdy_t236.fields
            return cdy_rt.primitives.map_set(acc, core__global_key(_cdy_m_64, _cdy_name_65), core__TFn(check__fields_types(fields), core__TCon(_cdy_m_64, _cdy_name_65, check__tvar_types(tvars))))
        elif isinstance(_cdy_t236, core__TDeftSum):
            _cdy_m_68 = _cdy_t236.module
            _cdy_name_69 = _cdy_t236.name
            _cdy_tvars_70 = _cdy_t236.tvars
            variants = _cdy_t236.variants
            return check__variant_types(variants, _cdy_m_68, core__TCon(_cdy_m_68, _cdy_name_69, check__tvar_types(_cdy_tvars_70)), acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t237, {}, tops)

def check__variant_types(variants: tuple[core__Variant, ...], module: str, sum_: core__CType, start: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    return cdy_rt.primitives.list_fold((lambda acc, v: cdy_rt.primitives.map_set(acc, core__global_key(module, v.name), core__TFn(check__fields_types(v.fields), sum_))), start, variants)

def check__fields_types(fields: tuple[tuple[str, core__CType], ...]) -> tuple[core__CType, ...]:
    def _cdy_t238(f: tuple[str, core__CType]) -> core__CType:
        _tup = f
        _name = _tup[0]
        t = _tup[1]
        return t
    return cdy_rt.primitives.list_map(_cdy_t238, fields)

def check__tvar_types(names: tuple[str, ...]) -> tuple[core__CType, ...]:
    return cdy_rt.primitives.list_map((lambda name: core__TVar(name)), names)

def check__top_shapes(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, check__Shape]:
    def _cdy_t240(acc: _cdy_Mapping[str, check__Shape], top: core__Top) -> _cdy_Mapping[str, check__Shape]:
        _cdy_t239: object = top
        if isinstance(_cdy_t239, core__TDeft):
            m = _cdy_t239.module
            name = _cdy_t239.name
            tvars = _cdy_t239.tvars
            fields = _cdy_t239.fields
            return cdy_rt.primitives.map_set(acc, core__global_key(m, name), check__Shape(tvars, fields, ''))
        elif isinstance(_cdy_t239, core__TDeftSum):
            _cdy_m_92 = _cdy_t239.module
            _cdy_name_93 = _cdy_t239.name
            _cdy_tvars_94 = _cdy_t239.tvars
            variants = _cdy_t239.variants
            return check__variant_shapes(variants, _cdy_tvars_94, _cdy_m_92, _cdy_name_93, acc)
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t240, {}, tops)

def check__variant_shapes(variants: tuple[core__Variant, ...], tvars: tuple[str, ...], module: str, sum_: str, start: _cdy_Mapping[str, check__Shape]) -> _cdy_Mapping[str, check__Shape]:
    return cdy_rt.primitives.list_fold((lambda acc, v: cdy_rt.primitives.map_set(acc, core__global_key(module, v.name), check__Shape(tvars, v.fields, core__global_key(module, sum_)))), start, variants)

def check__top_sums(tops: tuple[core__Top, ...]) -> _cdy_Mapping[str, check__Shape]:
    def _cdy_t242(acc: _cdy_Mapping[str, check__Shape], top: core__Top) -> _cdy_Mapping[str, check__Shape]:
        _cdy_t241: object = top
        if isinstance(_cdy_t241, core__TDeftSum):
            m = _cdy_t241.module
            name = _cdy_t241.name
            tvars = _cdy_t241.tvars
            variants = _cdy_t241.variants
            return cdy_rt.primitives.map_set(acc, core__global_key(m, name), check__Shape(tvars, cdy_rt.primitives.list_map((lambda v: (core__global_key(m, v.name), core__ANY)), variants), ''))
        else:
            return acc
    return cdy_rt.primitives.list_fold(_cdy_t242, {}, tops)

def check__check_expr(e: core__Expr, want: core__CType, what: str, outer: check__Ctx, st: check__St) -> check__St:
    while True:
        ctx = check__at_node(e, outer)
        _cdy_t243: object = e
        if isinstance(_cdy_t243, core__If):
            test = _cdy_t243.test
            then = _cdy_t243.then
            other = _cdy_t243.other
            if check__is_var(check__prune(want, st.subst)):
                return check__infer_expect(e, want, what, ctx, st)
            else:
                rt = check__infer(test, ctx, st)
                st1 = check__expect_is(check__tcon('Bool'), rt.t, 'if: the test', ctx, rt.st)
                return check__typed(e, want, check__check_expr(other, want, what, ctx, check__check_expr(then, want, what, ctx, st1)))
        elif isinstance(_cdy_t243, core__Do):
            body = _cdy_t243.body
            return check__typed(e, want, (check__expect(want, check__tcon('Unit'), what, ctx, st) if (len(body) == 0) else check__check_expr(cdy_rt.primitives.at(body, (len(body) - 1)), want, what, ctx, check__infer_do(cdy_rt.primitives.slice_(body, 0, (len(body) - 1)), ctx, check__Res(core__ANY, st)).st)))
        elif isinstance(_cdy_t243, core__Call):
            callee = _cdy_t243.callee
            args = _cdy_t243.args
            _cdy_t244: object = callee
            if isinstance(_cdy_t244, core__Lambda):
                params = _cdy_t244.params
                _cdy_body_126 = _cdy_t244.body
                if (len(params) == len(args)):
                    _tup = check__infer_all(args, ctx, st)
                    ts = _tup[0]
                    st0 = _tup[1]
                    _cdy_st1_130 = check__typed_all(params, ts, check__typed(callee, core__TFn(ts, want), check__typed(e, want, st0)))
                    e, outer, st = (_cdy_body_126, ctx._replace(env=check__bind_all(params, ts, ctx.env, 0)), _cdy_st1_130)
                    continue
                else:
                    return check__infer_expect(e, want, what, ctx, st)
            else:
                return check__infer_expect(e, want, what, ctx, st)
        elif isinstance(_cdy_t243, core__Lambda):
            return check__check_lambda(e, want, what, ctx, st)
        elif isinstance(_cdy_t243, core__MatchE):
            subject = _cdy_t243.subject
            clauses = _cdy_t243.clauses
            default = _cdy_t243.default
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
    _cdy_t245: object = e
    if isinstance(_cdy_t245, core__Lit):
        form = _cdy_t245.form
        return form__form_pos(form)
    elif isinstance(_cdy_t245, core__Local):
        pos = _cdy_t245.pos
        return pos
    elif isinstance(_cdy_t245, core__Global):
        _cdy_pos_140 = _cdy_t245.pos
        return _cdy_pos_140
    elif isinstance(_cdy_t245, core__Prim):
        _cdy_pos_141 = _cdy_t245.pos
        return _cdy_pos_141
    elif isinstance(_cdy_t245, core__Do):
        _cdy_pos_142 = _cdy_t245.pos
        return _cdy_pos_142
    elif isinstance(_cdy_t245, core__Call):
        _cdy_pos_143 = _cdy_t245.pos
        return _cdy_pos_143
    elif isinstance(_cdy_t245, core__If):
        _cdy_pos_144 = _cdy_t245.pos
        return _cdy_pos_144
    elif isinstance(_cdy_t245, core__Lambda):
        _cdy_pos_145 = _cdy_t245.pos
        return _cdy_pos_145
    elif isinstance(_cdy_t245, core__Tuple):
        _cdy_pos_146 = _cdy_t245.pos
        return _cdy_pos_146
    elif isinstance(_cdy_t245, core__ListOf):
        _cdy_pos_147 = _cdy_t245.pos
        return _cdy_pos_147
    elif isinstance(_cdy_t245, core__Fmt):
        _cdy_pos_148 = _cdy_t245.pos
        return _cdy_pos_148
    elif isinstance(_cdy_t245, core__Field):
        _cdy_pos_149 = _cdy_t245.pos
        return _cdy_pos_149
    elif isinstance(_cdy_t245, core__Assoc):
        _cdy_pos_150 = _cdy_t245.pos
        return _cdy_pos_150
    elif isinstance(_cdy_t245, core__MatchE):
        _cdy_pos_151 = _cdy_t245.pos
        return _cdy_pos_151
    else:
        return form__NOWHERE

def check__is_missing_else(e: core__Expr) -> bool:
    _cdy_t246: object = e
    if isinstance(_cdy_t246, core__Prim):
        name = _cdy_t246.name
        pos = _cdy_t246.pos
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
    _cdy_t247: object = e
    if isinstance(_cdy_t247, core__Lit):
        form = _cdy_t247.form
        return check__Res(check__literal_type(form), st)
    elif isinstance(_cdy_t247, core__Local):
        name = _cdy_t247.name
        key = check__local_key(e)
        return check__Res((cdy_rt.primitives.map_get(ctx.env, key) if cdy_rt.primitives.map_has(ctx.env, key) else core__ANY), st)
    elif isinstance(_cdy_t247, core__Global):
        return check__as_value(check__name_type(e, ctx, st))
    elif isinstance(_cdy_t247, core__Prim):
        return check__as_value(check__name_type(e, ctx, st))
    elif isinstance(_cdy_t247, core__Call):
        callee = _cdy_t247.callee
        args = _cdy_t247.args
        return check__infer_call(callee, args, ctx, st)
    elif isinstance(_cdy_t247, core__If):
        test = _cdy_t247.test
        then = _cdy_t247.then
        other = _cdy_t247.other
        rt = check__infer(test, ctx, st)
        st1 = check__expect_is(check__tcon('Bool'), rt.t, 'if: the test', ctx, rt.st)
        ra = check__infer(then, ctx, st1)
        rb = check__infer(other, ctx, ra.st)
        if check__is_missing_else(other):
            return check__Res(check__tcon('Unit'), check__expect_is(check__tcon('Unit'), ra.t, 'if: with no else, the then', ctx, rb.st))
        else:
            return check__join_types(ra.t, rb.t, 'if: the branches', ctx, rb.st)
    elif isinstance(_cdy_t247, core__Do):
        body = _cdy_t247.body
        return check__infer_do(body, ctx, check__Res(check__tcon('Unit'), st))
    elif isinstance(_cdy_t247, core__Lambda):
        params = _cdy_t247.params
        _cdy_body_183 = _cdy_t247.body
        return check__infer_lambda(params, _cdy_body_183, ctx, st)
    elif isinstance(_cdy_t247, core__Tuple):
        items = _cdy_t247.items
        _tup = check__infer_all(items, ctx, st)
        ts = _tup[0]
        _cdy_st1_187 = _tup[1]
        return check__Res(core__TCon(core__SYSTEM, 'Tup', ts), _cdy_st1_187)
    elif isinstance(_cdy_t247, core__ListOf):
        _cdy_items_188 = _cdy_t247.items
        return check__infer_list_of(_cdy_items_188, ctx, st)
    elif isinstance(_cdy_t247, core__Fmt):
        parts = _cdy_t247.parts
        return check__Res(check__tcon('String'), check__infer_holes(parts, ctx, st))
    elif isinstance(_cdy_t247, core__Field):
        obj = _cdy_t247.obj
        field = _cdy_t247.field
        return check__infer_field(obj, field, ctx, st)
    elif isinstance(_cdy_t247, core__Assoc):
        _cdy_obj_192 = _cdy_t247.obj
        fields = _cdy_t247.fields
        return check__infer_assoc(_cdy_obj_192, fields, ctx, st)
    elif isinstance(_cdy_t247, core__MatchE):
        subject = _cdy_t247.subject
        clauses = _cdy_t247.clauses
        default = _cdy_t247.default
        return check__infer_match(subject, clauses, default, ctx, st)
    else:
        return check__Res(core__ANY, st)

def check__literal_type(form: form__Form) -> core__CType:
    _cdy_t248: object = form
    if isinstance(_cdy_t248, form__Txt):
        return check__tcon('String')
    elif isinstance(_cdy_t248, form__IntLit):
        return check__tcon('Int')
    elif isinstance(_cdy_t248, form__LongLit):
        return check__tcon('Long')
    elif isinstance(_cdy_t248, form__ByteLit):
        return check__tcon('Byte')
    elif isinstance(_cdy_t248, form__FloatLit):
        return check__tcon('Float')
    elif isinstance(_cdy_t248, form__DoubleLit):
        return check__tcon('Double')
    elif isinstance(_cdy_t248, form__CharLit):
        return check__tcon('Char')
    elif isinstance(_cdy_t248, form__BoolLit):
        return check__tcon('Bool')
    else:
        return core__ANY

def check__name_type(e: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t249: object = e
    if isinstance(_cdy_t249, core__Global):
        m = _cdy_t249.module
        name = _cdy_t249.name
        key = core__global_key(m, name)
        if cdy_rt.primitives.map_has(ctx.globals_, key):
            return check__noted(name, check__instantiate(cdy_rt.primitives.map_get(ctx.globals_, key), st), ctx)
        else:
            return check__Res(core__ANY, st)
    elif isinstance(_cdy_t249, core__Prim):
        _cdy_name_204 = _cdy_t249.name
        return check__noted(_cdy_name_204, check__prim_type(_cdy_name_204, ctx, st), ctx)
    else:
        return check__Res(core__ANY, st)

def check__noted(name: str, r: check__Res, ctx: check__Ctx) -> check__Res:
    vars_ = check__equatable_vars(r.t)
    if (len(vars_) == 0):
        return r
    else:
        return check__Res(r.t, r.st._replace(compared=(r.st.compared + cdy_rt.primitives.list_map((lambda v: check__Compared(v, name, ctx.here)), vars_))))

def check__equatable_vars(t: core__CType) -> tuple[str, ...]:
    def _cdy_t250(acc: tuple[str, ...], v: str) -> tuple[str, ...]:
        if cdy_rt.primitives.list_contains(v, acc):
            return acc
        else:
            return (acc + (v,))
    return cdy_rt.primitives.list_fold(_cdy_t250, (), check__all_equatable(t))

def check__all_equatable(t: core__CType) -> tuple[str, ...]:
    _cdy_t251: object = t
    if isinstance(_cdy_t251, core__TVar):
        name = _cdy_t251.name
        if (check__is_flexible(name) and (core__constraint_of(name) == 'equatable')):
            return (name,)
        else:
            return ()
    elif isinstance(_cdy_t251, core__TCon):
        args = _cdy_t251.args
        return cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(check__all_equatable, args))
    else:
        assert isinstance(_cdy_t251, core__TFn)
        params = _cdy_t251.params
        ret = _cdy_t251.ret
        return (cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(check__all_equatable, params)) + check__all_equatable(ret))

def check__as_value(r: check__Res) -> check__Res:
    _cdy_t252: object = r.t
    if isinstance(_cdy_t252, core__TFn):
        params = _cdy_t252.params
        ret = _cdy_t252.ret
        if core__is_variadic(r.t):
            return check__Res(core__TFn(cdy_rt.primitives.slice_(params, 0, (len(params) - 1)), ret), r.st)
        else:
            return r
    else:
        return r

def check__infer_callee(callee: core__Expr, ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t253: object = callee
    if isinstance(_cdy_t253, core__Global):
        return check__callee_typed(callee, check__name_type(callee, ctx, st))
    elif isinstance(_cdy_t253, core__Prim):
        return check__callee_typed(callee, check__name_type(callee, ctx, st))
    else:
        return check__infer(callee, ctx, st)

def check__callee_typed(callee: core__Expr, r: check__Res) -> check__Res:
    return check__Res(r.t, check__typed(callee, check__as_value(r).t, r.st))

def check__prim_type(name: str, ctx: check__Ctx, st: check__St) -> check__Res:
    if cdy_rt.primitives.map_has(ctx.builtins, name):
        _cdy_t254: object = cdy_rt.primitives.map_get(ctx.builtins, name)
        if isinstance(_cdy_t254, core__Typed):
            type_ = _cdy_t254.type_
            return check__instantiate(type_, st)
        else:
            return check__Res(core__ANY, st)
    else:
        return check__Res(core__ANY, st)

def check__infer_all(es: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> tuple[tuple[core__CType, ...], check__St]:
    def _cdy_t255(s: check__St, e: core__Expr) -> tuple[check__St, core__CType]:
        r = check__infer(e, ctx, s)
        return (r.st, r.t)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t255, st, es)
    st1 = _tup[0]
    ts = _tup[1]
    return (ts, st1)

def check__infer_list_of(items: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    rv = check__fresh(st)
    st1 = cdy_rt.primitives.list_fold((lambda s, e: check__infer_expect(e, rv.t, 'List: an item', ctx, s)), rv.st, items)
    return check__Res(core__TCon(core__SYSTEM, 'List', (rv.t,)), st1)

def check__infer_do(body: tuple[core__Expr, ...], ctx: check__Ctx, start: check__Res) -> check__Res:
    return cdy_rt.primitives.list_fold((lambda last, e: check__infer(e, ctx, last.st)), start, body)

def check__infer_holes(parts: tuple[core__FPart, ...], ctx: check__Ctx, start: check__St) -> check__St:
    def _cdy_t257(st: check__St, p: core__FPart) -> check__St:
        _cdy_t256: object = p
        if isinstance(_cdy_t256, core__FHole):
            e = _cdy_t256.expr
            return check__infer(e, ctx, st).st
        else:
            return st
    return cdy_rt.primitives.list_fold(_cdy_t257, start, parts)

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
            count, st, acc = ((count - 1), st._replace(n=(st.n + 1)), (acc + (core__TVar(('?' + str(st.n))),)))
            continue

def check__fresh(st: check__St) -> check__Res:
    return check__Res(core__TVar(('?' + str(st.n))), st._replace(n=(st.n + 1)))

def check__infer_call(callee: core__Expr, args: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    _cdy_t258: object = callee
    if isinstance(_cdy_t258, core__Lambda):
        params = _cdy_t258.params
        body = _cdy_t258.body
        if (len(params) == len(args)):
            return check__typed_callee(callee, args, check__infer_applied(params, body, args, ctx, st))
        else:
            return check__infer_called(callee, args, ctx, st)
    elif isinstance(_cdy_t258, core__Prim):
        name = _cdy_t258.name
        if ((name == 'at') and check__is_tup_item(args)):
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
    _cdy_t259: object = ct
    if isinstance(_cdy_t259, core__TFn):
        params = _cdy_t259.params
        ret = _cdy_t259.ret
        if core__is_variadic(ct):
            if (len(args) < (len(params) - 1)):
                st1 = check__report(('(' + name + ' ...) takes at least ' + str((len(params) - 1)) + ' argument(s), got ' + str(len(args))), ctx, rc.st)
                return check__Res(ret, check__args_st(args, ctx, st1))
            else:
                return check__Res(ret, check__check_args(args, check__spread_rest(params, len(args)), name, ctx, rc.st))
        elif (len(params) != len(args)):
            unit = ('field(s)' if cdy_rt.primitives.map_has(ctx.shapes, check__global_key_of(callee)) else 'argument(s)')
            _cdy_st1_297 = check__report(('(' + name + ' ...) takes ' + str(len(params)) + ' ' + unit + ', got ' + str(len(args))), ctx, rc.st)
            return check__Res(ret, check__args_st(args, ctx, _cdy_st1_297))
        else:
            return check__Res(ret, check__check_args(args, params, name, ctx, rc.st))
    elif isinstance(_cdy_t259, core__TVar):
        v = _cdy_t259.name
        if check__is_flexible(v):
            _tup = check__infer_all(args, ctx, rc.st)
            ts = _tup[0]
            _cdy_st1_301 = _tup[1]
            rr = check__fresh(_cdy_st1_301)
            _cdy__tup_303 = check__unify(ct, core__TFn(ts, rr.t), rr.st.subst)
            _ok = _cdy__tup_303[0]
            s = _cdy__tup_303[1]
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
    _cdy_t260: object = e
    if isinstance(_cdy_t260, core__Lambda):
        return True
    else:
        return False

def check__check_lambda(lam: core__Expr, expected: core__CType, what: str, ctx: check__Ctx, st: check__St) -> check__St:
    _cdy_t261: object = lam
    if isinstance(_cdy_t261, core__Lambda):
        params = _cdy_t261.params
        body = _cdy_t261.body
        _cdy_t262: object = check__prune(expected, st.subst)
        if isinstance(_cdy_t262, core__TFn):
            ptypes = _cdy_t262.params
            ret = _cdy_t262.ret
            if (len(ptypes) == len(params)):
                return check__check_expr(body, ret, (what + "'s result"), ctx._replace(env=check__bind_all(params, ptypes, ctx.env, 0)), check__typed_all(params, ptypes, check__typed(lam, expected, st)))
            else:
                _cdy_r_346 = check__infer(lam, ctx, st)
                return check__expect(expected, _cdy_r_346.t, what, ctx, _cdy_r_346.st)
        else:
            r = check__infer(lam, ctx, st)
            return check__expect(expected, r.t, what, ctx, r.st)
    else:
        return st

def check__global_key_of(e: core__Expr) -> str:
    _cdy_t263: object = e
    if isinstance(_cdy_t263, core__Global):
        m = _cdy_t263.module
        name = _cdy_t263.name
        return core__global_key(m, name)
    else:
        return ''

def check__callee_name(e: core__Expr) -> str:
    _cdy_t264: object = e
    if isinstance(_cdy_t264, core__Global):
        name = _cdy_t264.name
        return name
    elif isinstance(_cdy_t264, core__Prim):
        _cdy_name_353 = _cdy_t264.name
        return _cdy_name_353
    elif isinstance(_cdy_t264, core__Local):
        _cdy_name_354 = _cdy_t264.name
        return _cdy_name_354
    else:
        return 'the function'

def check__is_tup_item(args: tuple[core__Expr, ...]) -> bool:
    return ((len(args) == 2) and (check__tup_name(args[0]) == '_tup') and (check__int_lit(args[1]) >= 0))

def check__tup_name(e: core__Expr) -> str:
    _cdy_t265: object = e
    if isinstance(_cdy_t265, core__Local):
        name = _cdy_t265.name
        return name
    else:
        return ''

def check__int_lit(e: core__Expr) -> int:
    _cdy_t266: object = e
    if isinstance(_cdy_t266, core__Lit):
        form = _cdy_t266.form
        _cdy_t267: object = form
        if isinstance(_cdy_t267, form__IntLit):
            k = _cdy_t267.val
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
    elif (check__tcon_name(tt) != core__global_key(core__SYSTEM, 'Tup')):
        return check__Res(core__ANY, (check__report(('a Tup pattern takes a tuple, not a ' + check__show(tt, r.st.subst)), ctx, r.st) if (i == 0) else r.st))
    elif (i < len(items)):
        return check__Res(cdy_rt.primitives.at(items, i), r.st)
    else:
        return check__Res(core__ANY, check__report(('a ' + check__show(tt, r.st.subst) + ' has ' + str(len(items)) + ' items, not ' + str((i + 1))), ctx, r.st))

def check__tup_items(t: core__CType) -> tuple[core__CType, ...]:
    _cdy_t268: object = t
    if isinstance(_cdy_t268, core__TCon):
        args = _cdy_t268.args
        return args
    else:
        return ()

def check__check_compared(ctx: check__Ctx, start: check__St) -> check__St:
    def _cdy_t269(st: check__St, c: check__Compared) -> check__St:
        t = check__resolve_type(core__TVar(c.var), st.subst)
        if check__has_fn(t, st.subst, ctx, ()):
            return check__report((c.what + ": a function can't be compared, got " + check__show(t, st.subst)), ctx._replace(here=c.here), st)
        else:
            return st
    return cdy_rt.primitives.list_fold(_cdy_t269, start, start.compared)

def check__has_fn(t: core__CType, subst: _cdy_Mapping[str, core__CType], ctx: check__Ctx, seen: tuple[str, ...]) -> bool:
    _cdy_t270: object = check__prune(t, subst)
    if isinstance(_cdy_t270, core__TFn):
        return True
    elif isinstance(_cdy_t270, core__TCon):
        m = _cdy_t270.module
        n = _cdy_t270.name
        args = _cdy_t270.args
        key = core__global_key(m, n)
        return (cdy_rt.primitives.list_any((lambda a: check__has_fn(a, subst, ctx, seen)), args) or ((not cdy_rt.primitives.list_contains(key, seen)) and check__fields_have_fn(key, subst, ctx, (seen + (key,)))))
    else:
        return False

def check__fields_have_fn(name: str, subst: _cdy_Mapping[str, core__CType], ctx: check__Ctx, seen: tuple[str, ...]) -> bool:
    if cdy_rt.primitives.map_has(ctx.shapes, name):
        def _cdy_t271(f: tuple[str, core__CType]) -> bool:
            _tup = f
            _name = _tup[0]
            t = _tup[1]
            return check__has_fn(t, subst, ctx, seen)
        return cdy_rt.primitives.list_any(_cdy_t271, cdy_rt.primitives.map_get(ctx.shapes, name).fields)
    elif cdy_rt.primitives.map_has(ctx.sums, name):
        def _cdy_t272(v: tuple[str, core__CType]) -> bool:
            _tup = v
            variant = _tup[0]
            _t = _tup[1]
            return check__has_fn(check__key_tcon(variant, ()), subst, ctx, seen)
        return cdy_rt.primitives.list_any(_cdy_t272, cdy_rt.primitives.map_get(ctx.sums, name).fields)
    else:
        return False

def check__join_all(types: tuple[core__CType, ...], what: str, ctx: check__Ctx, start: check__Res) -> check__Res:
    return cdy_rt.primitives.list_fold((lambda r, ty: check__join_types(r.t, ty, what, ctx, r.st)), start, prelude__rest(types))

def check__field_of(t: core__CType, field: str, ctx: check__Ctx) -> tuple[bool, core__CType]:
    _cdy_t273: object = t
    if isinstance(_cdy_t273, core__TCon):
        m = _cdy_t273.module
        n = _cdy_t273.name
        args = _cdy_t273.args
        name = core__global_key(m, n)
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
    def _cdy_t274(v: tuple[str, core__CType]) -> tuple[bool, core__CType]:
        _cdy__tup_415 = v
        variant = _cdy__tup_415[0]
        _t = _cdy__tup_415[1]
        return check__field_of(check__key_tcon(variant, args), field, ctx)
    found = cdy_rt.primitives.list_map(_cdy_t274, sum_.fields)
    if (len(found) == 0):
        return (False, core__ANY)
    else:
        _tup = found[0]
        _ok = _tup[0]
        first = _tup[1]
        def _cdy_t275(f: tuple[bool, core__CType]) -> bool:
            _cdy__tup_423 = f
            ok = _cdy__tup_423[0]
            t = _cdy__tup_423[1]
            return (ok and (t == first))
        if cdy_rt.primitives.list_all(_cdy_t275, found):
            return found[0]
        else:
            return (False, core__ANY)

def check__in_every_variant(name: str, field: str, ctx: check__Ctx) -> bool:
    _cdy_t277 = cdy_rt.primitives.map_has(ctx.sums, name)
    if _cdy_t277:
        def _cdy_t276(v: tuple[str, core__CType]) -> bool:
            _tup = v
            variant = _tup[0]
            _t = _tup[1]
            _cdy__tup_433 = check__field_of(check__key_tcon(variant, ()), field, ctx)
            ok = _cdy__tup_433[0]
            _ft = _cdy__tup_433[1]
            return ok
        _cdy_t277 = cdy_rt.primitives.list_all(_cdy_t276, cdy_rt.primitives.map_get(ctx.sums, name).fields)
    return _cdy_t277

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
    _cdy_t278: object = t
    if isinstance(_cdy_t278, core__TVar):
        name = _cdy_t278.name
        if cdy_rt.primitives.map_has(vars_, name):
            return cdy_rt.primitives.map_get(vars_, name)
        else:
            return t
    elif isinstance(_cdy_t278, core__TCon):
        m = _cdy_t278.module
        _cdy_name_449 = _cdy_t278.name
        args = _cdy_t278.args
        return core__TCon(m, _cdy_name_449, cdy_rt.primitives.list_map((lambda a: check__put_vars(a, vars_)), args))
    else:
        assert isinstance(_cdy_t278, core__TFn)
        params = _cdy_t278.params
        ret = _cdy_t278.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__put_vars(p, vars_)), params), check__put_vars(ret, vars_))

def check__infer_field(obj: core__Expr, field: str, ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(obj, ctx, st)
    ot = check__prune(r.t, r.st.subst)
    return check__field_type(ot, obj, field, 'get', ctx, r.st)

def check__field_type(ot0: core__CType, obj: core__Expr, field: str, what: str, ctx: check__Ctx, st: check__St) -> check__Res:
    ot = check__narrow(ot0, obj, ctx)
    _cdy_t279: object = ot
    if isinstance(_cdy_t279, core__TVar):
        v = _cdy_t279.name
        if check__is_flexible(v):
            r = check__fresh(st)
            p = check__Pending(obj, field, what, ot, r.t, ctx.here)
            return check__Res(r.t, r.st._replace(pending=(r.st.pending + (p,))))
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
    _cdy_t281: object = obj
    if isinstance(_cdy_t281, core__Local):
        _cdy_t280 = check__local_key(obj)
    else:
        _cdy_t280 = ''
    key = _cdy_t280
    if cdy_rt.primitives.map_has(ctx.narrowed, key):
        variant = cdy_rt.primitives.map_get(ctx.narrowed, key)
        _cdy_t282: object = ot
        if isinstance(_cdy_t282, core__TCon):
            m = _cdy_t282.module
            name = _cdy_t282.name
            args = _cdy_t282.args
            if (core__global_key(m, name) == cdy_rt.primitives.map_get(ctx.shapes, variant).sum_):
                return check__key_tcon(variant, args)
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
    def _cdy_t283(acc: tuple[check__St, tuple[check__Pending, ...]], p: check__Pending) -> tuple[check__St, tuple[check__Pending, ...]]:
        _tup = acc
        st = _tup[0]
        _cdy_left_496 = _tup[1]
        on = check__prune(p.on, st.subst)
        if cdy_rt.primitives.map_has(st.subst, ('any' + check__tvar_name(on))):
            return (st._replace(subst=check__mark_any(p.t, st.subst)), _cdy_left_496)
        elif check__is_var(on):
            return (st, (_cdy_left_496 + (p,)))
        else:
            c = ctx._replace(here=p.here)
            r = check__field_type(on, p.obj, p.field, p.what, c, st)
            what = (p.what + ': field ' + p.field + ' of ' + check__show(on, r.st.subst))
            return (check__expect_is(p.t, r.t, what, c, r.st), _cdy_left_496)
    return cdy_rt.primitives.list_fold(_cdy_t283, (start, left), ps)

def check__report_pending(ps: tuple[check__Pending, ...], ctx: check__Ctx, start: check__St) -> check__St:
    return cdy_rt.primitives.list_fold((lambda st, p: check__report((p.what + ': the type of ' + check__callee_name(p.obj) + " isn't known here (" + p.field + ')'), ctx._replace(here=p.here), st)), start, ps)

def check__tcon_name(t: core__CType) -> str:
    _cdy_t284: object = t
    if isinstance(_cdy_t284, core__TCon):
        m = _cdy_t284.module
        name = _cdy_t284.name
        return core__global_key(m, name)
    else:
        return ''

def check__infer_assoc(obj: core__Expr, fields: tuple[tuple[str, core__Expr], ...], ctx: check__Ctx, st: check__St) -> check__Res:
    r = check__infer(obj, ctx, st)
    ot = check__prune(r.t, r.st.subst)
    return check__Res(r.t, check__assoc_values(ot, obj, fields, ctx, r.st))

def check__assoc_values(ot: core__CType, obj: core__Expr, fields: tuple[tuple[str, core__Expr], ...], ctx: check__Ctx, start: check__St) -> check__St:
    def _cdy_t285(st: check__St, f: tuple[str, core__Expr]) -> check__St:
        _tup = f
        field = _tup[0]
        val = _tup[1]
        ft = check__field_type(ot, obj, field, 'assoc', ctx, st)
        return check__check_expr(val, ft.t, ('assoc: field ' + field + ' of ' + check__show(ot, st.subst)), ctx, ft.st)
    return cdy_rt.primitives.list_fold(_cdy_t285, start, fields)

def check__infer_match(subject: core__Expr, clauses: tuple[core__Clause, ...], default: tuple[core__Expr, ...], ctx: check__Ctx, st: check__St) -> check__Res:
    rs = check__infer(subject, ctx, st)
    variant = check__clause_key(clauses[0])
    sum_ = (cdy_rt.primitives.map_get(ctx.shapes, variant).sum_ if cdy_rt.primitives.map_has(ctx.shapes, variant) else '')
    tvars = (cdy_rt.primitives.map_get(ctx.sums, sum_).tvars if cdy_rt.primitives.map_has(ctx.sums, sum_) else ())
    _tup = check__fresh_types(len(tvars), rs.st, ())
    ftypes = _tup[0]
    st0 = _tup[1]
    vars_ = check__zip_map(tvars, ftypes, {})
    want = check__key_tcon(sum_, ftypes)
    st1 = check__expect_is(want, rs.t, 'match: the subject', ctx, st0)
    _cdy__tup_541 = check__infer_clauses(subject, clauses, vars_, ctx, st1)
    ctypes = _cdy__tup_541[0]
    st2 = _cdy__tup_541[1]
    if (len(default) == 0):
        return check__join_all(ctypes, 'match: the clauses', ctx, check__Res(ctypes[0], st2))
    else:
        rd = check__infer(default[0], ctx, st2)
        return check__join_all((ctypes + (rd.t,)), 'match: the clauses', ctx, check__Res(ctypes[0], rd.st))

def check__infer_clauses(subject: core__Expr, clauses: tuple[core__Clause, ...], vars_: _cdy_Mapping[str, core__CType], ctx: check__Ctx, st: check__St) -> tuple[tuple[core__CType, ...], check__St]:
    def _cdy_t288(s: check__St, c: core__Clause) -> tuple[check__St, core__CType]:
        shape = (cdy_rt.primitives.map_get(ctx.shapes, check__clause_key(c)) if cdy_rt.primitives.map_has(ctx.shapes, check__clause_key(c)) else check__Shape((), (), ''))
        bound = ctx._replace(env=check__bind_fields(c.binds, shape.fields, vars_, ctx.env))
        _cdy_t287: object = subject
        if isinstance(_cdy_t287, core__Local):
            _cdy_t286 = bound._replace(narrowed=cdy_rt.primitives.map_set(ctx.narrowed, check__local_key(subject), check__clause_key(c)))
        else:
            _cdy_t286 = bound
        inner = _cdy_t286
        r = check__infer(c.body, inner, check__typed_binds(c.binds, inner.env, s))
        return (r.st, r.t)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t288, st, clauses)
    st1 = _tup[0]
    ts = _tup[1]
    return (ts, st1)

def check__clause_key(c: core__Clause) -> str:
    return core__global_key(c.module, c.variant)

def check__bind_fields(binds: tuple[tuple[str, core__Expr], ...], fields: tuple[tuple[str, core__CType], ...], vars_: _cdy_Mapping[str, core__CType], start: _cdy_Mapping[str, core__CType]) -> _cdy_Mapping[str, core__CType]:
    def _cdy_t289(env: _cdy_Mapping[str, core__CType], b: tuple[str, core__Expr]) -> _cdy_Mapping[str, core__CType]:
        _tup = b
        field = _tup[0]
        loc = _tup[1]
        _cdy__tup_569 = check__find_field(fields, field, vars_)
        found = _cdy__tup_569[0]
        ft = _cdy__tup_569[1]
        return cdy_rt.primitives.map_set(env, check__local_key(loc), (ft if found else core__ANY))
    return cdy_rt.primitives.list_fold(_cdy_t289, start, binds)

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
    def _cdy_t290(st: check__St, b: tuple[str, core__Expr]) -> check__St:
        _tup = b
        _field = _tup[0]
        loc = _tup[1]
        return check__typed(loc, (cdy_rt.primitives.map_get(env, check__local_key(loc)) if cdy_rt.primitives.map_has(env, check__local_key(loc)) else core__ANY), st)
    return cdy_rt.primitives.list_fold(_cdy_t290, start, binds)

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
    _cdy_t291: object = check__prune(t, subst)
    if isinstance(_cdy_t291, core__TCon):
        m = _cdy_t291.module
        name = _cdy_t291.name
        args = _cdy_t291.args
        return core__TCon(m, name, cdy_rt.primitives.list_map((lambda a: check__final_type(a, subst)), args))
    elif isinstance(_cdy_t291, core__TFn):
        params = _cdy_t291.params
        ret = _cdy_t291.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__final_type(p, subst)), params), check__final_type(ret, subst))
    else:
        assert isinstance(_cdy_t291, core__TVar)
        _cdy_name_606 = _cdy_t291.name
        if cdy_rt.primitives.map_has(subst, ('any' + _cdy_name_606)):
            return core__ANY
        else:
            return core__TVar(_cdy_name_606)

def check__retype_top(top: core__Top, f: _cdy_Callable[[core__CType, int], core__CType]) -> core__Top:
    _cdy_t292: object = top
    if isinstance(_cdy_t292, core__TDef):
        m = _cdy_t292.module
        name = _cdy_t292.name
        init = _cdy_t292.init
        t = _cdy_t292.t
        pos = _cdy_t292.pos
        _tup = check__retype(init, f, 0)
        e = _tup[0]
        _n = _tup[1]
        return core__TDef(m, name, e, t, pos)
    elif isinstance(_cdy_t292, core__TDefn):
        _cdy_m_617 = _cdy_t292.module
        _cdy_name_618 = _cdy_t292.name
        params = _cdy_t292.params
        body = _cdy_t292.body
        _cdy_t_621 = _cdy_t292.t
        _cdy_pos_622 = _cdy_t292.pos
        _cdy__tup_623 = check__retype_all(params, f, 0)
        ps = _cdy__tup_623[0]
        n1 = _cdy__tup_623[1]
        _cdy__tup_626 = check__retype(body, f, n1)
        b = _cdy__tup_626[0]
        _ = _cdy__tup_626[1]
        return core__TDefn(_cdy_m_617, _cdy_name_618, ps, b, _cdy_t_621, _cdy_pos_622)
    elif isinstance(_cdy_t292, core__TExpr):
        _cdy_e_629 = _cdy_t292.expr
        _cdy__tup_630 = check__retype(_cdy_e_629, f, 0)
        e1 = _cdy__tup_630[0]
        _cdy__n_632 = _cdy__tup_630[1]
        return core__TExpr(e1)
    else:
        return top

def check__retype(e: core__Expr, f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[core__Expr, int]:
    k = (n + 1)
    _cdy_t293: object = e
    if isinstance(_cdy_t293, core__Lit):
        form = _cdy_t293.form
        t = _cdy_t293.t
        return (core__Lit(form, f(t, n)), k)
    elif isinstance(_cdy_t293, core__Local):
        name = _cdy_t293.name
        id_ = _cdy_t293.id_
        pos = _cdy_t293.pos
        _cdy_t_642 = _cdy_t293.t
        return (core__Local(name, id_, pos, f(_cdy_t_642, n)), k)
    elif isinstance(_cdy_t293, core__Global):
        m = _cdy_t293.module
        _cdy_name_644 = _cdy_t293.name
        _cdy_pos_645 = _cdy_t293.pos
        _cdy_t_646 = _cdy_t293.t
        return (core__Global(m, _cdy_name_644, _cdy_pos_645, f(_cdy_t_646, n)), k)
    elif isinstance(_cdy_t293, core__Prim):
        _cdy_name_647 = _cdy_t293.name
        _cdy_pos_648 = _cdy_t293.pos
        _cdy_t_649 = _cdy_t293.t
        return (core__Prim(_cdy_name_647, _cdy_pos_648, f(_cdy_t_649, n)), k)
    elif isinstance(_cdy_t293, core__Temp):
        _cdy_id__650 = _cdy_t293.id_
        _cdy_t_651 = _cdy_t293.t
        return (core__Temp(_cdy_id__650, f(_cdy_t_651, n)), k)
    elif isinstance(_cdy_t293, core__Call):
        callee = _cdy_t293.callee
        args = _cdy_t293.args
        _cdy_pos_654 = _cdy_t293.pos
        _cdy_t_655 = _cdy_t293.t
        _tup = check__retype(callee, f, k)
        c = _tup[0]
        n1 = _tup[1]
        _cdy__tup_659 = check__retype_all(args, f, n1)
        xs = _cdy__tup_659[0]
        n2 = _cdy__tup_659[1]
        return (core__Call(c, xs, _cdy_pos_654, f(_cdy_t_655, n)), n2)
    elif isinstance(_cdy_t293, core__If):
        test = _cdy_t293.test
        then = _cdy_t293.then
        other = _cdy_t293.other
        _cdy_pos_665 = _cdy_t293.pos
        _cdy_t_666 = _cdy_t293.t
        _cdy__tup_667 = check__retype(test, f, k)
        a = _cdy__tup_667[0]
        _cdy_n1_669 = _cdy__tup_667[1]
        _cdy__tup_670 = check__retype(then, f, _cdy_n1_669)
        b = _cdy__tup_670[0]
        _cdy_n2_672 = _cdy__tup_670[1]
        _cdy__tup_673 = check__retype(other, f, _cdy_n2_672)
        _cdy_c_674 = _cdy__tup_673[0]
        n3 = _cdy__tup_673[1]
        return (core__If(a, b, _cdy_c_674, _cdy_pos_665, f(_cdy_t_666, n)), n3)
    elif isinstance(_cdy_t293, core__Do):
        body = _cdy_t293.body
        _cdy_pos_677 = _cdy_t293.pos
        _cdy_t_678 = _cdy_t293.t
        _cdy__tup_679 = check__retype_all(body, f, k)
        _cdy_xs_680 = _cdy__tup_679[0]
        _cdy_n1_681 = _cdy__tup_679[1]
        return (core__Do(_cdy_xs_680, _cdy_pos_677, f(_cdy_t_678, n)), _cdy_n1_681)
    elif isinstance(_cdy_t293, core__Lambda):
        params = _cdy_t293.params
        _cdy_body_683 = _cdy_t293.body
        _cdy_pos_684 = _cdy_t293.pos
        _cdy_t_685 = _cdy_t293.t
        _cdy__tup_686 = check__retype_all(params, f, k)
        ps = _cdy__tup_686[0]
        _cdy_n1_688 = _cdy__tup_686[1]
        _cdy__tup_689 = check__retype(_cdy_body_683, f, _cdy_n1_688)
        _cdy_b_690 = _cdy__tup_689[0]
        _cdy_n2_691 = _cdy__tup_689[1]
        return (core__Lambda(ps, _cdy_b_690, _cdy_pos_684, f(_cdy_t_685, n)), _cdy_n2_691)
    elif isinstance(_cdy_t293, core__Tuple):
        items = _cdy_t293.items
        _cdy_pos_693 = _cdy_t293.pos
        _cdy_t_694 = _cdy_t293.t
        _cdy__tup_695 = check__retype_all(items, f, k)
        _cdy_xs_696 = _cdy__tup_695[0]
        _cdy_n1_697 = _cdy__tup_695[1]
        return (core__Tuple(_cdy_xs_696, _cdy_pos_693, f(_cdy_t_694, n)), _cdy_n1_697)
    elif isinstance(_cdy_t293, core__ListOf):
        _cdy_items_698 = _cdy_t293.items
        _cdy_pos_699 = _cdy_t293.pos
        _cdy_t_700 = _cdy_t293.t
        _cdy__tup_701 = check__retype_all(_cdy_items_698, f, k)
        _cdy_xs_702 = _cdy__tup_701[0]
        _cdy_n1_703 = _cdy__tup_701[1]
        return (core__ListOf(_cdy_xs_702, _cdy_pos_699, f(_cdy_t_700, n)), _cdy_n1_703)
    elif isinstance(_cdy_t293, core__Fmt):
        parts = _cdy_t293.parts
        _cdy_pos_705 = _cdy_t293.pos
        _cdy_t_706 = _cdy_t293.t
        _cdy__tup_707 = check__retype_parts(parts, f, k)
        _cdy_ps_708 = _cdy__tup_707[0]
        _cdy_n1_709 = _cdy__tup_707[1]
        return (core__Fmt(_cdy_ps_708, _cdy_pos_705, f(_cdy_t_706, n)), _cdy_n1_709)
    elif isinstance(_cdy_t293, core__Field):
        obj = _cdy_t293.obj
        field = _cdy_t293.field
        _cdy_pos_712 = _cdy_t293.pos
        _cdy_t_713 = _cdy_t293.t
        _cdy__tup_714 = check__retype(obj, f, k)
        o = _cdy__tup_714[0]
        _cdy_n1_716 = _cdy__tup_714[1]
        return (core__Field(o, field, _cdy_pos_712, f(_cdy_t_713, n)), _cdy_n1_716)
    elif isinstance(_cdy_t293, core__Assoc):
        _cdy_obj_717 = _cdy_t293.obj
        fields = _cdy_t293.fields
        _cdy_pos_719 = _cdy_t293.pos
        _cdy_t_720 = _cdy_t293.t
        _cdy__tup_721 = check__retype(_cdy_obj_717, f, k)
        _cdy_o_722 = _cdy__tup_721[0]
        _cdy_n1_723 = _cdy__tup_721[1]
        _cdy__tup_724 = check__retype_pairs(fields, f, _cdy_n1_723)
        fs = _cdy__tup_724[0]
        _cdy_n2_726 = _cdy__tup_724[1]
        return (core__Assoc(_cdy_o_722, fs, _cdy_pos_719, f(_cdy_t_720, n)), _cdy_n2_726)
    else:
        assert isinstance(_cdy_t293, core__MatchE)
        subject = _cdy_t293.subject
        clauses = _cdy_t293.clauses
        default = _cdy_t293.default
        _cdy_pos_730 = _cdy_t293.pos
        _cdy_t_731 = _cdy_t293.t
        _cdy__tup_732 = check__retype(subject, f, k)
        s = _cdy__tup_732[0]
        _cdy_n1_734 = _cdy__tup_732[1]
        _cdy__tup_735 = check__retype_clauses(clauses, f, _cdy_n1_734)
        cs = _cdy__tup_735[0]
        _cdy_n2_737 = _cdy__tup_735[1]
        _cdy__tup_738 = check__retype_all(default, f, _cdy_n2_737)
        d = _cdy__tup_738[0]
        _cdy_n3_740 = _cdy__tup_738[1]
        return (core__MatchE(s, cs, d, _cdy_pos_730, f(_cdy_t_731, n)), _cdy_n3_740)

def check__retype_all(es: tuple[core__Expr, ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[core__Expr, ...], int]:
    def _cdy_t294(k: int, e: core__Expr) -> tuple[int, core__Expr]:
        _cdy__tup_746 = check__retype(e, f, k)
        e1 = _cdy__tup_746[0]
        k1 = _cdy__tup_746[1]
        return (k1, e1)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t294, n, es)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__retype_pairs(pairs: tuple[tuple[str, core__Expr], ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[tuple[str, core__Expr], ...], int]:
    def _cdy_t295(k: int, pair: tuple[str, core__Expr]) -> tuple[int, tuple[str, core__Expr]]:
        _cdy__tup_757 = pair
        name = _cdy__tup_757[0]
        e = _cdy__tup_757[1]
        _cdy__tup_760 = check__retype(e, f, k)
        e1 = _cdy__tup_760[0]
        k1 = _cdy__tup_760[1]
        return (k1, (name, e1))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t295, n, pairs)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__retype_parts(parts: tuple[core__FPart, ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[core__FPart, ...], int]:
    def _cdy_t297(k: int, part: core__FPart) -> tuple[int, core__FPart]:
        _cdy_t296: object = part
        if isinstance(_cdy_t296, core__FHole):
            e = _cdy_t296.expr
            _cdy__tup_772 = check__retype(e, f, k)
            e1 = _cdy__tup_772[0]
            k1 = _cdy__tup_772[1]
            return (k1, core__FHole(e1))
        else:
            return (k, part)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t297, n, parts)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__retype_clauses(clauses: tuple[core__Clause, ...], f: _cdy_Callable[[core__CType, int], core__CType], n: int) -> tuple[tuple[core__Clause, ...], int]:
    def _cdy_t298(k: int, c: core__Clause) -> tuple[int, core__Clause]:
        _cdy__tup_783 = check__retype_pairs(c.binds, f, k)
        bs = _cdy__tup_783[0]
        k1 = _cdy__tup_783[1]
        _cdy__tup_786 = check__retype(c.body, f, k1)
        b = _cdy__tup_786[0]
        k2 = _cdy__tup_786[1]
        return (k2, core__Clause(c.module, c.variant, bs, b))
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t298, n, clauses)
    n1 = _tup[0]
    out = _tup[1]
    return (out, n1)

def check__is_flexible(name: str) -> bool:
    return cdy_rt.primitives.starts_with(name, '?')

def check__prune(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> core__CType:
    while True:
        _cdy_t299: object = t
        if isinstance(_cdy_t299, core__TVar):
            name = _cdy_t299.name
            if cdy_rt.primitives.map_has(subst, name):
                t = cdy_rt.primitives.map_get(subst, name)
                continue
            else:
                return t
        else:
            return t

def check__resolve_type(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> core__CType:
    _cdy_t300: object = check__prune(t, subst)
    if isinstance(_cdy_t300, core__TCon):
        m = _cdy_t300.module
        name = _cdy_t300.name
        args = _cdy_t300.args
        return core__TCon(m, name, cdy_rt.primitives.list_map((lambda a: check__resolve_type(a, subst)), args))
    elif isinstance(_cdy_t300, core__TFn):
        params = _cdy_t300.params
        ret = _cdy_t300.ret
        return core__TFn(cdy_rt.primitives.list_map((lambda p: check__resolve_type(p, subst)), params), check__resolve_type(ret, subst))
    else:
        return check__prune(t, subst)

def check__occurs(v: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> bool:
    _cdy_t301: object = check__prune(t, subst)
    if isinstance(_cdy_t301, core__TVar):
        name = _cdy_t301.name
        return (name == v)
    elif isinstance(_cdy_t301, core__TCon):
        args = _cdy_t301.args
        return cdy_rt.primitives.list_any((lambda a: check__occurs(v, a, subst)), args)
    else:
        assert isinstance(_cdy_t301, core__TFn)
        params = _cdy_t301.params
        ret = _cdy_t301.ret
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
            _cdy_t302: object = pa
            if isinstance(_cdy_t302, core__TVar):
                name = _cdy_t302.name
                _cdy_t304: object = pb
                if isinstance(_cdy_t304, core__TVar):
                    other = _cdy_t304.name
                    _cdy_t303 = (name == other)
                else:
                    _cdy_t303 = False
                return (_cdy_t303, subst)
            elif isinstance(_cdy_t302, core__TCon):
                m = _cdy_t302.module
                _cdy_name_822 = _cdy_t302.name
                args = _cdy_t302.args
                _cdy_t305: object = pb
                if isinstance(_cdy_t305, core__TCon):
                    bm = _cdy_t305.module
                    _cdy_other_825 = _cdy_t305.name
                    bargs = _cdy_t305.args
                    if ((m == bm) and (_cdy_name_822 == _cdy_other_825) and (len(args) == len(bargs))):
                        return check__unify_all(args, bargs, subst)
                    else:
                        return (False, subst)
                else:
                    return (False, subst)
            else:
                assert isinstance(_cdy_t302, core__TFn)
                params = _cdy_t302.params
                ret = _cdy_t302.ret
                _cdy_t306: object = pb
                if isinstance(_cdy_t306, core__TFn):
                    bparams = _cdy_t306.params
                    bret = _cdy_t306.ret
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
    _cdy_t307: object = check__prune(t, subst)
    if isinstance(_cdy_t307, core__TVar):
        name = _cdy_t307.name
        if check__is_flexible(name):
            return cdy_rt.primitives.map_set(subst, ('any' + name), core__ANY)
        else:
            return subst
    elif isinstance(_cdy_t307, core__TCon):
        args = _cdy_t307.args
        return cdy_rt.primitives.list_fold((lambda s, a: check__mark_any(a, s)), subst, args)
    else:
        assert isinstance(_cdy_t307, core__TFn)
        params = _cdy_t307.params
        ret = _cdy_t307.ret
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
    _cdy_t309: object = t
    if isinstance(_cdy_t309, core__TVar):
        other = _cdy_t309.name
        _cdy_t308 = (other == v)
    else:
        _cdy_t308 = False
    if _cdy_t308:
        return (True, subst)
    elif check__occurs(v, t, subst):
        return (False, subst)
    elif (core__constraint_of(v) == ''):
        return (True, cdy_rt.primitives.map_set(subst, v, t))
    else:
        return check__bind_constrained(v, core__constraint_of(v), t, subst)

def check__bind_constrained(v: str, c: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    if (c == 'equatable'):
        return check__bind_equatable(v, t, subst)
    else:
        return check__bind_listed(v, c, t, subst)

def check__bind_listed(v: str, c: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    takes = cdy_rt.primitives.map_get(core__CONSTRAINTS, c)
    _cdy_t310: object = t
    if isinstance(_cdy_t310, core__TCon):
        m = _cdy_t310.module
        name = _cdy_t310.name
        if ((m == core__SYSTEM) and cdy_rt.primitives.list_contains(name, takes)):
            return (True, cdy_rt.primitives.map_set(subst, v, t))
        else:
            return (False, subst)
    elif isinstance(_cdy_t310, core__TVar):
        other = _cdy_t310.name
        oc = core__constraint_of(other)
        if (not check__is_flexible(other)):
            if ((oc != '') and check__within(oc, c)):
                return (True, cdy_rt.primitives.map_set(subst, v, t))
            else:
                return (False, subst)
        elif (oc == ''):
            return (True, cdy_rt.primitives.map_set(subst, other, core__TVar(v)))
        elif (oc == 'equatable'):
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

def check__bind_equatable(v: str, t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> tuple[bool, _cdy_Mapping[str, core__CType]]:
    _cdy_t311: object = t
    if isinstance(_cdy_t311, core__TVar):
        other = _cdy_t311.name
        oc = core__constraint_of(other)
        if (not check__is_flexible(other)):
            if ((oc != '') and check__within(oc, 'equatable')):
                return (True, cdy_rt.primitives.map_set(subst, v, t))
            else:
                return (False, subst)
        elif (oc == ''):
            return (True, cdy_rt.primitives.map_set(subst, other, core__TVar(v)))
        else:
            return (True, cdy_rt.primitives.map_set(subst, v, t))
    else:
        return (True, cdy_rt.primitives.map_set(subst, v, t))

def check__within(a: str, b: str) -> bool:
    if (b == 'equatable'):
        return (a != 'appendable')
    elif (a == 'equatable'):
        return False
    else:
        return cdy_rt.primitives.list_all((lambda x: cdy_rt.primitives.list_contains(x, cdy_rt.primitives.map_get(core__CONSTRAINTS, b))), cdy_rt.primitives.map_get(core__CONSTRAINTS, a))

def check__is_any(t: core__CType) -> bool:
    _cdy_t312: object = t
    if isinstance(_cdy_t312, core__TCon):
        m = _cdy_t312.module
        name = _cdy_t312.name
        return ((m == core__SYSTEM) and (name == 'Any'))
    else:
        return False

def check__is_var(t: core__CType) -> bool:
    _cdy_t313: object = t
    if isinstance(_cdy_t313, core__TVar):
        name = _cdy_t313.name
        return check__is_flexible(name)
    else:
        return False

def check__tvar_name(t: core__CType) -> str:
    _cdy_t314: object = t
    if isinstance(_cdy_t314, core__TVar):
        name = _cdy_t314.name
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
    _cdy_t315: object = t
    if isinstance(_cdy_t315, core__TVar):
        name = _cdy_t315.name
        if (check__is_flexible(name) or cdy_rt.primitives.list_contains(name, acc)):
            return acc
        else:
            return (acc + (name,))
    elif isinstance(_cdy_t315, core__TCon):
        args = _cdy_t315.args
        return cdy_rt.primitives.list_fold((lambda a, x: check__rigid_vars(x, a)), acc, args)
    else:
        assert isinstance(_cdy_t315, core__TFn)
        params = _cdy_t315.params
        ret = _cdy_t315.ret
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
cdy_rt.primitives.register_type(check__Order, 'Order', (), (('Map', 'String', 'String'), ('Map', 'String', 'core.Expr')))

def check__order_of(tops: tuple[core__Top, ...]) -> check__Order:
    def _cdy_t317(o: check__Order, top: core__Top) -> check__Order:
        _cdy_t316: object = top
        if isinstance(_cdy_t316, core__TDef):
            m = _cdy_t316.module
            name = _cdy_t316.name
            return o._replace(kinds=cdy_rt.primitives.map_set(o.kinds, core__global_key(m, name), 'def'))
        elif isinstance(_cdy_t316, core__TDefn):
            _cdy_m_944 = _cdy_t316.module
            _cdy_name_945 = _cdy_t316.name
            body = _cdy_t316.body
            key = core__global_key(_cdy_m_944, _cdy_name_945)
            return check__Order(cdy_rt.primitives.map_set(o.kinds, key, 'defn'), cdy_rt.primitives.map_set(o.bodies, key, body))
        else:
            return cdy_rt.primitives.list_fold((lambda o2, n: o2._replace(kinds=cdy_rt.primitives.map_set(o2.kinds, n, 'deft'))), o, check__defined_by(top))
    return cdy_rt.primitives.list_fold(_cdy_t317, check__Order({}, {}), tops)

def check__defined_by(top: core__Top) -> tuple[str, ...]:
    _cdy_t318: object = top
    if isinstance(_cdy_t318, core__TDeft):
        m = _cdy_t318.module
        name = _cdy_t318.name
        return (core__global_key(m, name),)
    elif isinstance(_cdy_t318, core__TDeftSum):
        _cdy_m_953 = _cdy_t318.module
        variants = _cdy_t318.variants
        return cdy_rt.primitives.list_map((lambda v: core__global_key(_cdy_m_953, v.name)), variants)
    elif isinstance(_cdy_t318, core__TDef):
        _cdy_m_956 = _cdy_t318.module
        _cdy_name_957 = _cdy_t318.name
        return (core__global_key(_cdy_m_956, _cdy_name_957),)
    elif isinstance(_cdy_t318, core__TDefn):
        _cdy_m_958 = _cdy_t318.module
        _cdy_name_959 = _cdy_t318.name
        return (core__global_key(_cdy_m_958, _cdy_name_959),)
    else:
        assert isinstance(_cdy_t318, core__TExpr)
        return ()

def check__check_order(tops: tuple[core__Top, ...], order: check__Order, start: _cdy_Mapping[str, bool]) -> tuple[str, ...]:
    def _cdy_t322(defined: _cdy_Mapping[str, bool], top: core__Top) -> tuple[_cdy_Mapping[str, bool], tuple[str, ...]]:
        _cdy_t321 = cdy_rt.primitives.list_fold((lambda d, n: cdy_rt.primitives.map_set(d, n, True)), defined, check__defined_by(top))
        _cdy_t320: object = top
        if isinstance(_cdy_t320, core__TDef):
            init = _cdy_t320.init
            _cdy_t319 = check__order_errors(init, order, defined)
        elif isinstance(_cdy_t320, core__TExpr):
            e = _cdy_t320.expr
            _cdy_t319 = check__order_errors(e, order, defined)
        else:
            _cdy_t319 = ()
        return (_cdy_t321, _cdy_t319)
    _tup = cdy_rt.primitives.list_map_acc(_cdy_t322, start, tops)
    _defined = _tup[0]
    errors = _tup[1]
    return cdy_rt.primitives.list_concat(errors)

def check__order_errors(e: core__Expr, order: check__Order, defined: _cdy_Mapping[str, bool]) -> tuple[str, ...]:
    def _cdy_t323(u: tuple[str, form__Pos]) -> tuple[str, ...]:
        _tup = u
        name = _tup[0]
        pos = _tup[1]
        reached = check__reach((name,), order, cdy_rt.primitives.map_from(((name, True),)))
        return cdy_rt.primitives.list_map((lambda n: (form__pos_text(pos) + check__used_early(n, name, order))), cdy_rt.primitives.list_filter((lambda n: (cdy_rt.primitives.map_has(order.kinds, n) and (not cdy_rt.primitives.map_has(defined, n)))), cdy_rt.primitives.map_keys(reached)))
    return cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(_cdy_t323, check__uses(e, ())))

def check__used_early(n: str, name: str, order: check__Order) -> str:
    through = ('' if (n == name) else (', through ' + check__shown_name(name)))
    return (check__shown_name(n) + ' is used before its ' + cdy_rt.primitives.map_get(order.kinds, n) + through)

def check__reach(todo: tuple[str, ...], order: check__Order, seen: _cdy_Mapping[str, bool]) -> _cdy_Mapping[str, bool]:
    if (len(todo) == 0):
        return seen
    else:
        name = todo[0]
        if cdy_rt.primitives.map_has(order.bodies, name):
            _cdy_t325 = (lambda n: (not cdy_rt.primitives.map_has(seen, n)))
            def _cdy_t324(u: tuple[str, form__Pos]) -> str:
                _tup = u
                n = _tup[0]
                _pos = _tup[1]
                return n
            _cdy_t326 = cdy_rt.primitives.list_filter(_cdy_t325, cdy_rt.primitives.list_map(_cdy_t324, check__uses(cdy_rt.primitives.map_get(order.bodies, name), ())))
        else:
            _cdy_t326 = ()
        found = _cdy_t326
        return check__reach((prelude__rest(todo) + found), order, cdy_rt.primitives.list_fold((lambda m, n: cdy_rt.primitives.map_set(m, n, True)), seen, found))

def check__uses(e: core__Expr, acc: tuple[tuple[str, form__Pos], ...]) -> tuple[tuple[str, form__Pos], ...]:
    _cdy_t327: object = e
    if isinstance(_cdy_t327, core__Global):
        m = _cdy_t327.module
        name = _cdy_t327.name
        pos = _cdy_t327.pos
        return (acc + ((core__global_key(m, name), pos),))
    elif isinstance(_cdy_t327, core__Call):
        callee = _cdy_t327.callee
        args = _cdy_t327.args
        return check__uses_all(args, check__uses(callee, acc))
    elif isinstance(_cdy_t327, core__If):
        test = _cdy_t327.test
        then = _cdy_t327.then
        other = _cdy_t327.other
        return check__uses(other, check__uses(then, check__uses(test, acc)))
    elif isinstance(_cdy_t327, core__Do):
        body = _cdy_t327.body
        return check__uses_all(body, acc)
    elif isinstance(_cdy_t327, core__Lambda):
        _cdy_body_1009 = _cdy_t327.body
        return check__uses(_cdy_body_1009, acc)
    elif isinstance(_cdy_t327, core__Tuple):
        items = _cdy_t327.items
        return check__uses_all(items, acc)
    elif isinstance(_cdy_t327, core__ListOf):
        _cdy_items_1011 = _cdy_t327.items
        return check__uses_all(_cdy_items_1011, acc)
    elif isinstance(_cdy_t327, core__Fmt):
        parts = _cdy_t327.parts
        def _cdy_t329(a: tuple[tuple[str, form__Pos], ...], p: core__FPart) -> tuple[tuple[str, form__Pos], ...]:
            _cdy_t328: object = p
            if isinstance(_cdy_t328, core__FHole):
                x = _cdy_t328.expr
                return check__uses(x, a)
            else:
                return a
        return cdy_rt.primitives.list_fold(_cdy_t329, acc, parts)
    elif isinstance(_cdy_t327, core__Field):
        obj = _cdy_t327.obj
        return check__uses(obj, acc)
    elif isinstance(_cdy_t327, core__Assoc):
        _cdy_obj_1017 = _cdy_t327.obj
        fields = _cdy_t327.fields
        def _cdy_t330(f: tuple[str, core__Expr]) -> core__Expr:
            _tup = f
            _name = _tup[0]
            v = _tup[1]
            return v
        return check__uses_all(cdy_rt.primitives.list_map(_cdy_t330, fields), check__uses(_cdy_obj_1017, acc))
    elif isinstance(_cdy_t327, core__MatchE):
        subject = _cdy_t327.subject
        clauses = _cdy_t327.clauses
        default = _cdy_t327.default
        return check__uses_all(default, check__uses_all(cdy_rt.primitives.list_map((lambda c: c.body), clauses), check__uses(subject, acc)))
    else:
        return acc

def check__uses_all(es: tuple[core__Expr, ...], acc: tuple[tuple[str, form__Pos], ...]) -> tuple[tuple[str, form__Pos], ...]:
    return cdy_rt.primitives.list_fold((lambda a, x: check__uses(x, a)), acc, es)

def check__report(msg: str, ctx: check__Ctx, st: check__St) -> check__St:
    return st._replace(errors=(st.errors + ((form__pos_text(ctx.here) + msg),)))

def check__show(t: core__CType, subst: _cdy_Mapping[str, core__CType]) -> str:
    _cdy_t331: object = check__resolve_type(t, subst)
    if isinstance(_cdy_t331, core__TCon):
        name = _cdy_t331.name
        args = _cdy_t331.args
        if (len(args) == 0):
            return name
        else:
            return ('(' + name + ' ' + cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda a: check__show(a, subst)), args), ' ') + ')')
    elif isinstance(_cdy_t331, core__TFn):
        params = _cdy_t331.params
        ret = _cdy_t331.ret
        return ('(Fn (' + cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda p: check__show(p, subst)), params), ' ') + ') ' + check__show(ret, subst) + ')')
    else:
        assert isinstance(_cdy_t331, core__TVar)
        _cdy_name_1042 = _cdy_t331.name
        if (not check__is_flexible(_cdy_name_1042)):
            return _cdy_name_1042
        elif (core__constraint_of(_cdy_name_1042) != ''):
            return core__constraint_of(_cdy_name_1042)
        else:
            return ('t' + cdy_rt.primitives.substring(_cdy_name_1042, 1, len(_cdy_name_1042)))

def check__shown_name(key: str) -> str:
    parts = cdy_rt.primitives.split(key, '.')
    return cdy_rt.primitives.at(parts, (len(parts) - 1))

def math__abs[number: (int, float)](x: number) -> number:
    if (x < (x - x)):
        return ((x - x) - x)
    else:
        return x

def math__min[comparable: (int, float, str)](a: comparable, b: comparable) -> comparable:
    if (b < a):
        return b
    else:
        return a

def math__max[comparable: (int, float, str)](a: comparable, b: comparable) -> comparable:
    if (b > a):
        return b
    else:
        return a

class interp__VInt(_cdy_NamedTuple):
    n: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VInt, 'VInt', (), ('Int',))

class interp__VLong(_cdy_NamedTuple):
    n: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VLong, 'VLong', (), ('Int',))

class interp__VByte(_cdy_NamedTuple):
    n: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VByte, 'VByte', (), ('Int',))

class interp__VFloat(_cdy_NamedTuple):
    x: float
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VFloat, 'VFloat', (), ('Double',))

class interp__VDouble(_cdy_NamedTuple):
    x: float
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VDouble, 'VDouble', (), ('Double',))

class interp__VBool(_cdy_NamedTuple):
    b: bool
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VBool, 'VBool', (), ('Bool',))

class interp__VChar(_cdy_NamedTuple):
    c: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VChar, 'VChar', (), ('Char',))

class interp__VStr(_cdy_NamedTuple):
    s: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VStr, 'VStr', (), ('String',))

class interp__VUnit(_cdy_NamedTuple):
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VUnit, 'VUnit', (), ())

class interp__VList(_cdy_NamedTuple):
    items: tuple[interp__Value, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VList, 'VList', (), (('List', 'interp.Value'),))

class interp__VTup(_cdy_NamedTuple):
    items: tuple[interp__Value, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VTup, 'VTup', (), (('List', 'interp.Value'),))

class interp__VMap(_cdy_NamedTuple):
    m: _cdy_Mapping[interp__Value, interp__Value]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VMap, 'VMap', (), (('Map', 'interp.Value', 'interp.Value'),))

class interp__VRec(_cdy_NamedTuple):
    module: str
    name: str
    fields: tuple[tuple[str, interp__Value], ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VRec, 'VRec', (), ('String', 'String', ('List', ('Tup', 'String', 'interp.Value'))))

class interp__VFn(_cdy_NamedTuple):
    params: tuple[core__Expr, ...]
    body: core__Expr
    env: _cdy_Mapping[int, interp__Value]
    name: str
    rest: bool
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VFn, 'VFn', (), (('List', 'core.Expr'), 'core.Expr', ('Map', 'Int', 'interp.Value'), 'String', 'Bool'))

class interp__VCtor(_cdy_NamedTuple):
    module: str
    name: str
    fields: tuple[str, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VCtor, 'VCtor', (), ('String', 'String', ('List', 'String')))

class interp__VPrim(_cdy_NamedTuple):
    key: str
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__VPrim, 'VPrim', (), ('String',))
type interp__Value = interp__VInt | interp__VLong | interp__VByte | interp__VFloat | interp__VDouble | interp__VBool | interp__VChar | interp__VStr | interp__VUnit | interp__VList | interp__VTup | interp__VMap | interp__VRec | interp__VFn | interp__VCtor | interp__VPrim

class interp__Ctx(_cdy_NamedTuple):
    globals_: _cdy_Mapping[str, interp__Value]
    builtins: _cdy_Mapping[str, _cdy_Callable[[_cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], tuple[interp__Value, ...]], interp__Value]]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__Ctx, 'Ctx', (), (('Map', 'String', 'interp.Value'), ('Map', 'String', 'Fn')))

def interp__interpret(tops: tuple[core__Top, ...], top: str, args: tuple[str, ...], builtins: _cdy_Mapping[str, _cdy_Callable[[_cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], tuple[interp__Value, ...]], interp__Value]]) -> int:
    cx = interp__load_tops(tops, builtins)
    if core__has_main(tops, top):
        _cdy_t332: object = interp__apply(cx, interp__global(cx, top, 'main'), (interp__VList(cdy_rt.primitives.list_map((lambda a: interp__VStr(a)), args)),))
        if isinstance(_cdy_t332, interp__VInt):
            n = _cdy_t332.n
            return n
        else:
            return cdy_rt.primitives.fail('internal error: interp: main gave no Int')
    else:
        return 0

def interp__load_tops(tops: tuple[core__Top, ...], builtins: _cdy_Mapping[str, _cdy_Callable[[_cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], tuple[interp__Value, ...]], interp__Value]]) -> interp__Ctx:
    return cdy_rt.primitives.list_fold(interp__run_top, interp__Ctx({}, builtins), tops)

def interp__call_global(cx: interp__Ctx, key: str, args: tuple[interp__Value, ...]) -> interp__Value:
    return interp__apply(cx, cdy_rt.primitives.map_get(cx.globals_, key), args)

def interp__run_top(cx: interp__Ctx, t: core__Top) -> interp__Ctx:
    _cdy_t333: object = t
    if isinstance(_cdy_t333, core__TDeft):
        module = _cdy_t333.module
        name = _cdy_t333.name
        fields = _cdy_t333.fields
        return interp__define(cx, module, name, interp__constructor(module, name, fields))
    elif isinstance(_cdy_t333, core__TDeftSum):
        _cdy_module_17 = _cdy_t333.module
        variants = _cdy_t333.variants
        return cdy_rt.primitives.list_fold((lambda c, v: interp__define(c, _cdy_module_17, v.name, interp__constructor(_cdy_module_17, v.name, v.fields))), cx, variants)
    elif isinstance(_cdy_t333, core__TDef):
        _cdy_module_21 = _cdy_t333.module
        _cdy_name_22 = _cdy_t333.name
        init = _cdy_t333.init
        return interp__define(cx, _cdy_module_21, _cdy_name_22, interp__eval(cx, {}, init))
    elif isinstance(_cdy_t333, core__TDefn):
        _cdy_module_24 = _cdy_t333.module
        _cdy_name_25 = _cdy_t333.name
        params = _cdy_t333.params
        body = _cdy_t333.body
        ty = _cdy_t333.t
        return interp__define(cx, _cdy_module_24, _cdy_name_25, interp__VFn(params, body, {}, core__global_key(_cdy_module_24, _cdy_name_25), core__is_variadic(ty)))
    else:
        assert isinstance(_cdy_t333, core__TExpr)
        expr = _cdy_t333.expr
        interp__eval(cx, {}, expr)
        return cx

def interp__define(cx: interp__Ctx, module: str, name: str, v: interp__Value) -> interp__Ctx:
    return cx._replace(globals_=cdy_rt.primitives.map_set(cx.globals_, core__global_key(module, name), v))

def interp__constructor(module: str, name: str, fields: tuple[tuple[str, core__CType], ...]) -> interp__Value:
    def _cdy_t334(f: tuple[str, core__CType]) -> str:
        _tup = f
        field = _tup[0]
        _t = _tup[1]
        return field
    return interp__VCtor(module, name, cdy_rt.primitives.list_map(_cdy_t334, fields))

def interp__global(cx: interp__Ctx, module: str, name: str) -> interp__Value:
    key = core__global_key(module, name)
    if cdy_rt.primitives.map_has(cx.globals_, key):
        return cdy_rt.primitives.map_get(cx.globals_, key)
    else:
        return cdy_rt.primitives.fail(('internal error: interp: ' + key + " isn't defined yet"))

def interp__eval(cx: interp__Ctx, env: _cdy_Mapping[int, interp__Value], e: core__Expr) -> interp__Value:
    _cdy_t335: object = e
    if isinstance(_cdy_t335, core__Lit):
        form = _cdy_t335.form
        return interp__literal(form)
    elif isinstance(_cdy_t335, core__Local):
        id_ = _cdy_t335.id_
        return cdy_rt.primitives.map_get(env, id_)
    elif isinstance(_cdy_t335, core__Global):
        module = _cdy_t335.module
        name = _cdy_t335.name
        return interp__global(cx, module, name)
    elif isinstance(_cdy_t335, core__Prim):
        _cdy_name_52 = _cdy_t335.name
        return interp__prim_value(_cdy_name_52)
    elif isinstance(_cdy_t335, core__Call):
        callee = _cdy_t335.callee
        args = _cdy_t335.args
        return interp__eval_call(cx, env, callee, args)
    elif isinstance(_cdy_t335, core__If):
        test = _cdy_t335.test
        then = _cdy_t335.then
        other = _cdy_t335.other
        if interp__truth(interp__eval(cx, env, test)):
            return interp__eval(cx, env, then)
        else:
            return interp__eval(cx, env, other)
    elif isinstance(_cdy_t335, core__Do):
        body = _cdy_t335.body
        vals = cdy_rt.primitives.list_map((lambda x: interp__eval(cx, env, x)), body)
        return cdy_rt.primitives.at(vals, (len(vals) - 1))
    elif isinstance(_cdy_t335, core__Lambda):
        params = _cdy_t335.params
        _cdy_body_62 = _cdy_t335.body
        return interp__VFn(params, _cdy_body_62, env, '', False)
    elif isinstance(_cdy_t335, core__Tuple):
        items = _cdy_t335.items
        return interp__VTup(cdy_rt.primitives.list_map((lambda x: interp__eval(cx, env, x)), items))
    elif isinstance(_cdy_t335, core__ListOf):
        _cdy_items_65 = _cdy_t335.items
        return interp__VList(cdy_rt.primitives.list_map((lambda x: interp__eval(cx, env, x)), _cdy_items_65))
    elif isinstance(_cdy_t335, core__Fmt):
        parts = _cdy_t335.parts
        return interp__VStr(cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda p: interp__part_text(cx, env, p)), parts), ''))
    elif isinstance(_cdy_t335, core__Field):
        obj = _cdy_t335.obj
        field = _cdy_t335.field
        return interp__field_of(interp__eval(cx, env, obj), field)
    elif isinstance(_cdy_t335, core__Assoc):
        _cdy_obj_71 = _cdy_t335.obj
        fields = _cdy_t335.fields
        def _cdy_t336(v: interp__Value, f: tuple[str, core__Expr]) -> interp__Value:
            _tup = f
            _cdy_name_76 = _tup[0]
            x = _tup[1]
            return interp__with_field(v, _cdy_name_76, interp__eval(cx, env, x))
        return cdy_rt.primitives.list_fold(_cdy_t336, interp__eval(cx, env, _cdy_obj_71), fields)
    elif isinstance(_cdy_t335, core__MatchE):
        subject = _cdy_t335.subject
        clauses = _cdy_t335.clauses
        default = _cdy_t335.default
        return interp__eval_match(cx, env, interp__eval(cx, env, subject), clauses, default)
    else:
        assert isinstance(_cdy_t335, core__Temp)
        return cdy_rt.primitives.fail('internal error: interp: a Temp, which only lower makes')

def interp__eval_call(cx: interp__Ctx, env: _cdy_Mapping[int, interp__Value], callee: core__Expr, args: tuple[core__Expr, ...]) -> interp__Value:
    if interp__is_prim(callee, 'and'):
        return interp__VBool(interp__all_true(cx, env, args, 0))
    elif interp__is_prim(callee, 'or'):
        return interp__VBool(interp__any_true(cx, env, args, 0))
    else:
        vals = cdy_rt.primitives.list_map((lambda a: interp__eval(cx, env, a)), args)
        _cdy_t337: object = callee
        if isinstance(_cdy_t337, core__Lambda):
            params = _cdy_t337.params
            body = _cdy_t337.body
            return interp__eval(cx, interp__bind_params(env, params, vals, False), body)
        else:
            return interp__apply(cx, interp__eval(cx, env, callee), vals)

def interp__is_prim(e: core__Expr, name: str) -> bool:
    _cdy_t338: object = e
    if isinstance(_cdy_t338, core__Prim):
        n = _cdy_t338.name
        return (n == name)
    else:
        return False

def interp__all_true(cx: interp__Ctx, env: _cdy_Mapping[int, interp__Value], args: tuple[core__Expr, ...], i: int) -> bool:
    while True:
        if (i == len(args)):
            return True
        elif interp__truth(interp__eval(cx, env, cdy_rt.primitives.at(args, i))):
            i = (i + 1)
            continue
        else:
            return False

def interp__any_true(cx: interp__Ctx, env: _cdy_Mapping[int, interp__Value], args: tuple[core__Expr, ...], i: int) -> bool:
    while True:
        if (i == len(args)):
            return False
        elif interp__truth(interp__eval(cx, env, cdy_rt.primitives.at(args, i))):
            return True
        else:
            i = (i + 1)
            continue

class interp__Done(_cdy_NamedTuple):
    v: interp__Value
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__Done, 'Done', (), ('interp.Value',))

class interp__Again(_cdy_NamedTuple):
    f: interp__Value
    args: tuple[interp__Value, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(interp__Again, 'Again', (), ('interp.Value', ('List', 'interp.Value')))
type interp__Tail = interp__Done | interp__Again

def interp__apply(cx: interp__Ctx, f: interp__Value, args: tuple[interp__Value, ...]) -> interp__Value:
    while True:
        _cdy_t339: object = f
        if isinstance(_cdy_t339, interp__VFn):
            params = _cdy_t339.params
            body = _cdy_t339.body
            env = _cdy_t339.env
            rest = _cdy_t339.rest
            _cdy_t340: object = interp__eval_tail(cx, interp__bind_params(env, params, args, rest), body)
            if isinstance(_cdy_t340, interp__Done):
                v = _cdy_t340.v
                return v
            else:
                assert isinstance(_cdy_t340, interp__Again)
                g = _cdy_t340.f
                more = _cdy_t340.args
                f, args = (g, more)
                continue
        elif isinstance(_cdy_t339, interp__VCtor):
            module = _cdy_t339.module
            name = _cdy_t339.name
            fields = _cdy_t339.fields
            return interp__VRec(module, name, cdy_rt.primitives.list_zip(fields, args))
        elif isinstance(_cdy_t339, interp__VPrim):
            key = _cdy_t339.key
            return interp__call_builtin(cx, key, args)
        else:
            return cdy_rt.primitives.fail("internal error: interp: a call of a value that isn't a function")

def interp__bind_params(env: _cdy_Mapping[int, interp__Value], params: tuple[core__Expr, ...], args: tuple[interp__Value, ...], rest: bool) -> _cdy_Mapping[int, interp__Value]:
    fixed = ((len(params) - 1) if rest else len(params))
    def _cdy_t341(m: _cdy_Mapping[int, interp__Value], pv: tuple[core__Expr, interp__Value]) -> _cdy_Mapping[int, interp__Value]:
        _tup = pv
        p = _tup[0]
        v = _tup[1]
        return cdy_rt.primitives.map_set(m, interp__local_id(p), v)
    bound = cdy_rt.primitives.list_fold(_cdy_t341, env, cdy_rt.primitives.list_zip(cdy_rt.primitives.list_take(fixed, params), args))
    if rest:
        return cdy_rt.primitives.map_set(bound, interp__local_id(cdy_rt.primitives.at(params, fixed)), interp__VList(cdy_rt.primitives.list_drop(fixed, args)))
    else:
        return bound

def interp__local_id(e: core__Expr) -> int:
    _cdy_t342: object = e
    if isinstance(_cdy_t342, core__Local):
        id_ = _cdy_t342.id_
        return id_
    else:
        return cdy_rt.primitives.fail("internal error: interp: a parameter that isn't a Local")

def interp__call_builtin(cx: interp__Ctx, key: str, args: tuple[interp__Value, ...]) -> interp__Value:
    if cdy_rt.primitives.map_has(cx.builtins, key):
        return cdy_rt.primitives.map_get(cx.builtins, key)((lambda f, xs: interp__apply(cx, f, xs)), args)
    else:
        return cdy_rt.primitives.fail(('internal error: interp: no built-in ' + key))

def interp__prim_value(name: str) -> interp__Value:
    if (name == 'nil'):
        return interp__VUnit()
    elif (name == 'empty-list'):
        return interp__VList(())
    elif (name == 'map.empty'):
        return interp__VMap({})
    elif (name == 'math.PI'):
        return interp__VDouble(math.pi)
    else:
        return interp__VPrim(name)

def interp__truth(v: interp__Value) -> bool:
    _cdy_t343: object = v
    if isinstance(_cdy_t343, interp__VBool):
        b = _cdy_t343.b
        return b
    else:
        return cdy_rt.primitives.fail("internal error: interp: a test that isn't a Bool")

def interp__literal(form: form__Form) -> interp__Value:
    _cdy_t344: object = form
    if isinstance(_cdy_t344, form__IntLit):
        n = _cdy_t344.val
        return interp__VInt(n)
    elif isinstance(_cdy_t344, form__LongLit):
        _cdy_n_137 = _cdy_t344.val
        return interp__VLong(_cdy_n_137)
    elif isinstance(_cdy_t344, form__ByteLit):
        _cdy_n_138 = _cdy_t344.val
        return interp__VByte(_cdy_n_138)
    elif isinstance(_cdy_t344, form__FloatLit):
        x = _cdy_t344.val
        return interp__VFloat(x)
    elif isinstance(_cdy_t344, form__DoubleLit):
        _cdy_x_140 = _cdy_t344.val
        return interp__VDouble(_cdy_x_140)
    elif isinstance(_cdy_t344, form__BoolLit):
        b = _cdy_t344.val
        return interp__VBool(b)
    elif isinstance(_cdy_t344, form__CharLit):
        c = _cdy_t344.val
        return interp__VChar(c)
    elif isinstance(_cdy_t344, form__Txt):
        s = _cdy_t344.val
        return interp__VStr(s)
    else:
        return cdy_rt.primitives.fail("internal error: interp: a literal that isn't one")

def interp__part_text(cx: interp__Ctx, env: _cdy_Mapping[int, interp__Value], p: core__FPart) -> str:
    _cdy_t345: object = p
    if isinstance(_cdy_t345, core__FText):
        s = _cdy_t345.text
        return s
    else:
        assert isinstance(_cdy_t345, core__FHole)
        x = _cdy_t345.expr
        return interp__str_of(interp__call_builtin(cx, 'text', (interp__eval(cx, env, x),)))

def interp__field_of(v: interp__Value, field: str) -> interp__Value:
    _cdy_t346: object = v
    if isinstance(_cdy_t346, interp__VRec):
        fields = _cdy_t346.fields
        def _cdy_t347(f: tuple[str, interp__Value]) -> bool:
            _cdy__tup_153 = f
            name = _cdy__tup_153[0]
            _v = _cdy__tup_153[1]
            return (name == field)
        i = cdy_rt.primitives.list_find_index(_cdy_t347, fields)
        if (i < 0):
            return cdy_rt.primitives.fail(('internal error: interp: no field ' + field))
        else:
            _tup = cdy_rt.primitives.at(fields, i)
            _name = _tup[0]
            x = _tup[1]
            return x
    else:
        return cdy_rt.primitives.fail(('internal error: interp: a field ' + field + " of a value that isn't a record"))

def interp__with_field(v: interp__Value, field: str, x: interp__Value) -> interp__Value:
    _cdy_t348: object = v
    if isinstance(_cdy_t348, interp__VRec):
        module = _cdy_t348.module
        name = _cdy_t348.name
        fields = _cdy_t348.fields
        def _cdy_t349(f: tuple[str, interp__Value]) -> tuple[str, interp__Value]:
            _tup = f
            n = _tup[0]
            _v = _tup[1]
            if (n == field):
                return (n, x)
            else:
                return f
        return interp__VRec(module, name, cdy_rt.primitives.list_map(_cdy_t349, fields))
    else:
        return cdy_rt.primitives.fail(('internal error: interp: assoc ' + field + " on a value that isn't a record"))

def interp__eval_match(cx: interp__Ctx, env: _cdy_Mapping[int, interp__Value], v: interp__Value, clauses: tuple[core__Clause, ...], default: tuple[core__Expr, ...]) -> interp__Value:
    _tup = interp__choose_clause(env, v, clauses, default)
    inner = _tup[0]
    body = _tup[1]
    return interp__eval(cx, inner, body)

def interp__choose_clause(env: _cdy_Mapping[int, interp__Value], v: interp__Value, clauses: tuple[core__Clause, ...], default: tuple[core__Expr, ...]) -> tuple[_cdy_Mapping[int, interp__Value], core__Expr]:
    _cdy_t350: object = v
    if isinstance(_cdy_t350, interp__VRec):
        module = _cdy_t350.module
        name = _cdy_t350.name
        i = cdy_rt.primitives.list_find_index((lambda _cdy_c_184: ((_cdy_c_184.module == module) and (_cdy_c_184.variant == name))), clauses)
        if (i >= 0):
            c = cdy_rt.primitives.at(clauses, i)
            def _cdy_t351(m: _cdy_Mapping[int, interp__Value], b: tuple[str, core__Expr]) -> _cdy_Mapping[int, interp__Value]:
                _tup = b
                field = _tup[0]
                loc = _tup[1]
                return cdy_rt.primitives.map_set(m, interp__local_id(loc), interp__field_of(v, field))
            return (cdy_rt.primitives.list_fold(_cdy_t351, env, c.binds), c.body)
        elif (len(default) == 1):
            return (env, default[0])
        else:
            return cdy_rt.primitives.fail('internal error: interp: no clause matches')
    else:
        return cdy_rt.primitives.fail("internal error: interp: a match on a value that isn't a variant")

def interp__eval_tail(cx: interp__Ctx, env: _cdy_Mapping[int, interp__Value], e: core__Expr) -> interp__Tail:
    _cdy_t352: object = e
    if isinstance(_cdy_t352, core__Call):
        callee = _cdy_t352.callee
        args = _cdy_t352.args
        if (interp__is_prim(callee, 'and') or interp__is_prim(callee, 'or')):
            return interp__Done(interp__eval(cx, env, e))
        else:
            vals = cdy_rt.primitives.list_map((lambda a: interp__eval(cx, env, a)), args)
            _cdy_t353: object = callee
            if isinstance(_cdy_t353, core__Lambda):
                params = _cdy_t353.params
                body = _cdy_t353.body
                return interp__eval_tail(cx, interp__bind_params(env, params, vals, False), body)
            else:
                return interp__Again(interp__eval(cx, env, callee), vals)
    elif isinstance(_cdy_t352, core__If):
        test = _cdy_t352.test
        then = _cdy_t352.then
        other = _cdy_t352.other
        if interp__truth(interp__eval(cx, env, test)):
            return interp__eval_tail(cx, env, then)
        else:
            return interp__eval_tail(cx, env, other)
    elif isinstance(_cdy_t352, core__Do):
        _cdy_body_204 = _cdy_t352.body
        last = (len(_cdy_body_204) - 1)
        cdy_rt.primitives.list_map((lambda x: interp__eval(cx, env, x)), cdy_rt.primitives.list_take(last, _cdy_body_204))
        return interp__eval_tail(cx, env, cdy_rt.primitives.at(_cdy_body_204, last))
    elif isinstance(_cdy_t352, core__MatchE):
        subject = _cdy_t352.subject
        clauses = _cdy_t352.clauses
        default = _cdy_t352.default
        _tup = interp__choose_clause(env, interp__eval(cx, env, subject), clauses, default)
        inner = _tup[0]
        _cdy_body_212 = _tup[1]
        return interp__eval_tail(cx, inner, _cdy_body_212)
    else:
        return interp__Done(interp__eval(cx, env, e))

def interp__int_of(v: interp__Value) -> int:
    _cdy_t354: object = v
    if isinstance(_cdy_t354, interp__VInt):
        n = _cdy_t354.n
        return n
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected an Int')

def interp__long_of(v: interp__Value) -> int:
    _cdy_t355: object = v
    if isinstance(_cdy_t355, interp__VLong):
        n = _cdy_t355.n
        return n
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a Long')

def interp__byte_of(v: interp__Value) -> int:
    _cdy_t356: object = v
    if isinstance(_cdy_t356, interp__VByte):
        n = _cdy_t356.n
        return n
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a Byte')

def interp__float_of(v: interp__Value) -> float:
    _cdy_t357: object = v
    if isinstance(_cdy_t357, interp__VFloat):
        x = _cdy_t357.x
        return x
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a Float')

def interp__double_of(v: interp__Value) -> float:
    _cdy_t358: object = v
    if isinstance(_cdy_t358, interp__VDouble):
        x = _cdy_t358.x
        return x
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a Double')

def interp__str_of(v: interp__Value) -> str:
    _cdy_t359: object = v
    if isinstance(_cdy_t359, interp__VStr):
        s = _cdy_t359.s
        return s
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a String')

def interp__char_of(v: interp__Value) -> str:
    _cdy_t360: object = v
    if isinstance(_cdy_t360, interp__VChar):
        c = _cdy_t360.c
        return c
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a Char')

def interp__items_of(v: interp__Value) -> tuple[interp__Value, ...]:
    _cdy_t361: object = v
    if isinstance(_cdy_t361, interp__VList):
        xs = _cdy_t361.items
        return xs
    elif isinstance(_cdy_t361, interp__VTup):
        _cdy_xs_229 = _cdy_t361.items
        return _cdy_xs_229
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a List or a Tup')

def interp__map_of(v: interp__Value) -> _cdy_Mapping[interp__Value, interp__Value]:
    _cdy_t362: object = v
    if isinstance(_cdy_t362, interp__VMap):
        m = _cdy_t362.m
        return m
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a Map')

def interp__list_of(v: interp__Value) -> tuple[interp__Value, ...]:
    _cdy_t363: object = v
    if isinstance(_cdy_t363, interp__VList):
        xs = _cdy_t363.items
        return xs
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a List')

def interp_builtins__check_interp_builtins(builtins: _cdy_Mapping[str, core__Builtin]) -> None:
    declared = cdy_rt.primitives.list_filter((lambda key: interp_builtins__is_interpreted(cdy_rt.primitives.map_get(builtins, key))), cdy_rt.primitives.map_keys(builtins))
    missing = cdy_rt.primitives.list_filter((lambda key: (not cdy_rt.primitives.map_has(interp_builtins__BUILTINS, key))), declared)
    extra = cdy_rt.primitives.list_filter((lambda key: (not cdy_rt.primitives.list_contains(key, declared))), cdy_rt.primitives.map_keys(interp_builtins__BUILTINS))
    none = cdy_rt.primitives.join(missing, ', ')
    stray = cdy_rt.primitives.join(extra, ', ')
    if (len(missing) > 0):
        cdy_rt.primitives.fail(('internal error: interp: no built-in for ' + none))
    elif (len(extra) > 0):
        cdy_rt.primitives.fail(('internal error: interp: a built-in nothing declares: ' + stray))

def interp_builtins__is_interpreted(b: core__Builtin) -> bool:
    _cdy_t364: object = b
    if isinstance(_cdy_t364, core__Typed):
        t = _cdy_t364.type_
        m = _cdy_t364.module
        return ((m != 'translator') and interp_builtins__is_function(t))
    else:
        return False

def interp_builtins__is_function(t: core__CType) -> bool:
    _cdy_t365: object = t
    if isinstance(_cdy_t365, core__TFn):
        return True
    else:
        return False

def interp_builtins__fold_num(fi: _cdy_Callable[[int, int], int], fd: _cdy_Callable[[float, float], float], args: tuple[interp__Value, ...]) -> interp__Value:
    def _cdy_t367(a: interp__Value, b: interp__Value) -> interp__Value:
        _cdy_t366: object = a
        if isinstance(_cdy_t366, interp__VInt):
            x = _cdy_t366.n
            return interp__VInt(fi(x, interp__int_of(b)))
        elif isinstance(_cdy_t366, interp__VLong):
            _cdy_x_19 = _cdy_t366.n
            return interp__VLong(fi(_cdy_x_19, interp__long_of(b)))
        elif isinstance(_cdy_t366, interp__VByte):
            _cdy_x_20 = _cdy_t366.n
            return interp__VByte(fi(_cdy_x_20, interp__byte_of(b)))
        elif isinstance(_cdy_t366, interp__VFloat):
            _cdy_x_21 = _cdy_t366.x
            return interp__VFloat(fd(_cdy_x_21, interp__float_of(b)))
        elif isinstance(_cdy_t366, interp__VDouble):
            _cdy_x_22 = _cdy_t366.x
            return interp__VDouble(fd(_cdy_x_22, interp__double_of(b)))
        else:
            return cdy_rt.primitives.fail("internal error: interp: arithmetic on a value that isn't a number")
    return cdy_rt.primitives.list_fold(_cdy_t367, args[0], cdy_rt.primitives.list_drop(1, args))

def interp_builtins__no_int(_a: int, _b: int) -> int:
    return cdy_rt.primitives.fail('internal error: interp: / on integers')

def interp_builtins__no_float(_a: float, _b: float) -> float:
    return cdy_rt.primitives.fail('internal error: interp: quot or mod on floats')

def interp_builtins__chain(ok: _cdy_Callable[[interp__Value, interp__Value], bool], args: tuple[interp__Value, ...]) -> bool:
    return cdy_rt.primitives.list_all((lambda i: ok(cdy_rt.primitives.at(args, i), cdy_rt.primitives.at(args, (i + 1)))), cdy_rt.primitives.list_range(0, (len(args) - 1)))

def interp_builtins__compare(a: interp__Value, b: interp__Value) -> int:
    _cdy_t368: object = a
    if isinstance(_cdy_t368, interp__VInt):
        x = _cdy_t368.n
        return interp_builtins__order(x, interp__int_of(b))
    elif isinstance(_cdy_t368, interp__VLong):
        _cdy_x_33 = _cdy_t368.n
        return interp_builtins__order(_cdy_x_33, interp__long_of(b))
    elif isinstance(_cdy_t368, interp__VByte):
        _cdy_x_34 = _cdy_t368.n
        return interp_builtins__order(_cdy_x_34, interp__byte_of(b))
    elif isinstance(_cdy_t368, interp__VFloat):
        _cdy_x_35 = _cdy_t368.x
        return interp_builtins__order(_cdy_x_35, interp__float_of(b))
    elif isinstance(_cdy_t368, interp__VDouble):
        _cdy_x_36 = _cdy_t368.x
        return interp_builtins__order(_cdy_x_36, interp__double_of(b))
    elif isinstance(_cdy_t368, interp__VStr):
        _cdy_x_37 = _cdy_t368.s
        return interp_builtins__order(_cdy_x_37, interp__str_of(b))
    elif isinstance(_cdy_t368, interp__VChar):
        _cdy_x_38 = _cdy_t368.c
        return interp_builtins__order(_cdy_x_38, interp__char_of(b))
    else:
        return cdy_rt.primitives.fail("internal error: interp: a comparison of values that aren't comparable")

def interp_builtins__order[comparable: (int, float, str)](x: comparable, y: comparable) -> int:
    if (x < y):
        return -1
    elif (x > y):
        return 1
    else:
        return 0

def interp_builtins__append(a: interp__Value, b: interp__Value) -> interp__Value:
    _cdy_t369: object = a
    if isinstance(_cdy_t369, interp__VStr):
        x = _cdy_t369.s
        return interp__VStr((x + interp__str_of(b)))
    elif isinstance(_cdy_t369, interp__VList):
        _cdy_x_44 = _cdy_t369.items
        return interp__VList((_cdy_x_44 + interp__list_of(b)))
    else:
        return cdy_rt.primitives.fail("internal error: interp: ++ on a value that isn't a string or a list")

def interp_builtins__show_value(v: interp__Value) -> str:
    _cdy_t370: object = v
    if isinstance(_cdy_t370, interp__VInt):
        n = _cdy_t370.n
        return str(n)
    elif isinstance(_cdy_t370, interp__VLong):
        _cdy_n_47 = _cdy_t370.n
        return (str(_cdy_n_47) + 'l')
    elif isinstance(_cdy_t370, interp__VByte):
        _cdy_n_48 = _cdy_t370.n
        return (str(_cdy_n_48) + 'b')
    elif isinstance(_cdy_t370, interp__VFloat):
        x = _cdy_t370.x
        return (cdy_rt.primitives.show(x, 'Double') + 'f')
    elif isinstance(_cdy_t370, interp__VDouble):
        _cdy_x_50 = _cdy_t370.x
        return cdy_rt.primitives.show(_cdy_x_50, 'Double')
    elif isinstance(_cdy_t370, interp__VBool):
        b = _cdy_t370.b
        if b:
            return 'true'
        else:
            return 'false'
    elif isinstance(_cdy_t370, interp__VChar):
        c = _cdy_t370.c
        return ('\\' + c)
    elif isinstance(_cdy_t370, interp__VStr):
        s = _cdy_t370.s
        return interp_builtins__show_string(s)
    elif isinstance(_cdy_t370, interp__VUnit):
        return 'nil'
    elif isinstance(_cdy_t370, interp__VList):
        xs = _cdy_t370.items
        return interp_builtins__show_items('List', cdy_rt.primitives.list_map(interp_builtins__show_value, xs))
    elif isinstance(_cdy_t370, interp__VTup):
        _cdy_xs_55 = _cdy_t370.items
        return interp_builtins__show_items('Tup', cdy_rt.primitives.list_map(interp_builtins__show_value, _cdy_xs_55))
    elif isinstance(_cdy_t370, interp__VMap):
        m = _cdy_t370.m
        return interp_builtins__show_items('Map', cdy_rt.primitives.list_map((lambda k: ('(Tup ' + interp_builtins__show_value(k) + ' ' + interp_builtins__show_value(cdy_rt.primitives.map_get(m, k)) + ')')), cdy_rt.primitives.map_keys(m)))
    elif isinstance(_cdy_t370, interp__VRec):
        name = _cdy_t370.name
        fields = _cdy_t370.fields
        if (len(fields) == 0):
            return name
        else:
            def _cdy_t371(f: tuple[str, interp__Value]) -> str:
                _tup = f
                _n = _tup[0]
                _cdy_x_63 = _tup[1]
                return interp_builtins__show_value(_cdy_x_63)
            return interp_builtins__show_items(name, cdy_rt.primitives.list_map(_cdy_t371, fields))
    else:
        return cdy_rt.primitives.fail("show: a function can't be shown")

def interp_builtins__text_value(v: interp__Value) -> str:
    _cdy_t372: object = v
    if isinstance(_cdy_t372, interp__VStr):
        s = _cdy_t372.s
        return s
    elif isinstance(_cdy_t372, interp__VChar):
        c = _cdy_t372.c
        return c
    else:
        return interp_builtins__show_value(v)

def interp_builtins__show_items(head: str, items: tuple[str, ...]) -> str:
    return ('(' + cdy_rt.primitives.join(((head,) + items), ' ') + ')')

def interp_builtins__show_string(s: str) -> str:
    return ('"' + cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda i: interp_builtins__escape(cdy_rt.primitives.char_at(s, i))), cdy_rt.primitives.list_range(0, len(s))), '') + '"')

def interp_builtins__escape(c: str) -> str:
    n = ord(c)
    if (n == 34):
        return '\\"'
    elif (n == 92):
        return '\\\\'
    elif (n == 8):
        return '\\b'
    elif (n == 12):
        return '\\f'
    elif (n == 10):
        return '\\n'
    elif (n == 13):
        return '\\r'
    elif (n == 9):
        return '\\t'
    elif (n < 32):
        return ('\\u' + interp_builtins__hex4(n))
    else:
        return c

def interp_builtins__hex4(n: int) -> str:
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda d: cdy_rt.primitives.substring('0123456789abcdef', d, (d + 1))), ((n // 4096), ((n // 256) % 16), ((n // 16) % 16), (n % 16))), '')

def interp_builtins__at_in(who: str, i: int, n: int) -> None:
    if ((i < 0) or (i >= n)):
        cdy_rt.primitives.fail((who + ': index out of range: ' + str(i) + ', for length ' + str(n)))

def interp_builtins__slice_in(who: str, i: int, j: int, n: int) -> None:
    if ((i < 0) or (i > j) or (j > n)):
        cdy_rt.primitives.fail((who + ': index out of range: ' + str(i) + ' to ' + str(j) + ', for length ' + str(n)))

def interp_builtins__list_at(l: interp__Value, iv: interp__Value) -> interp__Value:
    xs = interp__items_of(l)
    i = interp__int_of(iv)
    interp_builtins__at_in('at', i, len(xs))
    return cdy_rt.primitives.at(xs, i)

def interp_builtins__list_slice(l: interp__Value, iv: interp__Value, jv: interp__Value) -> interp__Value:
    xs = interp__list_of(l)
    i = interp__int_of(iv)
    j = interp__int_of(jv)
    interp_builtins__slice_in('slice', i, j, len(xs))
    return interp__VList(cdy_rt.primitives.slice_(xs, i, j))

def interp_builtins__string_at(sv: interp__Value, iv: interp__Value) -> interp__Value:
    s = interp__str_of(sv)
    i = interp__int_of(iv)
    interp_builtins__at_in('string.at', i, len(s))
    return interp__VChar(cdy_rt.primitives.char_at(s, i))

def interp_builtins__string_slice(sv: interp__Value, iv: interp__Value, jv: interp__Value) -> interp__Value:
    s = interp__str_of(sv)
    i = interp__int_of(iv)
    j = interp__int_of(jv)
    interp_builtins__slice_in('string.slice', i, j, len(s))
    return interp__VStr(cdy_rt.primitives.substring(s, i, j))

def interp_builtins__test(call: _cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], f: interp__Value, x: interp__Value) -> bool:
    return interp__truth(call(f, (x,)))

def interp_builtins__pair_of(v: interp__Value) -> tuple[interp__Value, interp__Value]:
    items = interp__items_of(v)
    if (len(items) == 2):
        return (items[0], items[1])
    else:
        return cdy_rt.primitives.fail('internal error: interp: expected a pair')

def interp_builtins__strs(xs: tuple[str, ...]) -> interp__Value:
    return interp__VList(cdy_rt.primitives.list_map((lambda s: interp__VStr(s)), xs))
_cdy_t380 = ('+', (lambda _c, a: interp_builtins__fold_num((lambda x, y: (x + y)), (lambda x, y: (x + y)), a)))
_cdy_t381 = ('-', (lambda _c, a: interp_builtins__fold_num((lambda x, y: (x - y)), (lambda x, y: (x - y)), a)))
_cdy_t382 = ('*', (lambda _c, a: interp_builtins__fold_num((lambda x, y: (x * y)), (lambda x, y: (x * y)), a)))
_cdy_t383 = ('/', (lambda _c, a: interp_builtins__fold_num(interp_builtins__no_int, (lambda x, y: (x / y)), a)))
_cdy_t384 = ('quot', (lambda _c, a: interp_builtins__fold_num((lambda x, y: (x // y)), interp_builtins__no_float, a)))
_cdy_t385 = ('mod', (lambda _c, a: interp_builtins__fold_num((lambda x, y: (x % y)), interp_builtins__no_float, a)))
_cdy_t386 = ('++', (lambda _c, a: cdy_rt.primitives.list_fold(interp_builtins__append, a[0], cdy_rt.primitives.list_drop(1, a))))
_cdy_t387 = ('=', (lambda _c, a: interp__VBool(interp_builtins__chain((lambda x, y: (x == y)), a))))
_cdy_t388 = ('!=', (lambda _c, a: interp__VBool(interp_builtins__chain((lambda x, y: (x != y)), a))))
_cdy_t389 = ('<', (lambda _c, a: interp__VBool(interp_builtins__chain((lambda x, y: (interp_builtins__compare(x, y) < 0)), a))))
_cdy_t390 = ('>', (lambda _c, a: interp__VBool(interp_builtins__chain((lambda x, y: (interp_builtins__compare(x, y) > 0)), a))))
_cdy_t391 = ('<=', (lambda _c, a: interp__VBool(interp_builtins__chain((lambda x, y: (interp_builtins__compare(x, y) <= 0)), a))))
_cdy_t392 = ('>=', (lambda _c, a: interp__VBool(interp_builtins__chain((lambda x, y: (interp_builtins__compare(x, y) >= 0)), a))))
_cdy_t393 = ('and', (lambda _c, a: interp__VBool(cdy_rt.primitives.list_all(interp__truth, a))))
_cdy_t394 = ('or', (lambda _c, a: interp__VBool(cdy_rt.primitives.list_any(interp__truth, a))))
_cdy_t395 = ('not', (lambda _c, a: interp__VBool((not interp__truth(a[0])))))
def _cdy_t373(_c: _cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], a: tuple[interp__Value, ...]) -> interp__Value:
    print(interp__str_of(a[0]))
    return interp__VUnit()
_cdy_t396 = ('put-line', _cdy_t373)
def _cdy_t374(_c: _cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], a: tuple[interp__Value, ...]) -> interp__Value:
    cdy_rt.primitives.put_err(interp__str_of(a[0]))
    return interp__VUnit()
_cdy_t397 = ('put-err', _cdy_t374)
_cdy_t398 = ('text', (lambda _c, a: interp__VStr(interp_builtins__text_value(a[0]))))
_cdy_t399 = ('show', (lambda _c, a: interp__VStr(interp_builtins__show_value(a[0]))))
_cdy_t400 = ('slurp', (lambda _c, a: interp__VStr(cdy_rt.primitives.slurp(interp__str_of(a[0])))))
def _cdy_t375(_c: _cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], a: tuple[interp__Value, ...]) -> interp__Value:
    cdy_rt.primitives.spit(interp__str_of(a[0]), interp__str_of(a[1]))
    return interp__VUnit()
_cdy_t401 = ('spit', _cdy_t375)
_cdy_t402 = ('file-exists', (lambda _c, a: interp__VBool(cdy_rt.primitives.file_exists(interp__str_of(a[0])))))
def _cdy_t376(_c: _cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], a: tuple[interp__Value, ...]) -> interp__Value:
    cdy_rt.primitives.make_dirs(interp__str_of(a[0]))
    return interp__VUnit()
_cdy_t403 = ('make-dirs', _cdy_t376)
_cdy_t404 = ('path-stem', (lambda _c, a: interp__VStr(cdy_rt.primitives.path_stem(interp__str_of(a[0])))))
_cdy_t405 = ('path-dir', (lambda _c, a: interp__VStr(cdy_rt.primitives.path_dir(interp__str_of(a[0])))))
_cdy_t406 = ('path-join', (lambda _c, a: interp__VStr(cdy_rt.primitives.path_join(interp__str_of(a[0]), interp__str_of(a[1])))))
_cdy_t407 = ('path-resolve', (lambda _c, a: interp__VStr(cdy_rt.primitives.path_resolve(interp__str_of(a[0])))))
_cdy_t408 = ('len', (lambda _c, a: interp__VInt(len(interp__list_of(a[0])))))
_cdy_t409 = ('at', (lambda _c, a: interp_builtins__list_at(a[0], a[1])))
_cdy_t410 = ('slice', (lambda _c, a: interp_builtins__list_slice(a[0], a[1], a[2])))
_cdy_t411 = ('map', (lambda c, a: interp__VList(cdy_rt.primitives.list_map((lambda x: c(a[0], (x,))), interp__list_of(a[1])))))
_cdy_t412 = ('filter', (lambda c, a: interp__VList(cdy_rt.primitives.list_filter((lambda x: interp_builtins__test(c, a[0], x)), interp__list_of(a[1])))))
_cdy_t413 = ('fold', (lambda c, a: cdy_rt.primitives.list_fold((lambda acc, x: c(a[0], (acc, x))), a[1], interp__list_of(a[2]))))
def _cdy_t377(c: _cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], a: tuple[interp__Value, ...]) -> interp__Value:
    _tup = cdy_rt.primitives.list_map_acc((lambda _cdy_s_213, x: interp_builtins__pair_of(c(a[0], (_cdy_s_213, x)))), a[1], interp__list_of(a[2]))
    s = _tup[0]
    ys = _tup[1]
    return interp__VTup((s, interp__VList(ys)))
_cdy_t414 = ('map-acc', _cdy_t377)
_cdy_t415 = ('any', (lambda c, a: interp__VBool(cdy_rt.primitives.list_any((lambda x: interp_builtins__test(c, a[0], x)), interp__list_of(a[1])))))
_cdy_t416 = ('all', (lambda c, a: interp__VBool(cdy_rt.primitives.list_all((lambda x: interp_builtins__test(c, a[0], x)), interp__list_of(a[1])))))
_cdy_t417 = ('find-index', (lambda c, a: interp__VInt(cdy_rt.primitives.list_find_index((lambda x: interp_builtins__test(c, a[0], x)), interp__list_of(a[1])))))
_cdy_t418 = ('reverse', (lambda _c, a: interp__VList(cdy_rt.primitives.list_reverse(interp__list_of(a[0])))))
_cdy_t419 = ('range', (lambda _c, a: interp__VList(cdy_rt.primitives.list_map((lambda n: interp__VInt(n)), cdy_rt.primitives.list_range(interp__int_of(a[0]), interp__int_of(a[1]))))))
_cdy_t420 = ('take', (lambda _c, a: interp__VList(cdy_rt.primitives.list_take(interp__int_of(a[0]), interp__list_of(a[1])))))
_cdy_t421 = ('drop', (lambda _c, a: interp__VList(cdy_rt.primitives.list_drop(interp__int_of(a[0]), interp__list_of(a[1])))))
_cdy_t422 = ('concat', (lambda _c, a: interp__VList(cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(interp__list_of, interp__list_of(a[0]))))))
def _cdy_t379(_c: _cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], a: tuple[interp__Value, ...]) -> interp__Value:
    def _cdy_t378(p: tuple[interp__Value, interp__Value]) -> interp__Value:
        _tup = p
        x = _tup[0]
        y = _tup[1]
        return interp__VTup((x, y))
    return interp__VList(cdy_rt.primitives.list_map(_cdy_t378, cdy_rt.primitives.list_zip(interp__list_of(a[0]), interp__list_of(a[1]))))
interp_builtins__BUILTINS: _cdy_Mapping[str, _cdy_Callable[[_cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], tuple[interp__Value, ...]], interp__Value]] = cdy_rt.primitives.map_from((_cdy_t380, _cdy_t381, _cdy_t382, _cdy_t383, _cdy_t384, _cdy_t385, _cdy_t386, _cdy_t387, _cdy_t388, _cdy_t389, _cdy_t390, _cdy_t391, _cdy_t392, _cdy_t393, _cdy_t394, _cdy_t395, _cdy_t396, _cdy_t397, _cdy_t398, _cdy_t399, _cdy_t400, _cdy_t401, _cdy_t402, _cdy_t403, _cdy_t404, _cdy_t405, _cdy_t406, _cdy_t407, _cdy_t408, _cdy_t409, _cdy_t410, _cdy_t411, _cdy_t412, _cdy_t413, _cdy_t414, _cdy_t415, _cdy_t416, _cdy_t417, _cdy_t418, _cdy_t419, _cdy_t420, _cdy_t421, _cdy_t422, ('zip', _cdy_t379), ('contains', (lambda _c, a: interp__VBool(cdy_rt.primitives.list_any((lambda y: (a[0] == y)), interp__list_of(a[1]))))), ('fail', (lambda _c, a: cdy_rt.primitives.fail(interp__str_of(a[0])))), ('math.sin', (lambda _c, a: interp__VDouble(math.sin(interp__double_of(a[0]))))), ('math.cos', (lambda _c, a: interp__VDouble(math.cos(interp__double_of(a[0]))))), ('math.tan', (lambda _c, a: interp__VDouble(math.tan(interp__double_of(a[0]))))), ('string.len', (lambda _c, a: interp__VInt(len(interp__str_of(a[0]))))), ('string.at', (lambda _c, a: interp_builtins__string_at(a[0], a[1]))), ('string.slice', (lambda _c, a: interp_builtins__string_slice(a[0], a[1], a[2]))), ('string.contains', (lambda _c, a: interp__VBool(cdy_rt.primitives.str_contains(interp__str_of(a[0]), interp__str_of(a[1]))))), ('string.starts-with', (lambda _c, a: interp__VBool(cdy_rt.primitives.starts_with(interp__str_of(a[0]), interp__str_of(a[1]))))), ('string.ends-with', (lambda _c, a: interp__VBool(cdy_rt.primitives.ends_with(interp__str_of(a[0]), interp__str_of(a[1]))))), ('string.split', (lambda _c, a: interp_builtins__strs(cdy_rt.primitives.split(interp__str_of(a[0]), interp__str_of(a[1]))))), ('string.join', (lambda _c, a: interp__VStr(cdy_rt.primitives.join(cdy_rt.primitives.list_map(interp__str_of, interp__list_of(a[0])), interp__str_of(a[1]))))), ('string.repeat', (lambda _c, a: interp__VStr(cdy_rt.primitives.repeat(interp__str_of(a[0]), interp__int_of(a[1]))))), ('string.replace', (lambda _c, a: interp__VStr(cdy_rt.primitives.replace(interp__str_of(a[0]), interp__str_of(a[1]), interp__str_of(a[2]))))), ('string.to-int', (lambda _c, a: interp__VInt(cdy_rt.primitives.to_int(interp__str_of(a[0]))))), ('string.to-float', (lambda _c, a: interp__VDouble(cdy_rt.primitives.to_float(interp__str_of(a[0]))))), ('string.is-decimal', (lambda _c, a: interp__VBool(cdy_rt.primitives.is_decimal(interp__str_of(a[0]))))), ('string.code', (lambda _c, a: interp__VInt(ord(interp__str_of(a[0]))))), ('string.hex-char', (lambda _c, a: interp__VStr(cdy_rt.primitives.hex_char(interp__str_of(a[0]))))), ('string.is-space', (lambda _c, a: interp__VBool(cdy_rt.primitives.isspace(interp__str_of(a[0]))))), ('map.at', (lambda _c, a: cdy_rt.primitives.map_get(interp__map_of(a[0]), a[1]))), ('map.has', (lambda _c, a: interp__VBool(cdy_rt.primitives.map_has(interp__map_of(a[0]), a[1])))), ('map.set', (lambda _c, a: interp__VMap(cdy_rt.primitives.map_set(interp__map_of(a[0]), a[1], a[2])))), ('map.keys', (lambda _c, a: interp__VList(cdy_rt.primitives.map_keys(interp__map_of(a[0]))))), ('map.from', (lambda _c, a: interp__VMap(cdy_rt.primitives.map_from(cdy_rt.primitives.list_map(interp_builtins__pair_of, interp__list_of(a[0])))))), ('map.size', (lambda _c, a: interp__VInt(len(interp__map_of(a[0])))))))
interp_builtins__MACRO_BUILTINS: _cdy_Mapping[str, _cdy_Callable[[_cdy_Callable[[interp__Value, tuple[interp__Value, ...]], interp__Value], tuple[interp__Value, ...]], interp__Value]] = cdy_rt.primitives.map_set(interp_builtins__BUILTINS, 'translator.fresh-name', (lambda _c, a: interp__VStr(cdy_rt.primitives.fresh_name(interp__str_of(a[0])))))

def interp_macros__macro_runner(tops: tuple[core__Top, ...]) -> _cdy_Callable[[str], _cdy_Callable[[tuple[form__Form, ...]], form__Form]]:
    cx = interp__load_tops(tops, interp_builtins__MACRO_BUILTINS)
    return (lambda key: (lambda args: interp_macros__value_form(interp__call_global(cx, key, (interp__VList(cdy_rt.primitives.list_map((lambda a: interp_macros__form_value('form', a)), args)),)))))

def interp_macros__pos_value(module: str, p: form__Pos) -> interp__Value:
    return interp__VRec(module, 'Pos', (('file', interp__VStr(p.file)), ('line', interp__VInt(p.line)), ('col', interp__VInt(p.col))))

def interp_macros__form_value(module: str, f: form__Form) -> interp__Value:
    at_pos: _cdy_Callable[[str, str, interp__Value], interp__Value] = (lambda _cdy_name_9, field, v: interp__VRec(module, _cdy_name_9, ((field, v), ('pos', interp_macros__pos_value(module, form__form_pos(f))))))
    _cdy_t423: object = f
    if isinstance(_cdy_t423, form__Sym):
        name = _cdy_t423.name
        return at_pos('Sym', 'name', interp__VStr(name))
    elif isinstance(_cdy_t423, form__Lst):
        items = _cdy_t423.items
        return at_pos('Lst', 'items', interp__VList(cdy_rt.primitives.list_map((lambda i: interp_macros__form_value(module, i)), items)))
    elif isinstance(_cdy_t423, form__Txt):
        s = _cdy_t423.val
        return at_pos('Txt', 'val', interp__VStr(s))
    elif isinstance(_cdy_t423, form__IntLit):
        n = _cdy_t423.val
        return at_pos('IntLit', 'val', interp__VInt(n))
    elif isinstance(_cdy_t423, form__LongLit):
        _cdy_n_18 = _cdy_t423.val
        return at_pos('LongLit', 'val', interp__VInt(_cdy_n_18))
    elif isinstance(_cdy_t423, form__ByteLit):
        _cdy_n_19 = _cdy_t423.val
        return at_pos('ByteLit', 'val', interp__VInt(_cdy_n_19))
    elif isinstance(_cdy_t423, form__FloatLit):
        x = _cdy_t423.val
        return at_pos('FloatLit', 'val', interp__VDouble(x))
    elif isinstance(_cdy_t423, form__DoubleLit):
        _cdy_x_21 = _cdy_t423.val
        return at_pos('DoubleLit', 'val', interp__VDouble(_cdy_x_21))
    elif isinstance(_cdy_t423, form__CharLit):
        c = _cdy_t423.val
        return at_pos('CharLit', 'val', interp__VChar(c))
    else:
        assert isinstance(_cdy_t423, form__BoolLit)
        b = _cdy_t423.val
        return at_pos('BoolLit', 'val', interp__VBool(b))

def interp_macros__value_pos(v: interp__Value) -> form__Pos:
    return form__Pos(interp__str_of(interp__field_of(v, 'file')), interp__int_of(interp__field_of(v, 'line')), interp__int_of(interp__field_of(v, 'col')))

def interp_macros__value_form(v: interp__Value) -> form__Form:
    _cdy_t424: object = v
    if isinstance(_cdy_t424, interp__VRec):
        name = _cdy_t424.name
        pos = interp_macros__value_pos(interp__field_of(v, 'pos'))
        if (name == 'Sym'):
            return form__Sym(interp__str_of(interp__field_of(v, 'name')), pos)
        elif (name == 'Lst'):
            return form__Lst(cdy_rt.primitives.list_map(interp_macros__value_form, interp__list_of(interp__field_of(v, 'items'))), pos)
        elif (name == 'Txt'):
            return form__Txt(interp__str_of(interp__field_of(v, 'val')), pos)
        elif (name == 'IntLit'):
            return form__IntLit(interp__int_of(interp__field_of(v, 'val')), pos)
        elif (name == 'LongLit'):
            return form__LongLit(interp__int_of(interp__field_of(v, 'val')), pos)
        elif (name == 'ByteLit'):
            return form__ByteLit(interp__int_of(interp__field_of(v, 'val')), pos)
        elif (name == 'FloatLit'):
            return form__FloatLit(interp__double_of(interp__field_of(v, 'val')), pos)
        elif (name == 'DoubleLit'):
            return form__DoubleLit(interp__double_of(interp__field_of(v, 'val')), pos)
        elif (name == 'CharLit'):
            return form__CharLit(interp__char_of(interp__field_of(v, 'val')), pos)
        elif (name == 'BoolLit'):
            return form__BoolLit(interp__truth(interp__field_of(v, 'val')), pos)
        else:
            return cdy_rt.primitives.fail(('internal error: interp: a macro gave a ' + name + ', not a Form'))
    else:
        return cdy_rt.primitives.fail("internal error: interp: a macro gave a value that isn't a Form")

class spec_runner__Block(_cdy_NamedTuple):
    info: str
    text: str
    line: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(spec_runner__Block, 'Block', (), ('String', 'String', 'Int'))

def spec_runner__blocks(text: str) -> tuple[spec_runner__Block, ...]:
    lines = string__lines(text)
    return spec_runner__blocks_from(lines, 0, ())

def spec_runner__blocks_from(lines: tuple[str, ...], i: int, acc: tuple[spec_runner__Block, ...]) -> tuple[spec_runner__Block, ...]:
    while True:
        if (i >= len(lines)):
            return acc
        else:
            line = cdy_rt.primitives.at(lines, i)
            indent = spec_runner__run_of(line, 0, ' ')
            ticks = spec_runner__run_of(line, indent, '`')
            if (ticks < 3):
                i = (i + 1)
                continue
            else:
                end = spec_runner__closing(lines, (i + 1), ticks)
                info = string__trim(cdy_rt.primitives.substring(line, (indent + ticks), len(line)))
                body = spec_runner__block_text(cdy_rt.primitives.slice_(lines, (i + 1), end), indent)
                i, acc = ((end + 1), (acc + (spec_runner__Block(info, body, (i + 1)),)))
                continue

def spec_runner__block_text(lines: tuple[str, ...], indent: int) -> str:
    return cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda l: (spec_runner__dedent(l, indent) + '\n')), lines), '')

def spec_runner__closing(lines: tuple[str, ...], i: int, ticks: int) -> int:
    while True:
        if (i >= len(lines)):
            return len(lines)
        elif spec_runner__closes(cdy_rt.primitives.at(lines, i), ticks):
            return i
        else:
            i = (i + 1)
            continue

def spec_runner__closes(line: str, ticks: int) -> bool:
    indent = spec_runner__run_of(line, 0, ' ')
    n = spec_runner__run_of(line, indent, '`')
    return ((n >= ticks) and (string__trim(cdy_rt.primitives.substring(line, (indent + n), len(line))) == ''))

def spec_runner__run_of(s: str, i: int, c: str) -> int:
    return spec_runner__run_from(s, i, c, 0)

def spec_runner__run_from(s: str, i: int, c: str, n: int) -> int:
    while True:
        if ((i < len(s)) and (cdy_rt.primitives.substring(s, i, (i + 1)) == c)):
            i, n = ((i + 1), (n + 1))
            continue
        else:
            return n

def spec_runner__dedent(line: str, indent: int) -> str:
    spaces = spec_runner__run_of(line, 0, ' ')
    return cdy_rt.primitives.substring(line, (spaces if (spaces < indent) else indent), len(line))
spec_runner__STATUSES: tuple[str, ...] = ('draft', 'stable', 'deprecated')

def spec_runner__status(text: str) -> str:
    return prelude__with_default('', prelude__find((lambda s: (s != '')), cdy_rt.primitives.list_map(spec_runner__status_of, string__lines(text))))

def spec_runner__status_of(line: str) -> str:
    if (not cdy_rt.primitives.starts_with(line, 'status: ')):
        return ''
    else:
        rest = cdy_rt.primitives.substring(line, 8, len(line))
        word = prelude__with_default('', prelude__find((lambda s: cdy_rt.primitives.starts_with(rest, s)), spec_runner__STATUSES))
        after = cdy_rt.primitives.substring(rest, len(word), len(rest))
        if ((word != '') and spec_runner__status_tail(after)):
            return word
        else:
            return ''

def spec_runner__status_tail(after: str) -> bool:
    since = ', since: '
    if (string__trim(after) == ''):
        return True
    elif (not cdy_rt.primitives.starts_with(after, since)):
        return False
    else:
        return spec_runner__is_word(cdy_rt.primitives.substring(after, len(since), len(after)))

def spec_runner__is_word(s: str) -> bool:
    word = string__trim(s)
    return ((word != '') and cdy_rt.primitives.starts_with(s, word) and (not cdy_rt.primitives.str_contains(' ', word)))

class spec_runner__Example(_cdy_NamedTuple):
    kind: str
    source: str
    expected: str
    line: int
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(spec_runner__Example, 'Example', (), ('String', 'String', 'String', 'Int'))
spec_runner__PAIRS: tuple[tuple[str, str], ...] = (('candy run', 'run'), ('candy error', 'error'), ('candy panic', 'panic'))

def spec_runner__pair_kind(info: str) -> str:
    _cdy_t426 = (lambda k: (k != ''))
    def _cdy_t425(p: tuple[str, str]) -> str:
        _tup = p
        i = _tup[0]
        k = _tup[1]
        if (i == info):
            return k
        else:
            return ''
    return prelude__with_default('', prelude__find(_cdy_t426, cdy_rt.primitives.list_map(_cdy_t425, spec_runner__PAIRS)))

def spec_runner__examples(text: str, name: str) -> tuple[spec_runner__Example, ...]:
    all_ = spec_runner__blocks(text)
    _tup = cdy_rt.primitives.list_fold((lambda acc, b: spec_runner__example_step(acc, b, name)), (spec_runner__NO_EXAMPLES, spec_runner__NO_BLOCK), all_)
    found = _tup[0]
    pending = _tup[1]
    _cdy_t427 = pending
    if isinstance(_cdy_t427, prelude__Some):
        p: spec_runner__Block = _cdy_t427.v
        return cdy_rt.primitives.fail((name + ':' + str(p.line) + ': ' + p.info + ' at the end, with no expect'))
    elif isinstance(_cdy_t427, prelude__None):
        return found
spec_runner__NO_EXAMPLES: tuple[spec_runner__Example, ...] = ()
spec_runner__NO_BLOCK: prelude__Maybe[spec_runner__Block] = prelude__None()

def spec_runner__example_step(acc: tuple[tuple[spec_runner__Example, ...], prelude__Maybe[spec_runner__Block]], b: spec_runner__Block, name: str) -> tuple[tuple[spec_runner__Example, ...], prelude__Maybe[spec_runner__Block]]:
    _tup = acc
    found = _tup[0]
    pending = _tup[1]
    info = b.info
    _cdy_t428 = pending
    if isinstance(_cdy_t428, prelude__Some):
        p: spec_runner__Block = _cdy_t428.v
        kind = spec_runner__pair_kind(p.info)
        want = ('expect' if (kind == 'run') else ('expect-' + kind))
        if (info != want):
            return cdy_rt.primitives.fail((name + ':' + str(p.line) + ': ' + p.info + ' needs ' + want + ' after it'))
        else:
            expected = (b.text if (kind == 'run') else string__trim(b.text))
            return ((found + (spec_runner__Example(kind, p.text, expected, p.line),)), prelude__None())
    elif isinstance(_cdy_t428, prelude__None):
        if (spec_runner__pair_kind(info) != ''):
            return (found, prelude__Some(b))
        elif cdy_rt.primitives.list_contains(info, ('expect', 'expect-error', 'expect-panic')):
            return cdy_rt.primitives.fail((name + ':' + str(b.line) + ': ' + info + ' with no example before it'))
        elif (info == 'candy errors'):
            return ((found + spec_runner__error_table(b, name)), prelude__None())
        else:
            return (found, prelude__None())

def spec_runner__error_table(b: spec_runner__Block, name: str) -> tuple[spec_runner__Example, ...]:
    rows = string__lines(b.text)
    seps = cdy_rt.primitives.list_filter((lambda i: (string__trim(cdy_rt.primitives.at(rows, i)) == '---')), cdy_rt.primitives.list_range(0, len(rows)))
    line = b.line
    if (len(seps) > 1):
        return cdy_rt.primitives.fail((name + ':' + str((line + seps[1] + 1)) + ': a second --- (a table has one setup)'))
    else:
        first = (0 if (len(seps) == 0) else (seps[0] + 1))
        setup = cdy_rt.primitives.join(cdy_rt.primitives.list_map((lambda r: (r + '\n')), cdy_rt.primitives.list_take((first - 1), rows)), '')
        head = (spec_runner__NO_EXAMPLES if (setup == '') else (spec_runner__Example('setup', setup, '', (line + 1)),))
        return (head + cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map((lambda offset: spec_runner__table_row(cdy_rt.primitives.at(rows, (offset - 1)), setup, (line + offset), name)), cdy_rt.primitives.list_range((first + 1), (len(rows) + 1)))))

def spec_runner__table_row(row: str, setup: str, line: int, name: str) -> tuple[spec_runner__Example, ...]:
    if (string__trim(row) == ''):
        return spec_runner__NO_EXAMPLES
    elif (not cdy_rt.primitives.str_contains(' => ', row)):
        return cdy_rt.primitives.fail((name + ':' + str(line) + ': expected source => message'))
    else:
        parts = cdy_rt.primitives.split(row, ' => ')
        source = parts[0]
        message = cdy_rt.primitives.join(prelude__rest(parts), ' => ')
        return (spec_runner__Example('error', (setup + string__trim(source)), string__trim(message), line),)

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
cdy_rt.primitives.register_type(Ready, 'Ready', (), ('include.Module', ('List', 'form.Form'), ('Map', 'String', 'form.Macro'), 'core.Exports'))

def translate_modules(modules: tuple[include__Module, ...], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]]) -> str:
    builtins = expand__library_builtins(None)
    return python_of(check__type_check(program_tops(modules, parse, builtins), builtins), cdy_rt.primitives.at(modules, (len(modules) - 1)).stem)

def expander(builtins: _cdy_Mapping[str, core__Builtin]) -> expand__Expander:
    base = macro_base(builtins)
    return expand__new_expander(builtins, load_macro_file(builtins, base), load_own_macros(builtins, base))

class MacroBase(_cdy_NamedTuple):
    imports: tuple[core__Import, ...]
    modules: tuple[expand__Loaded, ...]
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and tuple.__eq__(self, other)
    def __ne__(self, other: object) -> bool:
        return not self == other
    def __hash__(self) -> int:
        return hash((type(self), tuple(self)))
cdy_rt.primitives.register_type(MacroBase, 'MacroBase', (), (('List', 'core.Import'), ('List', 'expand.Loaded')))

def macro_base(builtins: _cdy_Mapping[str, core__Builtin]) -> MacroBase:
    prelude_path = include__library_path('prelude.cdy')
    prelude_forms = read__read_source(prelude_path, cdy_rt.primitives.slurp(prelude_path))
    prelude_exports = core__module_exports(prelude_forms, 'prelude')
    translator = declaration_exports('translator')
    form_path = include__library_path('form.cdy')
    form_forms = cdy_rt.primitives.list_filter((lambda f: (not include__is_import(f))), read__read_source(form_path, cdy_rt.primitives.slurp(form_path)))
    form_exports = core__module_exports(form_forms, 'form')
    return MacroBase(macro_imports(form_exports, translator), (expand__Loaded(cdy_rt.primitives.path_resolve(prelude_path), prelude_exports, core__analyse_module(prelude_forms, prelude_exports, (), {}, builtins, read__read_hole, {}, False)), expand__Loaded(cdy_rt.primitives.path_resolve(form_path), form_exports, core__analyse_module(form_forms, form_exports, (core__Import(prelude_exports, form__NOWHERE, prelude__None()), core__Import(translator, form__NOWHERE, prelude__None())), {}, builtins, read__read_hole, {}, False))))

def declaration_exports(name: str) -> core__Exports:
    path = include__library_path((name + '.cdy'))
    return core__declared_exports(read__read_source(path, cdy_rt.primitives.slurp(path)), name)

def macro_imports(form: core__Exports, translator: core__Exports) -> tuple[core__Import, ...]:
    return (core__Import(form, form__NOWHERE, prelude__None()), core__Import(translator, form__NOWHERE, prelude__None()), core__Import(declaration_exports('string'), form__NOWHERE, prelude__Some(())))

def load_macro_file(builtins: _cdy_Mapping[str, core__Builtin], base: MacroBase) -> _cdy_Callable[[str, expand__Expander, tuple[str, ...]], tuple[expand__MacroFile, expand__Expander]]:
    def _cdy_t429(path: str, ex: expand__Expander, loading: tuple[str, ...]) -> tuple[expand__MacroFile, expand__Expander]:
        modules = include__read_modules(path)
        file = cdy_rt.primitives.at(modules, (len(modules) - 1))
        base_keys = cdy_rt.primitives.list_map((lambda l: l.key), base.modules)
        others = cdy_rt.primitives.list_filter((lambda m: (not cdy_rt.primitives.list_contains(m.key, base_keys))), cdy_rt.primitives.list_take((len(modules) - 1), modules))
        _tup = expand_modules(others, ex)
        ready = _tup[0]
        ex1 = _tup[1]
        _cdy__tup_32 = expand__expand_macro_file(file.forms, ex1, loading)
        expanded = _cdy__tup_32[0]
        ex2 = _cdy__tup_32[1]
        files = expanded.files
        deps = add_loaded(cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map((lambda f: f.modules), files)), ())
        by_key = loaded_exports((base.modules + deps), exports_by_key(ready))
        stem = file.stem
        exports = core__module_exports(expanded.forms, stem)
        macros = expanded.macros
        own_imports = (imported(file.imports, by_key) + implicit_imports(base, file.imports, by_key) + file_imports(files))
        mine = (cdy_rt.primitives.list_map((lambda r: macro_module(r, base, by_key, builtins)), ready) + (expand__Loaded(cdy_rt.primitives.path_resolve(path), exports, core__analyse_module(expanded.forms, exports, own_imports, {}, builtins, (lambda text, where: expand__expand_all(read__read_hole(text, where), macros)), macros, True)),))
        all_ = add_loaded(mine, deps)
        run = load_macro_tops(builtins, (base.modules + all_), ())
        return (expand__MacroFile(cdy_rt.primitives.path_resolve(path), expand__macro_list(expanded.defs, (lambda name: run(core__global_key(stem, name)))), all_), ex2)
    return _cdy_t429

def macro_module(r: Ready, base: MacroBase, by_key: _cdy_Mapping[str, core__Exports], builtins: _cdy_Mapping[str, core__Builtin]) -> expand__Loaded:
    m = r.module
    macros = r.macros
    return expand__Loaded(m.key, r.exports, core__analyse_module(r.forms, r.exports, (imported(m.imports, by_key) + implicit_imports(base, m.imports, by_key)), {}, builtins, (lambda text, where: expand__expand_all(read__read_hole(text, where), macros)), macros, True))

def load_own_macros(builtins: _cdy_Mapping[str, core__Builtin], base: MacroBase) -> _cdy_Callable[[tuple[form__Form, ...], tuple[expand__MacroFile, ...]], _cdy_Callable[[str], _cdy_Callable[[tuple[form__Form, ...]], form__Form]]]:
    def _cdy_t430(forms: tuple[form__Form, ...], files: tuple[expand__MacroFile, ...]) -> _cdy_Callable[[str], _cdy_Callable[[tuple[form__Form, ...]], form__Form]]:
        deps = add_loaded(cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map((lambda f: f.modules), files)), ())
        prelude = base.modules[0].exports
        imports = ((core__Import(prelude, form__NOWHERE, prelude__None()),) + base.imports + file_imports(files))
        return load_macro_tops(builtins, (base.modules + deps), core__analyse_module(forms, core__module_exports(forms, ''), imports, {}, builtins, read__read_hole, {}, True))
    return _cdy_t430

def load_macro_tops(builtins: _cdy_Mapping[str, core__Builtin], loaded: tuple[expand__Loaded, ...], tops: tuple[core__Top, ...]) -> _cdy_Callable[[str], _cdy_Callable[[tuple[form__Form, ...]], form__Form]]:
    all_ = check__type_check((cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map((lambda l: l.tops), loaded)) + tops), builtins)
    cdy_rt.primitives.restart_fresh_names(None)
    return interp_macros__macro_runner(all_)

def add_loaded(loaded: tuple[expand__Loaded, ...], start: tuple[expand__Loaded, ...]) -> tuple[expand__Loaded, ...]:
    def _cdy_t431(acc: tuple[expand__Loaded, ...], l: expand__Loaded) -> tuple[expand__Loaded, ...]:
        if cdy_rt.primitives.list_any((lambda m: (m.key == l.key)), acc):
            return acc
        else:
            return (acc + (l,))
    return cdy_rt.primitives.list_fold(_cdy_t431, start, loaded)

def loaded_exports(loaded: tuple[expand__Loaded, ...], start: _cdy_Mapping[str, core__Exports]) -> _cdy_Mapping[str, core__Exports]:
    return cdy_rt.primitives.list_fold((lambda m, l: cdy_rt.primitives.map_set(m, l.key, l.exports)), start, loaded)

def implicit_imports(base: MacroBase, imps: tuple[include__Imp, ...], by_key: _cdy_Mapping[str, core__Exports]) -> tuple[core__Import, ...]:
    stems = cdy_rt.primitives.list_map((lambda imp: cdy_rt.primitives.map_get(by_key, imp.key).stem), imps)
    return cdy_rt.primitives.list_filter((lambda i: (not cdy_rt.primitives.list_contains(i.exports.stem, stems))), base.imports)

def file_imports(files: tuple[expand__MacroFile, ...]) -> tuple[core__Import, ...]:
    def _cdy_t432(f: expand__MacroFile) -> core__Import:
        modules = f.modules
        return core__Import(cdy_rt.primitives.at(modules, (len(modules) - 1)).exports, form__NOWHERE, prelude__None())
    return cdy_rt.primitives.list_map(_cdy_t432, files)

def program_tops(modules: tuple[include__Module, ...], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]], builtins: _cdy_Mapping[str, core__Builtin]) -> tuple[core__Top, ...]:
    _tup = expand_modules(modules, expander(builtins))
    ready = _tup[0]
    _ex = _tup[1]
    by_key = exports_by_key(ready)
    elsewhere = core__elsewhere_names(exports_of(ready))
    return analyse_modules(ready, by_key, elsewhere, builtins, parse)

def expand_modules(modules: tuple[include__Module, ...], ex: expand__Expander) -> tuple[tuple[Ready, ...], expand__Expander]:
    def _cdy_t433(acc: tuple[tuple[Ready, ...], expand__Expander], m: include__Module) -> tuple[tuple[Ready, ...], expand__Expander]:
        _tup = acc
        done = _tup[0]
        e = _tup[1]
        declaring = include__is_declaration(m.key)
        all_ = m.forms
        _cdy__tup_106 = expand__expand_program((core__definitions(all_) if declaring else all_), e)
        forms = _cdy__tup_106[0]
        macros = _cdy__tup_106[1]
        e1 = _cdy__tup_106[2]
        own = core__module_exports(forms, m.stem)
        return ((done + (Ready(m, forms, macros, (core__with_declared(own, all_, m.stem) if declaring else own)),)), e1)
    return cdy_rt.primitives.list_fold(_cdy_t433, (NO_READY, ex), modules)
NO_READY: tuple[Ready, ...] = ()

def exports_by_key(ready: tuple[Ready, ...]) -> _cdy_Mapping[str, core__Exports]:
    return cdy_rt.primitives.list_fold((lambda m, r: cdy_rt.primitives.map_set(m, r.module.key, r.exports)), {}, ready)

def exports_of(ready: tuple[Ready, ...]) -> tuple[core__Exports, ...]:
    return cdy_rt.primitives.list_map((lambda r: r.exports), ready)

def analyse_modules(ready: tuple[Ready, ...], by_key: _cdy_Mapping[str, core__Exports], elsewhere: _cdy_Mapping[str, str], builtins: _cdy_Mapping[str, core__Builtin], parse: _cdy_Callable[[str, form__Pos], tuple[form__Form, ...]]) -> tuple[core__Top, ...]:
    def _cdy_t434(r: Ready) -> tuple[core__Top, ...]:
        macros = r.macros
        return core__analyse_module(r.forms, r.exports, imported(r.module.imports, by_key), elsewhere, builtins, (lambda text, where: expand__expand_all(parse(text, where), macros)), macros, False)
    return cdy_rt.primitives.list_concat(cdy_rt.primitives.list_map(_cdy_t434, ready))

def imported(imps: tuple[include__Imp, ...], by_key: _cdy_Mapping[str, core__Exports]) -> tuple[core__Import, ...]:
    return cdy_rt.primitives.list_map((lambda imp: core__Import(cdy_rt.primitives.map_get(by_key, imp.key), imp.pos, imp.only)), imps)

def load_macro_code(path: str) -> None:
    ex = expander(expand__library_builtins(None))
    _file = ex.load_file(path, ex, ())

def python_of(tops: tuple[core__Top, ...], top: str) -> str:
    stmts = lower__lower_program(tops, 0)
    globals_ = emit__global_names(tops, emit__Env({}, {}, {}, emit__generic_variants(tops), cdy_rt.spelling.SPELLINGS, {}, emit__deft_field_types(tops), top))
    env = emit__bind_locals(emit__bound_locals(stmts, ()), globals_)
    return (emit__HEADER + emit__emit_imports(emit__PY_IMPORTS) + '\ncdy_rt.primitives.stop_on_panic()\n' + emit__emit_stmts(stmts, 0, env) + (emit__emit_main(env) if core__has_main(tops, top) else ''))

def translate_text(text: str) -> str:
    return translate_modules(include__text_modules(text), read__read_hole)

def translate_file(path: str) -> str:
    return translate_modules(include__read_modules(path), read__read_hole)

def interpret_file(path: str, args: tuple[str, ...]) -> int:
    return interpret_modules(include__read_modules(path), args)

def interpret_text(text: str, args: tuple[str, ...]) -> int:
    return interpret_modules(include__text_modules(text), args)

def interpret_modules(modules: tuple[include__Module, ...], args: tuple[str, ...]) -> int:
    builtins = expand__library_builtins(None)
    interp_builtins__check_interp_builtins(builtins)
    return interp__interpret(check__type_check(program_tops(modules, read__read_hole, builtins), builtins), cdy_rt.primitives.at(modules, (len(modules) - 1)).stem, args, interp_builtins__BUILTINS)
USAGE: str = 'usage: cdy_translator.py FILE.cdy [OUT.py] | --interpret FILE.cdy [ARG ...]'

def main(args: tuple[str, ...]) -> int:
    if ((len(args) > 0) and (args[0] == '--interpret')):
        if (len(args) < 2):
            cdy_rt.primitives.put_err(USAGE)
            return 2
        else:
            return interpret_file(args[1], cdy_rt.primitives.list_drop(2, args))
    elif ((len(args) == 0) or (len(args) > 2)):
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
