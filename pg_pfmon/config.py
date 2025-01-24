import os

DB_VERSION_THRESHOLD = os.environ.get("DB_VERSION_THRESHOLD", 16)
MAX_NR_OF_CONNECTIONS = os.environ.get("MAX_NR_OF_CONNECTIONS", 90) # default db global limit is 100
QUERY_LENGTH_TO_PRINT = os.environ.get("QUERY_LENGTH_TO_PRINT", 2048)

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_DATABASE = os.environ.get("DB_DATABASE")