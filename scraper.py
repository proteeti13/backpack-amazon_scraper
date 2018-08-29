import csv
import requests
import json
from bs4 import BeautifulSoup
filename = "ASIN.csv"
f = open(filename, "w",encoding="utf-8")


def getAsin(gist):
    gist_data = requests.get(gist)
    asins = gist_data.text
    f.write(asins)  ####writes asin to csv file
    with open('ASIN.csv') as csvfile:
        reader = csv.reader(csvfile)
        asin_list = list(reader)
    return asin_list   ##########csv to list

def getSoup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    #print(soup)
    return soup
    
 def getFeatures(soup):
    features = []
    feature = soup.findAll("div",{"id":"featurebullets_feature_div"})
    # print(feature)
    for i in range(len(feature)):
        f_list = feature[i].findAll("span",{"class":"a-list-item"})
        for j in range(len(f_list)):
            if ((f_list[j].string) == None):
                pass
            else:
                f_string = f_list[j].string
                f_string = f_string.replace('\n','')
                f_string = f_string.replace('\t','')
                features.append(f_string)
    return features

def makeDict(soup):
    data = {
        'asin': soup.find(id="ASIN").attrs['value'],
        'title': soup.find(id="title").text.strip(),
        'brand': soup.find(id="bylineInfo").text.strip(),
        'feature': getFeatures(soup),

        }
    print(data)

        



def main():
    gistData= 'https://gist.githubusercontent.com/Corei13/00161af3a7c07c4eafcc166d484defff/raw/3ff0c7e74647e622af629ff076dae35ed115ab50/asin.list'
    ASIN_list = getAsin(gistData)
    for i in range(5):
        print(ASIN_list[i][0])
        productUrl = "http://www.amazon.com/dp/" + ASIN_list[i][0]
        getSoup(productUrl)
        pageMarkup = getSoup(productUrl)
        makeDict(pageMarkup)



if __name__ == "__main__":
    main()
