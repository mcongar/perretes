from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Ladrido(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ladridos')
    contenido = models.CharField(max_length=140)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']  # más reciente primero

    def __str__(self):
        return f'{self.autor.username}: {self.contenido[:30]}'

    @staticmethod
    def validar_contenido(contenido):
        if not contenido:
            raise ValidationError('El ladrido no puede estar vacío.')
        if len(contenido) > 140:
            raise ValidationError('El ladrido no puede superar los 140 caracteres.')