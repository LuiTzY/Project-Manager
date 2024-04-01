
from . import views
from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView,TokenObtainPairView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['nombre'] = user.nombre
        token['email'] = user.email
        # ...

        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
urlpatterns = [
    path("api/users", views.register, name="users"),
    path("api/userss", views.getUsers, name="listar-usuarios"),
    path('api/token', MyTokenObtainPairView.as_view(), name="obtain-token"),
    path('api/token/refreshToken', TokenRefreshView.as_view(), name="obtain-refresh-token")
]
 