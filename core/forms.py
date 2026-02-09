"""
Django Forms for Clinical Triage System
Formularios para registro de pacientes y triaje
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Paciente, Triaje, Atencion, Usuario


class LoginForm(AuthenticationForm):
    """Custom login form with styled widgets"""
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingrese su usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password'
        })
    )


class PacienteForm(forms.ModelForm):
    """Form for patient registration - Step 1: General Data"""
    class Meta:
        model = Paciente
        fields = ['nombre_completo', 'ci', 'sexo', 'fecha_nacimiento', 'tipo_paciente']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nombre completo del paciente',
                'minlength': 3
            }),
            'ci': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Cédula de identidad'
            }),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'tipo_paciente': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre_completo': 'Nombre Completo *',
            'ci': 'Cédula de Identidad *',
            'sexo': 'Sexo *',
            'fecha_nacimiento': 'Fecha de Nacimiento *',
            'tipo_paciente': 'Tipo de Paciente *',
        }


class TriajeAntecedentesForm(forms.Form):
    """Form for triage - Step 2: Medical History/Assignment"""
    especialidad = forms.ChoiceField(
        choices=Triaje.ESPECIALIDADES,
        label='Especialidad *',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    medico = forms.CharField(
        label='Médico Asignado *',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nombre del médico'
        })
    )
    enfermeria = forms.CharField(
        label='Enfermería *',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nombre del personal de enfermería'
        })
    )


class TriajeSignosVitalesForm(forms.Form):
    """Form for triage - Step 3: Vital Signs"""
    talla = forms.DecimalField(
        label='Talla (cm) *',
        min_value=40, max_value=250,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: 170',
            'step': '0.1'
        })
    )
    peso = forms.DecimalField(
        label='Peso (kg) *',
        min_value=1, max_value=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: 70',
            'step': '0.1'
        })
    )
    temperatura = forms.DecimalField(
        label='Temperatura (°C) *',
        min_value=32, max_value=43,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: 36.5',
            'step': '0.1'
        })
    )
    presion_arterial = forms.CharField(
        label='Presión Arterial (mmHg) *',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: 120/80',
            'pattern': r'\d{2,3}/\d{2,3}'
        })
    )
    pulsacion = forms.IntegerField(
        label='Pulsación (ppm) *',
        min_value=40, max_value=200,
        widget=forms.NumberInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ej: 72'
        })
    )
    nivel_prioridad = forms.ChoiceField(
        choices=Triaje.PRIORIDAD_CHOICES,
        label='Nivel de Prioridad *',
        widget=forms.RadioSelect(attrs={'class': 'priority-radio'})
    )


class TriajeDiagnosticoForm(forms.Form):
    """Form for triage - Step 4: Diagnosis"""
    sintomatologia = forms.CharField(
        label='Sintomatología',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Describa los síntomas del paciente...',
            'rows': 4
        })
    )
    tratamiento = forms.CharField(
        label='Tratamiento e Indicaciones',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Indicaciones médicas y prescripciones...',
            'rows': 4
        })
    )
    estudios_complementarios = forms.CharField(
        label='Estudios Complementarios',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Solicitud de análisis, imágenes, etc...',
            'rows': 4
        })
    )


class AtencionForm(forms.ModelForm):
    """Form for completing patient attention"""
    class Meta:
        model = Atencion
        fields = ['observaciones', 'medicamentos_dispensados']
        widgets = {
            'observaciones': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Observaciones adicionales durante la atención...',
                'rows': 4
            }),
            'medicamentos_dispensados': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Lista de medicamentos dispensados (nombre, dosis, cantidad)...',
                'rows': 4
            }),
        }


class BusquedaPacienteForm(forms.Form):
    """Form for patient search in history module"""
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input search-input',
            'placeholder': 'Buscar por nombre o CI...'
        })
    )
    estado = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos'), ('atendido', 'Atendido'), ('en_espera', 'No atendido')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date'
        })
    )
