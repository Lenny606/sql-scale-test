# PostgreSQL Performance Optimization Reference

## Indexing Best Practices
- **B-Tree**: Default. Good for equality and range queries on most data types.
- **GIN (Generalized Inverted Index)**: Essential for JSONB (`@>` operator) and full-text search.
- **BRIN (Block Range Index)**: Very small, good for very large tables where data is physically sorted by the indexed column (e.g., `created_at`).
- **Partial Indexes**: `CREATE INDEX ... WHERE (active = true);` reduces index size and improves performance for specific subsets of data.
- **Covering Indexes**: `CREATE INDEX ... INCLUDE (col3);` allows "Index Only Scans" by including extra columns in the index leaf nodes.

## Query Tuning
- **Avoid SELECT \***: Retrieve only the columns you need.
- **LIMIT & OFFSET**: For large offsets, use "seek method" (keyset pagination) instead of `OFFSET`.
- **EXPLAIN ANALYZE**: 
    - `Seq Scan`: Full table scan. Often indicates a missing index.
    - `Index Scan`: Using an index to find rows.
    - `Index Only Scan`: Retrieving data directly from the index.
    - `Bitmap Index Scan`: Useful when multiple indexes can be combined.

## Configuration (postgresql.conf)
- **shared_buffers**: Recommended ~25% of total system memory.
- **work_mem**: Memory for complex sorts and hash tables. Increase for complex queries, but be careful as it's per-operation.
- **maintenance_work_mem**: Memory for VACUUM, CREATE INDEX, etc.
- **effective_cache_size**: Estimate of memory available for disk caching.

## Monitoring Queries
- **pg_stat_statements**: Must be enabled in `shared_preload_libraries`. Tracks execution statistics for all queries.
- **pg_stat_user_tables**: Shows sequential scans vs index scans per table.
- **pg_stat_activity**: Shows currently running queries and their wait events.
