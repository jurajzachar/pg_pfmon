import asyncio

from db import connect_db, fetch_db_version, check_pg_stat_statements, fetch_pg_stat_statements_count, run_probe
from pg_pfmon import config
from probes import probe_connections


async def main():
    host = config.DB_HOST
    assert host, "DB_HOST environment variable is not set"
    port = config.DB_PORT
    assert port, "DB_PORT environment variable is not set"
    user = config.DB_USER
    assert user, "DB_USER environment variable is not set"
    password = config.DB_PASSWORD
    assert password, "DB_PASSWORD environment variable is not set"
    database = config.DB_DATABASE
    assert database, "DB_DATABASE environment variable is not set"

    conn = await connect_db(host, port, user, password, database)

    db_version = await fetch_db_version(conn)
    print(f"Database Version: {db_version}")

    if not await check_pg_stat_statements(conn):
        print("The pg_stat_statements table does not exist. Please create extension pg_stat_statements.")
        return

    if await fetch_pg_stat_statements_count(conn) == 0:
        print("The pg_stat_statements table is empty. Please enable pg_stat_statements")
        return

    probe, issue, recommendation, sql_query, sql_query_extra = await probe_connections(conn)
    result, evidence = await run_probe(conn, sql_query, sql_query_extra)

    if not result:
        print("No issues found.")
        return
    
    print(f"Probe: {probe}")
    print(f"Issue: {issue}")
    print(f"Recommendation: {recommendation}")
    print(f"Result: {result}")

    if evidence:
        print(f"Evidence: {evidence}")
        for item in evidence[0].items():
            print(f"{item[0]}: {item[1]}")
            print("-" * 80)

    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())