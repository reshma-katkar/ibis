from ibis.sql.ibis_DB2.client import DB2Client

# from ibis.sql.ibis_DB2.compiler import dialect, rewrites  # noqa: F401


# def compile(expr, params=None):
#     return to_sqlalchemy(expr, dialect.make_context(params=params))


def connect(
    host='localhost',
    user=None,
    password=None,
    port=50000,
    database=None,
    url=None,
    driver='ibm_db_sa',
):
    return DB2Client(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database,
        url=url,
        driver=driver,
    )
