# coding=utf-8
import json
import re
import jieba
import pandas as pd
import numpy
from PIL import Image, ImageSequence
import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud

# with open("./douban.json", "rb") as f:
#     content = f.read().decode()
#
# con = json.loads(content)
# comment = ""
# for i in range(len(con)):
#     comment += con[i]["shorts"]


class douban_analy(object):
    def __init__(self,id,comment):
        self.id = id
        self.comment = comment

    def fen_ci(self):
        pattern = re.compile(u'[\u4e00-\u9fa5]+')
        filterdata = re.findall(pattern, self.comment.decode('utf-8'))
        clean_comment = "".join(filterdata)
        # return clean_comment

        segment = jieba.lcut(clean_comment)
        word_df = pd.DataFrame({"segment": segment})

        stopwords = pd.read_csv("../static/stop/stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')#quoting=3全不引用
        words_df = word_df[~word_df.segment.isin(stopwords.stopword)]

        words_stat = words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
        words_stat = words_df.groupby(by=['segment'])['segment'].agg(numpy.size)
        words_stat = words_stat.to_frame()
        words_stat.columns = ['计数']
        words_stat = words_stat.reset_index().sort_values(by=["计数"],ascending=False)
        return words_stat
        # return str(stopwords)

    def ciyun(self,words_stat):
        image = Image.open('../static/images/haiwang.png')
        graph = numpy.array(image)
        wc=WordCloud(font_path="../static/font/simhei.ttf",background_color="black",max_font_size=80,mask=graph) #指定字体类型、字体大小和字体颜色
        # wc=WordCloud(font_path="simhei.ttf",background_color="black",max_font_size=80) #指定字体类型、字体大小和字体颜色
        word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}
        # print(word_frequence)
        wc.generate_from_frequencies(word_frequence)
        # plt.imshow(wc)
        # plt.axis("off")
        # plt.show()
        img = "../static/images/"+str(self.id)+".png"
        wc.to_file(img)
        return word_frequence

    def run(self):
        fenci_result = self.fen_ci()
        yuntu = self.ciyun(fenci_result)
        return fenci_result