from django.urls import path, include, reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.sites.models import Site

@api_view(['GET'])
def api_root(request, format=None):
    current_site = Site.objects.get_current().domain
    if current_site=='example.com':
        current_site = '127.0.0.1:8000'  

    return Response({
        'users': f"http://{current_site}{reverse('users-list')}",
        'send_friend_request': f"http://{current_site}{reverse('friendrequests:send_friend_request')}",  
        'list_pending_requests': f"http://{current_site}{reverse('friendrequests:list_pending_requests')}",
        'respond_friend_request': f"http://{current_site}{reverse('friendrequests:respond_friend_request')}",  
        'list_friends': f"http://{current_site}{reverse('friendrequests:list_friends')}",
        'search_users': f"http://{current_site}{reverse('user-search')}",
        
    })
