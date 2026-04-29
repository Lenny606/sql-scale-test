import time
import psycopg2
from locust import User, task, between

class PostgresClient:
    """Jednoduchý klient, který loguje výsledky do Locustu"""
    def __init__(self, host, database, user, password, environment):
        self.conn = psycopg2.connect(
            host=host, database=database, user=user, password=password
        )
        self.conn.autocommit = True
        self.environment = environment

    def query(self, name, sql, params=None):
        start_time = time.perf_counter()
        res = []
        exception = None
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                if cur.description:
                    res = cur.fetchall()
        except Exception as e:
            exception = e
        
        total_time = (time.perf_counter() - start_time) * 1000
        
        # Nový způsob logování v Locustu 2.x
        self.environment.events.request.fire(
            request_type="SQL",
            name=name,
            response_time=total_time,
            response_length=len(res),
            exception=exception,
        )
        return res

class DatabaseUser(User):
    # Simulujeme náhodné čekání uživatele mezi akcemi
    wait_time = between(1, 2)

    def on_start(self):
        # Každý simulovaný uživatel má vlastní spojení do DB
        self.client = PostgresClient(
            host="localhost", 
            database="scaling_test", 
            user="user", 
            password="password",
            environment=self.environment
        )

    @task(3)
    def heavy_aggregation(self):
        # Tento dotaz bude bez indexů na 1M datech náročný
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