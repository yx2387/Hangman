# Script used to initiate and monitor DB
import sqlalchemy as sql

db_string = "postgres://yx2387:68958995@hangman.crdce7xwzn1m.us-east-1.rds.amazonaws.com:5432/Credentials"


db = sql.create_engine(db_string)

#db.execute("DROP TABLE IF EXISTS scores")

db.execute("CREATE TABLE IF NOT EXISTS credentials (username text unique, password text)") 
db.execute("CREATE TABLE IF NOT EXISTS scores (username text unique, score int)") 
#try:
#	db.execute("INSERT INTO credentials (username,password) VALUES ('abc', '123'),('zxc', '123')")

#except:
#	print "Username exists"

result_set = db.execute("SELECT * FROM credentials")  
rows = result_set.fetchall() 
print(rows)

result_set = db.execute("SELECT * FROM scores")  
rows = result_set.fetchall() 
print(rows)