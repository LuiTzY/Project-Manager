from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import User
import sys
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

@api_view (["POST"])
def register(request):
    
    #Primer paso serializar los datos que me llegan en la soliciutd
    serializer = UserSerializer(data=request.data)
    
    #Si es valido guardo mi usuario
    if serializer.is_valid():
        user = serializer.save()
        token = RefreshToken.for_user(user)
        return Response({"user":serializer.data, "token":str(token) }, status=status.HTTP_201_CREATED)
    
    return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def getUsers(request):
    usuarios = User.objects.all()
    serializer = UserSerializer(usuarios, many=True)

    print("Usuarios obtenidos {}, {}".format(usuarios, serializer))
    sys.stdout.flush()
    return Response({"usuarios":serializer.data},status=status.HTTP_200_OK)