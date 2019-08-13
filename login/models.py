from django.db import models

# Create your models here.
#可以使用django自带的AbstactUser表.也可以继承自己的添加字段
#但内部代码不好修改，建议根据业务要求自己创建user表
class User(models.Model):
    name = models.CharField(verbose_name='用户名',max_length=20)
    email = models.CharField(verbose_name='邮箱',null=True,blank=True,max_length=100)
    password = models.CharField(verbose_name='明文密码',max_length=20)
    hash_password = models.CharField(verbose_name='哈希密码',max_length=256,null=True,blank=True)

    #is_admin   join_time  last_login  等字段
