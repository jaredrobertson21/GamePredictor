from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^$', views.user_login),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^signup/', views.user_signup, name='user_signup'),
]
