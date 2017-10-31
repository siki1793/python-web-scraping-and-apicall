import requests as req
import json
import csv
import os
from textblob import TextBlob
# import sample as s

def writeJson(data):
    data = data.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)

def openData():
    d = None
    with open('data.json') as json_data:
        d = json.load(json_data)
    return d

def topGamesAndroidDetail(gameid):#keep a constant for country and language
    try:
        # url = "https://data.42matters.com/api/v2.0/android/apps/lookup.json?p="+gameid+"&access_token=614c69f2d10cedb54019dfe9bf5cd0f9f2ffba75"
        # url = "https://data.42matters.com/api/v2.0/android/apps/lookup.json?p="+gameid+"&access_token=5de6027bdd7b22976838ec41df580917319c979a"        
        # url = "https://data.42matters.com/api/v2.0/android/apps/lookup.json?p="+gameid+"&access_token=55b01deb2a05577e10de72b2f70de6af6f8af618"        
        # url = "https://data.42matters.com/api/v2.0/android/apps/lookup.json?p="+gameid+"&access_token=43816078b0ddd5f7273e2dcf69df9b34bdf4ae04"        
        url = "https://data.42matters.com/api/v2.0/android/apps/lookup.json?p="+gameid+"&access_token=a8b7aac050671f589a3b492632f9bec3ccb24965"        
        
        
        
        res = req.get(url)
        
        if(res.ok):
            return res.json()
        else:
            print "error"
    except Exception as e:
        print e
        return false


def csv_reader(file_name):
    reader = csv.reader(file_name)
    csv_file_name = "top_games_detiles.csv"
    gameCSV = None
    if(os.path.isfile(csv_file_name)):
        gameCSV = csv.writer(open(csv_file_name,"ab+"))
    else:    
        gameCSV = csv.writer(open(csv_file_name,"wb+"))
        gameCSV.writerow(['gameid','gameName','datePublished','rating','category','developer','website','numRatings','androidLvl','minDownloads','maxDownloads','icon','promoVideo','lastUpdated','badges','contentRating','gameUrl','inAppPurchase','minInAppPurchase','maxInAppPurchase','shortDescription','description','appSize','appScreenShot','currentVersion','rating_1','rating_2','rating_3','rating_4','rating_5','interactiveElements'])

    for row in reader:
        data = topGamesAndroidDetail(row[0])
        if data!=None:
            gameid,gameName,datePublished,rating,category,developer,website,numRatings,androidLvl,minDownloads,maxDownloads,icon,promoVideo,lastUpdated,contentRating,gameUrl,inAppPurchase,minInAppPurchase,maxInAppPurchase,shortDescription,description,appSize,appScreenShot,currentVersion,rating_1,rating_2,rating_3,rating_4,rating_5 = '','','','','','','','','','','','','','','','','','','','','','','','','','','','',''
            badges,interactiveElements = '',''
            print row[0]
            if data.get('package_name'):
                gameid = data['package_name'].encode('utf8')
            if data.get('title'):
                gameName = data['title'].encode('utf8')
            if data.get('created'):
                datePublished = data['created'].encode('utf8')
            if data.get('rating'):
                rating = data['rating']
            if data.get('category'):
                category = data['category'].encode('utf8')
            if data.get('developer'):
                developer = data['developer'].encode('utf8')
            if data.get('website'):
                website = data['website'].encode('utf8')
            if data.get('number_ratings'):
                numRatings = data['number_ratings']
            if data.get('min_sdk'):
                androidLvl = data['min_sdk'].encode('utf8')
            if data.get('downloads_min'):
                minDownloads = data['downloads_min']
            if data.get('downloads_max'):
                maxDownloads = data['downloads_max']
            if data.get('icon'):
                icon = data['icon'].encode('utf8')
            if data.get('promo_video'):
                promoVideo = data['promo_video'].encode('utf8')
            if data.get('market_update'):
                lastUpdated = data['market_update'].encode('utf8')
            if data.get('badges'):
                for i in data['badges']:
                    badges+= str(i.encode('utf8')) + '|'
            if data.get('content_rating'):
                contentRating = data['content_rating'].encode('utf8')
            
            if data.get('market_url'):
                gameUrl = data['market_url'].encode('utf8')
            if data.get('iap'):
                inAppPurchase = data['iap']
            if data.get('iap_min'):
                minInAppPurchase = data['iap_min']
            if data.get('iap_max'):
                maxInAppPurchase = data['iap_max']
            if data.get('short_desc'):
                shortDescription = data['short_desc'].encode('utf8')
            if data.get('description'):
                description = data['description'].encode('utf8')
            if data.get('size'):
                appSize = data['size']
            if data.get('screenshots'):
                appScreenShot = data['screenshots'][0].encode('utf8')
            if data.get('version'):
                currentVersion = data['version']
            if data.get('ratings_1'):
                rating_1 = data['ratings_1']
            if data.get('ratings_2'):
                rating_2 = data['ratings_2']
            if data.get('ratings_3'):
                rating_3 = data['ratings_3']
            if data.get('ratings_4'):
                rating_4 = data['ratings_4']
            if data.get('ratings_5'):
                rating_5 = data['ratings_5']
            
            if data.get('interactive_elements'):
                for i in data['interactive_elements']:
                    interactiveElements += str(i.encode('utf8'))+'|'
            gameCSV.writerow([gameid,gameName,datePublished,rating,category,developer,website,numRatings,androidLvl,minDownloads,maxDownloads,icon,promoVideo,lastUpdated,badges,contentRating,gameUrl,inAppPurchase,minInAppPurchase,maxInAppPurchase,shortDescription,description,appSize,appScreenShot,currentVersion,rating_1,rating_2,rating_3,rating_4,rating_5,interactiveElements])
            print "on issue data entered"

if __name__ == "__main__":
    # json2csv(openData())
    file_path = "all_10_top_games_2.csv"
    with open(file_path, "rb") as file_obj:
        csv_reader(file_obj)
