from django.db import models
from django.utils import timezone
import datetime

class UserData(models.Model):
    user_name = models.TextField(max_length = 20, blank="True")
    visit_lank = models.IntegerField(blank="True", default=1)
    study_lank = models.TextField(max_length = 1000, blank="True", default="1_1_1_1_1_1")
    coding_lank = models.TextField(max_length = 1000, blank="True", default="1_1_1_1_1_1")
    def __str__(self):
        return " name :"+self.user_name+" how many visit? :"+str(self.visit_lank)

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
class LoginUser(models.Model):
    user_ip = models.TextField(max_length=100, blank="True")
    login_now = models.IntegerField(blank="True")
    login_date = models.DateTimeField(blank="True", auto_now = True)
    last_id = models.TextField(max_length = 20, blank="True")
    last_pwd = models.TextField(max_length = 20, blank="True")
    def __str__(self):
        return " ip :"+self.user_ip+" time: "+str(self.login_date)
'''

class UserLogin(models.Model):
    user_ip = models.TextField(max_length=100)
    login_now = models.BooleanField(default = True)
    login_date = models.DateTimeField(blank="True", auto_now = True)
    last_id = models.TextField(max_length = 20, blank="True")
    last_pwd = models.TextField(max_length = 20, blank="True")
    def __str__(self):
        return " ip :"+self.user_ip+" time: "+str(self.login_date)

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