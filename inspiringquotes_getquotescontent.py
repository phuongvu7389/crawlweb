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

#function get list_link_author from DB

url ="http://www.inspiringquotes.us/author/1939-abraham-lincoln"

def insertTag(tag):
    return
class tags: 
    tag_name=""
    tag_link=""

class quotes:
    quote_name= ""
    quote_link= ""
    author_name= ""
    author_link= ""
    
#function get quotes content from author link
def crawlQuotesContent(url):
    content =  requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    try:
        for li in soup.find('div' , {'class':'quotes-list'}).findAll('li'):
            quote = li.find('p',{'class':'quote'})
            if(quote):
                quote_links = li.findAll('a')
                if(len(quote_links)>0):
                    quote_text = quote_links[0].string.strip()
                    print("---quote:",quote)
                    quote_link = quote_links[0].get('href')
                    print("---quote link:",quote_link)
                if(len(quote_links)>1):
                    author_name = quote_links[1].string.strip()
                    print("---quote author name:",author_name)
                    author_link = quote_links[1].get('href')

            quote_tags = li.find('p',{'class':'quote-tags'})
            print('TAGGGGGGGGGGGGGGGGGGG', quote_tags)
            if(quote_tags!= None):
                print('111111111111111111111111111111')
                quote_tags_links = quote_tags.findAll('a')
                quote_tags_text = []
                
                for tag_link in quote_tags_links:
                    print('tag:',tag_link.string.strip())
                    quote_tags_text.append(tag_link.string.strip()) 
                    quote_tags_link
            
##            quoteget = li.findAll('a')
##            if(len(quoteget)>0):
##            quote = quoteget[0].string.strip()
##            print("---quote:",quote)
##            quote_link = quoteget[0].get('href')
##            print("---quote link:",quote_link)
##            if(len(quoteget)>1):
##            author_name = quoteget[1].string.strip()
##            print("---quote author name:",author_name)
##            author_link = quoteget[1].get('href')
##            print("---quote author link:",author_link)
##            for tags in li:
##                tag = tags.
##            for tags in soup.find('p', {'class':'quote-tags'}):
##                for t in tag.findAll('a'):
##                    t1 = t[0].string.strip()
##                    print('t1', t1)
##                    t1_link = t[0].get('href')
##                    print('t1 link', t1_link)
##                    t2 = t[1].string.strip()
##                    print('t2', t2)
##                    t2_link = t[1].get('href')
##                    print('t2_link', t2_link)
##                    t2 = t[2].string.strip()
##                    print('t3', t2)
##                    t2_link = t[2].get('href')
##                    print('t3', t2_link)
##                    

                    
                    
            
           
    except:
        print("error")

crawlQuotesContent(url)
