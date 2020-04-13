from django.db import models


# Create your models here.
class BookInfoManager(models.Manager):  # TODO 为什么要定义一个自定义模型管理类？
    # 1.改变查询结果集
    # 不用加@classmethod，因为它本来就是类方法
    def all(self):
        # 在类的继承中，如果你想要重写父类的方法而不是覆盖的父类方法，这个时候我们可以使用super()方法来实现
        # 例如：调用object.all()的时候会过滤掉isDelete=True的数据
        # 1.调用父类的all()，获取所有数据
        books = super().all()  # super(BookInfoManager, self).all()
        # 2.对数据进行过滤
        books = books.filter(isDelete=False)
        # 返回books
        return books

    # 2.封装函数，操作模型类对应的数据表（增删改查都可以这样）
    # 保存数据的函数封装（类方法）
    def create_book(self, btitle, bpub_date):
        # obj=BookInfo() # 为了避免模型类名发生变化封装得函数中也要发生变化，所以可以进行下面这部分代码
        model_class = self.model  # model方法，获取self所在的模型类
        obj = model_class()
        obj.btitle = btitle
        obj.bpub_date = bpub_date
        obj.save()
        # 返回这个实例对象给，调用这个方法的“那家伙”
        return obj
    # 传日期的时候一般需要用到date()方法，但是如果你用的是合规的字符串也是可以的。 例如：1990-12-23
    # Modles.Manager中其实有封装好得保存得方法，但是它需要指定类型(关键字传参)。例如：BookInfo.objects.create(btittle='test3',bpub_date='1990-12-23')

class BookInfo(models.Model):
    '''图书模型类'''
    btitle = models.CharField(max_length=20)  # 图书名称
    # btitle = models.CharField(max_length=20,db_column='title')  # 指定后表的名字将为‘title’
    # btitle = models.CharField(max_length=20,unique=True)  # 表里的标题不可以重复

    # bprice= models.DecimalField(max_digits=10,decimal_places=2)  # 价格 一共十位，小数两位

    bpub_date = models.DateField()  # 出版日期
    # bpub_date = models.DateField(auto_now_add=True)  # 创建时间
    # bpub_date = models.DateField(auto_now=True)  # 更新时间

    bread = models.IntegerField(default=0)  # 阅读量
    bcomment = models.IntegerField(default=0)  # 评论量
    isDelete = models.BooleanField(default=False)  # 删除的标记

    # book = models.Manager()  # 自定义一个manager管理类对象，当自定义完成后objects将会失效,但是这样没实际作用，所以就有了下一行的操作
    objects = BookInfoManager()  # 此时自定义的管理类对象是包含它实例方法及原本的objects所有的方法的一个对象（因为它继承了modles.Manager类）

    # # 保存数据的函数封装（类方法）
    # @classmethod
    # def create_book(cls,btitle,bpub_date):
    #     obj=cls
    #     obj.btitle=btitle
    #     obj.bpub_date=bpub_date
    #     obj.save()
    #     # 返回这个实例对象给，调用这个方法的“那家伙”
    #     return obj
    # # 传日期的时候一般需要用到date()方法，但是如果你用的是合规的字符串也是可以的。 例如：1990-12-23
    # # 一般为了避免导入表的时候出现很多问题，所以我们一般将这种函数放在模型管理类里面

    # TODO 元选项 指定表名 避免文件夹被改报错
    class Meta:
        db_table = 'booktest_bookinfo'  # 指定模型类对应的表名


# 一本图书可能对应多个英雄，多个英雄也许对应一本图书，但是一个英雄只会对应一本图书。
class HeroIofo(models.Model):
    '''英雄模型类'''
    hname = models.CharField(max_length=20)  # 英雄名字
    hgender = models.BooleanField(default=False)  # 性别

    hcomment = models.CharField(max_length=200)  # 备注
    # hcomment = models.CharField(max_length=200,blank=True)  # 后台管理的时候可以使该字段为空白
    # hcomment = models.CharField(max_length=200,null=True)  # 允许为空
    # 当null=false blank=true的时候，在后台写该字段并提交的时候，存入的是一个空字符串

    hbook = models.ForeignKey('BookInfo')  # 外键 hbook_id （一对多关系）
    isDelete = models.BooleanField(default=False)  # 删除的标记


