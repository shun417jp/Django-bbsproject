from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#Userモデルをインポート

# Create your models here.
class Article(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # その高騰の詳細ページへのリンク
    def get_absolute_url(self):
        return reverse("bbs:detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return self.content 
