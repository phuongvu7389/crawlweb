import MySQLdb
import requests
from bs4 import BeautifulSoup
encoding = "utf-8"
on_error = "replace"


#connect to mysql
db = MySQLdb.connect(host="localhost",port = 3306, user="root", db="inspiringquotes",charset='utf8')
cursor = db.cursor()
cursor.execute("select version()")
data = cursor.fetchone()
print("connect db success: %s" % data)

class tags:
    tag_name=[]
    tag_id=[]
    
class Quotes:
    quote_name= ""
    quote_link= ""
    author_name= ""
    author_link= ""
    tag_name=[]
    
#define class CrawledLink
class CrawledLink:
    id = ""
    link = ""
    def __init__(self, _id, _link):
        self.id=_id
        self.link = _link
        
# function get list_link_author from DB
def getCrawledLinkQuotesFromDB():
    sql = ("select id, link FROM list_link_author where status ='temp' limit 2")
    cursor.execute(sql)
    print("SQLSQLSQLSQLSQLSQL", sql)
    data = cursor.fetchall()
    arrLink = []
    for item in data:
        arrLink.append(CrawledLink(item[0], item[1]))
        print ('>>>>>>>>>>>>TOTAL LINKS: ',len(arrLink))
    return arrLink


getCrawledLinkQuotesFromDB()
