from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from friendrequests.views import FriendRequestViewSet
from .views import api_root

# Define the DefaultRouter and register the UserViewSet and FriendRequestViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'friendrequests', FriendRequestViewSet, basename='friend-requests')

# Friend request URLs
friend_request_urls = [
    path('send/', FriendRequestViewSet.as_view({'post': 'send_request'}), name='send_friend_request'),
    path('respond/', FriendRequestViewSet.as_view({'put': 'respond_request'}), name='respond_friend_request'),
    path('friends/', FriendRequestViewSet.as_view({'get': 'list_friends'}), name='list_friends'),
    path('pending/', FriendRequestViewSet.as_view({'get': 'list_pending_requests'}), name='list_pending_requests'),
]

# Combine the router URLs with friend request URLs
urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
    path('friend-requests/', include((friend_request_urls, 'friendrequests'), namespace='friendrequests')),
]
