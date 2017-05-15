import MySQLdb
import requests
from bs4 import BeautifulSoup
encoding = "utf-8"
on_error = "replace"


#connect to mysql
db = MySQLdb.connect(host="localhost",user="root", db="inspiringquotes",charset='utf8')
cursor = db.cursor()
cursor.execute("select version()")
data = cursor.fetchone()
print("connect db success: %s" % data)

class Author:
    flink = ""
    name =""
    career = ""
    dob = ""
class CrawledLink:
    id = ""
    link = ""
    def __init__(self, _id, _link):
        self.id=_id
        self.link = _link

#function get link author tu mysql
def getCrawledLinksAuthorFromDB():
    sql = ("SELECT id, link FROM list_link WHERE status = '' limit 10")
    cursor.execute(sql)
    data = cursor.fetchall()
    arrLink = []
    for item in data:
        arrLink.append(CrawledLink(item[0], item[1]))
    print ('>>>>>>>>>>>>>>>>>>>>TOTAL LINKS: ',len(arrLink))
    return arrLink
     
 
#function get info of author link
def crawlAuthorInfo(clink):
    url = clink.link
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")

    try:
        for li in soup.find('div',{'class': 'author-list'}).findAll('li'):
            author = Author()
            a = li.find('a')
            author.flink = "http://www.inspiringquotes.us" + a.get('href')
            author.name = a.string.strip()
            info = li.find('br').text
            parts = info.split('|')
            author.career = parts[0].strip()
            if(len(parts)>1):
                author.dob = parts[1].strip()

##            for link in list.findAll('a'):
##                author.flink = "http://www.inspiringquotes.us" + link.get('href')
##                print('---Link Quotes',author.flink)
##                author.name = link.string.strip()
##                print('---Name Author',author.name)
##            for info in list.findAll('br'):
##                re = info.text.split('|')
##                c,d = re
##                author.career = c.strip()
##                author.dob = d.strip()
##                print('---career',author.career)
##                print('---dob',author.dob)

            if(SaveAnAuthor(author)):
                print('ok')
                SaveAuthorLink(author.flink)
            
    except:
        print('Error!')



   #function luu vao DB
def SaveAnAuthor(author):    
    sql="INSERT INTO author(link_author,name,career,dob_dod) \
    VALUES('%s', '%s', '%s', '%s');" % (author.flink,author.name,author.career,author.dob)
    
    print (sql)
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except:
        db.rollback()
       # db.close()
    return False

def SaveAuthorLink(link):
    sql = "INSERT INTO list_link_author(link, status) \
    VALUES('%s','%s');" %(link, "temp" )
    
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

#set Done when finish add tp DB
def SetDONECrawledLinks(crawledLinks):
      crawledLinkIds = []
      for cLink in crawledLinks:
            crawledLinkIds.append('\''+str(cLink.id)+'\'')
      sql = "UPDATE list_link SET status = 'done' WHERE id IN ("+ ','.join(crawledLinkIds) + ")"
      print ('SQL:',sql)
      cursor.execute(sql)
      db.commit()


         
for x in range(1, 300):
    print ('------------------------ LAN CHAY THU ',x)
    all_link = getCrawledLinksAuthorFromDB()
    for clink in all_link:
        crawlAuthorInfo(clink)    
    SetDONECrawledLinks(all_link)
