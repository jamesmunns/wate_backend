from faker import Factory
from random import random, randint
from datetime import date, timedelta
import psycopg2
import getpass
from decimal import Decimal

ff = Factory.create()

def generate_users(cursor):
  min_users = 10
  max_users = 100

  num_users = randint(min_users, max_users)

  for _ in xrange(num_users):
    name     = ff.name()
    email    = ff.email()
    username = ff.user_name()
    jdate    = date.today() - timedelta(days=randint(5,100))

    # print name, email, jdate,

    min_sample = 20
    max_sample = 100
    num_sample = randint( min_sample, max_sample )

    user_cmd = """
      INSERT INTO users ( name, email, username, joindate )
      VALUES ( %s, %s, %s, %s );
      """

    cursor.execute( user_cmd, [ name, email, username, jdate ] )

    # Get userid
    id_fetch_cmd = """
      SELECT * from users where email = %s;
      """

    cursor.execute( id_fetch_cmd, [ email ] )
    users = cursor.fetchall()
    assert len( users ) == 1
    userid = users[0][0]

    # Weights for the users
    max_wgt = float(randint( 120, 200 ))
    min_wgt = float(randint( 120, max_wgt ))
    
    # weight cmd
    wgt_cmd = """
      INSERT INTO weights ( user_id, weight_lbs, measure_date )
      VALUES ( %s, %s, %s );
      """

    for samp in xrange(num_sample):
      weight = float(max_wgt) - ( ( max_wgt - min_wgt ) * ( float(samp) / num_sample ) + ( 2 * random() ) )
      weight = Decimal( "%.2f" % weight )
      wdate  = jdate + timedelta(days=samp)
      # print wdate, weight, " > "
      cursor.execute( wgt_cmd, [ userid, weight, wdate ] )      

    # print ""

db = "wate"

with psycopg2.connect( dbname=db, user=getpass.getuser(), password=getpass.getpass("Password for user {}: ".format(getpass.getuser()))) as conn:
  with conn.cursor() as cur:
    generate_users(cur)
