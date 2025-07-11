from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='ユーザー名またはメールアドレス',
        widget=forms.TextInput(attrs={
            'class': 'flex-1 px-3 py-2 text-black focus:outline-none',
            'placeholder': 'ユーザー名またはメールアドレスでログイン'
        })
    )
