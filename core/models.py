from django.db import models
from django.contrib.auth.models import User

class Ladrido(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ladridos')
    contenido = models.CharField(max_length=140)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']  # más reciente primero

    def __str__(self):
        return f'{self.autor.username}: {self.contenido[:30]}'