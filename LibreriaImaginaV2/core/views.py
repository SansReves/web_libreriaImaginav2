from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib import messages
import re

from .forms import CustomUserCreationForm
from .models import Libro, Cliente,TipoCliente, Servicio, OrdenServicio,OrdenCompra, TipoPago

import cx_Oracle
from django.http import HttpResponse
from datetime import date,datetime

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
            response.set_cookie('cliente_rut', cliente.rut_cli)
            response.set_cookie('cliente_correo', cliente.correo_cli)
            response.set_cookie('cliente_telefono', str(cliente.telefono_cli))

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

        # Validar que el rut_cli tenga un largo admitido de 9 u 8 caracteres
        if len(rut_cli) not in [8, 9]:
            return render(request, 'registration/registrouser.html', {'error': 'El RUT debe tener 8 o 9 caracteres.'})
        
        if len(telefono_cli) not in [8, 9]:
            return render(request, 'registration/registrouser.html', {'error': 'Telefono incorrecto'})

        # Validar que el último carácter sea "K" o un dígito
        if not rut_cli[-1].isdigit() and rut_cli[-1] != 'K':
            return render(request, 'registration/registrouser.html', {'error': 'El último carácter debe ser "K" o un dígito.'})
        
        # Verificar si las contraseñas coinciden
        if contrasenia_cli != confirm_contrasenia_cli:
            return render(request, 'registration/registrouser.html', {'error': 'Las contraseñas no coinciden'})
        
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
    tipos_pagos = TipoPago.objects.all()
    tipos_servicios = Servicio.objects.all()

    if request.method == 'POST':
        cliente_rut = request.COOKIES.get('cliente_rut')
        fecha_actual = datetime.now().date()
        fecha_or_compra = date.today()
        total_final_or = request.POST.get('total_final_or')
        rut_emp = '12345678K' #se usa para las compras hechas por la pagina web
        id_est = 1 #estado en proceso
        id_tp_pago = 2
        rut_cli = cliente_rut

        conn = cx_Oracle.connect('bdLibreriav2/bdLibreriav2@127.0.0.1:1521/xe')
        
        try:
            # Crear un cursor
            cursor = conn.cursor()
            id_compra = cursor.var(cx_Oracle.NUMBER)
            cursor.callproc(
                'save_or_compra',
                [fecha_or_compra, total_final_or, rut_emp, id_est, id_tp_pago, rut_cli, id_compra]
            )

            id_compra_generado = id_compra.getvalue()
            precio_serv = 3000
            cant_serv = 1
            total_detalle_serv = precio_serv * cant_serv
            fecha_serv = request.POST.get('fecha_serv')
            if fecha_serv:
                fecha_serv = datetime.strptime(fecha_serv, '%Y-%m-%d').date()  # Convertir la fecha a objeto date

                if fecha_serv < fecha_actual:
                    return HttpResponse('La fecha de servicio no puede ser anterior a la fecha actual.')
                else:
                    return HttpResponse('La fecha de servicio es requerida.')
                
            detalle_serv = request.POST.get('detalle_serv')
            confirm_serv = None
            id_serv = 1

            cursor.callproc(
                'save_or_servicio',
                [total_detalle_serv, cant_serv, fecha_serv, detalle_serv, confirm_serv, id_serv, id_compra_generado]
            )
            conn.commit()
            cursor.close()
            conn.close()
            return HttpResponse('La orden de compra y la orden de servicio se han guardado exitosamente.')

        except cx_Oracle.Error as error:
            # Manejar cualquier error de Oracle
            print('Error de Oracle:', error)
            # Opcionalmente, puedes agregar un mensaje de error personalizado en la respuesta HTTP
            return HttpResponse('Ocurrió un error al guardar la orden de compra y la orden de servicio.')
    return render(request, 'formularios/contratar_serv.html', {'tipos_servicios': tipos_servicios, 'tipos_pagos': tipos_pagos})

def contratar_serv(request):
    tipos_servicios = Servicio.objects.all()
    tipos_pagos = TipoPago.objects.all()
    if request.method == 'POST':
        
        ##ORDEN COMPRA
        cliente_rut = request.COOKIES.get('cliente_rut')
        id_tp_pago = request.POST.get("cboPago")
        fecha_or_compra = date.today()
        total_final_or = 5000
        rut_emp = '12345678K'
        id_est = 1 #estado en proceso
        rut_cli = cliente_rut

        tipo_pago = TipoPago.objects.get(id_tp_pago=id_tp_pago)
        tipo_pago_id = tipo_pago.id_tp_pago

        tipo_servicio = Servicio.objects.get(id_serv=id_serv)
        tipo_servicio_id = tipo_servicio.id_serv

        # Establecer la conexión a la base de datos Oracle
        conn = cx_Oracle.connect('bdLibreriav2/bdLibreriav2@127.0.0.1:1521/xe')
        try:
            cursor = conn.cursor()
            id_compra = cursor.var(cx_Oracle.NUMBER)
            cursor.callproc(
                'save_or_compra',
                [fecha_or_compra, total_final_or, rut_emp, id_est, tipo_pago_id , rut_cli, id_compra]
            )
            id_compra_generado = id_compra.getvalue()
            
            cant_serv = 1
            total_detalle_serv = precio_serv * cant_serv
            fecha_serv = request.POST.get('fecha_serv')
            detalle_serv = request.POST.get('detalle_serv')
            confirm_serv = None
            id_serv = request.POST.get("cboServicio")
            precio_serv = tipo_servicio.precio_serv


            cursor.callproc(
                'save_or_servicio',
                [total_detalle_serv, cant_serv, fecha_serv, detalle_serv, confirm_serv, tipo_servicio_id, id_compra_generado]
            )
            conn.commit()
            cursor.close()
            conn.close()
            return render(request, 'core/home.html')
        except cx_Oracle.Error as error:
            # Manejar cualquier error de Oracle
            print('Error de Oracle:', error)
            # Opcionalmente, puedes agregar un mensaje de error personalizado en la respuesta HTTP
            return HttpResponse('Ocurrió un error al guardar la orden de compra y la orden de servicio.')
    
    return render(request, 'formularios/contratar_serv.html', {'tipos_servicios': tipos_servicios, 'tipos_pagos': tipos_pagos})



