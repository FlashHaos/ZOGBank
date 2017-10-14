import MySQLdb

def connect():
    try:
        conn = MySQLdb.connect(host="78.155.199.27", user="zogdbadmin",
                               passwd="p1l1d00b", db="zogdatabase")
    except MySQLdb.Error as err:
        print("Connection error: {}".format(err))
        conn.close()
        return False
    return conn

def disconnect(conn):
    conn.close()