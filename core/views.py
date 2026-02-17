"""
Views for Clinical Triage System
Vistas para todos los módulos del sistema
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count, Q, Avg
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
import json

from .models import Usuario, Paciente, Triaje, Atencion, RegistroAuditoria
from .forms import (
    LoginForm, PacienteForm, TriajeAntecedentesForm, 
    TriajeSignosVitalesForm, TriajeDiagnosticoForm, 
    AtencionForm, BusquedaPacienteForm
)
from .decorators import role_required, registrar_auditoria


# ============================================================
# RF-01: Authentication Module
# ============================================================

def login_view(request):
    """Handle user login with attempt limiting"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        username = request.POST.get('username', '')
        
        try:
            user = Usuario.objects.get(username=username)
            
            # Check if account is locked
            if user.bloqueado_hasta and user.bloqueado_hasta > timezone.now():
                messages.error(request, 'Cuenta bloqueada temporalmente. Intente más tarde.')
                return render(request, 'login.html', {'form': form})
            
            if form.is_valid():
                # Reset failed attempts on successful login
                user.intentos_fallidos = 0
                user.bloqueado_hasta = None
                user.save()
                
                login(request, user)
                registrar_auditoria(request, user, 'login', 'Inicio de sesión exitoso')
                return redirect('dashboard')
            else:
                # Increment failed attempts
                user.intentos_fallidos += 1
                if user.intentos_fallidos >= 3:
                    user.bloqueado_hasta = timezone.now() + timedelta(minutes=15)
                    messages.error(request, 'Cuenta bloqueada por 15 minutos debido a múltiples intentos fallidos.')
                else:
                    remaining = 3 - user.intentos_fallidos
                    messages.error(request, f'Credenciales inválidas. Intentos restantes: {remaining}')
                user.save()
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no existe.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """Handle user logout"""
    registrar_auditoria(request, request.user, 'logout', 'Cierre de sesión')
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('login')


# ============================================================
# RF-02: Dashboard / Triage Queue Module
# ============================================================

