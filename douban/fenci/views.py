# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import *
from douban_fenci import douban_analy

# Create your views here.
def index(request):
    # return HttpResponse("hello,there may be moive lover's home")
    content = {'title': "首页", 'list': range(10)}
    return render(request, 'fenci/index.html',content)


def deal_com(request):
    # return HttpResponse("hello,there may be moive lover's home")
    # content = {'title': "首页", 'list': range(10)}
    # return render(request, 'images/index.html',content)
    comment_info = CommentInfo.objects.all()
    content = {'com_info': comment_info}
    return render(request,'fenci/deal_com.html',content)


def detail(request, id):
    comment = CommentInfo.objects.get(id=id)
    douban_ana = douban_analy(id,str(comment))
    fenci_con = douban_ana.run()
    image = "images"+"/"+str(id)+".png"
    content = {'com_detail': str(comment),'fenci_con':fenci_con,"img": image}
    return render(request,'fenci/detail.html', content)
