from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.models import User # STEP 1: Import the user
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, response, views


class UserLogoutAPI(views.APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return response.Response(
            status=status.HTTP_200_OK,
            data = {
                'message': 'You have been logged out',
            })

        else:
            return response.Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data = {
                'message': 'Please login first',
        })
