import ibm_db_sa
import sqlalchemy as sa
from ibm_db_sa.base import DB2Dialect

import ibis.expr.datatypes as dt11
import ibis.sql.alchemy as s_al
import ibis.sql.ibis_DB2.expr.datatypes as dt

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


@dt.dtype.register(DB2Dialect, ibm_db_sa.CLOB)
def sa_db2_CLOB(_, satype, nullable=True):
    return dt.CLOB(nullable=nullable)


@dt.dtype.register(DB2Dialect, ibm_db_sa.BLOB)
def sa_db2_BLOB(_, satype, nullable=True):
    return dt.BLOB(nullable=nullable)


@dt.dtype.register(DB2Dialect, ibm_db_sa.GRAPHIC)
def sa_db2_GRAPHIC(_, satype, nullable=True):
    return dt.GRAPHIC(nullable=nullable)


@dt.dtype.register(DB2Dialect, ibm_db_sa.VARGRAPHIC)
def sa_db2_VARGRAPHIC(_, satype, nullable=True):
    return dt.VARGRAPHIC(nullable=nullable)


@dt.dtype.register(DB2Dialect, ibm_db_sa.SMALLINT)
def sa_db2_SMALLINT(_, satype, nullable=True):
    return dt.SMALLINT(nullable=nullable)


@dt.dtype.register(DB2Dialect, ibm_db_sa.INTEGER)
def sa_db2_INTEGER(_, satype, nullable=True):
    return dt.INTEGER(nullable=nullable)


@dt.dtype.register(DB2Dialect, ibm_db_sa.BIGINT)
def sa_db2_BIGINT(_, satype, nullable=True):
    return dt.BIGINT(nullable=nullable)
