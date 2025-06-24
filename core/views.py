# core/views.py

from django.shortcuts import render
from influencer.models import Gift
from influencer.models import Influencer


def admin_dashboard(request):
    total_gifts = Gift.objects.count()
    active_influencers = Influencer.objects.filter(is_public=True).count()
    gifts_with_product = Gift.objects.exclude(wish_item__isnull=True).count()
    influencer_count = Influencer.objects.count()
    average_gift_per_influencer = total_gifts // influencer_count if influencer_count > 0 else 0

    return render(request, 'manage/dashboard.html', {
        'total_gifts': total_gifts,
        'active_influencers': active_influencers,
        'gifts_with_product': gifts_with_product,
        'average_gift_per_influencer': average_gift_per_influencer,
    })

def admin_gift_list(request):
    gifts = Gift.objects.select_related('to_profile', 'wish_item').all()
    return render(request, 'manage/gift_list.html', {'gifts': gifts})

def admin_influencer_list(request):
    influencers = Influencer.objects.all().prefetch_related('received_gifts')
    return render(request, 'manage/influencer_list.html', {'influencers': influencers})
