"""Test support for already-defined UDFs in Oracle"""

import pytest

import ibis.expr.datatypes as dt
from ibis.sql.ibis_oracle.udf.api import existing_udf

# mark test module as oracle (for ability to easily exclude,
# e.g. in conda build tests)
#     TODO: update Windows pipeline to exclude oracle_extensions

pytestmark = [
    pytest.mark.oracle,
    pytest.mark.oracle_extensions,
]

# Database setup (tables and UDFs)


@pytest.fixture(scope='session')
def next_serial(con):
    serial_proxy = con.con.execute(
        "select test_sequence.nextval as value from dual"
    )
    return serial_proxy.fetchone()['value']


@pytest.fixture(scope='session')
def test_schema(con, next_serial):
    schema_name = 'udf_test_{}'.format(next_serial)
    # schema_name='"{}"'.format(schema_name)
    print(schema_name)
    con.con.execute("CREATE USER {}".format(schema_name))
    # con.con.execute("CREATE USER "+ schema_name)
    return schema_name


@pytest.fixture(scope='session')
def table_name():
    return 'udf_user_list_11'


@pytest.fixture(scope='session')
def sql_table_setup(test_schema, table_name):
    return """CREATE TABLE {schema}.{table_name} (
            user_id integer,
            user_name varchar(50),
            num integer,
            num_add integer
)""".format(
        schema=test_schema, table_name=table_name
    )


@pytest.fixture(scope='session')
def permission_schema(test_schema):
    return '''GRANT UNLIMITED TABLESPACE TO {schema}'''.format(
        schema=test_schema
    )


@pytest.fixture(scope='session')
def sql_table_Insert(test_schema, table_name):
    return """INSERT INTO {schema}.{table_name}(user_id, user_name, num, num_add)
    (SELECT 1, 'Raj', 3, 13 FROM dual) UNION ALL
    (SELECT 2, 'Judy', 4, 14 FROM dual) UNION ALL
    (SELECT 3, 'Jonathan', 8, 18 FROM dual)""".format(
        schema=test_schema, table_name=table_name
    )


@pytest.fixture(scope='session')
def sql_define_udf(test_schema):
    return """CREATE OR REPLACE FUNCTION {schema}.addition_func(n1 in integer)
RETURN integer
is
n3 number(8);
begin
n3 := n1+10;
return n3;
end;""".format(
        schema=test_schema
    )


@pytest.fixture(scope='session')
def con_for_udf(
    con,
    test_schema,
    table_name,
    sql_table_setup,
    permission_schema,
    sql_table_Insert,
    sql_define_udf,
):
    con.con.execute(sql_table_setup)
    con.con.execute(permission_schema)
    con.con.execute(sql_table_Insert)
    con.con.execute(sql_define_udf)

    try:
        yield con
    finally:
        # teardown
        print("In finally block")
        con.con.execute("DROP USER " + test_schema + " cascade")
        # con.con.execute("DROP USER schema CASCADE".format(test_schema))


@pytest.fixture
def table(con_for_udf, table_name, test_schema):
    return con_for_udf.table(table_name, schema=test_schema)


# Tests
def test_existing_sql_udf(test_schema, table):
    """Test creating ibis UDF object based on existing UDF in the database"""
    # Create ibis UDF objects referring to UDFs already created in the database
    custom_length_udf = existing_udf(
        'addition_func',
        input_types=[dt.int32],
        output_type=dt.int32,
        schema=test_schema,
    )
    result_obj = table[
        table, custom_length_udf(table['num']).name('addition_func')
    ]
    result = result_obj.execute()
    print(result)
    print(result['addition_func'].sum())
    assert result['addition_func'].sum() == result['num_add'].sum()


def pysplit(text, split):
    return text.split(split)
