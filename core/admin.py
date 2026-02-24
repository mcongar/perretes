from django.contrib import admin
from .models import Ladrido

@admin.register(Ladrido)
class LadridoAdmin(admin.ModelAdmin):
    list_display = ('autor', 'contenido', 'fecha')
    list_filter = ('autor',)
    search_fields = ('autor__username', 'contenido')
    ordering = ('-fecha',)