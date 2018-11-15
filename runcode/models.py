from django.db import models
from django.utils import timezone
import datetime

class UserInfo(models.Model):
    user_id = models.TextField(max_length = 20, blank="True")
    user_pwd = models.TextField(max_length = 20, blank="True")
    user_name = models.TextField(max_length = 20, blank="True")
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
    	return " id :"+self.user_id+" pwd: "+self.user_pwd+" name :"+self.user_name+" date :"+str(self.created_date)

class Login(models.Model):
    login_id = models.TextField(max_length = 20, blank="True")
    login_pwd = models.TextField(max_length = 20, blank="True")
    login_date = models.DateTimeField(auto_now = True)
    login_error = models.TextField(blank="True")
    def __str__(self):
    	return " id :"+self.login_id+" pwd: "+self.login_pwd+" error :"+self.login_error+" date :"+str(self.login_date)

'''
class LoginUser(models.Model)
    user_name = models.TextField(max_length = 20, blank="True")
    login_date = models.DateTimeField(auto_now = True)
    def __str__(self):
        return " name :"+self.user_name+" time: "+str(self.login_date)
        '''

class Run(models.Model):
    run_user = models.TextField(max_length = 20, blank="True")
    run_language = models.TextField(max_length = 20, blank="True")
    run_date = models.DateTimeField(auto_now = True)
    code = models.TextField(max_length = 2000, blank="True")
    def __str__(self):
        return " user :"+self.run_user+" language: "+self.run_language+" code :"+self.code+" date :"+str(self.run_date)

class Learning(models.Model):
    created_date = models.DateTimeField(auto_now_add = True)
    code_language = models.TextField(max_length = 30, blank="True")
    code = models.TextField(max_length = 2000, blank="True")
    context = models.TextField(max_length = 4000, blank="True")
    title = models.TextField(max_length = 20, blank="True")
    def __str__(self):
        return "id: "+str(self.id) + " code_language: "+self.code_language+" title :"+self.title

class Quiz(models.Model):
    code_language = models.TextField(max_length = 30, blank="True")
    context = models.TextField(max_length = 4000, blank="True")
    title = models.TextField(max_length = 20, blank="True")
    def __str__(self):
        return "id: "+str(self.id) + " code_language: "+self.code_language+" title :"+self.title