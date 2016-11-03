# WpBlogToMarkdownFile
将wp中的文章转化为md格式的文件，生成的md文件可以直接迁移到hexo框架中

首先需要知道wp站点有大量的css和js，是动态网站，无法使用urllib直接获取网站源码。
这里使用selenium 中的webdriver 配合phantomjs.exe ，这是一个真实的浏览器访问网站，所以不需要添加任何UA标识等。
在wp的首页，使用浏览器访问主页，按F12或者右键审查元素，查看文章标题的class.(不同的主题可能略微有些不同)

![](http://7xrrni.com1.z0.glb.clouddn.com/2016-11-03_14:24:52_1.jpg?imageView2/0/w/800)

可以知道文章的标题由 `<h2 class="entry-title">` 包含，再使用selenium获取网页源码之后，使用BeautifulSoup可以定位到这个标签：
	
	titles =soup.findAll(class_="entry-title")

因为主页中有很多文章，所以有很多类似的标题，我们需要将所有的都获取到。

	for title in titles:
            address = title.find("a")["href"]
            self.articles.add(address)

`self.articles` 是一个set集合。用于保存所有文章的url,通过上面的代码可以将每篇文章中的代码保存到`self.articles`中	

这是获取主页的第一页的所有文章，还有第2页等。所以定义一个函数，根据页码获取文章地址：

	def getArticlesByPageIndex(self,pageIndex):
        self.browser.get("http://www.orzangleli.com/page/%d/"%pageIndex)
        time.sleep(6)
        soup = BeautifulSoup(self.browser.page_source,"html5lib")
        titles =soup.findAll(class_="entry-title")
        for title in titles:
            address = title.find("a")["href"]
            self.articles.add(address)
            print(address)

通过一个for循环完成所有页面的文章url添加，之所以是`i+1`,是因为range(3)表示{0，1，2}：

	def getAllArticles(self):
	        for i in range(self.pages):
	            self.getArticlesByPageIndex(i+1)

这样，所有文章的url都存在`self.articles`中了，在浏览器中访问一个文章，观察文章的中信息，同样通过bs4可以获取文章的标题，发表时间，分类目录，hexo中的md文档还需要指明tag，这里我用分类代替，而分类使用之前分类的第一个分类代替，这些信息还要以特定格式保存在md中，下面代码负责返回一个md文档中head：

	def mdheader(self,title,date,tags,category):
	        head = """---
	title: %s
	date: %s
	tags:
	%scategories: %s
	---"""%(title,date,tags,category)
	        return head

获取到文章的正文内容后，使用html2text将html语言转为markdown语言。html2text的文档在：[html2text](https://pypi.python.org/pypi/html2text/2016.9.19)，将head和html2text转化的内容连接，组成完整的md文档。

入口函数为：
	
	def saveBlog(self):
	        self.getAllArticles()
	        for url in self.articles:
	            self.save2md(url)


在最外层使用下面代码初始化类：
  browser = webdriver.PhantomJS(executable_path ="phantomjs.exe")
  blog = Blog(browser,5)
  blog.saveBlog()
  
附上，我将博客上所有文章保存下来的截图，幸福感满满~待会可以使用hexo提交到hust201010701.github.io上：

![](http://7xrrni.com1.z0.glb.clouddn.com/2016-11-03_15:10:25_3.jpg?imageView2/0/w/1000)

##MIT License

Copyright (c) 2016 orzangleli

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

