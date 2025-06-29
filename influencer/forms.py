# influencer/forms.py

from django import forms
from .models import Influencer, WishItem, ShippingAddress
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='メールアドレス', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user




class InfluencerForm(forms.ModelForm):
    class Meta:
        model = Influencer
        fields = [
            'display_name',
            'bio',
            'profile_image',
            'instagram_url',
            'twitter_url',
            'tiktok_url',
            'free_url1',  # 追加
            'free_url2',
            'is_public',
        ]
        widgets = {
            'display_name': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': '表示名を入力'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-textarea mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'rows': 3,
                'placeholder': '自己紹介（任意）'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-input mt-1'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': 'https://www.instagram.com/...'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': 'https://twitter.com/...'
            }),
            'tiktok_url': forms.URLInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': 'https://www.tiktok.com/@...'
            }),

            'free_url1': forms.URLInput(attrs={
                            'class': 'form-input mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400',
                            'placeholder': 'フリーURL1（任意）'
            }),
                        'free_url2': forms.URLInput(attrs={
                            'class': 'form-input mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400',
                            'placeholder': 'フリーURL2（任意）'
            }),

            'is_public': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-400 border-gray-300 rounded'
            }),
        }


class WishItemForm(forms.ModelForm):
    class Meta:
        model = WishItem
        fields = [
            'product_name',
            'brand',
            'product_url',
            'image_url',
            'image_file',
            'desired_price',
            'order',
            'note',
            'is_visible',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': '例）HERMES バッグ'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': '例）HERMES'
            }),
            'product_url': forms.URLInput(attrs={
                'class': 'form-input block w-full pl-3 pr-10 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': 'https://...'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': '画像URL（任意）'
            }),
            'image_file': forms.ClearableFileInput(attrs={
                'class': 'hidden',  # テンプレートでカスタムボタンを当てる前提
            }),
            'desired_price': forms.NumberInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'placeholder': '例）80000'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-input mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'min': 0
            }),
            'note': forms.Textarea(attrs={
                'class': 'form-textarea mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none',
                'rows': 3,
                'placeholder': 'サイズや色など'
            }),
            'is_visible': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-400 border-gray-300 rounded'
            }),
        }



class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['recipient_name','postal_code','prefecture','city','building']
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class':'w-full border rounded p-2','placeholder':'宛名 (本名または任意)'}),
            'postal_code'   : forms.TextInput(attrs={'class':'w-full border rounded p-2','placeholder':'郵便番号'}),
            'prefecture'    : forms.TextInput(attrs={'class':'w-full border rounded p-2','placeholder':'都道府県'}),
            'city'          : forms.TextInput(attrs={'class':'w-full border rounded p-2','placeholder':'市区町村'}),
            'building'      : forms.TextInput(attrs={'class':'w-full border rounded p-2','placeholder':'建物名・部屋番号 (任意)'}),
        }