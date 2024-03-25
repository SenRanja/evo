# encoding=utf-8
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

__doc__ = '''虽然django不以第三方包的形式，而是以backend目录下软件包的形式引入，但是直接修改源码的User模型，django不会生效，必须在次引入自定义User，并在settings.py中声明 AUTH_USER_MODEL = "user.User" 才可以使用'''

# User类的中间代码产物
class UserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError('The name field must be set')
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(name, password, **extra_fields)


# 重新自定义用户model，替代django原有的auth.User
class User(AbstractBaseUser, PermissionsMixin):
    """创建如YourModel.objects.create(data_list=[1, 2, 3, "text"])
修改如
    your_instance.data_list = ["new", "data"]
    your_instance.save()"""
    name = models.CharField(verbose_name="姓名", max_length=30, null=True, blank=True,)
    # 学号、手机号、身份证号、邮箱地址 设置  unique=True
    stu_id = models.CharField(verbose_name="学号", max_length=20, null=True, blank=True, unique=True)
    tel = models.CharField(verbose_name="手机号", max_length=30, null=True, blank=True, unique=True)
    id_card = models.CharField(verbose_name="身份证号", max_length=18, null=True, blank=True, unique=True)
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    avatar = models.CharField(verbose_name="头像", max_length=300, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, blank=True, null=True, )

    # 身份，该字段暂不使用
    role = models.CharField(verbose_name="身份", max_length=50, null=True, blank=True)

    is_staff = models.BooleanField(
        verbose_name="",
        default=False,
        help_text=_('是否平台工作人员'),
    )
    is_active = models.BooleanField(
        verbose_name="激活状态",
        default=True,
        help_text=_(
            '账户是否有效'
        ),
    )

    # 指定使用什么登录，此处该变量名在外部auth模块叫 username ，但是此处可写其他字段。但是因为使用了自定义auth的登录方式（参见.auth.py），故此处功能上可直接忽略，但是得设置一个unique的键名
    USERNAME_FIELD = "stu_id"

    # 使用manger类管理
    objects = UserManager()

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        db_table = "users"

    def clean(self):
        super().clean()

    def __str__(self):
        return self.name

