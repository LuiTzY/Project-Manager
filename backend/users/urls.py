
from . import views
from django.urls import path

urlpatterns = [
    path("api/users", views.register, name="users"),
    path("api/userss", views.getUsers, name="listar-usuarios")

]
 