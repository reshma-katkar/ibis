import ibm_db_sa as DB2Dialect
import sqlalchemy as sa

import ibis.expr.datatypes as dt11
import ibis.sql.alchemy as s_al
import ibis.sql.ibis_oracle.expr.datatypes as dt

_ibis_type_to_sqla = {
    dt.CLOB: sa.CLOB,
    dt.BLOB: sa.BLOB,
    dt.SMALLINT: sa.SMALLINT,
    dt.INTEGER: sa.INTEGER,
    dt.BIGINT: sa.BIGINT,
}
_ibis_type_to_sqla.update(s_al._ibis_type_to_sqla)


def _to_sqla_type(itype, type_map=None):
    if type_map is None:
        type_map = _ibis_type_to_sqla
    if isinstance(itype, dt11.Decimal):
        return sa.types.NUMERIC(itype.precision, itype.scale)
    elif isinstance(itype, dt11.Date):
        return sa.Date()
    elif isinstance(itype, dt11.Timestamp):
        # SQLAlchemy DateTimes do not store the timezone, just whether the db
        # supports timezones.
        return sa.TIMESTAMP(bool(itype.timezone))
    elif isinstance(itype, dt11.Array):
        ibis_type = itype.value_type
        if not isinstance(ibis_type, (dt11.Primitive, dt11.String)):
            raise TypeError(
                'Type {} is not a primitive type or string type'.format(
                    ibis_type
                )
            )
        return sa.ARRAY(_to_sqla_type(ibis_type, type_map=type_map))
    else:
        return type_map[type(itype)]


class AlchemyExprTranslator(s_al.AlchemyExprTranslator):
    s_al.AlchemyExprTranslator._type_map = _ibis_type_to_sqla


class AlchemyDialect(s_al.AlchemyDialect):
    s_al.translator = AlchemyExprTranslator


@dt.dtype.register(DB2Dialect, DB2Dialect.CLOB)
def sa_oracle_CLOB(_, satype, nullable=True):
    return dt.CLOB(nullable=nullable)


@dt.dtype.register(DB2Dialect, DB2Dialect.BLOB)
def sa_oracle_BLOB(_, satype, nullable=True):
    return dt.BLOB(nullable=nullable)


@dt.dtype.register(DB2Dialect, DB2Dialect.DBCLOB)
def sa_oracle_DBCLOB(_, satype, nullable=True):
    return dt.DBCLOB(nullable=nullable)


@dt.dtype.register(DB2Dialect, DB2Dialect.GRAPHIC)
def sa_oracle_GRAPHIC(_, satype, nullable=True):
    return dt.GRAPHIC(nullable=nullable)


@dt.dtype.register(DB2Dialect, DB2Dialect.VARGRAPHIC)
def sa_oracle_VARGRAPHIC(_, satype, nullable=True):
    return dt.VARGRAPHIC(nullable=nullable)


@dt.dtype.register(DB2Dialect, DB2Dialect.SMALLINT)
def sa_oracle_SMALLINT(_, satype, nullable=True):
    return dt.SMALLINT(nullable=nullable)


@dt.dtype.register(DB2Dialect, DB2Dialect.INTEGER)
def sa_oracle_INTEGER(_, satype, nullable=True):
    return dt.INTEGER(nullable=nullable)


@dt.dtype.register(DB2Dialect, DB2Dialect.BIGINT)
def sa_oracle_BIGINT(_, satype, nullable=True):
    return dt.BIGINT(nullable=nullable)
