from django import forms

class loginForm(forms.ModelForm):
    class Meta:
        username = forms.CharField(max_length=200, label='Username')
        password = forms.CharField(widget=forms.PasswordInput, label= 'Password')


