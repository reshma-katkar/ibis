import os

import pandas as pd
import pytest

import ibis
import ibis.expr.types as ir
import ibis.ibis_mssql
from ibis.tests.util import assert_equal

sa = pytest.importorskip('sqlalchemy')

pytestmark = pytest.mark.mssql

MSSQL_USER = os.environ.get('IBIS_TEST_MSSQL_USER', 'user')
MSSQL_PASS = os.environ.get('IBIS_TEST_MSSQL_PASSWORD', 'pass')
MSSQL_HOST = os.environ.get('IBIS_TEST_MSSQL_HOST', 'host')
MSSQL_PORT = os.environ.get('IBIS_TEST_MSSQL_PORT', 'port')
MSSQL_DB = os.environ.get('IBIS_TEST_MSSQL_DATABASE', 'db_name')


def test_table(alltypes):
    assert isinstance(alltypes, ir.TableExpr)


def test_array_execute(alltypes):
    d = alltypes.limit(2).double_col
    s = d.execute()
    assert isinstance(s, pd.Series)
    assert len(s) == 2


def test_literal_execute(con):
    expr = ibis.literal('1234')
    result = con.execute(expr)
    assert result == '1234'


def test_simple_aggregate_execute(alltypes):
    d = alltypes.double_col.sum()
    v = d.execute()
    assert isinstance(v, float)


def test_list_tables(con):
    assert len(con.list_tables()) > 0
    assert len(con.list_tables(like='functional')) == 1


def test_compile_verify(alltypes):
    unsupported_expr = alltypes.double_col.approx_median()
    assert not unsupported_expr.verify()

    supported_expr = alltypes.double_col.sum()
    assert supported_expr.verify()


def test_database_layer(con, alltypes):
    db = con.database()
    t = db.functional_alltypes

    assert_equal(t, alltypes)

    assert db.list_tables() == con.list_tables()

    db_schema = con.schema("INFORMATION_SCHEMA")

    assert db_schema.list_tables() != con.list_tables()


def test_compile_toplevel():
    t = ibis.table([('foo', 'double')], name='t0')

    # it works!
    expr = t.foo.sum()
    result = ibis.ibis_mssql.compile(expr)
    expected = "SELECT sum(t0.foo) AS sum \nFROM t0 AS t0"  # noqa

    assert str(result) == expected


def test_list_databases(con):
    assert MSSQL_DB is not None
    assert MSSQL_DB in con.list_databases()


def test_list_schemas(con):
    assert 'dbo' in con.list_schemas()
    assert 'INFORMATION_SCHEMA' in con.list_schemas()


def test_metadata_is_per_table():
    con = ibis.ibis_mssql.api.connect(
        host=MSSQL_HOST,
        database=MSSQL_DB,
        user=MSSQL_USER,
        password=MSSQL_PASS,
        port=MSSQL_PORT,
    )
    assert len(con.meta.tables) == 0

    # assert that we reflect only when a table is requested
    t = con.table('functional_alltypes')  # noqa
    assert 'functional_alltypes' in con.meta.tables
    assert len(con.meta.tables) == 1


def test_schema_table():
    con = ibis.ibis_mssql.api.connect(
        host=MSSQL_HOST,
        database=MSSQL_DB,
        user=MSSQL_USER,
        password=MSSQL_PASS,
        port=MSSQL_PORT,
    )

    # ensure that we can reflect the information schema (which is guaranteed
    # to exist)
    schema = con.schema('dbo')

    assert isinstance(schema['functional_alltypes'], ir.TableExpr)


@pytest.mark.parametrize('params', [{}, {'database': MSSQL_DB}])
def test_create_and_drop_table(con, temp_table, params):
    sch = ibis.schema(
        [
            ('first_name', 'string'),
            ('last_name', 'string'),
            ('department_name', 'string'),
            ('salary', 'float64'),
        ]
    )

    con.create_table(temp_table, schema=sch, **params)
    assert con.table(temp_table, **params) is not None

    con.drop_table(temp_table, **params)

    with pytest.raises(sa.exc.NoSuchTableError):
        con.table(temp_table, **params)
