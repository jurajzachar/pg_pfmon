# About
This project is a simple tool to proactively monitor utilization of PostgreSQL database with `pg_stats` extension.
It has been developed off the back of work done by Dmitry Romanoff, who has written a great article on [the subject]()
https://medium.com/@dmitry.romanoff/proactive-postgresql-database-s-performance-scanner-9f1cad5c2c0f).

# Build
To build the project, run the following command:
```bash 
make build
```

# Run
configure your environment variables in a `.env` file. You can use this example as a template.
```
DB_DATABASE=mydatabase
DB_HOST=192.168.0.1
DB_PASSWORD=mysecretpassword
DB_PORT=5432
DB_USER=postgres
```

Then run as dockerized app:
```bash
docker run --env-file .env pg_pfmon:latest

Database Version: PostgreSQL 16.6 (Ubuntu 16.6-0ubuntu0.24.10.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 14.2.0-4ubuntu2) 14.2.0, 64-bit
No issues found.
```

# Probes
The tool will check the following probes:
  1. Check for database consuming too many connections
  2. Check for queries that allocate the most connection slots (coming soon)
  1. Check for queries that take too long to execute (coming soon)
     2. by CPU consumption
     3. by seconds to complete

# Custom Probes
Custom probes can be added to [probes.py](./pg_pfmon/probes.py) and called from the [main](./pg_pfmon/main.py) script.