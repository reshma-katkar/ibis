import collections
import re
import typing

from multipledispatch import Dispatcher

import ibis.expr.datatypes as dt
import ibis.sql.ibis_DB2.expr.types as ir

Token = collections.namedtuple('Token', ('type', 'value'))

_token_names = dict(
    (getattr(dt.Tokens, n), n)
    for n in dir(dt.Tokens)
    if n.isalpha() and n.isupper()
)


class CLOB(dt.String):
    scalar = ir.CLOBScalar
    column = ir.CLOBColumn
    __slots__ = ()


class BLOB(dt.String):
    scalar = ir.BLOBScalar
    column = ir.BLOBColumn
    __slots__ = ()


class DBCLOB(dt.Binary):
    scalar = ir.DBCLOBScalar
    column = ir.DBCLOBColumn
    __slots__ = ()


class GRAPHIC(dt.String):
    scalar = ir.GRAPHICScalar
    column = ir.GRAPHICColumn
    __slots__ = ()


class VARGRAPHIC(dt.String):
    scalar = ir.VARGRAPHICScalar
    column = ir.VARGRAPHICColumn
    __slots__ = ()


class SMALLINT(dt.SignedInteger):
    __slots__ = ()
    _nbytes = 4


class INTEGER(dt.Primitive):
    scalar = ir.INTEGERScalar
    column = ir.INTEGERColumn

    __slots__ = ()

    @property
    def _nbytes(self) -> int:
        raise TypeError(
            "Cannot determine the size in bytes of an abstract integer type."
        )


class BIGINT(dt.SignedInteger):
    __slots__ = ()
    _nbytes = 4


REAL = dt.Float32


clob = CLOB()
BLOB = BLOB()
DBCLOB = DBCLOB()
GRAPHIC = GRAPHIC()
VARGRAPHIC = VARGRAPHIC()
SMALLINT = SMALLINT()
INTEGER = INTEGER()
BIGINT = BIGINT()


class Token_DB2(dt.Tokens):
    __slots__ = ()
    CLOB = 1
    NCLOB = 2
    LONG = 3
    NUMBER = 4
    BFILE = 5
    RAW = 6
    LONGRAW = 7
    VARCHAR = 8
    CHAR = 9

    @staticmethod
    def name(value):
        return _token_names[value]


_TYPE_RULES = collections.OrderedDict(
    [
        # decimal + complex types
        (
            '(?P<{}>{})'.format(token.upper(), token),
            typing.cast(
                dt.Action, lambda token, toktype=toktype: Token(toktype, token)
            ),
        )
        for token, toktype in zip(
            ('varchar', 'char', 'number', 'time',),
            (
                Token_DB2.VARCHAR,
                Token_DB2.CHAR,
                Token_DB2.NUMBER,
                Token_DB2.TIME,
            ),
        )
    ]
)
_TYPE_RULES.update(dt._TYPE_RULES)
_TYPE_KEYS = tuple(_TYPE_RULES.keys())
_TYPE_PATTERN = re.compile('|'.join(_TYPE_KEYS), flags=re.IGNORECASE)


class TypeParser_Oracle(dt.TypeParser):
    def type(self) -> dt.DataType:
        if self._accept(Token_DB2.CLOB):
            return CLOB()
        elif self._accept(Token_DB2.BLOB):
            return BLOB()
        elif self._accept(Token_DB2.DBCLOB):
            return DBCLOB()
        elif self._accept(Token_DB2.GRAPHIC):
            return GRAPHIC()
        elif self._accept(Token_DB2.VARGRAPHIC):
            return VARGRAPHIC()
        elif self._accept(Token_DB2.SMALLINT):
            return SMALLINT()
        elif self._accept(Token_DB2.INTEGER):
            return INTEGER()
        elif self._accept(Token_DB2.BIGINT):
            return BIGINT()
        else:
            raise SyntaxError('Type cannot be parsed: {}'.format(self.text))


dtype = Dispatcher('dtype')
validate_type = dtype

castable = Dispatcher('castable')


@castable.register(CLOB, CLOB)
def can_cast_clob(source, target, **kwargs):
    return True


@castable.register(BLOB, BLOB)
def can_cast_blob(source, target, **kwargs):
    return True


@castable.register(DBCLOB, DBCLOB)
def can_cast_dbclob(source, target, **kwargs):
    return True


@castable.register(GRAPHIC, GRAPHIC)
def can_cast_graphic(source, target, **kwargs):
    return True


@castable.register(VARGRAPHIC, VARGRAPHIC)
def can_cast_vargraphic(source, target, **kwargs):
    return True


@castable.register(SMALLINT, SMALLINT)
def can_cast_smallint(source, target, **kwargs):
    return True


@castable.register(INTEGER, INTEGER)
def can_cast_integer(source, target, **kwargs):
    return True


@castable.register(BIGINT, BIGINT)
def can_cast_bigint(source, target, **kwargs):
    return True


@castable.register(REAL, REAL)
def can_cast_real(source, target, **kwargs):
    return True
