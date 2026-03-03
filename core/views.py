from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import redirect_if_authenticated
from .forms import RegistroForm
from .models import Ladrido


def home(request):
    if request.user.is_authenticated:
        return redirect('perfil', username=request.user.username)
    return render(request, 'core/home.html')


@redirect_if_authenticated
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('perfil', username=user.username)
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})


@redirect_if_authenticated
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if not username or not password:
            messages.error(request, 'Por favor, introduce usuario y contraseña.')
            return render(request, 'core/login.html')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('perfil', username=user.username)
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'core/login.html')


@require_POST
def logout_view(request):
    auth.logout(request)
    return redirect('login')


def perfil(request, username):
    try:
        usuario = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'errors/perfil_404.html', {'username': username}, status=404)

    ladridos = usuario.ladridos.all()
    es_propietario = request.user == usuario

    if es_propietario and request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        try:
            Ladrido.validar_contenido(contenido)
            Ladrido.objects.create(autor=request.user, contenido=contenido)
            messages.success(request, '¡Ladrido publicado! 🐾')
            return redirect('perfil', username=username)
        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, 'core/perfil.html', {
        'usuario': usuario,
        'ladridos': ladridos,
        'es_propietario': es_propietario,
    })


@login_required
@require_POST
def eliminar_ladrido(request, ladrido_id):
    ladrido = get_object_or_404(Ladrido, id=ladrido_id, autor=request.user)
    ladrido.delete()
    return redirect('perfil', username=request.user.username)


@login_required
@require_POST
def editar_ladrido(request, ladrido_id):
    ladrido = get_object_or_404(Ladrido, id=ladrido_id, autor=request.user)
    contenido = request.POST.get('contenido', '').strip()
    try:
        Ladrido.validar_contenido(contenido)
        ladrido.contenido = contenido
        ladrido.save()
        messages.success(request, 'Ladrido actualizado.')
    except ValidationError as e:
        messages.error(request, e.message)
    return redirect('perfil', username=request.user.username)


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)