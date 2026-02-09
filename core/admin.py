from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Paciente, Triaje, Atencion, RegistroAuditoria


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'nombre_completo', 'rol', 'activo', 'fecha_creacion')
    list_filter = ('rol', 'activo')
    search_fields = ('username', 'nombre_completo')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('nombre_completo', 'rol', 'activo', 'intentos_fallidos', 'bloqueado_hasta')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('nombre_completo', 'rol')
        }),
    )


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'ci', 'sexo', 'fecha_nacimiento', 'tipo_paciente', 'fecha_registro')
    list_filter = ('sexo', 'tipo_paciente')
    search_fields = ('nombre_completo', 'ci')
    date_hierarchy = 'fecha_registro'


@admin.register(Triaje)
class TriajeAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_hora_consulta', 'especialidad', 'nivel_prioridad', 'estado')
    list_filter = ('nivel_prioridad', 'estado', 'especialidad')
    search_fields = ('paciente__nombre_completo', 'paciente__ci')
    date_hierarchy = 'fecha_hora_consulta'
    raw_id_fields = ('paciente',)


@admin.register(Atencion)
class AtencionAdmin(admin.ModelAdmin):
    list_display = ('triaje', 'usuario', 'fecha_inicio', 'fecha_fin')
    list_filter = ('fecha_inicio',)
    search_fields = ('triaje__paciente__nombre_completo',)
    date_hierarchy = 'fecha_inicio'
    raw_id_fields = ('triaje', 'usuario')


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_hora', 'ip_address')
    list_filter = ('accion', 'fecha_hora')
    search_fields = ('usuario__username', 'descripcion')
    date_hierarchy = 'fecha_hora'
    readonly_fields = ('usuario', 'accion', 'descripcion', 'ip_address', 'fecha_hora')
