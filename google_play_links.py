import csv
import urllib2, json, re, sys, os
from bs4 import BeautifulSoup

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
    for row in reader:
        url.append("https://play.google.com/store/apps/details?id="+row[0])

    print len(url)
    tempurl = "https://play.google.com/store/apps/details?id=com.supercell.clashofclans"
    file_name = tempurl.split("id=")[1].replace(".","-")
    print file_name
    if os.path.isfile("results/%s.json" % file_name) == False:
        try:
            print "here"
            response = urllib2.urlopen(tempurl)
        except:
            response = False
        if response != False:
            print("generating %s.json" % file_name)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # print soup
            # file = open("testfile.txt","w") 
            # file.write(str(soup))
            datePublished 	= soup.find('div', {'itemprop': 'datePublished'}).text
            contentRating = soup.find('div',{'itemprop':'contentRating'}).text
            operatingSystems = soup.find('div',{'itemprop':'operatingSystems'}).text
            
            try:
                fileSize 	= soup.find('div', {'itemprop': 'fileSize'}).text.rstrip().lstrip()
            except:
                fileSize	= ''
            numDownloads 	= soup.find('div', {'itemprop': 'numDownloads'}).text.split('-')
            # print numDownloads[0].encode('ascii', errors='backslashreplace')
            appName 		= soup.select(".document-title")[0].text.rstrip().lstrip()
            category        = soup.find('span', {'itemprop': 'genre'}).text
            offered_by 		= soup.find('div', text='Offered By').findNext('div').text
            devInfo = soup.find('div', {'class': 'content contains-text-link'})

            site_array = [find_between(link['href'], '?q=', '&') for link in soup.findAll('a', href=True, text='Acesse o site')]
            site = site_array[0] if len(site_array) > 0 else ''
            try:
                email = re.search('(?=mailto:).*?(?=")', str(devInfo)).group(0).replace('mailto:', '')
            except:
                email = ''

            try:
                score_total = soup.select(".score")[0].text
                tempvalu = soup.select("div.rating-bar-container.one")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
                tempint = tempvalu.encode('ascii','ignore')
                print type(tempint)
                one_star 	= soup.select("div.rating-bar-container.one")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
                two_stars 	= soup.select("div.rating-bar-container.two")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
                three_stars = soup.select("div.rating-bar-container.three")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
                four_stars 	= soup.select("div.rating-bar-container.four")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
                five_stars 	= soup.select("div.rating-bar-container.five")[0].text.lstrip()[1:].rstrip().lstrip().replace('.','')
                sum_stars 	= one_star+two_stars+three_stars+four_stars+five_stars
            except:
                score_total = '0'

                one_star 	= 0
                two_stars 	= 0
                three_stars = 0
                four_stars 	= 0
                five_stars 	= 0
                sum_stars 	= 0

            app_info = {'AppName': appName,
                        'url': tempurl,
                        'category': category,
                        'datePublished': datePublished,
                        'contentRating':contentRating,
                        'operatingSystems':operatingSystems,
                        'fileSize': fileSize,
                        'numDownloads': [numDownloads[0].rstrip().lstrip().replace('.',''), numDownloads[1].rstrip().lstrip().replace('.','')],
                        'devInfo': {'author': offered_by,'site': site, 'email': email},
                        'reviews': {'scores': {
                                                '1_star': one_star,
                                                '2_stars': two_stars,
                                                '3_stars': three_stars,
                                                '4_stars': four_stars,
                                                '5_stars': five_stars,
                                                'total': score_total,
                                                'ratingCount': sum_stars
                                                }, 'comments': [] }
                        }
            for review in soup.findAll('div', {'class': 'single-review'}):
                author 	= review.find('span', {'class': 'author-name'}).text.rstrip().lstrip()
                authorId = find_between(str(review.find('span', {'class': 'author-name'})), '?id=', '"')
                date 	= review.find('span', {'class': 'review-date'}).text
                message = review.find('div', {'class': 'review-body'}).text.replace('Resenha completa', '').rstrip().lstrip()
                app_info['reviews']['comments'].append({'author': author, 'authorId': authorId, 'date': date, 'message': message.encode('utf-8')})
            json.dump(app_info, open('result.json', 'w'))

if __name__ == "__main__":
    file_path = "all_top_games.csv"
    with open(file_path, "rb") as file_obj:
        csv_reader(file_obj)