import psycopg2
import getpass

username = getpass.getuser()
password = getpass.getpass("Database password for {}: ".format(username))
database = "wate"

def create_user_table(cursor):
  user_schema = """
    CREATE TABLE users (
      id serial PRIMARY KEY,
      name text NOT NULL,
      username text NOT NULL,
      email citext UNIQUE NOT NULL,
      joindate date NOT NULL);
    """
  cursor.execute(user_schema)

def create_weight_table(cursor):
  weight_schema = """
    CREATE TABLE weights (
      user_id integer REFERENCES users(id) NOT NULL,
      weight_lbs numeric CHECK (weight_lbs > 0) NOT NULL,
      measure_date date NOT NULL,
      measure_time time);
    """
  cursor.execute(weight_schema)  

with psycopg2.connect(dbname=database, user=username, password=password) as conn:
  with conn.cursor() as cur:
    create_user_table(cur)
    create_weight_table(cur)
