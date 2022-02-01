from django.urls import path
from .views import Login_BlogList, BlogCreate, BlogDelete, BlogUpdate, CommentView, SignupView, LoginView, LogoutView, EvaluationView, No_Login_BlogList, detailview

app_name='blogapp'
urlpatterns = [
    path('login_list/', Login_BlogList.as_view(), name='login_list'),
    path('no_login_list/', No_Login_BlogList.as_view(), name='no_login_list'),
    path('detail/<int:pk>/', detailview, name='detail'),
    path('create_form/', BlogCreate.as_view(), name='create_form'),
    path('delete/<int:pk>/', BlogDelete.as_view(), name='delete'),
    path('update/<int:pk>/', BlogUpdate.as_view(),name='update'),
    path('comment_create/<int:pk>/', CommentView.as_view(), name='comment_create'),
    path('signup/', SignupView, name='signup'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('evaluation/<int:pk>/', EvaluationView, name='evaluation'),
]