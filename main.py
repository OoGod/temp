from selenium import webdriver
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from snownlp import SnowNLP
from pylab import mpl
import numpy as np
import csv
import jieba
import requests
import json
import sys
import os
import re


class reviewsAnalysis(object):

    def __init__(self,name):
        self.url = "https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P"
        self.search_url = 'https://movie.douban.com/j/subject_suggest?q={}'
        self.name = name
        self.BASE_DIR = 'staticccc/'
        self.movie_id = None
        self.movie_name = None
        self.sentimentslist = None
        self.file_csv = ''
        self.file_rev = ''

        self.deny_word = []
        self.posdict = []
        self.negdict = []
        self.degree_word = []
        self.mostdict = []
        self.verydict = []
        self.moredict = []
        self.ishdict = []
        pass

    def search(self):
        '''
        查询电影id,用于构造查询url
        :return:
        '''
        response = requests.get(self.search_url.format(self.name))
        namelist = json.loads(response.text)
        x = 0
        print('id\tname')
        list_a = []
        for i in namelist:
            print('%s\t%s' % (x, i['title']))
            dict_a = {x: i['title']}
            list_a.append(dict_a)
            x += 1
        print(list_a)
        print("您想要的查询结果可能是可能是这些，请输入id进行查询")
        input_id = sys.stdin.readline().strip()
        movie_id = namelist[int(input_id)]['id']
        self.movie_name = namelist[int(input_id)]['title']
        self.movie_id = movie_id
        self.file_csv = self.BASE_DIR+self.movie_name+'.csv'
        self.file_rev = self.BASE_DIR+self.movie_name+'.txt'
        return movie_id

    def parse_save(self):
        '''
        爬取评论并且保存到test-douban.csv中
        :return:
        '''
        # 写入文件
        if not os.path.exists(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
        c = open(self.file_csv, "w",encoding='utf-8')  # 写文件
        # c.write(codecs.BOM_UTF8)          #防止乱码
        writer = csv.writer(c)  # 写入对象
        writer.writerow(['序号', '用户名', '链接', '评分', '评分标题', '有用数', '日期', '评论'])
        # 打开Firefox浏览器 设定等待加载时间 访问URL
        driver = webdriver.PhantomJS()
        i = 0
        while i < 10:
            num = i * 20
            # url = "https://movie.douban.com/subject/1292052/comments?start=" + str(
            #     num) + "&limit=20&sort=new_score&status=P"
            url = self.url.format(int(self.movie_id),str(num))
            print(url)
            driver.get(url)
            # 用户姓名 超链接
            elem1 = driver.find_elements_by_xpath("//div[@class='avatar']/a")
            # 用户评分
            elem2 = driver.find_elements_by_xpath("//span[@class='comment-info']/span[2]")
            # 有用数
            elem3 = driver.find_elements_by_xpath("//span[@class='comment-vote']/span[1]")
            # 日期
            elem4 = driver.find_elements_by_xpath("//span[@class='comment-time ']")
            # 评论
            elem5 = driver.find_elements_by_xpath("//span[@class='short']")
            # next
            xxx = driver.find_elements_by_xpath("//a[@class='next']")
            # 循环写入20行评价
            tlist = []
            k = 0
            # print('----------------------------------------')
            # print(xxx,len(xxx))
            # print(len(elem1))
            # print("++++++++++++++++++++++++++++++++++++++++")
            while k < 20 and k < len(elem1):
                # 序号
                num = i * 20 + k + 1
                print(num)
                # 用户姓名
                name = elem1[k].get_attribute("title")
                print(name)
                # 超链接
                href = elem1[k].get_attribute("href")
                print(href)
                # 用户评分及内容
                score = elem2[k].get_attribute("class")
                print(score)
                content = elem2[k].get_attribute("title")
                print(content)
                # 有用数
                useful = elem3[k].text
                print(useful)
                # 日期
                date = elem4[k].text
                # 评论
                shortcon = elem5[k].text
                print(shortcon)

                # 写入文件
                templist = []
                templist.append(num)
                templist.append(name)
                templist.append(href)
                templist.append(score)
                templist.append(content)
                templist.append(useful)
                templist.append(date)
                templist.append(shortcon)
                writer.writerow(templist)

                k = k + 1

            i = i + 1

        c.close()
        pass

    def save(self):
        '''
        从csv文件中爬取评论数据，并且保存到data.txt中
        :return:
        '''
        # filename = 'test-douban.csv'

        data = ''
        with open(self.file_csv,encoding='utf-8') as f:
            reader = csv.reader(f)
            for i in reader:
                if len(i) != 0:
                    data += i[-1]
                    data += "\n"
        with open(self.file_rev, 'w',encoding='utf-8') as f:
            f.write(data)

        # print(data)

    def fenci(self):
        '''
        根据data.txt中的评论数据并且进行分词和词云展示
        :return:
        '''
        with open(self.file_rev,'r',encoding='utf-8') as f:
            text = f.read()
        print(type(text))
        jieba.load_userdict('./userdict.txt')
        # 结巴分词 cut_all=True 设置为精准模式
        wordlist = jieba.cut(text, cut_all=False)
        # 使用空格连接 进行中文分词
        wl_space_split = " ".join(wordlist)
        print(wl_space_split)

        # 对分词后的文本生成词云
        font = 'C:\Windows\Fonts\simhei.ttf'
        my_wordcloud = WordCloud(font_path = font).generate(wl_space_split)

        # 显示词云图
        plt.imshow(my_wordcloud)
        # 是否显示x轴、y轴下标
        plt.axis('off')
        plt.show()

    def analysis_a(self):
        '''
        读取data.txt中的评论数据，根据评论数据统计情感分数段并绘制对应的柱状图
        :return:
        '''
        with open(self.file_rev, "r", encoding='utf-8') as f:
            line = f.readlines()
        sentimentslist = []
        for i in line:
            s = SnowNLP(i)
            print(s.sentiments)
            sentimentslist.append(s.sentiments)
        self.sentimentslist = sentimentslist
        return sentimentslist

    def analysis(self):
        '''
        读取data.txt中的评论数据，根据评论数据统计情感分数段并绘制对应的柱状图
        :return:
        '''
        sentimentslist = self.sentimentslist if self.sentimentslist is not None else self.analysis_a()
        # 数值越靠近1说明评价越高，靠近0说明评价越低。
        plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01), facecolor='g')
        plt.xlabel('Sentiments Probability')
        plt.ylabel('Quantity')
        plt.title('Analysis of Sentiments')
        plt.show()

    def score(self):
        '''
        读取data.txt中的评论数据，根据评论数据统计情感分数段并绘制对应的柱状图
        :return:
        '''
        sentimentslist = self.sentimentslist if self.sentimentslist is not None else self.analysis_a()
        score_dict = {'high': 0, 'mid': 0, 'low': 0}
        for i in sentimentslist:
            if i > 0.7:
                score_dict['high'] += 1
            elif i > 0.35:
                score_dict['mid'] += 1
            elif i <= 0.35:
                score_dict['low'] += 1
            else:
                pass
        print('统计总评数\t好评数\t中评数\t差评数')
        print('{}\t{}\t{}\t{}'.format((score_dict['high']+score_dict['mid']+score_dict['low']),score_dict['high'],score_dict['mid'],score_dict['low']))
        plt.bar(['low','mid','high'],[score_dict['low'],score_dict['mid'],score_dict['high']],facecolor='cyan')
        plt.xlabel('Evaluation score')
        plt.ylabel('Number')
        plt.title('Analysis of Score')
        plt.show()
        return score_dict

    def analysis_wave(self):
        '''
        功能：情感波动分析
        读取data.txt中的评论数据，根据评论数据统计情感分数段并绘制对应的曲线图
        :return:
        '''
        sentimentslist = self.sentimentslist if self.sentimentslist is not None else self.analysis_a()
        result = [i - 0.5 for i in sentimentslist]
        # plt.plot(sentimentslist, 'k-')
        plt.plot(result, 'k-')
        plt.xlabel('Number')
        plt.ylabel('Sentiment')
        plt.title('Analysis of Sentiments')
        plt.show()
        pass

    def fenci_con(self):
        '''
        对每个评论进行分析，输出分析结果
        :return:
        '''
        with open(self.file_rev,'r',encoding='utf-8') as f:
            line = f.readlines()
        jieba.load_userdict('./userdict.txt')
        result = ''
        for text in line[1:]:
            wordlist = jieba.cut(text, cut_all=False)
            # 使用空格连接 进行中文分词
            wl_space_split = " ".join(wordlist)
            result += wl_space_split
            result += '\n'
            print(wl_space_split)
        with open('result.txt','w',encoding='utf-8') as f:
            f.write(result)

    def open_dict(self, Dict='hahah'):
        path = 'Textming/Textming/'+'%s.txt' % Dict
        dictionary = open(path, 'r', encoding='utf-8')
        list1 = []
        for word in dictionary:
            word = word.strip('\n')
            list1.append(word)
        return list1

    def sentiment_score_list(self, data):
        data = re.sub(r"，|,|！|!", "", data)

        seg = jieba.cut(data)
        a = []
        words = []
        for word in seg:
            if word in self.posdict:
                # print('pos', word)
                words.append(word)
                a.append(1)
            elif word in self.negdict:
                # print('neg', word)
                words.append(word)
                a.append(-1)
            elif word in self.mostdict:
                # print('most', word)
                words.append(word)
                a.append(4)
            elif word in self.verydict:
                # print('very', word)
                words.append(word)
                a.append(3)
            elif word in self.moredict:
                # print('more', word)
                words.append(word)
                a.append(2)
            elif word in self.ishdict:
                # print('ish', word)
                words.append(word)
                a.append(0.5)

        return a, words

    def ev_score(self, t):
        sum1 = 0
        i = 0
        temp = 0
        while i < len(t):
            if temp==0:
                temp += t[i]
            else:
                temp *= t[i]
            if abs(temp)==1:
                sum1 += temp
                temp = 0
            else:
                if i >= len(t)-1 or abs(t[i+1])==1:
                    sum1 = sum1 + temp*t[i+1] if i<len(t)-1 else sum1+temp
                    temp = 0
                    i += 1
            i += 1
        return sum1

    def sen_every_words(self):

        self.deny_word = self.open_dict(Dict='否定词')
        self.posdict = self.open_dict(Dict='positive')
        self.negdict = self.open_dict(Dict='negative')
        self.degree_word = self.open_dict(Dict='程度级别词语')
        self.mostdict = self.degree_word[self.degree_word.index('extreme') + 1: self.degree_word.index('very')]  # 权重4，即在情感词前乘以4
        self.verydict = self.degree_word[self.degree_word.index('very') + 1: self.degree_word.index('more')]  # 权重3
        self.moredict = self.degree_word[self.degree_word.index('more') + 1: self.degree_word.index('ish')]  # 权重2
        self.ishdict = self.degree_word[self.degree_word.index('ish') + 1: self.degree_word.index('last')]  # 权重0.5
        with open(self.file_rev,'r',encoding='utf-8') as f:
            text = f.read()
        print(type(text))
        data = text.split('\n')

        print(data)
        for dat in data:
            if not dat:
                continue
            a, words = self.sentiment_score_list(dat)
            wor = '句子：' + " ".join(words) + 'score:%d' % self.ev_score(a) + '原因：' + str(a)
            print(dat)
            print(wor)
            print(SnowNLP(dat).sentiments)

    def run(self):
        '''
        对评论相关数据进行爬取，并保存到文件中
        :return:
        '''
        # 3.查找电影获取电影id
        self.search()
        # 5.查看电影是否爬取，未爬取则进行爬取，爬取后不再爬取
        if not os.path.exists(self.file_rev):
            print('尚未爬取过此电影，现在开始爬取评论数据')
            self.parse_save()
            self.save()
            print('爬取数据已保存')
        pass


