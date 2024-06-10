from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from django.utils import timezone
from datetime import timedelta
from django.db import IntegrityError
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.exceptions import NotFound, PermissionDenied,ValidationError
class FriendRequestViewSet(viewsets.ViewSet):

    def send_request(self, request):
    # Extract the username from the request data
        receiver_username = request.data.get('username')
        
        # Retrieve the receiver user
        receiver = User.objects.filter(username=receiver_username).first()
        if not receiver:
            raise ValidationError("Receiver user not found.")

        # Check if the users are already friends
        if FriendRequest.objects.filter(sender=request.user, receiver=receiver, accepted=True) or \
        FriendRequest.objects.filter(sender=receiver, receiver=request.user, accepted=True):
            raise ValidationError("You are already friends.")

        # Check if the sender and receiver are the same
        if request.user == receiver:
            raise ValidationError("You cannot send a friend request to yourself.")

        # Check rate limit: no more than 3 requests in the last minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(sender=request.user, timestamp__gte=one_minute_ago).count()
        if recent_requests_count >= 3:
            raise ValidationError("You have reached the limit of 3 friend requests per minute.")

        # Create and save the friend request
        friend_request = FriendRequest(sender=request.user, receiver=receiver)
        friend_request.save()

        return Response({'message': 'Friend request sent.'}, status=status.HTTP_201_CREATED)
    from rest_framework.exceptions import NotFound, PermissionDenied

    def respond_request(self, request):
    # Extract the username from the request data
        username = request.data.get('username')
        
        # Retrieve the friend request
        try:
            friend_request = FriendRequest.objects.get(receiver=request.user, sender__username=username, accepted=False)
        except FriendRequest.DoesNotExist:
            raise NotFound("Friend request not found.")

        # Check if the action is either "accept" or "reject"
        action = request.data.get('action')
        if action not in ['accept', 'reject']:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        # Handle the "accept" action
        if action == 'accept':
            # Check if the users are already friends
            if FriendRequest.objects.filter(sender=request.user, receiver=friend_request.sender, accepted=True) or \
            FriendRequest.objects.filter(sender=friend_request.sender, receiver=request.user, accepted=True):
                return Response({'error': 'You are already friends.'}, status=status.HTTP_400_BAD_REQUEST)

            # Mark the friend request as accepted
            friend_request.accepted = True
            friend_request.save()
            return Response({'message': 'Friend request accepted.'}, status=status.HTTP_200_OK)
        
    # Handle the "reject" action
        elif action == 'reject':
            friend_request.delete()
            return Response({'message': 'Friend request rejected.'}, status=status.HTTP_200_OK)

        
    def list_friends(self, request):
        user = request.user
        accepted_requests = FriendRequest.objects.filter(
            Q(sender=user, accepted=True) | Q(receiver=user, accepted=True)
        )
        friends = [fr.sender if fr.receiver == user else fr.receiver for fr in accepted_requests]
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list_pending_requests(self, request):
        user = request.user
        pending_requests = FriendRequest.objects.filter(receiver=user, accepted=False)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
