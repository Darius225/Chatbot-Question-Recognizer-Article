import MySQLdb
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                 user="Darius",         # your username
                 passwd="grigore",  # your password
                 db="educational_website" )

cur = db.cursor()
db.close()