# python manage.py makemigrations 生成迁移文件
# python manage.py migrate 生成表

# 约束default 和 blank 是不影响表的结构的


# todo django查询函数的特点

# 通过模型类.objects属性调用如下函数，实现对应的数据表的查询
# get 返回表中满足条件的一条且只能有一条数据（如果没有或者有多的会报错）
# all 返回表格中对应的所有数据
# filter 返回满足条件的数据
# exclude 返回不满足条件的数据
# order_by 对查询结果排序
# 除了get其它返回的都是查询集，即使只返回一条数据



# 条件
# get filter exclude 中是可以包含条件判断的，而且可以多个条件，条件间是且的关系 
# 条件的标准写法——例：get(id=1)其实应该是get(id__exact=1)的。
# 完整的例子：查询标题包含‘传’的数据 BookInfo.objects.filter(btittle__contains='传')
# ## 结尾的条件是 endswith 开头的条件是 startswith 不为空的条件 isnull=False 包含的条件是contains
# 范围查询 in 。 例如：查询id=1，3，5的图书。BookInfo.objects.filter(id__in=[1,3,5])
# gt 大于 lt 小于 gte 大于等于 lte小于等于 例如：filter(id__gt=3)表示大于三的数据;filter(bpub_date__gt=(1980,1,1))表示查询这天之后的图书
# 查询1980年的数据 filter(bupu_date__year=1980) 类似的还有 month=5 五月的数据

# 将数据升序排列(所有数据排序.all()可以省略) BookInfo.objects.all().oder_by('id')  降序('-id')

# 查询集和模型类对象关系
# 查询集可以遍历，遍历出来的就是模型类对象。
# get()方法返回的只有一条数据，即是模型类对象

# #get filter exclude 中是可以包含条件判断的，而且可以多个条件，条件间是且的关系 ，如果想要与或非或者字段间的比较的话，需要QF类。
# Q
# 如果是与或非的操作需要导入Q类 from django.db.modles import Q
# BookInfo.objects.filter(Q(id__gt=3)|Q(bread__gt=30)) 或
# BookInfo.objects.filter(Q(id__gt=3)&Q(bread__gt=30)) 且（与） （可以直接传入条件）
# BookInfo.objects.filter(~Q(id=3)) 非 （类似exclude方法）
# F
# 类属性(字段)间得比较 from django.db.models import F
# BookInfo.objects.filter(bread__gt=F('bcomment')) ——图书阅读量大于评论量得图书
# BookInfo.objects.filter(bread__gt=F('bcomment')*2)

# 聚合函数
# Sum 求和 Count 统计 Avg平均值 Max 最大值 Min 最小值
# 需要先导入聚合类并且使用aggregate调用函数使用聚合 from django.db.models import Sum,Count,Max,Min
# BookInfo.objects.all().aggregate(Count('id')) --统计id数目 --返回得是字典类型{'id__count':6}
# #ps:与之类似得有一个count()函数查询总数的 BookInfo.objects.all().count() -- int类型
# # BookInfo.objects.filter(id__gt=3).count()
# BookInfo.objects.all().aggregate(Sum('bread')) --阅读量得总和 --all()可以省略

# #对于一个QuerySet实例对象，可以继续调用上面所有的函数。
# 查询集（QuerySet）的特性
# 惰性查询（只用用它的时候才会查询） 缓存（第二次使用不会再次查询）
# 查询集类似列表，可以进行遍历，切片等操作，但是切片的下标不可以为负
# 查询集（可以进行切片操作，但是下标不可以为负数）中的数据 books[0]第一条数据 b[0:1].get() --两者若是查不到数据的话抛出的异常时不一样的（IndexError和DoesNotExist）
# 查询集中的exists()方法(判断是否存在的方法)。当一个查询集为空的时候调用这个方法返回的值是False例： books[0:0].exists() False


# models.OneToOneField() 一对一关系，定义在哪个类中都可以，但是查询的时候要注意外键在谁的类里。
class EmployeeBasicInfo(models.Model):
    '''员工基本信息类'''
    name = models.CharField(max_length=20)
    gender = models.BooleanField(default=False)
    age = models.IntegerField()


