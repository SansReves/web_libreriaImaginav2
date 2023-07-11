# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import cx_Oracle
import uuid

class Cliente(models.Model):
    rut_cli = models.CharField(primary_key=True, max_length=9)
    nombre_cli = models.CharField(max_length=30)
    ap_paterno_cli = models.CharField(max_length=30, blank=True, null=True)
    correo_cli = models.CharField(max_length=50)
    telefono_cli = models.IntegerField()
    usuario_cli = models.CharField(max_length=30)
    contrasenia_cli = models.CharField(max_length=30)
    id_tp_cli = models.ForeignKey('TipoCliente', models.DO_NOTHING, db_column='id_tp_cli')

    class Meta:
        managed = False
        db_table = 'cliente'


class Despacho(models.Model):
    id_despc = models.AutoField(primary_key=True)
    nombre_despc = models.CharField(max_length=30)
    precio_despc = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'despacho'

class Empleado(models.Model):
    rut_emp = models.CharField(primary_key=True, max_length=9)
    nombre_emp = models.CharField(max_length=20)
    ap_paterno_emp = models.CharField(max_length=30)
    correo_emp = models.CharField(max_length=40)
    telefono_emp = models.IntegerField()
    usuario_emp = models.CharField(max_length=15)
    contrasenia_emp = models.CharField(max_length=20)
    id_tp_emp = models.ForeignKey('TipoEmpleado', models.DO_NOTHING, db_column='id_tp_emp')

    class Meta:
        managed = False
        db_table = 'empleado'


class Estado(models.Model):
    id_est = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'estado'

class CatgLibro(models.Model):
    id_catg = models.AutoField(primary_key=True)
    catg_libro = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'catg_libro'

class Libro(models.Model):
    id_libro = models.AutoField(primary_key=True)
    nombre_libro = models.CharField(max_length=40)
    autor_libro = models.CharField(max_length=40)
    sinopsis_libro = models.CharField(max_length=250, blank=True, null=True)
    precio_libro = models.IntegerField()
    stock_libro = models.IntegerField()
    imagen = models.ImageField(upload_to="libros", blank=True, null=True)
    id_catg = models.ForeignKey(CatgLibro, models.DO_NOTHING, db_column='id_catg')

    def get_imagen_url(self):
        if self.imagen and isinstance(self.imagen, cx_Oracle.LOB):
            raw_data = self.imagen.read()
            file_name = f"imagen_{uuid.uuid4().hex}.jpg"  # Generar un nombre de archivo único
            file = ContentFile(raw_data, name=file_name)
            return default_storage.url(file.name) if file.name else None
        else:
            return None
            
    class Meta:
        managed = False
        db_table = 'libro'


class OrdenCompra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha_or_compra = models.DateField()
    total_final_or = models.IntegerField(blank=True, null=True)
    rut_emp = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='rut_emp')
    id_est = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_est')
    id_tp_pago = models.ForeignKey('TipoPago', models.DO_NOTHING, db_column='id_tp_pago')
    rut_cli = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rut_cli')

    class Meta:
        managed = False
        db_table = 'orden_compra'


class OrdenDespacho(models.Model):
    fecha_despc = models.DateField()
    direccion_despc = models.CharField(max_length=100)
    indicaciones_despc = models.CharField(max_length=250, blank=True, null=True)
    id_despc = models.OneToOneField(Despacho, models.DO_NOTHING, db_column='id_despc', primary_key=True)
    id_compra = models.ForeignKey(OrdenCompra, models.DO_NOTHING, db_column='id_compra')

    class Meta:
        managed = False
        db_table = 'orden_despacho'
        unique_together = (('id_despc', 'id_compra'),)


class OrdenLibro(models.Model):
    total_detalle_libro = models.IntegerField()
    cant_libro = models.IntegerField()
    id_libro = models.OneToOneField(Libro, models.DO_NOTHING, db_column='id_libro', primary_key=True)
    id_compra = models.ForeignKey(OrdenCompra, models.DO_NOTHING, db_column='id_compra')

    class Meta:
        managed = False
        db_table = 'orden_libro'
        unique_together = (('id_libro', 'id_compra'),)


class OrdenServicio(models.Model):
    total_detalle_serv = models.IntegerField()
    cant_serv = models.IntegerField()
    fecha_serv = models.DateField(blank=True, null=True)
    detalle_serv = models.CharField(max_length=250, blank=True, null=True)
    confirm_serv = models.FloatField(blank=True, null=True)
    id_serv = models.OneToOneField('Servicio', models.DO_NOTHING, db_column='id_serv', primary_key=True)
    id_compra = models.ForeignKey(OrdenCompra, models.DO_NOTHING, db_column='id_compra')

    class Meta:
        managed = False
        db_table = 'orden_servicio'
        unique_together = (('id_serv', 'id_compra'),)


