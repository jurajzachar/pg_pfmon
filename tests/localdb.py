import pytest
from testcontainers.postgres import PostgresContainer

pytest_plugins = ["pytest_asyncio"]

@pytest.fixture(scope="function")
def postgres_testcontainer() -> PostgresContainer:
    with PostgresContainer("postgres:17.2") as postgres:
        postgres.driver = "asyncpg"
        postgres.start()
        yield postgres


async def db_connection(postgres_testcontainer):
    conn = await postgres_testcontainer.connect()
    return conn