class EmployDetailInfo(models.Model):
    '''员工详细信息类'''
    # 联系地址
    addr = models.CharField(max_length=128)
    # 关系属性（一对一）
    employee_basic = models.OneToOneField('EmployeeBasicInfo')


# models.ManyToManyField() 多对多关系，定义在哪个类中都可以，但是查询的时候要注意外键在谁的类里。
class NewsType(models.Model):
    '''新闻类型类'''
    type_name = models.CharField(max_length=20)


class NewsInfo(models.Model):
    '''新闻类'''
    title = models.CharField(max_length=128)
    pub_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    new_type = models.ManyToManyField('NewsInfo')

# 一本图书可能对应多个英雄，多个英雄也许对应一本图书，但是一个英雄只会对应一本图书。

# 一查多 查询id为1的图书关联的英雄信息
# books = BookInfo.object.get(id=1)  books.heroiofo_set.all() 等于 HeroIofo.objects.filter(hbook__id=1)  前者通过一个对象来查，后者通过类来查询信息
# select * from booktest_heroiofo inner join booktest_bookinfo on booktest_heroiofo.hbook_id=booktest_bookinfo.id having booktest_bookinfo.id=1;

# 多查一 查询id为1的英雄关联的图书信息
# b = HeroIofo.objects.get(id=1) b.hbook   等于 BookInfo.objects.filter(heroiofo__id=1)  
# select * from booktest_bookinfo inner join booktest_heroiofo on booktest_heroiofo.hbook_id=booktest_bookinfo.id having booktest_heroiofo.id=1;
# 
# 总结： on后面的确定的是外键要真正的关联起来（哪个英雄对应哪本书），having确定的是条数据对应的外键。
# 补充：
# _set是固定的，就像heroiofo__hcomment__contains='八'是固定的一样的意思。 
# 在flask中是没有_set的操作的，但是为了能达到同样的效果，会在类中定义一个字段，而这个字段只是为了方便查询，是不存在表中的。

# 答疑
# 为什么能实现类似BookInfo.objects.filter(heroiofo__id=1)这种查询？
# 此时在一类是没有外键的，但是却可以通过“heroiofo__id=1”直接来查，因为这两个表之间通过外键关联了。
# 而在数据库中，所有的查询操作都是通过关联查询来查询并显示数据的。
# 为什么一对多中外键要定义在多类中？
# 一类对应多条多类的信息，如果通过唯一id标记多类？难道要定义一个字段，存储其关联的所有多类信息？比如一本图书对应多个英雄，那么要定义一个字段存储这些英雄分别是谁？
# 多对多的表关系是怎么处理的？：新建一个关联表，每条数据存储两个表之间的关联信息。https://zhidao.baidu.com/question/583107449.html）

# #通过模型类查询
# 一查多
# TODO 查询图书信息，要求图书关联的英雄的描述包含‘八’ BookInfo.objects.filter(heroiofo__hcomment__contains='八') 
# 查询图书信息， 要求图书中的英雄id大于3 BookInfo.objects.filter(heroiofo__id__gt=3)
# 多查一
# 查询书名为天龙八部的所有英雄 HeroIofo.objects.filter(hbook__btitle='天龙八部')  # 因为多查一有外键(关联属性)，所以不可以用bookinfo
# #通过模型类实现关联查询时，要查哪个表中的数据，就要通过哪个类来查
# #写关联查询条件的时候，如果类中没有关系属性，条件中需要些对应类的名字（小写），如果类中有关系属性则直接写关系属性。





# todo 插入和 更新 save（）方法；删除 delete（）方法；

# 自关联
class AreaInfo(models.Model):
    '''地区模型类'''
    # 地区属性
    atitle = models.CharField(max_length=20)
    # 关系属性，代表当前地区的父级地区
    aparent = models.ForeignKey('self', null=True, blank=True)  # 父级可以为空 # 自关联，“外键”的表就是自己

    # todo 参照这个表数据理解一下吧
    # +----+--------+------------+
    # | id | atitle | aparent_id |
    # +----+--------+------------+
    # | 1 | 广东省 |        NULL |
    # | 2 | 广州市 |           1 |
    # | 3 | 东城区 |           2 |
    # | 4 | 魏都区 |           2 |
    # | 5 | 测试   |        NULL |
    # +----+--------+------------+

