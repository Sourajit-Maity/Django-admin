from pickle import FALSE
from pyexpat import model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.db.models.base import Model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
import datetime
import uuid


DJANGO_MANAGE = True
LENGTH_SMALL = 25
LENGTH_BIG = 50
LENGTH_LARGE = 100
LENGTH_EX_LARGE = 255 

# Create your models here.

#Use this data type to store IST as UTC in Django
#Instead of added_on = models.DateTimeField(auto_now_add=True, blank=True)
from django.utils import timezone
import pytz
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        #Remove the 2 lines, if always to be updated
        if not add:
            return getattr(model_instance, self.attname)
        #print("AutoDateTimeField CALLED---------")
        IST = pytz.timezone('Asia/Kolkata')
        IST_tm = datetime.datetime.now(IST)
        ret_tm = IST_tm
        # ret_tm = IST_tm.replace(tzinfo=pytz.utc)  # Uncomment this to set time as UTC format
        #print(">>>>>>>>>>>>>>>>>>>>>DATETIME:"+str(datetime.datetime.now()))
        #print(">>>>>>>>>>>>>>>>>>>>>DATETIME-IST  :"+str(IST_tm))
        #print(">>>>>>>>>>>>>>>>>>>>>DATETIME-ret  :"+str(ret_tm))
        setattr(model_instance, self.attname, ret_tm)
        return ret_tm

#=========================================================================================

#=========================================================================================
class usage_log(models.Model):
    task_type = models.CharField(blank=True, null=True, default=None, max_length = LENGTH_SMALL, choices=[
                                ('0', 'PDF Extractor'), 
                                ('1', 'SIM Extractor'), 
                                ('2', 'Import Data'),
                            ],  verbose_name="Task Type")
    task_details = models.CharField(blank=False, null=True, max_length = LENGTH_EX_LARGE, unique=False, verbose_name="Task Details")
    file_name = models.CharField(blank=False, null=True, max_length = LENGTH_EX_LARGE, unique=False, verbose_name="File Name")
    used_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    used_on = AutoDateTimeField(editable=False)

    class Meta:
        managed = DJANGO_MANAGE
        db_table = 'usage_log'
        verbose_name="Usage Log"
        verbose_name_plural="Usage Log"
    def __str__(self):
        return str(self.id)

#=========================================================================================