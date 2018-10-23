from bs4 import BeautifulSoup
import requests
import re
from lxml import etree
import codecs
import urllib
import sys
import os
import time
"""
    此爬虫只针对 https://wall.alphacoders.com   
"""

#-----------------------------------------------

"""
    Global Variables
"""

server = "https://wall.alphacoders.com/"
num = 1
timeStart = 0
timeEnd =  0


#------------------------------------------------



def findImageUrl(url) -> "Array":

    imageRepoUrls = []

    soup = BeautifulSoup(requests.session().get(url).text,features="lxml")
    imageUrlTags = soup.find_all('a',href=re.compile("big.php?"))

    for imageUrlTag in imageUrlTags:
        imageRepoUrls.append(server + etree.HTML(str(imageUrlTag))\
            .xpath("//a/@href")[0])

    if len(imageRepoUrls) == 0:
        return None
    else:
        return imageRepoUrls



def mkdir(path):
 
    folder = os.path.exists(path)
 
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
 
    else:
        print("---  Local Folder Ready  ---")
        


def saveFile(data):
    global num
    print("已下载 %s 张" % str(num))
    path = "D:/Wallpapers/" + str(num) + ".png"
    f = open(path,'wb')
    f.write(data)
    num = num + 1

    f.close()


def downloadImageFromOnePage(url):
    imageRepoUrls = findImageUrl(url)
    
    """
        经过验证获得的html没有被php日过
        htmlText = requests.session().get(imageRepoUrls[0]).text
        
    file = codecs.open("html.txt", "w","utf-8")
    file.write(htmlText)
    """
    for imageRepoUrl in imageRepoUrls:
        soup = BeautifulSoup(requests.session().get(imageRepoUrl).text,features="lxml")
        imgTag = str(soup.find_all('img',alt=re.compile("Wallpapers")))
        realUrl = etree.HTML(imgTag).xpath("//@src")[0]

        req = urllib.request.Request(realUrl, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req).read()
        saveFile(data)

def findMaxPageNum(url):
    soup = BeautifulSoup(requests.session().get(url).text,features="lxml")
    pageTags = str(soup.find_all('ul',class_=re.compile("pagination")))
    pageNum = etree.HTML(pageTags).xpath("//li/a/@href")
    MaxNum = 0
    for i in pageNum:
        num = i.split("page=")[-1]
        if num.isdigit() and int(num) > MaxNum:
            MaxNum = int(num)
        
    return MaxNum
   






def downloadImageFromOneCollection(url,local_Repo="./Wallpapers"):
    mkdir(local_Repo)
    pageNum = findMaxPageNum(url)
    print("There are %s pages in total"% pageNum)
    print("总共有 %s 页" % pageNum)
    timeStart = time.process_time()
    for page in range(1,pageNum+1):
        print("正在下载第%s页" % page)
        p_url =  url + "&page=%s" % str(page)
        downloadImageFromOnePage(p_url)
        timeEnd = time.process_time()
        timeDif = timeEnd - timeStart
        timeRemain = timeDif * (pageNum - page)
        timeStart = timeEnd
        print("预计还有 %s 秒完成爬去该网页"% str(timeRemain))

if __name__ == "__main__":


    url = "https://wall.alphacoders.com/by_sub_category.php?id=181807&name=Sword+Art+Online+Wallpapers&page=1"
    #print(findMaxPageNum(url))
    
    
    flag = False
    for i in range(len(sys.argv)):
        if sys.argv[i] == "url":
            url = sys.argv[i+1]
            flag = True


    if flag == False:
        print("No url is specified.The default site will be scraped")
        print("Crawling url: %s" % url)

    print("正在开始爬去 %s 中的壁纸" % url)
    downloadImageFromOneCollection(url,"D:/Wallpapers")
    print("爬取完成，谢谢使用")
    

    
