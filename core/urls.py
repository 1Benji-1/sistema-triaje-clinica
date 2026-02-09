"""
URL Configuration for core app
"""

from django.urls import path
from . import views

urlpatterns = [
    # Authentication (RF-01)
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard / Triage Queue (RF-02)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/queue/', views.api_queue_update, name='api_queue_update'),
    
    # Patient Registration (RF-03)
    path('registrar/', views.registrar_paciente_view, name='registrar_paciente'),
    path('registrar/cancelar/', views.cancelar_registro, name='cancelar_registro'),
    
    # Patient Care (RF-04)
    path('atencion/<int:triaje_id>/', views.atencion_view, name='atencion'),
    path('quitar-cola/<int:triaje_id>/', views.quitar_de_cola, name='quitar_de_cola'),
    
    # Patient History (RF-05)
    path('historial/', views.historial_view, name='historial'),
    path('paciente/<int:triaje_id>/', views.detalle_paciente_view, name='detalle_paciente'),
    
    # Reports (RF-06)
    path('reportes/', views.reportes_view, name='reportes'),
    path('api/reportes/', views.api_reportes_data, name='api_reportes'),
    
    # User Management (RF-07 - Admin only)
    path('usuarios/', views.gestion_usuarios_view, name='gestion_usuarios'),
    path('usuarios/crear/', views.crear_usuario_view, name='crear_usuario'),
    path('usuarios/<int:user_id>/editar/', views.editar_usuario_view, name='editar_usuario'),
    
    # Delete patient (Admin only)
    path('paciente/<int:triaje_id>/eliminar/', views.eliminar_paciente_view, name='eliminar_paciente'),
]
