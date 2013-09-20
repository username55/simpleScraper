import urllib
import re
import time

#tickerList = ["GOOG","AAPL","NFLX"]
tickerFile = open("ticker.txt")
tickerList = tickerFile.read()
tickerArr = tickerList.split("\n")

def main():
    try:
        print "Attempting scrapping"
        print len(tickerArr), " symbols found."
        for ticker in tickerArr:
            regex = '<span id="yfs_l84_' + ticker.lower() + '">(.+?)</span>'
            htmlfile = urllib.urlopen("http://finance.yahoo.com/q?s=" + ticker + "&ql=1")
            htmltext = htmlfile.read()
            
            pattern = re.compile(regex)
            price = re.findall(pattern, htmltext)
            
            print ticker, " : ", price
            time.sleep(3)
    except Exception, e:
        print str(e)
        print 'Error occured in main block'
        time.sleep(5)
    
main()