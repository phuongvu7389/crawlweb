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
    quote_link= ""
    author_name= ""
    author_link= ""
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
    sql = ("select id, link FROM list_link_author where status ='temp' limit 2")
    cursor.execute(sql)
    #print("SQLSQLSQLSQLSQLSQL", sql)
    data = cursor.fetchall()
    arrLink = []
    for item in data:
        arrLink.append(CrawledLink(item[0], item[1]))
        #print ('>>>>>>>>>>>>TOTAL LINKS: ',len(arrLink))
    return arrLink
   
   
##url = "http://www.inspiringquotes.us/author/1939-abraham-lincoln"

#function save data to DB
def saveQuotesToDB(quo):
    sql="INSERT INTO quotes(quote,author,tag_name) \
    VALUES('%s', '%s', '%s');" % (quo.quote_name,quo.author_name,quo.tag_name.join(','))
    print("save data><>>>>>>>>>>",sql)
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except:
        db.rollback()       
    return False

#function save tag_name to DB
def saveTags(quo):
    sql = "INSERT INTO tags(tag_name) \
    VALUES('%s','%s');" %(quo.tag_name)    
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        

# function get quotes content from author link
def crawlQuotesContent(clink):
    url = clink.link
    content =  requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
##    quo = Quotes()
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
                    quo.quote_text = quote_links[0].string.strip()
                    #print("quotequote_text_______>>>>", quo.quote_text)
                    quo.quote_link = quote_links[0].get('href')
                    #print("quote_text________>>>>:", quo.quote_link)
                if(len(quote_links)>1):
                    quo.author_name = quote_links[1].string.strip()
                    #print("quote author namequote_links_______>>>>:",quo.author_name)
                    # author_link = quote_links[1].get('href')

            quote_tags = li.find('p',{'class':'quote-tags'})
            #print('TAGGGGGGGGGGGGGGGGGGG', quote_tags)
            if(quote_tags!= None):
                
                quote_tags_links = quote_tags.findAll('a')
                                
                for tag_link in quote_tags_links:
                   #print('tag_______>>>>:',tag_link.string.strip())
                    quo.tag_name.append(tag_link.string.strip())
            #print('tags_______>>>>: ', quo.tag_name)

##        s = json.dumps(quo.__dict__)    
##        print('______________________________', s)    
        if(saveQuotesToDB(quo)):
            print("savequoteOK")
            saveTags(quo.tag_name)
    except:
        print("error")


all_link = getCrawledLinkQuotesFromDB()
for clink in all_link:
    crawlQuotesContent(clink)

