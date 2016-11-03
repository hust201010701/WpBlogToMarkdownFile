import requests
from selenium import webdriver
import time
import html2text
from bs4 import BeautifulSoup


class Blog():
    def __init__(self,browser,pages):
        self.browser = browser
        self.pages = pages
        self.articles = set()

    def getArticlesByPageIndex(self,pageIndex):
        self.browser.get("http://www.orzangleli.com/page/%d/"%pageIndex)
        time.sleep(6)
        soup = BeautifulSoup(self.browser.page_source,"html5lib")
        #print(self.browser.page_source)
        titles =soup.findAll(class_="entry-title")
        for title in titles:
            address = title.find("a")["href"]
            self.articles.add(address)
            print(address)

    def getAllArticles(self):
        for i in range(self.pages):
            self.getArticlesByPageIndex(i+1)

    def save2md(self,page_address):
        self.browser.get(page_address)
        time.sleep(6)
        #需要事先在wp后台关闭禁用掉代码高亮显示插件
            
        soup = BeautifulSoup(self.browser.page_source,"html5lib")
        title = soup.find(class_="entry-title").text
        date = soup.find(class_="updated")["datetime"].split("T")[0]
        content = soup.find(class_="entry-content")
        #获取标签
        categorys = soup.findAll("a",{"rel":"category tag"})
        tags = ""
        for category in categorys:
            if category.text.startswith("未分类"):
                break
            tags = "%s- %s\n"%(tags,category.text)

        head = self.mdheader(title,date,tags,categorys[0].text)        
        #print(content)
        
        mdcontent = html2text.html2text(str(content))
        #给md文档加上头
        mdcontent = "%s\n%s"%(head,mdcontent)
        #删除作者署名信息
        mdcontent = mdcontent.split("![](http://2.gravatar.com/avatar/e9a1c2c77d47ac4dcfeb1fa2fc1c936a?s=42&d=mm&r=g)")[0]
        
        with open("%s_%s.md"%(date,title),"w+",encoding="utf-8") as file:
            file.write(mdcontent)
            file.close()
            
    def saveBlog(self):
        self.getAllArticles()
        for url in self.articles:
            self.save2md(url)


    def mdheader(self,title,date,tags,category):
        head = """---
title: %s
date: %s
tags:
%scategories: %s
---"""%(title,date,tags,category)
        return head
            

browser = webdriver.PhantomJS(executable_path ="phantomjs.exe")
blog = Blog(browser,5)
blog.saveBlog()

