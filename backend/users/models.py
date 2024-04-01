from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Esta clase es para manejar mi modelo de usuario propio que he creado
#El manager es el que me permitira hacer las consultas a mi base de datos, como creacion,eliminar etc, si no lo especifico django el que me proporciona es el de objects para todos los modelos
class UsuarioManager(BaseUserManager):
    
    def create_user(self,email,nombre,apellidos,password = None):
        if not email:
            raise ValueError("El usuario debe de tener un correo electronico")
        #Cuando hago referencia a self.model la hago a mi clase User que creo yo
        usuario = self.model(
            email = self.normalize_email(email),
            nombre = nombre,
            apellidos = apellidos
        )
        #No es necesario colocarlo en la instancia ya que el meto set_password lo hara
        #ademas de encriptar la password que le pase
        usuario.set_password(password)
        #se guarda el usuario que se creo
        usuario.save()
        return usuario
    
    def create_superuser(self,email,nombre,apellidos,password):
        #Cuando hago referencia a self.model la hago a mi clase User que creo yo
        usuario = self.create_user(
            email = email,
            nombre = nombre,
            apellidos = apellidos,
            password=password
        )
        usuario.usuario_administrador = True
        usuario.save()
        return usuario
    
    
class User(AbstractBaseUser):
    nombre = models.CharField(max_length = 50, verbose_name="Nombre")
    apellidos = models.CharField(max_length = 50, verbose_name = "Apellidos", blank= True, null = True)
    email = models.EmailField(max_length=60, unique=True , verbose_name="Correo Electronico")
    image = models.ImageField(verbose_name="Imagen del usuario", upload_to="profile/", blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    
    created_at = models.DateField(auto_now_add = True, verbose_name = "Creado el")
    update_at = models.DateField(auto_now=True, verbose_name = "Actualizado el")
    objects = UsuarioManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('nombre','apellidos')
    
    def __str__(self):
        return f"{self.email} + {self.nombre}"
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador
    
class Rol(models.Model):
    #Especificamos el nombre del rol
    nombre = models.CharField(max_length=30)
    
class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length = 40, verbose_name = "Nombre Proyecto")
    descripcion = models.TextField(verbose_name="Descripcion del proyecto")
    objetivo_proyecto = models.TextField(verbose_name="Objetivo del proyecto")
    project_owner = models.ForeignKey(User, verbose_name = "Usuario", on_delete = models.CASCADE)
    miembros = models.ManyToManyField(User, related_name="proyectos")
    roles = models.ManyToManyField(Rol, related_name="proyectos")
    created_at = models.DateField(auto_now_add=True, verbose_name="Creado el ")

class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    #Esto es una relacion de que esta tarea esta relacionada a un proyecto en si
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    #La tarea es asginada a un usuario especifico, el related name hace que desde el modelo con el que se relacione
    #pueda acceder a ese campo con el related_name que le coloco, es una relacion inversa
    asignado_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas_asignadas')
    
    def save(self, *args, **kwargs):
        if self.asignado_a not in self.proyecto.miembros.all():
            raise ValueError("El usuario no pertenece al proyecto")
        super().save(*args,**kwargs)

class Miembro(models.Model):
    #Un miembro va a pertenecer a un usuario
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    #Un miembro va a pertenecer a un proyecto
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)