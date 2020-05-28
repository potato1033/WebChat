import django.contrib.auth.models
from django.db import models
import datetime,jsonschema
# Create your models here.
#论坛帖子表
#注意blank=True, null=True参数的使用
class Article(models.Model):
    '''
    [title','brief', 'category','content','author,pub_date', 'last_modify', 'priorty','status']
    '''
    title = models.CharField(max_length=255,blank=True, null=True,verbose_name=u"标题")
    brief = models.CharField(null=True,blank=True,max_length=255,verbose_name=u"描述")
    category = models.ForeignKey("Category",on_delete=models.CASCADE,blank=True, null=True,verbose_name=u"所属板块")#由于Category类在它的下方,所以要引号引起来,Django内部会自动反射去找
    content = models.TextField(blank=True, null=True,verbose_name=u"文章内容")
    author = models.ForeignKey("UserProfile",blank=True, null=True,on_delete=models.CASCADE,verbose_name=u"作者")
    pub_date = models.DateField(blank=True,null=True)
    last_modify = models.DateField(auto_now=True,verbose_name=u"修改时间")
    priorty = models.IntegerField(default=1000,verbose_name=u"优先级")
    status_choices = (('draft',u"草稿"),
                      ('published',u"已发布"),
                      ('hidden',u"隐藏"))
    status = models.CharField(choices=status_choices,max_length=50,default="published")
    def __str__(self):
        return self.title
    # django 的model类在保存数据时,会默认调用self.clean()方法的,所以可以在clean方法中定义数据的一些验证
    def clean(self):
        # 如果帖子有发布时间,就说明是发布过的帖子,发布过的帖子就不可以把状态在改成草稿状态了
        if self.status == "draft" and self.pub_date:
            raise jsonschema.ValidationError()
        # 如果帖子没有发布时间,并且保存状态是发布状态,那么就把发布日期设置成当天
        if self.status == "published" and not self.pub_date:
            self.pub_date = datetime.date.today()

#评论表
class Comment(models.Model):
    '''
    ['article', 'parent_comment', 'comment_type', 'comment', 'user'，'date']
    '''
    article = models.ForeignKey("Article",on_delete=models.CASCADE,blank=True, null=True,verbose_name=u"所属文章")
    parent_comment = models.ForeignKey('self',related_name="my_children",blank=True,null=True,on_delete=models.CASCADE,verbose_name=u"父评论")
    date = models.DateTimeField(auto_now=True,verbose_name=u"评论时间")
    comment_choices = ((1,u"评论"),
                       (2,u"点赞"))
    comment_type = models.IntegerField(choices=comment_choices,default=1,verbose_name=u"评论类型")
    user= models.ForeignKey("UserProfile",on_delete=models.CASCADE,blank=True, null=True,verbose_name=u"评论人")
    comment = models.TextField(blank=True,null=True)
#   这里有一个问题,这里我们设置了允许为空,那就意味着我们在页面上点了评论,却又没有输入内容,这样岂不是很不合理.那么怎么实现只要你
# 点了评论,内容就不能为空.
#   那么我们会问,为什么允许为空,直接不为空就好了.因为我们这里把评论和点赞放到了一张表中,当为点赞时,当然就不需要评论内容了.所以
# 可以为空.
#   我们会想在前端进行判断或者在views写代码进行判断,这里告诉你这里我们就可以实现这个限制.使用Django中clean()方法,models类在保存
# 之前它会调用self.clean方法,所以我们可以在这里定义clean方法,进行验证
    def clean(self):
        if self.comment_type==1 and not self.comment:
            raise jsonschema.ValidationError(u"评论内容不能为空")


#板块表
class Category(models.Model):
    ''''['name','brief', 'set_as_top_menu', 'position_index']'''
    name = models.CharField(max_length=64,unique=True,blank=True, null=True,verbose_name=u"板块名称")#unique板块是否唯一
    brief = models.CharField(null=True,blank=True,max_length=255,verbose_name=u"描述")
    set_as_top_menu = models.BooleanField(default=False,verbose_name=u"是否将此板块设置在页面顶部")
    position_index = models.SmallIntegerField(blank=True, null=True,verbose_name=u"顶部展示的位置")
    #ManyToMany中设置了null = True造成的, 为什么造成?因为ManyToMany本来就不会写到本表中, 纪录都是保存在第三张表.如果不选就
    # 不创建纪录, 所以这里设置null = True是多余的.
    admins = models.ManyToManyField("UserProfile",blank=True,verbose_name=u"版主")
    def __str__(self):
        return self.name

#用户表继承Django里的User
class UserProfile(models.Model):
    user = models.OneToOneField(django.contrib.auth.models.User,on_delete=models.CASCADE,blank=True, null=True,verbose_name=u"管理Gjango内部的用户")
    name = models.CharField(max_length=32,blank=True, null=True,verbose_name=u"昵称")
    signature = models.CharField(max_length=255,blank=True,null=True,verbose_name=u"签名")
    head_img = models.ImageField(blank=True,null=True,verbose_name=u"头像")
#   ImageFied字段说明https://docs.djangoproject.com/en/1.9/ref/models/fields/
#   大概的意思是,ImageField 继承的是FileField,除了FileField的属性被继承了,它还有两个属性 ImageField.height_field
#   和ImageField.width_field,设置后当你存入图片字段时,它会把默认尺寸设置成高height_field宽:width_field
#   如果想在前端上传图像,需要下载一个Pillow模块,具体使用后面会用到

# 用户组表,其实这里用不到,因为我们使用Django的 User,
class UserGroup(models.Model):
    pass