from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Dev, Opcion, Menu, Roles

def login(request):
    if request.session.get('dev_id'):
        return redirect('vistapl')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        dev = Dev.objects.filter(username=username).first()

        if dev and check_password(password, dev.password):
            request.session['dev_id'] = dev.id  # Guardar el ID en la sesión
            return redirect('vistapl')

        return render(request, 'rep_dev/login_rep_dev/login.html', {
            'error': 'Usuario o contraseña incorrectos'
        })

    return render(request, 'rep_dev/login_rep_dev/login.html')

@never_cache
def vistapl(request):
    dev_id = request.session.get('dev_id')
    if not dev_id:
        return redirect('login')

    dev = get_object_or_404(
        Dev.objects.prefetch_related(
            "roles__accesos", "vistapl", "opciones__opcion__descripcion"
        ),
        id=dev_id
    )

    opciones_usuario = Opcion.objects.filter(
        id__in=dev.opciones.values_list("opcion_id", flat=True)
    ).select_related("descripcion")

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

@never_cache
def vistads(request, ruta):
    dev_id = request.session.get('dev_id')
    if not dev_id:
        return redirect('login')

    dev = get_object_or_404(Dev, id=dev_id)

    if dev.roles.accesos.filter(ruta=ruta).exists():
        response = render(request, ruta)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

    return render(request, 'error.html', {'error': 'No tienes acceso a esta página.'})

@never_cache
def logout(request):
    request.session.flush()
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
