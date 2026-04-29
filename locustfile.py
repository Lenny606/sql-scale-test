import time
import psycopg2
from locust import User, task, between

class PostgresClient:
    """Jednoduchý klient, který loguje výsledky do Locustu"""
    def __init__(self, host, database, user, password, environment):
        self.conn = None
        self.environment = environment
        
        start_time = time.perf_counter()
        try:
            self.conn = psycopg2.connect(
                host=host, database=database, user=user, password=password
            )
            self.conn.autocommit = True
        except Exception as e:
            total_time = (time.perf_counter() - start_time) * 1000
            self.environment.events.request.fire(
                request_type="SQL",
                name="connection_established",
                response_time=total_time,
                response_length=0,
                exception=e,
            )
            raise e # Stále vyhodíme chybu, aby uživatel nepokračoval bez spojení

    def query(self, name, sql, params=None):
        start_time = time.perf_counter()
        res = []
        exception = None
        
        if not self.conn:
            return []

        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                if cur.description:
                    res = cur.fetchall()
        except Exception as e:
            exception = e
        
        total_time = (time.perf_counter() - start_time) * 1000
        
        self.environment.events.request.fire(
            request_type="SQL",
            name=name,
            response_time=total_time,
            response_length=len(res),
            exception=exception,
        )
        return res

class DatabaseUser(User):
    wait_time = between(1, 2)

    def on_start(self):
        try:
            self.client = PostgresClient(
                host="localhost", 
                database="scaling_test", 
                user="user", 
                password="password",
                environment=self.environment
            )
        except Exception:
            # Chyba už byla nahlášena v PostgresClient.__init__
            pass

    @task(3)
    def heavy_aggregation(self):
        if hasattr(self, 'client'):
            self.client.query(
                "count_top_users", 
                "SELECT username, COUNT(*) FROM users GROUP BY username HAVING COUNT(*) > 1 ORDER BY 2 DESC LIMIT 10;"
            )

    @task(1)
    def insert_comment(self):
        if hasattr(self, 'client'):
            self.client.query(
                "insert_comment",
                "INSERT INTO comments (post_id, user_id, comment_text) VALUES (%s, %s, %s) RETURNING id;",
                (1, 1, "Testing scaling...")
            )