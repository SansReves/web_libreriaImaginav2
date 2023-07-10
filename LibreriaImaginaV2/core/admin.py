from django.contrib import admin
from .models import CatgLibro,Cliente,Despacho,Empleado,Estado,Libro,OrdenCompra,OrdenDespacho,OrdenLibro,OrdenServicio,Servicio,TipoCliente,TipoEmpleado,TipoPago
# Register your models here.

# class ClienteAdmin(admin.ModelAdmin):
#     list_display = [""]

class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ["id_compra","fecha_or_compra","total_final_or","id_est","rut_cli"]
    list_filter = ["rut_cli","id_compra","id_est"]
    search_fields = ["rut_cli","id_compra"]

class OrdenDespachoAdmin(admin.ModelAdmin):
    list_display =["id_despc","id_compra","fecha_despc","direccion_despc","indicaciones_despc"]

class DespachoAdmin(admin.ModelAdmin):
    list_display = ["id_despc","nombre_despc","precio_despc"]

class OrdenLibroAdmin(admin.ModelAdmin):
    list_display = ["id_libro","id_compra","cant_libro","total_detalle_libro"]

class LibroAdmin(admin.ModelAdmin):
    list_display = ["nombre_libro","autor_libro","sinopsis_libro","imagen","precio_libro","stock_libro","id_catg"]
    list_editable = ["nombre_libro","autor_libro","sinopsis_libro","precio_libro","imagen","stock_libro"]
    search_fields = ["nombre_libro","autor_libro","id_catg"]
    list_filter = ["autor_libro","id_catg"]
    list_per_page = 10
    list_display_links = None

class CatgLibroAdmin(admin.ModelAdmin):
     list_display = ["id_catg","catg_libro"]

class OrdenServicioAdmin(admin.ModelAdmin):
    list_display = ["id_serv","id_compra","cant_serv","total_detalle_serv","fecha_serv","confirm_serv"]

class ServiciosAdmin(admin.ModelAdmin):
    list_display = ["id_serv","nombre_serv","dscrp_serv","precio_serv"]
    search_fields = ["nombre_serv"]

class TipoPagoAdmin(admin.ModelAdmin):
    list_display = ["id_tp_pago","nombre_tp_pago"]

admin.site.register(Libro,LibroAdmin)
admin.site.register(Cliente)
admin.site.register(CatgLibro,CatgLibroAdmin)
admin.site.register(Despacho,DespachoAdmin)
admin.site.register(Empleado)
admin.site.register(Estado)
admin.site.register(OrdenCompra,OrdenCompraAdmin)
admin.site.register(OrdenDespacho,OrdenDespachoAdmin)
admin.site.register(OrdenLibro,OrdenLibroAdmin)
admin.site.register(OrdenServicio,OrdenServicioAdmin)
admin.site.register(Servicio,ServiciosAdmin)
admin.site.register(TipoCliente)
admin.site.register(TipoEmpleado)
admin.site.register(TipoPago,TipoPagoAdmin)
