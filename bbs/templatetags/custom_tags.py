from django import template

register = template.Library()

@register.filter#定义截取上传文件的文件名的方法
def truncate_url(img_obj):
    print(img_obj.name,img_obj.url)#使用.name和.url都可以获取字符串如：uploads/head.jpg
    return img_obj.name.split('/',maxsplit=1)[-1]#使用'/'作为分隔符，maxsplit表示最多分隔次数，[-1]获取文件名