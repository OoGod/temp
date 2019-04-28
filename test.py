from selenium import webdriver
import time
import requests
import os
import sys


class MeiZiTu(object):
    def __init__(self,style,page):
        '''
        输入图片类型和想要爬取的页数
        :param style: 图片类型
        :param page: 爬取的页数
        '''
        self.BASE_DIR = '妹子图'
        if not os.path.exists(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
        if not os.path.exists('Apath'):
            os.mkdir('Apath')
        self.url = 'https://www.mzitu.com/{}/page/{}/'.format(style)
        self.pic_list = []
        self.page = page

    def parse_pic(self,num):
        '''
        根据传入的页面，获取相应的图片url列表
        :param num:
        :return:
        '''
        driver = webdriver.PhantomJS()
        url = self.url
        path = "//img[@class='lazy']"
        if not os.path.exists('Apath'+'/'+num):
            os.mkdir('Apath'+'/'+num)
        driver.get(url.format(num))
        driver.save_screenshot('page'+'/'+num+'/'+'test1.png')
        pic = driver.find_elements_by_xpath(path)
        print([i.get_attribute('src') for i in pic])
        js = 'var currentPosition,timer;function GoBottom(){ timer=setInterval("runToBottom()",1); };function runToBottom(){currentPosition=document.documentElement.scrollTop || document.body.scrollTop;currentPosition+=50;if(currentPosition<3500){window.scrollTo(0,currentPosition); }else{clearInterval(timer); }};GoBottom()'
        driver.execute_script(js)
        # time.sleep(1)
        driver.save_screenshot('page'+'/'+num+'/'+'test2.png')
        pic = driver.find_elements_by_xpath(path)
        print("========================================")
        print([i.get_attribute('src') for i in pic])
        return [i for i in pic]

    def save_pic(self,pic_list):
        '''
        根据传入的url列表，保存图片
        :param pic_list:
        :return:
        '''
        if not os.path.exists(self.BASE_DIR+"/"+self.page):
            os.mkdir(self.BASE_DIR+"/"+self.page)
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'referer': self.url.format(self.page)
        }
        urls = [i.get_attribute('src') for i in pic_list]
        names = [i.get_attribute('alt') for i in pic_list]
        print('本页有%d张图片'%len(urls))
        for i in range(len(pic_list)):
            con = requests.get(urls[i],headers = header)
            with open(BASE_DIR+"/"+self.page+'/'+names[i]+urls[i][-4:],'wb') as f:
                f.write(con.content)

    def run(self):
        # parse_
        pass

if __name__ == '__main__':
    print("1:性感妹子\t2:日本妹子\t3:台湾妹子\t4:清纯妹子")
    print('输入你想下载的图片类型序号(默认为1)：')
    style_id = sys.stdin.readline().strip()
    style_dict = {'1':'xinggan','2':'japan','3':'taiwan','4':'mm'}
    style = style_dict[style_id] if len(style_id)!= 0 else style_dict['1']
    print('输入的id为%s,图片类型为%s' % (style_id,style))
    print("输入你想要下载的图片页数")
    pages = sys.stdin.readline().strip()

    for page in range(1,(int(pages)+1)):
        print('开始下载第%d页' % page)
        t = parse_pic(page)
        save_pic(t,str(page))
        print('第%d页已下载完' % page)