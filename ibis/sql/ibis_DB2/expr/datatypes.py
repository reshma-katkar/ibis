import collections
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
blob = BLOB()
dbclob = DBCLOB()
graphic = GRAPHIC()
vargraphic = VARGRAPHIC()
smallint = SMALLINT()
integer = INTEGER()
bigint = BIGINT()


class Token_DB2(dt.Tokens):
    __slots__ = ()
    CLOB = 1
    BLOB = 2
    DBCLOB = 3
    GRAPHIC = 4
    VARGRAPHIC = 5
    SMALLINT = 6
    INTEGER = 7
    BIGINT = 8

    @staticmethod
    def name(value):
        return _token_names[value]


_TYPE_RULES = collections.OrderedDict(
    [
        # complex types
        (
            '(?P<{}>{})'.format(token.upper(), token),
            typing.cast(
                dt.Action, lambda token, toktype=toktype: Token(toktype, token)
            ),
        )
        for token, toktype in zip(
            (
                'clob',
                'blob',
                'dbclob',
                'graphic',
                'vargraphic',
                'smallint',
                'integer',
                'bigint',
            ),
            (
                Token_DB2.CLOB,
                Token_DB2.BLOB,
                Token_DB2.DBCLOB,
                Token_DB2.GRAPHIC,
                Token_DB2.VARGRAPHIC,
                Token_DB2.SMALLINT,
                Token_DB2.INTEGER,
                Token_DB2.BIGINT,
            ),
        )
    ]
)
_TYPE_RULES.update(dt._TYPE_RULES)
_TYPE_KEYS = tuple(_TYPE_RULES.keys())
# _TYPE_PATTERN = re.compile('|'.join(_TYPE_KEYS), flags=re.IGNORECASE)


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
