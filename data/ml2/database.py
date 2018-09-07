#! /usr/bin/python3
import csv, sqlite3

con = sqlite3.connect("heroData.db")
cur = con.cursor()
cur.execute("CREATE TABLE authorData (name,rank,rate,hero);") # use your column names here

with open('itemNames1.csv') as fin: # `with` statement available in 2.5+
    #csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['name'], i['rank'], i['rate'], i['hero']) for i in dr]

cur.executemany("INSERT INTO authorData (name,rank,rate,hero) VALUES (?, ?, ?, ?);", to_db)
rowID = "1"
rows = cur.fetchall()
con.commit()
for row in rows:
	print(row)
con.close()