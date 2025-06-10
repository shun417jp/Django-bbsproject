from django.shortcuts import render
from django.views import generic #汎用ビューのインポート
from .models import Article #models.pyのArticleクラスをインポート
from django.urls import reverse_lazy
from .forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin   # LoginRequiredMixinをインポート
from django.core.exceptions import PermissionDenied    # PermissionDeniedをインポート

# Create your views here.
#IndexViewクラスを作成
class IndexView(generic.ListView):
    model = Article #Articleクラスを仕様
    template_name = 'bbs/index.html'#使用するテンプレート名を指定(Articleも自動で渡す)
    
class DetailView(generic.DetailView):
    model = Article #Articleクラスを使用
    template_name = 'bbs/detail.html' #使用するテンプレート名を指定(Articleも自動で渡す)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.object
        return context
    
class CreateView(LoginRequiredMixin,generic.edit.CreateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']
    
     # 格納する値をチェック
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView,self).form_valid(form)

# UpdateViewクラスを作成
class UpdateView(LoginRequiredMixin,generic.edit.UpdateView):
    model = Article
    template_name = 'bbs/create.html'
    fields = ['content']
    
    def dispatch(self, request, *args, **kwargs):
        # 編集対象の投稿オブジェクトを取得
        obj = self.get_object()
        # 投稿者と現在のユーザーが一致しない場合は403エラーを発生
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません。')
        # 親クラスのdispatchを呼び出して通常の処理を継続
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    template_name = 'bbs/delete.html'
    success_url = reverse_lazy('bbs:index')
    
    def dispatch(self, request, *args, **kwargs):  # インデントを修正
        # 削除対象の投稿オブジェクトを取得
        obj = self.get_object()  # スペルミスを修正
        if obj.author != self.request.user:
            raise PermissionDenied('削除権限がありません。')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

#検索機能のビュー
def search(request):
    articles = None #検索結果を格納する変数を初期化
    searchform = SearchForm(request.GET)#GETリクエストで送信したデータが格納される
    
    #Formに正常なデータがあれば
    if searchform.is_valid():
        query = searchform.cleaned_data['words']
        #queryにフォームが持っているデータを代入
        articles = Article.objects.filter(content__icontains=query)
        #クエリを含むレコードをfilterメソッドで取り出し、article変数に代入
        return render(request, 'bbs/results.html',{'articles':articles,'searchform':searchform})

# カスタム403のビュー(アクセス権限が無い場合)
def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)
