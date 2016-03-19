from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.chart_view, name='chart_view'),
    #url(r'^$',views.index, name='index'),
    url(r'^gchart/$',views.google_chart ,name='google_chart'),
]
