from config import QUERY_LENGTH_TO_PRINT
from pg_pfmon import config


async def probe_connections(conn):
    n_threshold = config.MAX_NR_OF_CONNECTIONS
    probe = f"Check there are no databases with more than {n_threshold} active connections"
    issue = "Databases with the high number of active connections detected"
    recommendation = ("Check why applications open so many active connections. "
                      "It may be wrong configuration or unusual application pattern.")

    sql_query = f"""
    SELECT datname, count(1) num_of_active_connections, 'wvw' chk
    FROM pg_stat_activity
    WHERE datname!='' AND state!='idle'
    GROUP BY datname
    HAVING count(1)>{n_threshold}
    ORDER BY 2 DESC
    """

    sql_query_extra = f"""
    SELECT datname, state, client_addr, client_hostname, substr(query, 1, {QUERY_LENGTH_TO_PRINT}) query
    FROM pg_stat_activity
    WHERE state!='idle' AND datname IN (
        SELECT datname
        FROM (
            SELECT datname, count(1) num_of_active_sessions
            FROM pg_stat_activity
            WHERE state!='idle' AND datname!=''
            GROUP BY 1
            HAVING count(1)>0
        ) M
    )
    ORDER BY 1, 5
    """

    return probe, issue, recommendation, sql_query, sql_query_extra

