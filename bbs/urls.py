from django.urls import re_path
from bbs import views

urlpatterns = [
    re_path(r'^test', views.test),
    re_path(r'^$', views.index),
    re_path(r'category/(\d+)',views.category,name='category_detail')
]