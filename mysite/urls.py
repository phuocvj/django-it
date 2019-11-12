from django.conf.urls import include,url
from . import views
from .views import index,about
from . import views
urlpatterns = [ url('^$',views.index, name= 'index'),
                url(r'^about/$', views.about,name = 'about'),
                url(r'^proc1/$',views.proc1,name='proc1'),
                url(r'^ajax_test/$', views.ajax_test, name='ajax_test'),
              ]