from django.urls import path
from . import views
from .views import RegisterView


app_name = 'influencer'

urlpatterns = [
    path('profile/', views.influencer_profile_view,   name='profile'),
    path('dashboard/', views.influencer_dashboard_view, name='dashboard'),
    path('wish/add/', views.wishitem_create_view,      name='wish_add'),
    path('wish/<int:pk>/edit/', views.wishitem_edit_view,   name='wish_edit'),
    path('wish/<int:pk>/delete/', views.wishitem_delete_view, name='wish_delete'),
    path('gift/<int:pk>/mark-read/', views.gift_mark_read_view, name='gift_mark_read'),
    path('shipping-address/', views.shipping_address_view, name='shipping_address'),

    path('signup/', RegisterView.as_view(), name='signup'),
]

