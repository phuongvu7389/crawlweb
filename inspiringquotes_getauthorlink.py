import MySQLdb
import requests
from bs4 import BeautifulSoup
encoding = "utf-8"
on_error = "replace"
import string


#connect to mysql
db = MySQLdb.connect(host="localhost",user="root", db="inspiringquotes",charset='utf8')
cursor = db.cursor()
cursor.execute("select version()")
data = cursor.fetchone()

# DB SERVICES
#function luu link vao db MySQL
def savelinktoDB(url):
    sql = "INSERT INTO list_link(link) \
    VALUES('%s');" %( url )
    print(sql)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        #db.close()

AUTHOR_LINK = 'http://www.inspiringquotes.us/author-list-detail/'
DOMAIN = 'http://www.inspiringquotes.us/'


# crawlCategoryLinks
    # pushCategoryLinksFromTotalPage
# crawlLink
    # if(Format is Quote -> call CrawlAQoute)
    # crawlAQuote(quoteLink)
    # crawlQuoteLinks(categoryLink)

def crawlCategoryLinks(url):
    totalPage = 1;
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    try:
        for list in soup.findAll('ul',
                                     {'class': 'pagination'}):
            for link in list.findAll('a',{'rel':'last'}):
                results = link.get('href')
                #links.append(results)
                print('RESULT',results)
##                totalPage = int(results[-3:])
                totalPage = int(results.rpartition('page:')[-1])
                print('total page after crawl',totalPage)
               
            
    except:
        print('Error!')
        totalPage = 0
    for x in range(1, int(totalPage+1)):
        link = url+ str(x)
        print ("url",link)
        savelinktoDB(link)


print("connect db success: %s" % data)

for c in list(string.ascii_lowercase):
    url = AUTHOR_LINK+c+'/page:'
    print('++++++++++++++++++++ CRAWL CAT LINK: ', url)
    crawlCategoryLinks(url)

