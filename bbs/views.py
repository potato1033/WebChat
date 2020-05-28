from django.shortcuts import render,HttpResponse
from bbs import models
# Create your views here.

category_list = models.Category.objects.filter(set_as_top_menu = True).order_by('position_index')

def test(request):
    return render(request,"test.html")

def index(request):
    print(category_list)
    category_obj = models.Category.objects.get(position_index=1)  # 我们这里定义positon_index=1时,这个就是"全部"这个板块
    article_list = models.Article.objects.filter(status='published')
    return render(request,"bbs/index.html",{'category_list':category_list,
                                               'category_obj':category_obj,
                                               'article_list':article_list})


def category(request, id):  # id是URL配置中category/(\d+)/$的(\d+),一个括号就是一个参数
    category_obj = models.Category.objects.get(id=id)
    if category_obj.position_index == 1:  # 我们把板块"全部"认定为首页显示,把所有的文章都显示出来,首页就认定当position_index 为1时既是首页.
        article_list = models.Article.objects.filter(status='published')
    else:
        article_list = models.Article.objects.filter(category_id=category_obj.id, status='published')
    return render(request, "bbs/index.html", {'category_list': category_list,
                                                 'category_obj': category_obj,
                                                 'article_list': article_list})