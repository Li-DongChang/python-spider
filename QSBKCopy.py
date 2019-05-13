from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

#判断是否包含图片，若包含图片则不爬取该段子
def isPic(con):
    flag = True
    try:
        # 定位段子下的图片div
        pic = con.find_element_by_xpath("./div[2]")
    except:
        flag = False
    return flag

class QBSK:
    # 初始化方法
    def __init__(self):
        self.driver = webdriver.Chrome()
        #存放程序是否继续运行的变量
        self.enable = True

    #调用该方法，返回每一页段子的link列表
    def getLinks(self, index):
        #浏览器地址导航到该页
        self.driver.get("http://www.qiushibaike.com/hot/page/"+str(index))
        # 窗口最大化
        self.driver.maximize_window()
        # 获取每个段子element
        content_left = self.driver.find_elements_by_class_name("mb15")
        links = []
        for content in content_left:
            # 判断是否包含图片
            if isPic(content):
                continue
            else:
                # 获取该段子的link
                link = content.find_element_by_xpath("./a").get_attribute("href")
                links.append(link)
        return links

    #调用该方法，每次敲回车打印出一个段子
    def getOneStory(self, link):
        i = input()
        if i =="Q":
            # 设置程序停止
            self.enable = False
            self.driver.quit()
            return
        else:
            # 页面导航到link地址
            self.driver.get(link)
            # 发布日期
            releaseDate = self.driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div[1]/span[1]")
            # 发布人
            releaser = self.driver.find_element_by_xpath("//*[@id='articleSideLeft']/a/img").get_attribute("alt")
            # 段子内容
            releaseContent = self.driver.find_element_by_xpath("//*[@id='single-next-link']/div")
            # 好笑数
            funnyCnt = self.driver.find_element_by_xpath("//*[@id='content']/div/div[2]/div[1]/span[2]/i")
            print("发布人：" + releaser + "\t发布时间：" + releaseDate.text + "\t赞：" + funnyCnt.text + "\n段子内容：" + releaseContent.text + "\n")
        print("正在读取糗事百科,按回车查看新段子，Q退出")

    # 开始方法
    def start(self):
        print("正在读取糗事百科,按回车查看新段子，Q退出")
        # 变量初始时为True，使程序可以正常运行
        self.enable = True
        # 从第一页开始加载
        nowPage = 1
        while self.enable:
            # 总共13页，加载到最后一页程序停止
            if nowPage ==14:
                break
            else:
                # 获取每一页段子的link列表
                links = self.getLinks(nowPage)
                for link in links:
                    if self.enable:
                        # 对于每个link，将其段子item读取出来
                        self.getOneStory(link)
            # 页数加一
            nowPage+=1

spider = QBSK()
spider.start()