if __name__ == '__main__':

    # url = sys.stdin.readline().strip()
    # url = "https://movie.douban.com/subject/1292052/comments?start={}&limit=20&sort=new_score&status=P"
    # sys.stdout.write('movie name')
    # name = sys.stdin.readline().strip()
    #1. 输入需要爬取和分析的电影名
    try:
        name = sys.argv[1]
    except:
        print('输入电影名：')
        name = sys.stdin.readline().strip()
    finally:
        # 2.爬取并保存电影评论
        film = reviewsAnalysis(name)
        film.run()
    while True:
        print('=========================================')
        print('输入1进行分词，并绘制词图')
        print('输入2进行情感分析，绘制柱状图')
        print('输入3进行情感分析，绘制曲线图')
        print('输入4输出评分，绘制柱状图')
        print('输入5输出每一句的分词结果')
        print('输入6输出每一句的情感分词结果')
        print("输入7退出情感分析系统")
        print("=========================================")
        choice = sys.stdin.readline().strip()
        if choice == '1':
            film.fenci()
        elif choice == '2':
            film.analysis()
        elif choice == '3':
            film.analysis_wave()
        elif choice == '4':
            film.score()
        elif choice == '5':
            film.fenci_con()
        elif choice == '6':
            film.sen_every_words()
        elif choice == '7':
            break
        else:
            print('请根据提示信息进行输入')
