import csv
import time
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
    file_name = "games_details.csv"
    gameCSV = None
    if(os.path.isfile(file_name)):
        gameCSV = csv.writer(open(file_name,"ab+"))
    else:    
        gameCSV = csv.writer(open(file_name,"wb+"))
        gameCSV.writerow(["game_id","game_name","datePublished","appsize","developer","price","downloads","rating","ratingCount","ranking","contentRating","androidVersions"])
    for row in reader:
        tempurl = "http://www.appbrain.com/app/"+row[0]
        # tempurl = "http://www.appbrain.com/app/zozo.android.crosswords"
            
        try:
            # time.sleep(1)
            request = urllib2.Request(tempurl)
            time.sleep(30)
            request.add_header('Retry-After','5000')
            request.add_header('User-Agent','your bot 0.1')
            response = urllib2.urlopen(request)
            print "after response"
        except Exception as e:
            response = False
            print e
            # time.sleep(10000)
        print response
        if response != False:
            # print("generating %s.json" % file_name)
            appName,dataPublished,fileSize,appSize,developer,installs,rating,ratingCount,ranking,contentRating,price,androidVersions = None,None,None,None,None,None,None,None,None,None,None,None
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # print soup
            # file = open("testAppfile.txt","w")
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
                # tempContent = soup.find('div',{'title':'Content Rating'})
                # print tempContent
                if soup.find('div',{'title':'Content Rating'})!=None:
                    contentRating = soup.find('div',{'title':'Content Rating'}).findNext('div',{'class':'infotile-text infotile-text-solo'}).text.rstrip().lstrip()
                if soup.find('div',{'title':'Price'})!=None:
                    price = soup.find('div',{'title':'Price'}).findNext('div').findNext('div').text.rstrip().lstrip()
                if soup.find('div',{'title':'Android version'})!=None:
                    androidVersions = soup.find('div',{'title':'Android version'}).findNext('div',{'class':'infotile-text infotile-text-solo infotile-text-big'}).text.rstrip().lstrip()
                    # top500Other = soup.find('h2',{'id':'google-play-rankings'}).findNext('div',{'class':'data-table-container'}).text.rstrip().lstrip()
                    # top500Other = top500Other.decode('utf-8')
                    # rows = top500Other.findAll('tr')
                    # print top500Other
                    # print gs.translate(appName,'en')
                    # print datePublished["content"]
                    # print fileSize["content"]
                    # print appSize
                    # print developer
                    # print installs
                    # print rating
                    # print int(ratingCount.replace(",",""))
                    # print ranking
                print contentRating
                translatedAppName = None
                tempName = appName.encode('utf8')
                if not any(c.isdigit() for c in tempName):
                    translatedAppName = TextBlob(appName)
                    if translatedAppName.detect_language() != "en":
                        translatedAppName = translatedAppName.translate(to="en")
                else:
                    translatedAppName = tempName
                print translatedAppName
                gameCSV.writerow([row[0],translatedAppName,datePublished["content"],appSize,developer.encode('utf8'),price,installs,rating,int(ratingCount.replace(",","")),ranking,contentRating,androidVersions])
        # gameCSV.writerow(["Ashes2010_androidmkp.indvseng",appName.encode('utf8'),datePublished["content"],appSize,developer,price,installs,rating,int(ratingCount.replace(",","")),ranking,androidVersions])
            
            # contentRating = soup.find('div',{'itemprop':'contentRating'}).text
            # operatingSystems = soup.find('div',{'itemprop':'operatingSystems'}).text
            
            # try:
            #     fileSize 	= soup.find('div', {'itemprop': 'fileSize'}).text.rstrip().lstrip()
            # except:
            #     fileSize	= ''
            # numDownloads 	= soup.find('div', {'itemprop': 'numDownloads'}).text.split('-')
            # # print numDownloads[0].encode('ascii', errors='backslashreplace')
            # appName 		= soup.select(".document-title")[0].text.rstrip().lstrip()
            # category        = soup.find('span', {'itemprop': 'genre'}).text
            # offered_by 		= soup.find('div', text='Offered By').findNext('div').text
            # devInfo = soup.find('div', {'class': 'content contains-text-link'})

            # site_array = [find_between(link['href'], '?q=', '&') for link in soup.findAll('a', href=True, text='Acesse o site')]
            # site = site_array[0] if len(site_array) > 0 else ''
            # try:
            #     email = re.search('(?=mailto:).*?(?=")', str(devInfo)).group(0).replace('mailto:', '')
            # except:
            #     email = ''

            # try:
            #     score_total = soup.select(".score")[0].text
            #     tempvalu = soup.select("div.rating-bar-container.one")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
            #     tempint = tempvalu.encode('ascii','ignore')
            #     print type(tempint)
            #     one_star 	= soup.select("div.rating-bar-container.one")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
            #     two_stars 	= soup.select("div.rating-bar-container.two")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
            #     three_stars = soup.select("div.rating-bar-container.three")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
            #     four_stars 	= soup.select("div.rating-bar-container.four")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
            #     five_stars 	= soup.select("div.rating-bar-container.five")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
            #     sum_stars 	= one_star+two_stars+three_stars+four_stars+five_stars
            # except:
            #     score_total = '0'

            #     one_star 	= 0
            #     two_stars 	= 0
            #     three_stars = 0
            #     four_stars 	= 0
            #     five_stars 	= 0
            #     sum_stars 	= 0

            # app_info = {'AppName': appName,
            #             'url': tempurl,
            #             'category': category,
            #             'datePublished': datePublished,
            #             'contentRating':contentRating,
            #             'operatingSystems':operatingSystems,
            #             'fileSize': fileSize,
            #             'numDownloads': [numDownloads[0].rstrip().lstrip().replace('.',''), numDownloads[1].rstrip().lstrip().replace('.','')],
            #             'devInfo': {'author': offered_by,'site': site, 'email': email},
            #             'reviews': {'scores': {
            #                                     '1_star': one_star,
            #                                     '2_stars': two_stars,
            #                                     '3_stars': three_stars,
            #                                     '4_stars': four_stars,
            #                                     '5_stars': five_stars,
            #                                     'total': score_total,
            #                                     'ratingCount': sum_stars
            #                                     }, 'comments': [] }
            #             }
            # for review in soup.findAll('div', {'class': 'single-review'}):
            #     author 	= review.find('span', {'class': 'author-name'}).text.rstrip().lstrip()
            #     authorId = find_between(str(review.find('span', {'class': 'author-name'})), '?id=', '"')
            #     date 	= review.find('span', {'class': 'review-date'}).text
            #     message = review.find('div', {'class': 'review-body'}).text.replace('Resenha completa', '').rstrip().lstrip()
            #     app_info['reviews']['comments'].append({'author': author, 'authorId': authorId, 'date': date, 'message': message.encode('utf-8')})
            # json.dump(app_info, open('result.json', 'w'))

if __name__ == "__main__":
    file_path = "all_top_games.csv"
    with open(file_path, "rb") as file_obj:
        csv_reader(file_obj)