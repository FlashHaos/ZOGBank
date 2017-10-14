from pony.orm import *


db = Database()
db.bind(provider='mysql', host='78.155.199.27', user='zogdbadmin', passwd='p1l1d00b', db='zogdatabase')

class Users(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Optional(str, unique=True)
    passhash = Optional(str)
    role = Optional(str, default='user')

sql_debug(False)

db.generate_mapping(create_tables=True)

with db_session:
    for user in select(user for user in Users):
        print(user.login, user.id, user.role)