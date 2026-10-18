import re

from parsec import *

# ignore cases.
whitespace = regex(r'\s+', re.MULTILINE)
comment = regex(r';.*')
ignore = many((whitespace | comment))
