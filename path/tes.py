from selenium import webdriver
import threading
from queue import Queue
import time
import requests
import os
import sys


class MeiZiTu(object):
    def __init__(self,style,pages):
        '''
        输入图片类型和想要爬取的页数
        :param style: 图片类型
        :param page: 爬取的页数
        '''
        self.BASE_DIR = '妹子图'
        if not os.path.exists(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
        if not os.path.exists('path'):
            os.mkdir('path')
        self.style = style
        if not os.path.exists(self.BASE_DIR+"/"+self.style):
            os.mkdir(self.BASE_DIR+"/"+self.style)
        self.base_url = 'https://www.mzitu.com/{}/'.format(style)
        self.url = self.base_url+'page/{}/'
        self.pic_list = []
        self.pages = pages

    def parse_pic(self,num):
        '''
        根据传入的页面，获取相应的图片url列表
        :param num:
        :return:
        '''
        driver = webdriver.PhantomJS()
        url = self.url
        path = "//img[@class='lazy']"
        if not os.path.exists('path'+'/'+num):
            os.mkdir('path'+'/'+num)
        driver.get(url.format(num))
        driver.save_screenshot('path'+'/'+num+'/'+'test1.png')
        pic = driver.find_elements_by_xpath(path)
        print([i.get_attribute('src') for i in pic])
        js = 'var currentPosition,timer;function GoBottom(){ timer=setInterval("runToBottom()",1); };function runToBottom(){currentPosition=document.documentElement.scrollTop || document.body.scrollTop;currentPosition+=50;if(currentPosition<3500){window.scrollTo(0,currentPosition); }else{clearInterval(timer); }};GoBottom()'
        driver.execute_script(js)
        # time.sleep(1)
        driver.save_screenshot('path'+'/'+num+'/'+'test2.png')
        pic = driver.find_elements_by_xpath(path)
        print("========================================")
        urls = [i.get_attribute('src') for i in pic]
        names = [i.get_attribute('alt') for i in pic]
        print([i.get_attribute('src') for i in pic])
        driver.close()
        return (num,urls,names)

    def save_pic(self,pic_set):
        '''
        根据传入的url列表，保存图片
        :param pic_list:
        :return:
        '''
        page = pic_set[0]
        urls = pic_set[1]
        names = pic_set[2]
        if not os.path.exists(self.BASE_DIR+'/'+self.style+"/"+page):
            os.mkdir(self.BASE_DIR+"/"+self.style+"/"+page)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'referer': self.base_url
        }
        print('本页有%d张图片'%len(urls))
        for i in range(len(urls)):
            con = requests.get(urls[i],headers = header)
            with open(self.BASE_DIR+"/"+self.style+"/"+page+'/'+names[i]+urls[i][-4:],'wb') as f:
                f.write(con.content)

    def multithreading(self,num,q):
        print('开始下载第%s页'%num)
        x = time.time()
        a = self.parse_pic(num)
        self.save_pic(a)
        print('page%s time is %s'%(num,time.time()-x))
        print('threads %s'%threading.enumerate())
        print('第%s下载已完成'%num)
        q.put(num)
        pass

    def run(self):
        # parse_
        t = time.time()
        q = Queue()
        threads = []
        for page in range(1,int(self.pages)+1):
            t1 = threading.Thread(target=self.multithreading, args = [str(page),q],name='Page{}'.format(page))
            t1.start()
            threads.append(t1)
        for i in threads:
            i.join()
        print("_______________________________________")
        print(threads)
        # results = []
        # for i in threads:
        #     results.append(q.get())
        print("***************************************")
        print("all times:",time.time()-t)
        # print(results)
        # return results

if __name__ == '__main__':
    print("1:性感妹子\t2:日本妹子\t3:台湾妹子\t4:清纯妹子")
    print('输入你想下载的图片类型序号(默认为1)：')
    style_id = sys.stdin.readline().strip()
    style_dict = {'1':'xinggan','2':'japan','3':'taiwan','4':'mm'}
    style = style_dict[style_id] if len(style_id)!= 0 else style_dict['1']
    print('输入的id为%s,图片类型为%s' % (style_id,style))
    print("输入你想要下载的图片页数")
    pages = sys.stdin.readline().strip()
    meiZiTu = MeiZiTu(style,pages)
    meiZiTu.run()
    print('all done')
    print("+++++++++++++++++++++++")