@login_required
def dashboard_view(request):
    """Main dashboard with triage queue and statistics"""
    # Get patients in queue ordered by priority
    triajes_en_espera = Triaje.objects.filter(
        estado='en_espera'
    ).select_related('paciente').order_by(
        # Custom ordering: alta=0, media=1, baja=2
        'nivel_prioridad',
        'fecha_hora_consulta'
    )
    
    # Reorder by priority properly
    priority_order = {'alta': 0, 'media': 1, 'baja': 2}
    triajes_en_espera = sorted(triajes_en_espera, key=lambda x: (priority_order.get(x.nivel_prioridad, 3), x.fecha_hora_consulta))
    
    # Statistics
    hoy = timezone.now().date()
    
    # For non-admin users, show only their own attended patients
    if request.user.rol == 'admin':
        atendidos_hoy = Atencion.objects.filter(fecha_fin__date=hoy).count()
    else:
        atendidos_hoy = Atencion.objects.filter(
            fecha_fin__date=hoy,
            usuario=request.user
        ).count()
    
    stats = {
        'total_espera': len(triajes_en_espera),
        'prioridad_alta': sum(1 for t in triajes_en_espera if t.nivel_prioridad == 'alta'),
        'prioridad_media': sum(1 for t in triajes_en_espera if t.nivel_prioridad == 'media'),
        'prioridad_baja': sum(1 for t in triajes_en_espera if t.nivel_prioridad == 'baja'),
        'atendidos_hoy': atendidos_hoy,
        'total_pacientes': Paciente.objects.count(),
    }
    
    # En atención actualmente
    en_atencion = Triaje.objects.filter(estado='en_atencion').select_related('paciente')
    
    context = {
        'triajes': triajes_en_espera,
        'en_atencion': en_atencion,
        'stats': stats,
        'page_title': 'Panel Principal - Triaje'
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def api_queue_update(request):
    """API endpoint for real-time queue updates"""
    triajes = Triaje.objects.filter(estado='en_espera').select_related('paciente')
    priority_order = {'alta': 0, 'media': 1, 'baja': 2}
    triajes = sorted(triajes, key=lambda x: (priority_order.get(x.nivel_prioridad, 3), x.fecha_hora_consulta))
    
    data = [{
        'id': t.id,
        'paciente': t.paciente.nombre_completo,
        'ci': t.paciente.ci,
        'prioridad': t.nivel_prioridad,
        'prioridad_display': t.get_nivel_prioridad_display(),
        'prioridad_color': t.prioridad_color,
        'hora_ingreso': t.fecha_hora_consulta.strftime('%H:%M'),
        'tiempo_espera': t.tiempo_espera,
        'especialidad': t.get_especialidad_display(),
    } for t in triajes]
    
    return JsonResponse({'triajes': data, 'total': len(data)})


# ============================================================
# RF-03: Patient Registration Module
# ============================================================

@login_required
@role_required(['admin', 'farmacia', 'enfermeria', 'doctor'])
def registrar_paciente_view(request):
    """Multi-step patient registration form"""
    # Initialize session data if needed
    if 'registro_paciente' not in request.session:
        request.session['registro_paciente'] = {}
    
    step = int(request.GET.get('step', 1))
    session_data = request.session.get('registro_paciente', {})
    
    if request.method == 'POST':
        if step == 1:
            form = PacienteForm(request.POST)
            if form.is_valid():
                session_data['paciente'] = form.cleaned_data
                session_data['paciente']['fecha_nacimiento'] = str(form.cleaned_data['fecha_nacimiento'])
                request.session['registro_paciente'] = session_data
                return HttpResponseRedirect(reverse('registrar_paciente') + '?step=2')
        
        elif step == 2:
            form = TriajeAntecedentesForm(request.POST)
            if form.is_valid():
                session_data['antecedentes'] = form.cleaned_data
                request.session['registro_paciente'] = session_data
                return HttpResponseRedirect(reverse('registrar_paciente') + '?step=3')
        
        elif step == 3:
            form = TriajeSignosVitalesForm(request.POST)
            if form.is_valid():
                session_data['signos_vitales'] = form.cleaned_data
                session_data['signos_vitales']['talla'] = str(form.cleaned_data['talla'])
                session_data['signos_vitales']['peso'] = str(form.cleaned_data['peso'])
                session_data['signos_vitales']['temperatura'] = str(form.cleaned_data['temperatura'])
                request.session['registro_paciente'] = session_data
                return HttpResponseRedirect(reverse('registrar_paciente') + '?step=4')
        
        elif step == 4:
            form = TriajeDiagnosticoForm(request.POST)
            if form.is_valid():
                session_data['diagnostico'] = form.cleaned_data
                
                # Create patient and triage records
                try:
                    # Create or get patient
                    paciente_data = session_data['paciente']
                    from datetime import datetime
                    paciente_data['fecha_nacimiento'] = datetime.strptime(
                        paciente_data['fecha_nacimiento'], '%Y-%m-%d'
                    ).date()
                    
                    paciente, created = Paciente.objects.get_or_create(
                        ci=paciente_data['ci'],
                        defaults=paciente_data
                    )
                    
                    if not created:
                        # Update existing patient type
                        paciente.tipo_paciente = 'antiguo'
                        paciente.save()
                    
                    # Create triage record
                    triaje = Triaje.objects.create(
                        paciente=paciente,
                        especialidad=session_data['antecedentes']['especialidad'],
                        medico=session_data['antecedentes']['medico'],
                        enfermeria=session_data['antecedentes']['enfermeria'],
                        tipo_servicio=session_data['antecedentes']['tipo_servicio'],
                        talla=session_data['signos_vitales']['talla'],
                        peso=session_data['signos_vitales']['peso'],
                        temperatura=session_data['signos_vitales']['temperatura'],
                        presion_arterial=session_data['signos_vitales']['presion_arterial'],
                        pulsacion=session_data['signos_vitales']['pulsacion'],
                        nivel_prioridad=session_data['signos_vitales']['nivel_prioridad'],
                        sintomatologia=form.cleaned_data.get('sintomatologia'),
                        tratamiento=form.cleaned_data.get('tratamiento'),
                        estudios_complementarios=form.cleaned_data.get('estudios_complementarios'),
                    )
                    
                    # Clear session data
                    del request.session['registro_paciente']
                    
                    registrar_auditoria(request, request.user, 'crear_triaje', 
                                       f'Triaje creado para {paciente.nombre_completo}')
                    
                    messages.success(request, f'Paciente {paciente.nombre_completo} registrado exitosamente con prioridad {triaje.get_nivel_prioridad_display()}.')
                    return redirect('dashboard')
                    
                except Exception as e:
                    messages.error(request, f'Error al registrar paciente: {str(e)}')
    else:
        # GET request - show appropriate form
        if step == 1:
            form = PacienteForm(initial=session_data.get('paciente', {}))
        elif step == 2:
            form = TriajeAntecedentesForm(initial=session_data.get('antecedentes', {}))
        elif step == 3:
            form = TriajeSignosVitalesForm(initial=session_data.get('signos_vitales', {}))
        elif step == 4:
            form = TriajeDiagnosticoForm(initial=session_data.get('diagnostico', {}))
        else:
            return redirect('registrar_paciente')
    
    step_titles = {
        1: 'Datos Generales',
        2: 'Antecedentes',
        3: 'Triaje / Signos Vitales',
        4: 'Diagnóstico e Indicaciones'
    }
    
    context = {
        'form': form,
        'step': step,
        'step_title': step_titles.get(step, ''),
        'total_steps': 4,
        'page_title': 'Registrar Paciente'
    }
    
    return render(request, 'registrar.html', context)


@login_required
def cancelar_registro(request):
    """Cancel patient registration and clear session"""
    if 'registro_paciente' in request.session:
        del request.session['registro_paciente']
    messages.info(request, 'Registro cancelado.')
    return redirect('dashboard')


# ============================================================
# RF-04: Patient Care Module
# ============================================================

@login_required
def atencion_view(request, triaje_id):
    """View and complete patient care"""
    triaje = get_object_or_404(Triaje, id=triaje_id)
    
    # Check if already attended
    if triaje.estado == 'atendido':
        messages.warning(request, 'Este paciente ya fue atendido.')
        return redirect('historial')
    
    # Mark as in attention if still waiting
    if triaje.estado == 'en_espera':
        triaje.estado = 'en_atencion'
        triaje.save()
        
        # Create attention record
        atencion, created = Atencion.objects.get_or_create(
            triaje=triaje,
            defaults={'usuario': request.user}
        )
        
        registrar_auditoria(request, request.user, 'iniciar_atencion',
                           f'Atención iniciada para {triaje.paciente.nombre_completo}')
    else:
        atencion = triaje.atencion
    
    if request.method == 'POST':
        form = AtencionForm(request.POST, instance=atencion)
        if form.is_valid():
            atencion = form.save(commit=False)
            atencion.fecha_fin = timezone.now()
            atencion.save()
            
            # Update triage status
            triaje.estado = 'atendido'
            triaje.save()
            
            registrar_auditoria(request, request.user, 'finalizar_atencion',
                               f'Atención finalizada para {triaje.paciente.nombre_completo}')
            
            messages.success(request, f'Atención de {triaje.paciente.nombre_completo} finalizada correctamente.')
            return redirect('dashboard')
    else:
        form = AtencionForm(instance=atencion)
    
    context = {
        'triaje': triaje,
        'paciente': triaje.paciente,
        'atencion': atencion,
        'form': form,
        'page_title': f'Atención - {triaje.paciente.nombre_completo}'
    }
    
    return render(request, 'atencion.html', context)


@login_required
def quitar_de_cola(request, triaje_id):
    """Remove patient from queue (with confirmation)"""
    if request.method == 'POST':
        triaje = get_object_or_404(Triaje, id=triaje_id)
        if triaje.estado == 'en_espera':
            triaje.estado = 'atendido'  # Mark as attended (removed)
            triaje.save()
            messages.success(request, f'{triaje.paciente.nombre_completo} removido de la cola.')
    return redirect('dashboard')


# ============================================================
# RF-05: Patient History Module
# ============================================================

@login_required
def historial_view(request):
    """View patient history with filters and search"""
    form = BusquedaPacienteForm(request.GET)
    
    # Base query - filter by role
    if request.user.rol == 'admin':
        # Admin sees all triage records
        triajes = Triaje.objects.select_related('paciente').order_by('-fecha_hora_consulta')
    else:
        # Personal común only sees patients they attended
        triajes = Triaje.objects.filter(
            atencion__usuario=request.user
        ).select_related('paciente').order_by('-fecha_hora_consulta')
    
    # Apply filters
    if form.is_valid():
        busqueda = form.cleaned_data.get('busqueda')
        estado = form.cleaned_data.get('estado')
        fecha_desde = form.cleaned_data.get('fecha_desde')
        fecha_hasta = form.cleaned_data.get('fecha_hasta')
        
        if busqueda:
            triajes = triajes.filter(
                Q(paciente__nombre_completo__icontains=busqueda) |
                Q(paciente__ci__icontains=busqueda)
            )
        
        if estado:
            triajes = triajes.filter(estado=estado)
        
        if fecha_desde:
            triajes = triajes.filter(fecha_hora_consulta__date__gte=fecha_desde)
        
        if fecha_hasta:
            triajes = triajes.filter(fecha_hora_consulta__date__lte=fecha_hasta)
    
    registrar_auditoria(request, request.user, 'ver_historial', 'Consulta de historial')
    
    # Pagination
    paginator = Paginator(triajes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'page_title': 'Historial de Pacientes'
    }
    
    return render(request, 'historial.html', context)


@login_required
def detalle_paciente_view(request, triaje_id):
    """View detailed patient record"""
    triaje = get_object_or_404(Triaje.objects.select_related('paciente'), id=triaje_id)
    atencion = getattr(triaje, 'atencion', None)
    
    # Check access for personal común - only if they attended this patient
    if request.user.rol != 'admin':
        if not atencion or atencion.usuario != request.user:
            messages.error(request, 'No tiene permiso para ver este paciente.')
            return redirect('historial')
    
    # Get patient history (all triages)
    historial = Triaje.objects.filter(paciente=triaje.paciente).order_by('-fecha_hora_consulta')
    
    context = {
        'triaje': triaje,
        'paciente': triaje.paciente,
        'atencion': atencion,
        'historial': historial,
        'page_title': f'Detalle - {triaje.paciente.nombre_completo}'
    }
    
    return render(request, 'detalle_paciente.html', context)


# ============================================================
# RF-06: Reports Module
# ============================================================

@login_required
@role_required(['admin'])
def reportes_view(request):
    """Reports dashboard with statistics and charts"""
    # Date range filter
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    # Default to last 30 days
    if not fecha_hasta:
        fecha_hasta = timezone.now().date()
    else:
        from datetime import datetime
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
    
    if not fecha_desde:
        fecha_desde = fecha_hasta - timedelta(days=30)
    else:
        from datetime import datetime
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
    
    # Filter triajes by date range
    triajes = Triaje.objects.filter(
        fecha_hora_consulta__date__gte=fecha_desde,
        fecha_hora_consulta__date__lte=fecha_hasta
    )
    
    # Statistics
    stats = {
        'total_atendidos': triajes.filter(estado='atendido').count(),
        'total_registrados': triajes.count(),
    }
    
    # Priority distribution
    prioridad_stats = triajes.values('nivel_prioridad').annotate(
        total=Count('id')
    ).order_by('nivel_prioridad')
    
    # Specialty distribution
    especialidad_stats = triajes.values('especialidad').annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    # Daily trend
    tendencia_diaria = triajes.annotate(
        fecha=TruncDate('fecha_hora_consulta')
    ).values('fecha').annotate(
        total=Count('id')
    ).order_by('fecha')
    
    # Average attention time
    atenciones_finalizadas = Atencion.objects.filter(
        fecha_fin__isnull=False,
        triaje__fecha_hora_consulta__date__gte=fecha_desde,
        triaje__fecha_hora_consulta__date__lte=fecha_hasta
    )
    
    # Statistics per user (for admin)
    usuarios_stats = atenciones_finalizadas.values(
        'usuario__id', 'usuario__nombre_completo'
    ).annotate(
        total_atendidos=Count('id')
    ).order_by('-total_atendidos')
    
    # Calculate average attention time per user
    for user_stat in usuarios_stats:
        user_atenciones = atenciones_finalizadas.filter(usuario__id=user_stat['usuario__id'])
        total_minutes = 0
        count = 0
        for atencion in user_atenciones:
            if atencion.fecha_fin and atencion.fecha_inicio:
                delta = atencion.fecha_fin - atencion.fecha_inicio
                total_minutes += delta.seconds // 60
                count += 1
        user_stat['promedio_minutos'] = round(total_minutes / count) if count > 0 else 0
    
    registrar_auditoria(request, request.user, 'generar_reporte', 
                       f'Reporte generado: {fecha_desde} a {fecha_hasta}')
    
    context = {
        'stats': stats,
        'prioridad_stats': list(prioridad_stats),
        'especialidad_stats': list(especialidad_stats),
        'tendencia_diaria': list(tendencia_diaria),
        'usuarios_stats': list(usuarios_stats),
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'page_title': 'Reportes y Estadísticas'
    }
    
    return render(request, 'reportes.html', context)


@login_required
def api_reportes_data(request):
    """API endpoint for reports data (for charts)"""
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if not fecha_hasta:
        fecha_hasta = timezone.now().date()
    else:
        from datetime import datetime
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
    
    if not fecha_desde:
        fecha_desde = fecha_hasta - timedelta(days=30)
    else:
        from datetime import datetime
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
    
    triajes = Triaje.objects.filter(
        fecha_hora_consulta__date__gte=fecha_desde,
        fecha_hora_consulta__date__lte=fecha_hasta
    )
    
    # Priority data for pie chart
    prioridad_data = {
        'labels': ['Alta', 'Media', 'Baja'],
        'data': [
            triajes.filter(nivel_prioridad='alta').count(),
            triajes.filter(nivel_prioridad='media').count(),
            triajes.filter(nivel_prioridad='baja').count(),
        ],
        'colors': ['#DC3545', '#FFC107', '#28A745']
    }
    
    # Daily trend for line chart
    tendencia = triajes.annotate(
        fecha=TruncDate('fecha_hora_consulta')
    ).values('fecha').annotate(
        total=Count('id')
    ).order_by('fecha')
    
    tendencia_data = {
        'labels': [str(t['fecha']) for t in tendencia],
        'data': [t['total'] for t in tendencia]
    }
    
    return JsonResponse({
        'prioridad': prioridad_data,
        'tendencia': tendencia_data
    })


# ============================================================
# RF-07: User Management Module (Admin only)
# ============================================================

@login_required
@role_required(['admin'])
def gestion_usuarios_view(request):
    """List and manage users (admin only)"""
    usuarios = Usuario.objects.all().order_by('-fecha_creacion')
    
    context = {
        'usuarios': usuarios,
        'page_title': 'Gestión de Usuarios'
    }
    
    return render(request, 'gestion_usuarios.html', context)


@login_required
@role_required(['admin'])
def crear_usuario_view(request):
    """Create new user (admin only)"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        rol = request.POST.get('rol', 'personal')
        
        # Validation
        if not username or not password or not nombre_completo:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'usuario_form.html', {
                'page_title': 'Crear Usuario',
                'action': 'crear'
            })
        
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
            return render(request, 'usuario_form.html', {
                'page_title': 'Crear Usuario',
                'action': 'crear'
            })
        
        # Create user
        usuario = Usuario.objects.create_user(
            username=username,
            password=password,
            nombre_completo=nombre_completo,
            rol=rol
        )
        
        registrar_auditoria(request, request.user, 'crear_usuario',
                          f'Usuario creado: {usuario.nombre_completo}')
        
        messages.success(request, f'Usuario {nombre_completo} creado correctamente.')
        return redirect('gestion_usuarios')
    
    return render(request, 'usuario_form.html', {
        'page_title': 'Crear Usuario',
        'action': 'crear'
    })


@login_required
@role_required(['admin'])
def editar_usuario_view(request, user_id):
    """Edit existing user (admin only)"""
    usuario = get_object_or_404(Usuario, id=user_id)
    
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo', '').strip()
        rol = request.POST.get('rol', 'personal')
        activo = request.POST.get('activo') == 'on'
        new_password = request.POST.get('password', '').strip()
        
        if not nombre_completo:
            messages.error(request, 'El nombre completo es obligatorio.')
        else:
            usuario.nombre_completo = nombre_completo
            usuario.rol = rol
            usuario.activo = activo
            
            if new_password:
                usuario.set_password(new_password)
            
            usuario.save()
            
            registrar_auditoria(request, request.user, 'editar_usuario',
                              f'Usuario editado: {usuario.nombre_completo}')
            
            messages.success(request, f'Usuario {nombre_completo} actualizado correctamente.')
            return redirect('gestion_usuarios')
    
    return render(request, 'usuario_form.html', {
        'usuario': usuario,
        'page_title': f'Editar Usuario - {usuario.nombre_completo}',
        'action': 'editar'
    })


@login_required
@role_required(['admin'])
def eliminar_paciente_view(request, triaje_id):
    """Delete patient record (admin only)"""
    triaje = get_object_or_404(Triaje, id=triaje_id)
    paciente = triaje.paciente
    
    if request.method == 'POST':
        nombre = paciente.nombre_completo
        
        # Delete the triaje record
        triaje.delete()
        
        # Check if patient has other triajes, if not delete patient too
        if not Triaje.objects.filter(paciente=paciente).exists():
            paciente.delete()
        
        registrar_auditoria(request, request.user, 'eliminar_paciente',
                          f'Registro eliminado: {nombre}')
        
        messages.success(request, f'Registro de {nombre} eliminado correctamente.')
        return redirect('historial')
    
    return render(request, 'confirmar_eliminar.html', {
        'triaje': triaje,
        'paciente': paciente,
        'page_title': 'Confirmar Eliminación'
    })

