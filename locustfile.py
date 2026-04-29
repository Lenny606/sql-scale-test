import time
import psycopg2
from locust import User, task, between, events

class PostgresClient:
    """Jednoduchý klient, který loguje výsledky do Locustu"""
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host, database=database, user=user, password=password
        )
        self.conn.autocommit = True

    def query(self, name, sql, params=None):
        start_time = time.time()
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                res = cur.fetchall()
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="SQL", name=name, response_time=total_time, exception=e
            )
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="SQL", name=name, response_time=total_time, response_length=len(res)
            )

class DatabaseUser(User):
    # Simulujeme náhodné čekání uživatele mezi akcemi
    wait_time = between(1, 2)

    def on_start(self):
        # Každý simulovaný uživatel má vlastní spojení do DB
        self.client = PostgresClient(
            host="localhost", 
            database="scaling_test", 
            user="user", 
            password="password"
        )

    @task(3)
    def heavy_aggregation(self):
        # Tento dotaz bude bez indexů na 10M datech extrémně náročný
        self.client.query(
            "count_top_users", 
            "SELECT username, COUNT(*) FROM users GROUP BY username HAVING COUNT(*) > 1 ORDER BY 2 DESC LIMIT 10;"
        )

    @task(1)
    def insert_comment(self):
        # Simulace zápisu (INSERT)
        self.client.query(
            "insert_comment",
            "INSERT INTO comments (post_id, user_id, comment_text) VALUES (%s, %s, %s) RETURNING id;",
            (1, 1, "Testing scaling...")
        )