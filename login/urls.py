from django.urls import path
from  . import  views
urlpatterns = [
    path('index/',views.index),
    path('register/',views.register),
    path('pegister_email_active/',views.register_email_active),
    path('register_check/',views.register_check),
    path('do_register/',views.do_register),
    path('login/',views.login),
    path('auth/',views.auth,name='auth'),
    path('do_login/',views.do_login),
    path('logout/',views.logout),
]