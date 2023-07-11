from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib import messages
import re

from .forms import CustomUserCreationForm
from .models import Libro, Cliente,TipoCliente, Servicio, OrdenServicio

import cx_Oracle
from django.http import HttpResponse

def home(request):
    return render(request,'core/home.html')

def iniciosesion(request):
    if request.method == 'POST':
        usuario_cli = request.POST.get('usuario_cli')
        contrasenia_cli = request.POST.get('contrasenia_cli')

        # Buscar el cliente en la base de datos
        try:
            cliente = Cliente.objects.get(usuario_cli=usuario_cli, contrasenia_cli=contrasenia_cli)
            # Inicio de sesión exitoso
            # Almacena el nombre del cliente en una cookie
            response = redirect('home')
            response.set_cookie('cliente_nombre', cliente.nombre_cli)
            return response
        except Cliente.DoesNotExist:
            # Usuario o contraseña incorrectos
            messages.error(request, 'Credenciales inválidas')

    return render(request, 'registration/iniciosesion.html')


def cerrarsesion(request):
    response = redirect('iniciosesion')
    response.delete_cookie('cliente_nombre')
    return response


def catalogo(request):
    libros = Libro.objects.all()
    data = {
        'libros' : libros
    }
    return render(request,'core/catalogo.html',data)

def servicios(request):
    servicios = Servicio.objects.all()
    data = {
        'servicios' : servicios
    }
    return render(request,'core/servicios.html',data)

def quienessomos(request):
    return render(request,'core/quienessomos.html')

def seguimiento(request):
    return render(request,'core/seguimiento.html')

def registrouser(request):
    if request.method == 'POST':
        rut_cli = request.POST.get('rut_cli')
        nombre_cli = request.POST.get('nombre_cli')
        ap_paterno_cli = request.POST.get('ap_paterno_cli')
        correo_cli = request.POST.get('correo_cli')
        telefono_cli = request.POST.get('telefono_cli')
        usuario_cli = request.POST.get('usuario_cli')
        contrasenia_cli = request.POST.get('contrasenia_cli')
        confirm_contrasenia_cli = request.POST.get('confirm_contrasenia_cli')
        id_tp_cli = 2

        # Eliminar guiones y puntos del rut_cli
        rut_cli = re.sub(r'[-\.]', '', rut_cli)

        # Verificar si las contraseñas coinciden
        if contrasenia_cli != confirm_contrasenia_cli:
            return render(request, 'registration/registrouser.html', {'error': 'Las contraseñas no coinciden'})
        # Validar que el rut_cli tenga un largo admitido de 9 u 8 caracteres
        if len(rut_cli) not in [8, 9]:
            return render(request, 'registration/registrouser.html', {'error': 'El RUT debe tener 8 o 9 caracteres.'})
        
        if len(telefono_cli) not in [8, 9]:
            return render(request, 'registration/registrouser.html', {'error': 'Telefono incorrecto'})

        # Validar que el último carácter sea "K" o un dígito
        if not rut_cli[-1].isdigit() and rut_cli[-1] != 'K':
            return render(request, 'registration/registrouser.html', {'error': 'El último carácter debe ser "K" o un dígito.'})
        # Obtener la instancia de TipoCliente correspondiente al id_tp_cli
        tipo_cliente = TipoCliente.objects.get(id_tp_cli=id_tp_cli)

        # Crear un nuevo objeto Cliente
        cliente = Cliente(
            rut_cli=rut_cli,
            nombre_cli=nombre_cli,
            ap_paterno_cli=ap_paterno_cli,
            correo_cli=correo_cli,
            telefono_cli=telefono_cli,
            usuario_cli=usuario_cli,
            contrasenia_cli=contrasenia_cli,
            id_tp_cli=tipo_cliente  # Asignar la instancia de TipoCliente
        )
        cliente.save()

        # Redirigir a una página de registro exitoso
        return render(request, 'core/home.html')

    tipos_clientes = TipoCliente.objects.all()
    return render(request, 'registration/registrouser.html', {'tipos_clientes': tipos_clientes})

def form_servicio(request):
    #Combo box
    list_serv = Servicio.objects.all

    #Solicitud de Servicio
    if request.method == 'POST':
        orp = OrdenServicio()
        
        orp.id_serv = request.POST.get("")
        orp.fecha_serv = request.POST.get("fecha")
        orp.cant_serv = 1
        orp.total_detalle_serv = request.POST.get("")
        orp.detalle_serv = request.POST.get("detalle")

        serv = Servicio.objects.all()
        serv.id_serv = request.POST.get("cboServicio")
        orp.id_serv = serv

        try:
            orp.save()
            mensaje = "Guardado correctamente"
            messages.success(request, mensaje)
        except:
            mensaje = "Error al Enviar"
            messages.error(request, mensaje)
    return render(request,'formularios/form_servicio.html')