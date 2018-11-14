from django.conf.urls import url
from .views import get_user,login_user
urlpatterns = [
        url(r'^api/(?P<key>.*)$|api/$', view=get_user, name='home'),
        url(r'^login/$', view=login_user, name='login')
]
