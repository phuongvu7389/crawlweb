import json
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
    #quote_link= ""
    author_name= ""
    #author_link= ""
    tag_name=[]
    def __init__(self):
        self.tag_name=[]
    
#define class CrawledLink
class CrawledLink:
    id = ""
    link = ""
    def __init__(self, _id, _link):
        self.id=_id
        self.link = _link
        
# function get list_link_author from DB
def getCrawledLinkQuotesFromDB():
    sql = ("select id, link FROM list_link_author where status ='temp' limit 1")
    cursor.execute(sql)
    #print("SQL QUERY", sql)
    data = cursor.fetchall()
    arrLink = []
    for item in data:
        arrLink.append(CrawledLink(item[0], item[1]))
        #print ('>>>>>>>>>>>>TOTAL LINKS: ',len(arrLink))
    return arrLink
   
def replaceTag(chuoi):
    chuoi = chuoi.replace("#","")
    return chuoi
def sqlValue(chuoi):
    chuoi = chuoi.replace("'","''")
    return chuoi
    
##url = "http://www.inspiringquotes.us/author/1939-abraham-lincoln"

#function save quotes to DB
def saveQuoteToDB(quo):
    sql ="INSERT INTO quotes(quote,author,tag_name) \
        VALUES('%s','%s','%s')\
        ON DUPLICATE KEY UPDATE quote=(sqlValue(quo.quote_name);" % (sqlValue(quo.quote_name),quo.author_name,replaceTag(', '.join(quo.tag_name)))
    print("SQL  QUERY saveQuoteToDB_____________________>", sql)
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except:
        db.rollback()
       # db.close()
    return False


#save Tags to DB
##def SaveTagsToDB(tag):
##    sql = "INSERT INTO tags(tag_name) \
##    VALUES('%s')ON DUPLICATE KEY UPDATE tag_name=quo.tag_name;" %(tag, "temp" )
##    print("SQL  QUERY SaveTagsToDB_____________________>", sql)
##    try:
##        cursor.execute(sql)
##        db.commit()
##    except:
##        db.rollback()

#config save tag_name
def config(code, value):
    code.tags = value.quo.tag_name
    for x in code.tags:
        if any(x in code.tags):
             sql = "INSERT INTO tags(tag_name) \
             VALUES('%s');" %(quo.tag_name)
             print("SQL  QUERY SaveTagsToDB_____________________>", sql)
            
#set done after get quote link
def setDoneAuthorLinks(crawledLinks):
    crawledLinkIds=[]
    for cLink in crawledLinks:
            crawledLinkIds.append('\''+str(cLink.id)+'\'')
    sql = "UPDATE list_link_author SET status = 'done' WHERE id IN ("+ ','.join(crawledLinkIds) + ")"
    print ('SQL:',sql)
    cursor.execute(sql)
    db.commit()


      
# function get quotes content from author link
def crawlQuotesContent(clink):
    url = clink.link
    content =  requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    
    try:
        for li in soup.find('div' , {'class':'quotes-list'}).findAll('li'):
            quo = Quotes()
            #print('tags________________>>>>>>>>>: ', quo.tag_name)
            quote = li.find('p',{'class':'quote'})
            #print("---quote!@!@!@!@!@!@!@!:",quote)
            if(quote):
                quote_links = li.findAll('a')
                #print("quote_links_______>>>>",quote_links)
                if(len(quote_links)>0):
                    quo.quote_name = quote_links[0].string.strip()
                    print("quote_name_____________________>", quo.quote_name)
                    #quo.quote_link = quote_links[0].get('href')
                    #print("quote_text________>>>>:", quo.quote_link)
                if(len(quote_links)>1):
                    quo.author_name = quote_links[1].string.strip()
                    print("author_name_____________________>",quo.author_name)
                    # author_link = quote_links[1].get('href')

            quote_tags = li.find('p',{'class':'quote-tags'})
            #print('TAGGGGGGGGGGGGGGGGGGG', quote_tags)
            if(quote_tags!= None):
                
                quote_tags_links = quote_tags.findAll('a')
                                
                for tag_link in quote_tags_links:
                   #print('tag_______>>>>:',tag_link.string.strip())
                    quo.tag_name.append(tag_link.string.strip())
            print('quote_tag_____________________>', quo.tag_name)
            if(saveQuoteToDB(quo)):
                print("da ve vao DB, okay!")
                SaveTagsToDB(quo.tag_name)
        #s = json.dumps(quo.__dict__)   #convert object to json 
        print('______________________________')    
        
     
    except:
        print("error")

for x in range(1, 1):
    print ('------------------------ LAN CHAY THU ',x)
    all_link = getCrawledLinkQuotesFromDB()
    for clink in all_link:
        crawlQuotesContent(clink)
    setDoneAuthorLinks(all_link)
