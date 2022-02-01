from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



#ブログモデル
class BlogModel(models.Model):
    title = models.CharField('タイトル', max_length=100)
    content = models.TextField('本文')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    useful_review = models.IntegerField(null=True,blank=True,default=0)
    useful_review_record = models.TextField(default='None')
    images = models.ImageField('写真', upload_to="")
    postdate = models.DateField(auto_now_add=True)
    useful_comment = models.IntegerField(null=True,blank=True,default=0)

    def __str__ (self):
        return self.title


#コメントモデル
class Comment(models.Model):
    user_name = models.CharField('名前', max_length=100 , default='匿名')
    message = models.TextField('本文')
    target = models.ForeignKey(BlogModel, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)
    number = models.IntegerField(null=True,blank=True,default=0)

    def __str__(self):
        return self.message[:20]
