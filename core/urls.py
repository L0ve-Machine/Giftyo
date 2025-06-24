from django.urls import path
from . import views  # ← ここを views_admin ではなく views にする
from influencer.models import Influencer

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('gifts/', views.admin_gift_list, name='admin_gift_list'),
    path('influencers/', views.admin_influencer_list, name='admin_influencer_list'),
]