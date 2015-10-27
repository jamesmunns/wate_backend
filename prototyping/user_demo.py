from flask import Flask
import psycopg2 as pg
import getpass
from flask import g

username = getpass.getuser()
password = getpass.getpass("Password for {}: ".format(username))
dbname   = "wate"

app = Flask(__name__)

@app.route('/user/<username>')
def user_data(username=None):
    if username is None:
      return "Invalid User!", 404
    
    retval = ""

    get_user_name = """
      SELECT username, name FROM users
        WHERE username = %s;
      """

    get_all_wgt = """
      SELECT weights.weight_lbs,weights.measure_date
        FROM users,weights
        WHERE weights.user_id = users.id
          and users.username = %s;
      """

    with get_db().cursor() as cur:
        cur.execute(get_user_name, [username])
        user = cur.fetchall()[0]
        retval += "Username: {} | User Name: {}<br><br>".format( user[0], user[1] )
        
        cur.execute(get_all_wgt, [username])
        for wgt in cur.fetchall():
            retval += "{} | {}<br>".format(wgt[0], wgt[1])

    if retval == "":
        retval = "Unknown user error!", 520

    return retval
  

@app.route('/')
def hello_world():
    get_users = """
      SELECT * from users;
      """

    retval =  "Hello, world!<br>"
    retval += "id, name, email, jdate<br>"
    with get_db().cursor() as cur:
        cur.execute(get_users)
        for userline in cur.fetchall():
            retval += "{}, {}, {}, {}<br>".format( userline[0], userline[1], userline[2], userline[3] )

    return retval

def get_db():
    db = getattr(g, '_dbc', None)
    if db is None:
        db = g._dbc = pg.connect(dbname=dbname, user=username, password=password)
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_dbc', None)
    if db is not None:
        db.close()

if __name__ == '__main__':    
    app.run(host='0.0.0.0', debug=True)
