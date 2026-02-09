"""
Custom decorators for role-based access control and audit logging
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import RegistroAuditoria


def role_required(allowed_roles):
    """
    Decorator to restrict view access based on user role
    Usage: @role_required(['admin', 'clinico'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.rol not in allowed_roles:
                messages.error(request, 'No tiene permisos para acceder a esta sección.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def registrar_auditoria(request, usuario, accion, descripcion=''):
    """
    Helper function to create audit log entries
    """
    try:
        ip_address = get_client_ip(request)
        RegistroAuditoria.objects.create(
            usuario=usuario,
            accion=accion,
            descripcion=descripcion,
            ip_address=ip_address
        )
    except Exception:
        pass  # Don't fail if audit logging fails


def get_client_ip(request):
    """Extract client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
