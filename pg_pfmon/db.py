import json

import asyncpg


async def connect_db(host, port, user, password, database):
    conn = await asyncpg.connect(
        host=host, port=port, user=user, password=password, database=database
    )
    try:
        await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
    except asyncpg.exceptions.InterfaceError as e:
        raise Exception("Failed to set json codec") from e
    return conn


async def execute_query(conn, query):
    return await conn.fetch(query)

async def fetch_db_version(conn):
    result = await conn.fetchrow("SELECT version();")
    return result['version']

async def check_pg_stat_statements(conn):
    result = await conn.fetchval(
        "SELECT count(1) FROM information_schema.tables WHERE table_name = 'pg_stat_statements';"
    )
    return result > 0

async def fetch_pg_stat_statements_count(conn):
    result = await conn.fetchval(
        "SELECT count(1) FROM pg_stat_statements;"
    )
    return result

async def run_probe(conn, query, query_extra=None):
    result = await execute_query(conn, query)
    evidence = await execute_query(conn, query_extra) if query_extra else None
    return result, evidence