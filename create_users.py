"""
Script to create initial admin user
Run with: python manage.py shell < create_admin.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'triaje_clinico.settings')
django.setup()

from core.models import Usuario

# Create admin user if doesn't exist
if not Usuario.objects.filter(username='admin').exists():
    admin = Usuario.objects.create_superuser(
        username='admin',
        email='admin@clinica.com',
        password='Admin123!',
        nombre_completo='Administrador del Sistema',
        rol='admin'
    )
    print(f'Superuser created: {admin.username}')
else:
    print('Admin user already exists')

# Create test clinical user
if not Usuario.objects.filter(username='clinico1').exists():
    clinico = Usuario.objects.create_user(
        username='clinico1',
        email='clinico@clinica.com',
        password='Clinico123!',
        nombre_completo='Dr. Juan Pérez',
        rol='clinico'
    )
    print(f'Clinical user created: {clinico.username}')

# Create test pharmacy user
if not Usuario.objects.filter(username='farmacia1').exists():
    farmacia = Usuario.objects.create_user(
        username='farmacia1',
        email='farmacia@clinica.com',
        password='Farmacia123!',
        nombre_completo='María García',
        rol='farmacia'
    )
    print(f'Pharmacy user created: {farmacia.username}')

print('\n=== Users created successfully! ===')
print('Admin: admin / Admin123!')
print('Clinico: clinico1 / Clinico123!')
print('Farmacia: farmacia1 / Farmacia123!')
