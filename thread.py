from bs4 import BeautifulSoup
import requests
from time import sleep

from tornado import concurrent

#获取所有小说的初始url
def get_book_urls():
    target = "http://www.xbiquge.la/xiaoshuodaquan/"
    url_list = []
    res = requests.get(target)
    html = res.text
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find('div', attrs={'class', 'novellist'}).find('ul').find_all('li')
    for item in ul:
        url  = item.find('a').get('href')
        url_list.append(url)
    return url_list
#将每一章的内容写入对应的小说中
def write_to_txt(name,content):
    f = open(name+'.txt', 'a', encoding='utf-8')
    f.write(content)

#写入每一章的名称，也可将章名与章节内容连接，从而同时写入
def write_charpter_name(name, title):
    file = open(name+'.txt', 'a', encoding='utf-8')
    file.write("\n\n\n"+title+"\n\n\n")
#获取每一章的章节内容
def get_content(name,url):
    #如果发生timeout异常，则休眠2s再次尝试
    try:
        res = requests.get(url, timeout = 40)
    except:
        sleep(2)
        get_content(url)
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    title = soup.find('div', attrs={'class': 'bookname'}).find('h1').text
    content = soup.find(id="content")
    [content.extract() for content in content("p")]  # 去掉内容中多余的p标签
    ####分割线###
    #此处不知为何，利用soup.find(id = 'content').text无法直接获取所有章节内容
    #只能将其转为字符串进行替换，如有其他方法，烦请告知
    content = str(content)  # 将其转为字符串
    con_replace = content.replace('<br/>', '\n')
    con_replace = con_replace.replace('<div id="content">', '')
    con_replace = con_replace.replace('</div>', '')
    write_charpter_name(name,title)
    write_to_txt(name,con_replace)
#下载此url对应的小说
def download_book(name,url):
    try:
        req = requests.get(url, timeout = 40)
    except:
        sleep(2)
        download_book(url)
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, "lxml")
    chapter_list = soup.find(id="list").find_all('a')
    for index , value in enumerate(chapter_list):
        string = value.get('href')
        newstr = string.split('/')
        charpter_url = url+newstr[3]
        # print("\r"+str(index*100/len(chapter_list))+"%", end="", flush=True)
        get_content(name,charpter_url)
#获取此url对应的书名
def get_book_name(url):
    try:
        res = requests.get(url)
    except:
        sleep(2)
        get_book_name(url)
    res.encoding = 'utf-8'
    html = res.text
    soup = BeautifulSoup(html, "lxml")
    bookName = soup.find('div', attrs={'id': 'info'}).find('h1').text
    return bookName
#创建txt文件
def create_txt(name):
    f = open(name+'.txt','a', encoding='utf-8')
#主方法
if __name__ == "__main__":
    urlList = get_book_urls()
    #开启多线程，可以让所有小说同时下载
    with concurrent.futures.ThreadPoolExecutor(len(urlList)) as exector:
        for url in urlList:
            print(url)
            book_name =get_book_name(url)
            print("写入"+book_name+"中,请稍候......")
            create_txt(book_name)
            exector.submit(download_book, book_name,url)
