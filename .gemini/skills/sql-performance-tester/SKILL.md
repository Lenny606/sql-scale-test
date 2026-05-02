---
name: sql-performance-tester
description: Expert in SQL database scalability, performance testing, and optimization. Use this skill to orchestrate load tests with Locust, generate large datasets, analyze query plans (EXPLAIN ANALYZE), and monitor database metrics via Prometheus/Grafana. It provides structured workflows for identifying bottlenecks and recommending optimizations like indexing, query refactoring, or schema changes.
---

# SQL Performance Tester Skill

You are an expert database engineer specialized in performance tuning and scalability. This skill provides you with the methodology and tools to test, analyze, and optimize SQL databases (specifically PostgreSQL in this environment).

## Core Workflows

### 1. Data Generation & Environment Setup
Before testing, ensure the environment is correctly seeded with a realistic volume of data.
- **Start Infrastructure**: Ensure all services in `docker-compose.yaml` are running (`primary-db`, `prometheus`, `grafana`).
- **Scale Data**: Modify `generator.py` to increase `num_comments` or `num_posts` for higher stress.
- **Import Procedure**:
    1. Run `python generator.py`.
    2. Copy CSVs to the container: `docker cp <file>.csv primary-db:/tmp/`.
    3. Execute `COPY` commands via `docker exec primary-db psql`.

### 2. Load Testing with Locust
Use Locust to simulate concurrent user activity.
- **Execution**: Run `locust -f locustfile.py --headless -u <users> -r <spawn-rate> --run-time <time>`.
- **Metrics to Track**:
    - **RPS** (Requests Per Second)
    - **Latency** (p50, p95, p99)
    - **Error Rate** (especially timeouts)

### 3. Bottleneck Identification
When performance degrades, use the following investigative steps:
- **Query Analysis**: Identify the top slow queries from Locust reports or `pg_stat_statements`.
- **Execution Plans**: Run `EXPLAIN (ANALYZE, BUFFERS) <query>;` inside the database to see the exact bottleneck (e.g., Seq Scan on a large table).
- **Resource Monitoring**: Check Grafana/Prometheus for:
    - CPU/Memory saturation (especially since `primary-db` is limited).
    - Disk I/O Wait.
    - Active connection counts.

### 4. Optimization Strategies
Based on the analysis, propose and implement:
- **Indexing**: Add B-tree, GIN, or BRIN indexes where appropriate.
- **Query Refactoring**: Optimize `JOIN` order, replace subqueries with `WITH` clauses or joins, or use partial indexes.
- **Schema Optimization**: Denormalization for heavy reads, or partitioning for very large tables.
- **Configuration Tuning**: Adjust `shared_buffers`, `work_mem`, or `maintenance_work_mem` (if the environment allows).

## Verification
Always verify the impact of a change:
1. Record baseline metrics.
2. Apply a **single** optimization.
3. Rerun the identical load test.
4. Compare RPS and latency.

## Available Resources
- `scripts/import_data.sh`: Helper to automate the COPY process.
- `references/postgresql-optimization.md`: (Optional) Guide for standard Postgres tuning parameters.
