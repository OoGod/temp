from django.conf.urls import url
import views

urlpatterns=[
    url(r'^index/$', views.index),
    url(r'^deal_com/$', views.deal_com),
    url(r'^(\d+)/$', views.detail)
]