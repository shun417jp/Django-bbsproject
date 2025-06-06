from django.contrib import admin
from .models import Article #models.pyからArticleクラスをインポート

# Register your models here.
admin.site.register(Article) #DjangoAdminにArticleクラスを登録
