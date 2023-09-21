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

    # User
    path('get_user_list/', views.get_user_list, name="get_user_list"),
    path('signup/', views.signup, name="signup"),
    
    #Login / Register / Logout
    #Views
    path('', views.login_view, name="login_view"), 
    path('index/', views.login_view, name="login_index"), 
    path('forget_password/', views.forget_password, name="forget_password"), 

    #API's
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),

    #Dashboard
    #Views
    path('dashboard/', views.dashboard, name="dashboard"), 
    path('usage_count/', views.get_usage_count, name="get_usage_count"), 

    #Usage Log
    #Views
    path('Usage_Log/', views.usage_log_index, name="usage_log_view"), 
    #API's
    path('Usage_Log/show/', views.show_usage_log, name="show_usage_log"),



    # #User API
    # path('get_user_list/', views.get_user_list, name="get_user_list"),
    # path('update_user_status/', views.update_user_status, name="update_user_status"),
    # path('set_user_type/', views.set_user_type, name="set_user_type"),
    # path('approve_user/', views.approve_user, name="approve_user"),
    # path('edit_user/', views.edit_user, name="edit_user"),
    # path('delete_user/', views.delete_user, name="delete_user"),
    # path('change_user_password/', views.change_user_password, name="change_user_password"),
    
    # #Permission API
    # path('add_permission/', views.create_permission, name="add_permission"),
    # path('get_permission/', views.get_permission, name="get_permission"),
    # path('update_permission/', views.update_permission, name="update_permission"),
    # path('delete_permission/', views.delete_permission, name="delete_permission"),
    # path('get_permission_by_user_id/', views.get_permission_by_user_id, name="get_permission_by_user_id"),
    # path('get_permission_by_userType_id/', views.get_permission_by_userType_id, name="get_permission_by_userType_id"),


    # #Test API
    # path('test_email/', views.test_email, name="test_email"),
    # path('permissionTest/', views.permissionTest, name="permissionTest"),
    # ========================================================================================
] 