class Servicio(models.Model):
    id_serv = models.AutoField(primary_key=True)
    nombre_serv = models.CharField(max_length=50)
    dscrp_serv = models.CharField(max_length=250, blank=True, null=True)
    precio_serv = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'servicio'


class TipoCliente(models.Model):
    id_tp_cli = models.AutoField(primary_key=True)
    nombre_tp_cli = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipo_cliente'


class TipoEmpleado(models.Model):
    id_tp_emp = models.AutoField(primary_key=True)
    nombre_tp_emp = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tipo_empleado'


class TipoPago(models.Model):
    id_tp_pago = models.AutoField(primary_key=True)
    nombre_tp_pago = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipo_pago'

class AdminInterfaceTheme(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    active = models.BooleanField()
    title = models.CharField(max_length=50, blank=True, null=True)
    title_visible = models.BooleanField()
    logo = models.CharField(max_length=100, blank=True, null=True)
    logo_visible = models.BooleanField()
    css_header_background_color = models.CharField(max_length=10, blank=True, null=True)
    title_color = models.CharField(max_length=10, blank=True, null=True)
    css_header_text_color = models.CharField(max_length=10, blank=True, null=True)
    css_header_link_color = models.CharField(max_length=10, blank=True, null=True)
    css_header_link_hover_color = models.CharField(max_length=10, blank=True, null=True)
    css_module_background_color = models.CharField(max_length=10, blank=True, null=True)
    css_module_text_color = models.CharField(max_length=10, blank=True, null=True)
    css_module_link_color = models.CharField(max_length=10, blank=True, null=True)
    css_module_link_hover_color = models.CharField(max_length=10, blank=True, null=True)
    css_module_rounded_corners = models.BooleanField()
    css_generic_link_color = models.CharField(max_length=10, blank=True, null=True)
    css_generic_link_hover_color = models.CharField(max_length=10, blank=True, null=True)
    css_save_button_background5185 = models.CharField(max_length=10, blank=True, null=True)
    css_save_button_backgroundd677 = models.CharField(max_length=10, blank=True, null=True)
    css_save_button_text_color = models.CharField(max_length=10, blank=True, null=True)
    css_delete_button_backgroucea0 = models.CharField(max_length=10, blank=True, null=True)
    css_delete_button_backgrou6352 = models.CharField(max_length=10, blank=True, null=True)
    css_delete_button_text_color = models.CharField(max_length=10, blank=True, null=True)
    list_filter_dropdown = models.BooleanField()
    related_modal_active = models.BooleanField()
    related_modal_background_color = models.CharField(max_length=10, blank=True, null=True)
    related_modal_rounded_corners = models.BooleanField()
    logo_color = models.CharField(max_length=10, blank=True, null=True)
    recent_actions_visible = models.BooleanField()
    favicon = models.CharField(max_length=100, blank=True, null=True)
    related_modal_background_o7c6e = models.CharField(max_length=5, blank=True, null=True)
    env_name = models.CharField(max_length=50, blank=True, null=True)
    env_visible_in_header = models.BooleanField(blank=True, null=True)
    env_color = models.CharField(max_length=10, blank=True, null=True)
    env_visible_in_favicon = models.BooleanField()
    related_modal_close_button8203 = models.BooleanField()
    language_chooser_active = models.BooleanField()
    language_chooser_display = models.CharField(max_length=10, blank=True, null=True)
    list_filter_sticky = models.BooleanField()
    form_pagination_sticky = models.BooleanField()
    form_submit_sticky = models.BooleanField()
    css_module_background_selec21b = models.CharField(max_length=10, blank=True, null=True)
    css_module_link_selected_color = models.CharField(max_length=10, blank=True, null=True)
    logo_max_height = models.IntegerField()
    logo_max_width = models.IntegerField()
    foldable_apps = models.BooleanField()
    language_chooser_control = models.CharField(max_length=20, blank=True, null=True)
    list_filter_highlight = models.BooleanField()
    list_filter_removal_links = models.BooleanField()
    show_fieldsets_as_tabs = models.BooleanField()
    show_inlines_as_tabs = models.BooleanField()
    css_generic_link_active_color = models.CharField(max_length=10, blank=True, null=True)
    collapsible_stacked_inlines = models.BooleanField()
    collapsible_stacked_inlinea0a8 = models.BooleanField()
    collapsible_tabular_inlines = models.BooleanField()
    collapsible_tabular_inline8750 = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'admin_interface_theme'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

