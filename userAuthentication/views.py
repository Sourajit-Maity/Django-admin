# ======================================================================
# START import section
# ======================================================================
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import serializers
from pymysql import NULL
from django.conf import settings
from django.forms.models import model_to_dict
# from django.core.mail import send_mail
from django.template import Context, loader
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage  


# REST API interface with authentication
# ----------------------------------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_501_NOT_IMPLEMENTED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)


from userAuthentication.models import *


RET_STATUS = 'status'
RET_MSG = 'msg'
RET_DATA = 'data'

# ======================================================================
# User APIs
# ======================================================================
@api_view(["GET"])
def get_user_list(request):
    try:
        # if not Defaults.checkAPI_permission(request, functionName = "get_user_list"):
        #     return Response({RET_STATUS: False, RET_MSG: None, 'msg':"No permission"}, status=HTTP_400_BAD_REQUEST)

        try:
            data = User.objects.all().values('id', 'username', 'first_name', 'last_name')
        except:
            #Add error
            return Response({RET_STATUS: False, RET_MSG: 'Failed to get User list'},
                            status=HTTP_400_BAD_REQUEST)

        # --------------------------------------------------------

        return Response({
            RET_STATUS: True,
            RET_DATA: data,
        }, status=HTTP_200_OK)
    except Exception as e:
        Defaults.logger("User Exception: ", e, level="error")
        return Response({RET_STATUS: False, RET_MSG: str(e)}, status=HTTP_400_BAD_REQUEST)

# ======================================================================
# User - END
# ======================================================================

# ======================================================================
# Login/logout/Register APIs
# ======================================================================
def login_view(request):  
   template = loader.get_template('Authentication/sign-in.html') 
   return HttpResponse(template.render())

# ======================================================================

