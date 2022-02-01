from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import BlogModel, Comment
from django.urls import reverse_lazy
from .forms import CommentCreateForm, BlogCreateForm
from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout



#一覧ページ（ログイン済みユーザー）
class Login_BlogList(ListView):
    template_name = 'login_list.html'
    model = BlogModel

#一覧ページ（非ログインユーザー）
class No_Login_BlogList(ListView):
    template_name ='no_login_list.html'
    model = BlogModel   


#詳細ページ
def detailview(request, pk):
    detail_object = get_object_or_404(BlogModel, pk=pk)
    review_user_name = str(request.user.get_username())
    author_user_name = str(detail_object.author)
    
    if '' == str(request.user.get_username()):
        return render(request, 'detail_no_login.html', {'detail_object':detail_object})

    elif review_user_name != author_user_name :
        return render(request, 'detail_review.html', {'detail_object':detail_object})    
    else:
        return render(request, 'detail_author.html', {'detail_object':detail_object})



#記事作成
class BlogCreate(CreateView):
    template_name = 'create_form.html'
    model = BlogModel
    form_class = BlogCreateForm
    success_url = reverse_lazy('blogapp:login_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


#記事削除
class BlogDelete(DeleteView):
    template_name = 'delete.html'
    model = BlogModel
    success_url = reverse_lazy('blogapp:login_list')


#更新
class BlogUpdate(UpdateView):
    template_name = 'update.html'
    model = BlogModel
    fields =('title', 'content', 'images')

    ##フォームに入力された情報が正しい場合の処理 (DB保存と画面遷移)
    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.save()
        return redirect('blogapp:detail', pk=self.kwargs['pk'])

    #htmlテンプレートに渡すデータを定義(キャンセルボタンが押された時、記事詳細に戻る為のキーを取得)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reverse_page'] = get_object_or_404(BlogModel, pk=self.kwargs['pk'])
        return context



#コメント投稿ページのビュー
class CommentView(CreateView):
    template_name = 'comment_form.html'
    model = Comment
    form_class = CommentCreateForm
    
    #フォームに入力された情報が正しい場合の処理 (DB保存と画面遷移)
    def form_valid(self, form):
        post = get_object_or_404(BlogModel, pk=self.kwargs['pk'])
        post.useful_comment += 1
        post.save()
        comment = form.save(commit=False)
        comment.target = post
        comment.number = post.useful_comment
        comment.save()
        return redirect('blogapp:detail', pk=self.kwargs['pk'])

    #htmlテンプレートに渡すデータを定義(キャンセルボタンが押された時、記事詳細に戻る為のキーを取得)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reverse_page'] = get_object_or_404(BlogModel, pk=self.kwargs['pk'])
        return context


#会員登録
def SignupView(request):
    if request.method == 'POST':
        username_data= request.POST['username_data']
        password_data= request.POST['password_data']
        try:
            User.objects.create_user(username_data,"",password_data)
            user= authenticate(request, username=username_data, password= password_data)
            login(request,user)
            return redirect('blogapp:login_list')
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'このユーザー名は既に登録されています。'})
    else:
        return render(request, 'signup.html', {})


#ログイン
def LoginView(request):
    if request.method == 'POST':
        username_data= request.POST['username_data']
        password_data= request.POST['password_data']
        user= authenticate(request, username= username_data, password= password_data)
        if user is not None:
            login(request,user)
            return redirect('blogapp:login_list')
        else:
            return render(request, 'login.html', {'error': 'ユーザー名 or パスワード が間違っています。'})
    else:
        return render(request, 'login.html')


#ログアウト
def LogoutView(request):
    logout(request)
    return redirect('blogapp:no_login_list')


#いいね（参考になった)
def EvaluationView(request, pk):
    post= get_object_or_404(BlogModel, pk=pk)
    review_username= request.user.get_username() + str(request.user.id)
    if not review_username in post.useful_review_record:
        post.useful_review += 1
        post.useful_review_record += review_username
        post.save()
        return redirect('blogapp:detail',post.pk)
    else:
        return redirect('blogapp:detail',post.pk)
        