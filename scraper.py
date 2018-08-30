import csv
import requests
import json
from bs4 import BeautifulSoup
filename = "ASIN.csv"
f = open(filename, "w",encoding="utf-8")


def getAsin(gist):
    gist_data = requests.get(gist)
    asins = gist_data.text
    f.write(asins)
    with open('ASIN.csv') as csvfile:
        reader = csv.reader(csvfile)
        asin_list = list(reader)
    return asin_list


def getSoup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    return soup


def getFeatures(soup):
    features = []
    feature = soup.findAll("div",{"id":"featurebullets_feature_div"})
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

def getPrice(soup):
    if (soup.find(id="priceblock_ourprice")== None):
        price_div = soup.find_all(class_ = "a-color-price")
        price_inDollar = price_div[1].text.strip()
        try:
            price_inCent = float(price_inDollar.strip('$').strip("'")) * 100
            return price_inCent
        except:
            return price_inDollar

    elif(soup.find(id="priceblock_ourprice") != None):
        price_span = soup.find(id="price_inside_buybox")
        price_inDollar = price_span.text.strip()
        try:
            price_inCent= float(price_inDollar.strip('$').strip("'")) * 100
            return price_inCent
        except:
            return price_inDollar

    else:
        price_inDollar= soup.find(id="priceblock_ourprice").text.strip()
        try:
            price_inCent = float(price_inDollar.strip('$').strip("'")) * 100
            return price_inCent
        except:
            return price_inDollar


def getListPrice(soup):
    uniprice_div = soup.find(id="unifiedPrice_feature_div")
    if (uniprice_div == None):
        return "None"
    else:
        price_div = uniprice_div.find(id="price")
        if (price_div == None):
            return "None"
        else:
            listprice_span = price_div.findAll("span",{"class":"a-text-strike"})
            if (listprice_span == []):
                return "None"
            else:
                listprice_inDollar = listprice_span[0].text.strip()
                listprice_inCent = float(listprice_inDollar.strip('$'))*100
                return listprice_inCent



def getDescription(soup):
    desc_div= soup.find(id="productDescription")
    if (desc_div == None):
        return "None"
    else:
        description = desc_div.text.strip()
        return description


def getImages(soup):
    img = soup.find("div", {"id": "imgTagWrapperId"}).find("img")
    if (img == None):
        return "None"
    else:
        data = json.loads(img["data-a-dynamic-image"])
        return list(data.keys())


def getRating(soup):
    review_div = soup.find(id="reviewSummary")
    if(review_div == None):
        return "None"
    else:
        rating_span =  review_div.find(class_="a-icon-alt")
        if (rating_span == None):
            return "None"
        else:
            rating_string = rating_span.getText().strip()
            rating_list = rating_string.split(" ")
            rating = float(rating_list[0])
            return rating

def getPrime(soup):
    val = soup.find(id="bbop-check-box")
    if (val == None):
        return False
    else:
        return True

def getBrand(soup):
    b_anchor = soup.find(id="bylineInfo")
    if (b_anchor == None):
        return "None"
    else:
        brand = soup.find(id="bylineInfo").text.strip()
        return brand

def getAttributes(soup):
    attributes = []
    obj = {}
    attribute_div = soup.find(id="twister")
    if (attribute_div == None):
        return "None"
    else:
        section_divList = attribute_div.findAll("div",{"class":"a-section"})
        for i in range(len(section_divList)):
            try:
                obj ['name'] = section_divList[i].find(class_="a-form-label").text.strip()
                obj ['value'] = section_divList[i].find(class_="selection").text.strip()
                attributes.append(obj)
            except:
                time.wait(3)
    return attributes



def makeDict(soup):
    data = {
        'asin': soup.find(id="ASIN").attrs['value'],
        'title': soup.find(id="title").text.strip(),
        'brand':getBrand(soup) ,
        'feature': getFeatures(soup),
        'price': getPrice(soup),
        'description': getDescription(soup),
        'listPrice': getListPrice(soup),
        'prime' :getPrime(soup),
        'images': getImages(soup),
        'attributes': getAttributes(soup),
        'rating': getRating(soup),


        }
    return data


def main():
    gistData= 'https://gist.githubusercontent.com/Corei13/00161af3a7c07c4eafcc166d484defff/raw/3ff0c7e74647e622af629ff076dae35ed115ab50/asin.list'
    ASIN_list = getAsin(gistData)
    for i in range(10):
        print(ASIN_list[i][0])
        productUrl = "http://www.amazon.com/dp/" + ASIN_list[i][0]
        pageMarkup = getSoup(productUrl)
        result = makeDict(pageMarkup)
        json_output = json.dumps(result)
        print(json_output)


if __name__ == "__main__":
    main()
