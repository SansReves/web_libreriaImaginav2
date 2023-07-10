from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Libro, Cliente, Servicio, OrdenServicio

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

def home(request):
    return render(request,'core/home.html')

def seguimiento(request):
    return render(request,'core/seguimiento.html')

def registrouser(request):
    return render(request,'registration/registrouser.html')

def form_servicio(request):
    #Combo box
    list_serv = Servicio.objects.all
    data = {"Servicio" : list_serv}

    #Solicitud de Servicio
    if request.method == 'POST':
        orp = OrdenServicio()
        
        orp.id_serv = request.POST.get("")
        orp.fecha_serv = request.POST.get("fecha")
        orp.cant_serv = 1
        orp.total_detalle_serv = request.POST.get("")
        orp.detalle_serv = request.POST.get("detalle")

        serv = Servicio()
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