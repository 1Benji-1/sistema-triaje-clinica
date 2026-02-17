"""
Core Models for Clinical Triage System
Modelos de base de datos siguiendo el SRS
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser): 
    """
    Extended User model with role-based access control
    Roles: Administrador, Farmacia, Enfermería, Doctor (los 3 últimos son Personal Común)
    """
    ROLES = [
        ('admin', 'Administrador'),
        ('farmacia', 'Farmacia'),
        ('enfermeria', 'Enfermería'),
        ('doctor', 'Doctor'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='enfermeria')
    nombre_completo = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado_hasta = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.nombre_completo} ({self.get_rol_display()})"


class Paciente(models.Model):
    """
    Patient master data
    """
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    TIPO_PACIENTE = [
        ('nuevo', 'Nuevo'),
        ('antiguo', 'Antiguo'),
    ]
    
    nombre_completo = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, unique=True, verbose_name='Cédula de Identidad')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    tipo_paciente = models.CharField(max_length=10, choices=TIPO_PACIENTE, default='nuevo')
    fecha_registro = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombre_completo} - CI: {self.ci}"
    
    @property
    def edad(self):
        today = timezone.now().date()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )


class Triaje(models.Model):
    """
    Triage evaluation record with vital signs and priority
    """
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    ESTADO_CHOICES = [
        ('en_espera', 'En Espera'),
        ('en_atencion', 'En Atención'),
        ('atendido', 'Atendido'),
    ]
    
    ESPECIALIDADES = [
        ('medicina_general', 'Medicina General'),
        ('pediatria', 'Pediatría'),
        ('ginecologia', 'Ginecología'),
        ('traumatologia', 'Traumatología'),
        ('cardiologia', 'Cardiología'),
        ('dermatologia', 'Dermatología'),
        ('neurologia', 'Neurología'),
        ('oftalmologia', 'Oftalmología'),
        ('otorrinolaringologia', 'Otorrinolaringología'),
        ('urologia', 'Urología'),
        ('psiquiatria', 'Psiquiatría'),
        ('emergencias', 'Emergencias'),
    ]
    
    TIPO_SERVICIO = [
        ('consulta_externa', 'Consulta Externa'),
        ('laboratorio', 'Laboratorio'),
        ('internacion', 'Internación'),
        ('cirugia', 'Cirugía'),
        ('emergencia', 'Emergencia'),
        ('farmacia', 'Farmacia'),
        ('otro', 'Otro'),
    ]
    
    # Relationships
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='triajes')
    
    # Consultation info
    fecha_hora_consulta = models.DateTimeField(default=timezone.now)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDADES)
    medico = models.CharField(max_length=100)
    enfermeria = models.CharField(max_length=100)
    tipo_servicio = models.CharField(max_length=20, choices=TIPO_SERVICIO, default='consulta_externa', verbose_name='Tipo de Servicio')
    
    # Vital signs
    talla = models.DecimalField(max_digits=5, decimal_places=2, help_text='Talla en cm')
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text='Peso en kg')
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, help_text='Temperatura en °C')
    presion_arterial = models.CharField(max_length=10, help_text='Formato: 120/80')
    pulsacion = models.IntegerField(help_text='Pulsaciones por minuto')
    
    # Priority and status
    nivel_prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_espera')
    
    # Diagnosis
    sintomatologia = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    estudios_complementarios = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Triaje'
        verbose_name_plural = 'Triajes'
        ordering = [
            models.Case(
                models.When(nivel_prioridad='alta', then=0),
                models.When(nivel_prioridad='media', then=1),
                models.When(nivel_prioridad='baja', then=2),
            ),
            'fecha_hora_consulta'
        ]
    
    def __str__(self):
        return f"Triaje {self.id} - {self.paciente.nombre_completo} ({self.get_nivel_prioridad_display()})"
    
    @property
    def prioridad_color(self):
        colors = {
            'alta': '#DC3545',
            'media': '#FFC107', 
            'baja': '#28A745'
        }
        return colors.get(self.nivel_prioridad, '#6C757D')
    
    @property
    def tiempo_espera(self):
        if self.estado == 'en_espera':
            delta = timezone.now() - self.fecha_hora_consulta
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours}h {minutes}m"
        return None


class Atencion(models.Model):
    """
    Care/Attention record for completed consultations
    """
    triaje = models.OneToOneField(Triaje, on_delete=models.CASCADE, related_name='atencion')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='atenciones')
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    medicamentos_dispensados = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Atención'
        verbose_name_plural = 'Atenciones'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"Atención {self.id} - {self.triaje.paciente.nombre_completo}"
    
    @property
    def duracion_atencion(self):
        if self.fecha_fin:
            delta = self.fecha_fin - self.fecha_inicio
            minutes = delta.seconds // 60
            return f"{minutes} minutos"
        return "En curso"


class RegistroAuditoria(models.Model):
    """
    Audit log for tracking user actions
    """
    ACCIONES = [
        ('login', 'Inicio de sesión'),
        ('logout', 'Cierre de sesión'),
        ('crear_paciente', 'Crear paciente'),
        ('crear_triaje', 'Crear triaje'),
        ('iniciar_atencion', 'Iniciar atención'),
        ('finalizar_atencion', 'Finalizar atención'),
        ('ver_historial', 'Ver historial'),
        ('generar_reporte', 'Generar reporte'),
        ('eliminar_paciente', 'Eliminar paciente'),
        ('crear_usuario', 'Crear usuario'),
        ('editar_usuario', 'Editar usuario'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=50, choices=ACCIONES)
    descripcion = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    fecha_hora = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.usuario} - {self.get_accion_display()} - {self.fecha_hora}"
