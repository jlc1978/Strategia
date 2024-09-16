from django import forms

class QuestionsForm(forms.Form):
    pass

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class LogoutForm(forms.Form):
    username = forms.CharField()

#class Log