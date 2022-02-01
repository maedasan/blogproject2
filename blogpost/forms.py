from django import forms
from .models import Comment, BlogModel

#コメント投稿フォーム
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('target', 'created_at', 'number')


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        exclude = ('author', 'useful_review', 'useful_review_record', 'postdate', 'useful_comment')
        