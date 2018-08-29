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
    with open('main.csv') as csvfile:
        reader = csv.reader(csvfile)
        asin_list = list(reader)
    return asin_list   ##########csv to list

def getSoup(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,"lxml")
        print(soup)



def main():
    gistData= 'https://gist.githubusercontent.com/Corei13/00161af3a7c07c4eafcc166d484defff/raw/3ff0c7e74647e622af629ff076dae35ed115ab50/asin.list'
    ASIN_list = getAsin(gistData)
    for i in range(5):
        print(ASIN_list[i][0])
        productUrl = "http://www.amazon.com/dp/" + ASIN_list[i][0]
        getSoup(productUrl)



if __name__ == "__main__":
    main()
