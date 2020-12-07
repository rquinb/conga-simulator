import time
import psycopg2

class DatabaseConnection:

    def __init__(self, max_wait_seconds=15):
        self.max_wait_seconds = max_wait_seconds

    def connect_to_db(self, **kwargs):
        seconds_waited = 0
        db_conn = None
        while seconds_waited < self.max_wait_seconds:
            try:
                db_conn = psycopg2.connect(**kwargs)
                db_conn.autocommit = True
                break
            except Exception:
                seconds_waited += 1
                time.sleep(1)
        return db_conn


class SimulationsRepository:
    def __init__(self, db_connection):
        self._db_connection = db_connection

    def save_simulation(self, simulation_id, created_time, total_games, mean_rounds_per_game, details):
        with self._db_connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO simulations (id, created, total_games, mean_rounds_per_game, details)
            VALUES(%(simulation_id)s, %(created_time)s, %(total_games)s, %(mean_rounds_per_game)s, %(details)s) 
            ON CONFLICT (id) 
            DO 
               UPDATE SET details = %(details)s, 
                          total_games=%(total_games)s, 
                          mean_rounds_per_game=%(mean_rounds_per_game)s;
            """, {'simulation_id': simulation_id,
                  'created_time': created_time,
                  'total_games': total_games,
                  'mean_rounds_per_game': mean_rounds_per_game,
                  'details': details })

    def get_simulation(self, simulation_id):
        with self._db_connection.cursor() as cursor:
            cursor.execute("""
            SELECT id as simulation_id, created, total_games, mean_rounds_per_game, details
            FROM simulations
            WHERE id=%s
            """,[simulation_id])
            return cursor.fetchone()

    def get_simulations(self):
        with self._db_connection.cursor() as cursor:
            cursor.execute("""
            SELECT id as simulation_id, created, total_games, mean_rounds_per_game, details
            FROM simulations
            """)
            return [row for row in cursor]



