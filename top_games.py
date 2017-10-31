import requests as req
import json
import csv
import language
import country
import os
import catagories
# import sample as s

def json2csv(data,country,deviceType):
    file_name = country+"_top_games_new.csv"
    gameCSV = None
    if(os.path.isfile(file_name)):
        gameCSV = csv.writer(open(file_name,"ab+"))
    else:    
        gameCSV = csv.writer(open(file_name,"wb+"))
        gameCSV.writerow(["game_id","game_name","developer","price","genres",country,deviceType])
    for i in data["content"]:
        id_0 = i["id"].encode('utf8')
        title = i["title"].encode('utf8')
        price = i["price"].encode('utf8')
        developer = i["developer"].encode('utf8')
        for g in i["genres"]:
            # print g
            gameCSV.writerow([id_0,title,developer,price,g.encode('utf8'),"1","1"])

def topGamesAndroid(country,language,gamecatagorie):#keep a constant for country and language
    url = "https://api.apptweak.com/android/categories/"+gamecatagorie+"/top.json?country="+country+"&language="+language
    print url
    headers = {'X-Apptweak-Key':'5AqviwWqaTgGWfTapNKdL68BEnI'}
    
    res = req.get(url,headers=headers)
    if(res.ok):
        #print(res.json())
        json2csv(res.json(),country,"android")
    else:
        res.raise_for_status()


if __name__ == "__main__":
    for i in catagories.game_catagories:
        # topGamesAndroid(country.australia,language.english,i)
        topGamesAndroid(country.canada,language.english,i)
        # topGamesAndroid(country.indonesia,language.english,i)
        # topGamesAndroid(country.russia,language.english,i)
        # topGamesAndroid(country.new_zealand,language.english,i)
        # topGamesAndroid(country.Malaysia,language.english,i)
        
