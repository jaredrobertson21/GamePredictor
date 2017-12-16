from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^submit_data/', views.submit_data, name='data'),
]
