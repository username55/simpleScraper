from cookielib import CookieJar
import urllib2
from bs4 import BeautifulSoup

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match  


# The following method only retrieve currently playing movie in JAKARTA.
# You could however, extend the code to retrieve the whole schedule (both upcoming and now playing)
# By simply iterating the city links
# Learn the target source code first to understand

# This is only a proof of concept. A more robust approach to scrap could be by using famous python package
# Such as:
# scrapy or else.
def main():
    try:
        baseurl = "http://www.21cineplex.com/"
        
        opener.open(baseurl)
        urllib2.install_opener(opener)
        
        request = urllib2.Request('http://www.21cineplex.com/nowplaying/jakarta,3,JKT.htm/1')
        request.add_header('Referer', baseurl)
        
        requestData = urllib2.urlopen(request)
        htmlText = BeautifulSoup(requestData.read())
        
        total = htmlText.find(match_class(["pagenating"]))
        
        length = len(total.find_all('a')) - 1
        links = total.find_all('a', limit=length)
        links.pop(0)

        movies = htmlText.find_all(match_class(["w462"]))
         
        print "Upcoming Movies:", "\n"
        if not movies:
            print "List is empty. Printing source instead...", "\n\n"
            print htmlText
        else:
            for movie in movies:
                titles = movie.find_all('h3')
                desc = movie.find_all('p')
                  
                for index in range(len(titles)):
                    print "Title: " ,titles[index].find('a').contents[0]
                    print desc[index].contents[0]
                    print "-----------------------------\n"
                    
        for link in links:
            rLink = urllib2.Request(link.get('href'))
            rLink.add_header('Referer', baseurl)
            rData = urllib2.urlopen(rLink)
            rText = BeautifulSoup(rData.read())
            rMovies = rText.find_all(match_class(["w462"]))
            
            if not rMovies:
                print "List is empty. Printing source instead...", "\n\n"
                print htmlText
            else:
                for rMovie in rMovies:
                    titles = rMovie.find_all('h3')
                    desc = rMovie.find_all('p')
                      
                    for index in range(len(titles)):
                        print "Title: " ,titles[index].find('a').contents[0]
                        print desc[index].contents[0]
                        print "-----------------------------\n"

    except Exception, e:
        str(e)
        print "Error occured in main Block"
        
main()