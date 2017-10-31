import csv
import urllib2, json, re, sys, os
from bs4 import BeautifulSoup
# import goslate
# gs = goslate.Goslate()
from textblob import TextBlob

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def csv_reader(file_name):
    reader = csv.reader(file_name)
    url = list()
    file_name = "temp_games_details.csv"
    gameCSV = None
    if(os.path.isfile(file_name)):
        gameCSV = csv.writer(open(file_name,"ab+"))
    else:    
        gameCSV = csv.writer(open(file_name,"wb+"))
        gameCSV.writerow(["game_id","game_name","datePublished","appsize","developer","price","downloads","rating","ratingCount","ranking","contentRating","androidVersions"])
    # for row in reader:
        # tempurl = "http://www.appbrain.com/app/"+row[0]
    appid = "air.com.gan.stations.slots"
    tempurl = "http://www.appbrain.com/app/"+appid
            
    try:
        request = urllib2.Request(tempurl)
        request.add_header('Retry-After','1')
        request.add_header('User-Agent','Mozilla/5.0')
        response = urllib2.urlopen(request)
        print response
        print "after response"
    except Exception as e:
        response = False
        print e
    if response != False:
            # print("generating %s.json" % file_name)
        appName,dataPublished,fileSize,appSize,developer,installs,rating,ratingCount,ranking,contentRating,price,androidVersions = None,None,None,None,None,None,None,None,None,None,None,None
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        # print soup
        # file = open("testAppOutfile.txt","w")
        # file.write(str(soup))
        if soup.find('a',{'class':'sexy-button sexy-button-important'}).findNext('a').findNext('a').findNext('a').text != "Yes":
            print "inside response"
            if soup.find('h1',{'itemprop':'name'})!=None:
                appName = soup.find('h1',{'itemprop':'name'}).text.rstrip().lstrip()
                # appName = str(appName, encoding='utf-8', errors = 'ignore')
            if soup.find('meta', {'itemprop': 'datePublished'})!=None:
                datePublished 	= soup.find('meta', {'itemprop': 'datePublished'})
            if soup.find('meta', {'itemprop': 'fileSize'})!=None:
                fileSize = soup.find('meta', {'itemprop': 'fileSize'})
            if soup.find('div',{'title':'App size'})!=None:
                appSize = soup.find('div',{'title':'App size'}).findNext('div',{'class':'infotile-text infotile-text-solo'}).text.rstrip().lstrip()
            if soup.find('div',{'class':'td app-top-title'})!=None:
                developer = soup.find('div',{'class':'td app-top-title'}).findNext('a').text
            if soup.find('div',{'class':'infotile-top infotile-top-installs'})!=None:
                installs = soup.find('div',{'class':'infotile-top infotile-top-installs'}).findNext('div',{'class':'infotile-text infotile-text-big'}).text.rstrip().lstrip()+" "+soup.find('div',{'class':'infotile-top infotile-top-installs'}).findNext('div',{'class':'infotile-subtext'}).text.rstrip().lstrip()
            if soup.find('div',{'class':'infotile-top infotile-top-rating'})!=None:
                rating = soup.find('div',{'class':'infotile-top infotile-top-rating'}).findNext('div',{'class':'infotile-text infotile-text-big'}).text.rstrip().lstrip()
                ratingCount = soup.find('div',{'class':'infotile-top infotile-top-rating'}).findNext('div',{'class':'infotile-subtext'}).text.rstrip().lstrip()
            if soup.find('div',{'class':'infotile-top infotile-top-ranking'})!=None:
                ranking = soup.find('div',{'class':'infotile-top infotile-top-ranking'}).findNext('div').text.rstrip().lstrip()+" "+soup.find('div',{'class':'infotile-top infotile-top-ranking'}).findNext('div',{'class':'infotile-subtext'}).text.rstrip().lstrip()
            if soup.find('div',{'title':'Content Rating'})!=None:
                contentRating = soup.find('div',{'title':'Content Rating'}).findNext('div',{'class':'infotile-text infotile-text-solo'}).text.rstrip().lstrip()
            if soup.find('div',{'title':'Price'})!=None:
                price = soup.find('div',{'title':'Price'}).findNext('div').findNext('div').text.rstrip().lstrip()
            if soup.find('div',{'title':'Android version'})!=None:
                androidVersions = soup.find('div',{'title':'Android version'}).findNext('div',{'class':'infotile-text infotile-text-solo infotile-text-big'}).text.rstrip().lstrip()
            translatedAppName = None
            tempName = appName.encode('utf8')
            if not any(c.isdigit() for c in tempName):
                translatedAppName = TextBlob(appName)
                if translatedAppName.detect_language() != "en":
                    translatedAppName = translatedAppName.translate(to="en")
                else:
                    translatedAppName = tempName
            print translatedAppName
            gameCSV.writerow([appid,translatedAppName,datePublished["content"],appSize,developer,price,installs,rating,int(ratingCount.replace(",","")),ranking,contentRating,androidVersions])

if __name__ == "__main__":
    file_path = "all_top_games.csv"
    with open(file_path, "rb") as file_obj:
        csv_reader(file_obj)