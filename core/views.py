from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from .models import Ladrido

def home(request):
    if request.user.is_authenticated:
        return redirect('perfil', username=request.user.username)
    return render(request, 'core/home.html')

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('perfil', username=user.username)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'core/login.html')

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
        if contenido and len(contenido) <= 140:
            Ladrido.objects.create(autor=request.user, contenido=contenido)
            return redirect('perfil', username=username)

    return render(request, 'core/perfil.html', {
        'usuario': usuario,
        'ladridos': ladridos,
        'es_propietario': es_propietario,
    })

@login_required
def eliminar_ladrido(request, ladrido_id):
    ladrido = get_object_or_404(Ladrido, id=ladrido_id, autor=request.user)
    if request.method == 'POST':
        ladrido.delete()
    return redirect('perfil', username=request.user.username)

@login_required
def editar_ladrido(request, ladrido_id):
    ladrido = get_object_or_404(Ladrido, id=ladrido_id, autor=request.user)
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido and len(contenido) <= 140:
            ladrido.contenido = contenido
            ladrido.save()
    return redirect('perfil', username=request.user.username)