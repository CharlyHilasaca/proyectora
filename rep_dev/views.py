from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import *

def login(request):
    if request.session.get('dev_id'):
        return redirect('vistapl')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            dev = Dev.objects.get(username=username)
            if check_password(password, dev.password):
                request.session['dev_id'] = dev.id  # Guardar el ID en la sesión
                return redirect('vistapl')
            else:
                return render(request, 'rep_dev/login_rep_dev/login.html', {'error': 'Contraseña incorrecta'})
        except Dev.DoesNotExist:
            return render(request, 'rep_dev/login_rep_dev/login.html', {'error': 'Usuario no encontrado'})
    
    return render(request, 'rep_dev/login_rep_dev/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            hashed_password = make_password(password)
            default_role = Roles.objects.get(nombre='default_role')  # Asigna un rol por defecto
            default_access = Accesos.objects.get(ruta='rep_dev/vistapl.html')  # Asigna una vista por defecto
            
            dev = Dev(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=hashed_password,
                roles=default_role,
                vistapl=default_access
            )
            dev.save()
            
            return redirect('login')
        else:
            return render(request, 'rep_dev/register_rep_dev/register.html', {'error': 'Las contraseñas no coinciden'})
    return render(request, 'rep_dev/register_rep_dev/register.html')

@never_cache
def vistapl(request):
    dev_id = request.session.get('dev_id')
    
    if not dev_id:
        return redirect('login')
    
    # Obtener el usuario en sesión con sus relaciones
    dev = get_object_or_404(
        Dev.objects.prefetch_related(
            "roles__accesos", "vistapl", "opciones__opcion__descripcion"
        ),
        id=dev_id
    )
    
    # Filtrar opciones del usuario con su descripción
    opciones_usuario = Opcion.objects.filter(
        id__in=dev.opciones.values_list("opcion_id", flat=True)
    ).select_related("descripcion")  # Se trae la relación con Descripcion

    # Filtrar menús asociados a las opciones del usuario
    menus_usuario = Menu.objects.filter(opciones__in=opciones_usuario).distinct()
    
    return render(request, dev.vistapl.ruta, {
        'usersesion': dev,
        'nombresesion': dev.first_name,
        'apellidosesion': dev.last_name,
        'usernamesesion': dev.username,
        'emailsesion': dev.email,
        'rolessesion': dev.roles,
        'vistaplsesion': dev.vistapl,
        'roleslist': Roles.objects.prefetch_related("accesos"),
        'menus_usuario': menus_usuario,
        'opciones_usuario': opciones_usuario,
    })

def vistads(request, ruta):
    dev_id = request.session.get('dev_id')

    if not dev_id:
        return redirect('login')

    try:
        dev = Dev.objects.get(id=dev_id)
        accesos_permitidos = dev.roles.accesos.all()

        if accesos_permitidos.filter(ruta=ruta).exists():
            return render(request, ruta)
        else:
            return render(request, 'error.html', {'error': 'No tienes acceso a esta página.'})

    except Dev.DoesNotExist:
        return redirect('login')
    
def logout(request):
    request.session.flush()
    return redirect('login')

@never_cache
def vistads(request, ruta):
    dev_id = request.session.get('dev_id')

    if not dev_id:
        return redirect('login')

    try:
        dev = Dev.objects.get(id=dev_id)
        accesos_permitidos = dev.roles.accesos.all()

        if accesos_permitidos.filter(ruta=ruta).exists():
            response = render(request, ruta)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
        else:
            return render(request, 'error.html', {'error': 'No tienes acceso a esta página.'})

    except Dev.DoesNotExist:
        return redirect('login')

@never_cache
def logout(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

