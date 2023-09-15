#URLs in userAuthentication
from django.urls import path
#For authorization URLs
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings

#for custom urls
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # ========================================================================================
    # PDF Extractor userAuthentication custom URLs
    # ========================================================================================
    # for test only
    #path('testReq/', views.testReq, name="testReq"),
    # ========================================================================================

    
    # ========================================================================================
] 