@api_view(["POST"])
@permission_classes((AllowAny,))
@csrf_exempt
def login(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")
        #Defaults.logger("login: entered", [email, password], level="info")
        if email is None or password is None:
            return Response({RET_STATUS: False, RET_MSG: 'Please provide both email and password'},
                            status=HTTP_400_BAD_REQUEST)


        user = authenticate(username=email, password=password)

        if not user:
            #Defaults.logger("Login failed", email, level="debug")
            return Response({RET_STATUS: False, RET_MSG: 'Invalid Credentials'}, status=HTTP_200_OK)
        
        # user_type = None
        # user_type_obj = {}
        # if not user.is_superuser:
        #     try:
        #         user_type_name = Profile.objects.get(user=user).UserType
        #         user_type = str(user_type_name)
        #         user_type_obj = model_to_dict(user_type_name)
        #         print(user_type_name)
        #         # user_type_object =  user_permission.objects.get(user_type=user_type_name)
                

        #         user_status = Profile.objects.get(user=user).user_status

        #         if user_status != '1':                    
        #             return Response({RET_STATUS: False, RET_MSG: 'Your account is not activated yet!'}, status=HTTP_200_OK)
        #     except Exception as e:
        #         print(e)
        #         return Response({RET_STATUS: False, RET_MSG: 'You are not authorised to log in'}, status=HTTP_200_OK)
        # else:
        #     user_type = 'Super Admin'   

        #Defaults.logger("Login", user.id, level="debug")
        

        token, _ = Token.objects.get_or_create(user=user)
        #Defaults.logger("Login success", str(token.key), level="debug")

        # --------------------------------------------------------

        return Response({
            RET_STATUS: True,
            RET_MSG: "Login success",
            'username': user.email.split('@')[0],
            # 'user_type': user_type,
            # 'user_type_obj': user_type_obj,
            'email': user.email,
            'token': token.key,
            # 'permission' : user_type_object,
        }, status=HTTP_200_OK)
    except Exception as e:
        #Defaults.logger("Login Exception:", e, level="error")
        return Response({RET_STATUS: False, RET_MSG: str(e)}, status=HTTP_400_BAD_REQUEST)

# ======================================================================

@api_view(["GET"])
def logout(request):
    """simply delete the token to force a login"""
    request.user.auth_token.delete()
    data = {
        RET_STATUS: True,
        RET_MSG: 'Successfully logged out'
    }
    return Response(data=data, status=HTTP_200_OK)
# ======================================================================

def forget_password(request):  
   template = loader.get_template('Authentication/password-reset.html') 
   return HttpResponse(template.render())


# ======================================================================
# Login/logout/Register - END
# ======================================================================

# ======================================================================
# Dashboard APIs
# ======================================================================
def dashboard(request):  
   template = loader.get_template('Dashboard/dashboard.html') 
   return HttpResponse(template.render())

# ======================================================================
# Dashboard - END
# ======================================================================

# ======================================================================
# Usage Log APIs
# ======================================================================
def usage_log_index(request):  
   template = loader.get_template('Usage_Log/index.html') 
   return HttpResponse(template.render())

# ======================================================================
@api_view(["POST"])
def show_usage_log(request):
    try:
        entered_info = get_entered_info(request)
        #Defaults.logger("show_usage_log: Entered", entered_info, level="info")

        filter_option = entered_info.get('filter_option')

        # Get Header
        fields = {
            'task_type': 'Task Type',
            'task_details': 'Task Details',
            'file_name': 'File Name',
            'used_by': 'Used by',
            'used_on': 'Used on'
        }

        start_date = entered_info.get('start_date')
        end_date = entered_info.get('end_date')
        date_category = 'used_on'

        date_filter = {}
        if (start_date != '') and (end_date != ''):
            start_date = datetime.datetime.strptime(entered_info.get('start_date'), '%d/%m/%Y')
            end_date = datetime.datetime.strptime(entered_info.get('end_date'), '%d/%m/%Y')
            end_date += datetime.timedelta(days=1)

            date_type = date_category + '__range'
            date_filter[date_type] = [start_date, end_date]

        elif (start_date != '') and (end_date == ''):
            start_date = datetime.datetime.strptime(entered_info.get('start_date'), '%d/%m/%Y')

            date_type = date_category + '__gte'
            date_filter[date_type] = start_date

        elif (start_date == '') and (end_date != ''):
            end_date = datetime.datetime.strptime(entered_info.get('end_date'), '%d/%m/%Y')

            date_type = date_category + '__lte'
            date_filter[date_type] = end_date

        data = usage_log.objects.filter(**filter_option, **date_filter).values('task_details', 'file_name', 'used_by__username', 'used_on')

        return Response({
            RET_STATUS: True,
            RET_DATA: data,
            'header': fields
        }, status=HTTP_200_OK)

    except Exception as e:
        #Defaults.logger("Show Usage Log Exception: ", e, level="error")
        return Response({RET_STATUS: False, RET_MSG: str(e)}, status=HTTP_400_BAD_REQUEST)

# ======================================================================

@api_view(["GET"])
def get_usage_count(request):
    try:
        entered_info = get_entered_info(request)
        #Defaults.logger("get_usage_count: Entered", entered_info, level="info")

        pdf_extractor_count = usage_log.objects.filter(used_by = request.user, task_type='0').count()
        sim_extractor_count = usage_log.objects.filter(used_by = request.user, task_type='1').count()
        import_data_count = usage_log.objects.filter(used_by = request.user, task_type='2').count()

        data = {
            'pdf_extactor': pdf_extractor_count,
            'sim_extactor': sim_extractor_count,
            'import_data': import_data_count
        }

        return Response({
            RET_STATUS: True,
            RET_DATA: data
        }, status=HTTP_200_OK)

    except Exception as e:
        #Defaults.logger("Show Usage Count Exception: ", e, level="error")
        return Response({RET_STATUS: False, RET_MSG: str(e)}, status=HTTP_400_BAD_REQUEST)

# ======================================================================
# Usage Log - END
# ======================================================================

