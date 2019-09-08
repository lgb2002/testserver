from __future__ import unicode_literals
from django import forms
from .models import Login

class LoginForm(forms.Form):

	class Meta:
		model = Login
		fields = ('user_id', 'user_pwd', 'login_error')