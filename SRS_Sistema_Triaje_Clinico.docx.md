  
**DOCUMENTO DE ESPECIFICACIÓN DE REQUERIMIENTOS**

*(Software Requirements Specification \- SRS)*

**SISTEMA DE TRIAJE CLÍNICO**

Aplicación Web para Gestión de Pacientes por Prioridad

**Versión 1.0**

Febrero 2026

# **TABLA DE CONTENIDOS**

# **CONTROL DE VERSIONES**

| Versión | Fecha | Autor | Descripción |
| ----- | ----- | ----- | ----- |
| 1.0 | 08/02/2026 | Equipo de Desarrollo | Documento inicial de especificaciones |

# **1\. INTRODUCCIÓN**

## **1.1 Propósito del Documento**

Este documento describe las especificaciones de requerimientos para el desarrollo del Sistema de Triaje Clínico, una aplicación web moderna diseñada para optimizar la atención de pacientes en clínicas mediante la clasificación por nivel de emergencia y prioridad.

El documento está dirigido a:

* Equipo de desarrollo técnico  
* Personal administrativo de la clínica  
* Personal clínico (médicos, enfermeras)  
* Stakeholders del proyecto

## **1.2 Alcance del Proyecto**

El Sistema de Triaje Clínico es una aplicación web completa que permitirá:

* Registro integral de pacientes con datos demográficos y clínicos  
* Clasificación de pacientes según nivel de prioridad médica (Alta, Media, Baja)  
* Gestión dinámica de cola de atención  
* Seguimiento completo del proceso de atención médica  
* Historial clínico centralizado y accesible  
* Generación de reportes estadísticos y gerenciales

## **1.3 Definiciones, Acrónimos y Abreviaturas**

| Término | Definición |
| ----- | ----- |
| Triaje | Sistema de selección y clasificación de pacientes según urgencia y gravedad |
| SRS | Software Requirements Specification (Especificación de Requerimientos de Software) |
| CI | Cédula de Identidad |
| HTML | HyperText Markup Language |
| CSS | Cascading Style Sheets |
| JS | JavaScript |
| Django | Framework de desarrollo web en Python |
| UI | User Interface (Interfaz de Usuario) |
| CRUD | Create, Read, Update, Delete |

# **2\. DESCRIPCIÓN GENERAL DEL SISTEMA**

## **2.1 Perspectiva del Producto**

El Sistema de Triaje Clínico es una aplicación web independiente diseñada para funcionar en entornos clínicos de pequeña y mediana escala. El sistema opera sobre una arquitectura cliente-servidor utilizando tecnologías web estándar y el framework Django para garantizar seguridad, escalabilidad y mantenibilidad.

## **2.2 Características de los Usuarios**

| Tipo de Usuario | Nivel Técnico | Funciones Principales |
| ----- | ----- | ----- |
| Administrador | Alto \- Conocimientos técnicos de sistemas | Configuración del sistema, gestión de usuarios, acceso completo a todas las funcionalidades |
| Personal Clínico | Medio \- Usuario con formación médica | Registro de pacientes, evaluación de triaje, atención médica, consulta de historiales |
| Farmacia | Medio \- Usuario especializado | Registro de medicamentos dispensados, consulta de prescripciones médicas |

## **2.3 Restricciones del Sistema**

* El sistema debe ser accesible mediante navegadores web modernos (Chrome, Firefox, Safari, Edge)  
* Debe funcionar en dispositivos de escritorio y tablets  
* Requiere conexión a internet para funcionalidad completa  
* Debe cumplir con normativas de privacidad de datos médicos  
* Tecnologías obligatorias: HTML, CSS, JavaScript, Django

# **3\. REQUERIMIENTOS FUNCIONALES**

## **3.1 RF-01: Módulo de Login / Inicio de Sesión**

**Descripción:** Sistema de autenticación seguro para controlar el acceso de usuarios al sistema.

**Prioridad:** Alta

| Requerimiento | Descripción |
| ----- | ----- |
| RF-01.1 | El sistema debe solicitar usuario y contraseña |
| RF-01.2 | Las contraseñas deben estar encriptadas en la base de datos |
| RF-01.3 | Debe implementarse sistema de roles: Administrador, Personal Clínico, Farmacia |
| RF-01.4 | Después de autenticación exitosa, redirigir a pestaña Principal/Triaje |
| RF-01.5 | Mostrar mensajes de error claros para credenciales inválidas |
| RF-01.6 | Implementar límite de intentos fallidos (3 intentos) |
| RF-01.7 | Opción de cerrar sesión disponible en todo momento |

## **3.2 RF-02: Módulo Principal / Triaje**

**Descripción:** Pantalla principal que muestra la cola de pacientes ordenados por nivel de prioridad.

**Prioridad:** Alta

| Requerimiento | Descripción |
| ----- | ----- |
| RF-02.1 | Visualizar lista completa de pacientes en espera |
| RF-02.2 | Ordenamiento automático por nivel de prioridad (Alta → Media → Baja) |
| RF-02.3 | Mostrar información resumida: Código, Nombre, Prioridad, Hora de ingreso, Estado |
| RF-02.4 | Código de colores visuales por prioridad: Rojo (Alta), Amarillo (Media), Verde (Baja) |
| RF-02.5 | Botón 'Atender' que redirige a módulo de Atención |
| RF-02.6 | Opción de quitar paciente de cola (con confirmación) |
| RF-02.7 | Actualización automática en tiempo real de la cola |
| RF-02.8 | Contador de pacientes por nivel de prioridad |

## **3.3 RF-03: Módulo Registrar Paciente**

**Descripción:** Sistema de registro completo de pacientes organizado en pasos secuenciales.

**Prioridad:** Alta

### **3.3.1 RF-03.1: Datos Generales**

| Campo | Descripción / Validación |
| ----- | ----- |
| Nombre completo | Campo obligatorio, mínimo 3 caracteres |
| Sexo | Selección: Masculino / Femenino / Otro |
| Fecha de nacimiento | Formato DD/MM/AAAA, validar edad coherente |
| CI (Cédula) | Campo único, validar formato numérico |
| Fecha y hora consulta | Auto-generada al momento del registro |
| Tipo de paciente | Selección: Nuevo / Antiguo (existente en sistema) |

### **3.3.2 RF-03.2: Antecedentes**

| Campo | Descripción / Validación |
| ----- | ----- |
| Especialidad | Lista desplegable de especialidades médicas disponibles |
| Médico asignado | Selección de médico disponible (filtrado por especialidad) |
| Enfermería | Selección de enfermera/o responsable del triaje |

### **3.3.3 RF-03.3: Triaje / Ficha Técnica**

| Campo | Descripción / Validación |
| ----- | ----- |
| Talla | En centímetros (cm), rango válido: 40-250 cm |
| Peso | En kilogramos (kg), rango válido: 1-300 kg |
| Temperatura | En grados Celsius (°C), rango válido: 32-43°C |
| Presión arterial | Formato: Sistólica/Diastólica (ej: 120/80 mmHg) |
| Pulsación | Pulsaciones por minuto (ppm), rango válido: 40-200 ppm |
| Nivel de prioridad | Selección obligatoria: Alta (Rojo) / Media (Amarillo) / Baja (Verde) |

### **3.3.4 RF-03.4: Diagnóstico e Indicaciones**

| Campo | Descripción / Validación |
| ----- | ----- |
| Sintomatología | Área de texto para descripción detallada de síntomas |
| Tratamiento | Área de texto para indicaciones médicas y prescripciones |
| Estudios complementarios | Área de texto para solicitud de análisis, imágenes, etc. |

***Nota:** Al finalizar el registro completo, el paciente ingresa automáticamente a la cola de triaje según su nivel de prioridad.*

## **3.4 RF-04: Módulo de Atención**

**Descripción:** Módulo para realizar la atención clínica o farmacéutica del paciente.

**Prioridad:** Alta

| Requerimiento | Descripción |
| ----- | ----- |
| RF-04.1 | Mostrar todos los datos del paciente de forma organizada y legible |
| RF-04.2 | Visualizar: Datos generales, Antecedentes, Resultados de triaje, Diagnóstico |
| RF-04.3 | Sección para registrar medicamentos dispensados (nombre, dosis, cantidad) |
| RF-04.4 | Campo de observaciones adicionales durante la atención |
| RF-04.5 | Botón 'Finalizar Atención' que confirma el cierre del caso |
| RF-04.6 | Al finalizar, el paciente sale de cola activa y pasa a estado 'Atendido' |
| RF-04.7 | Registro automático de fecha/hora de finalización de atención |
| RF-04.8 | Opción de imprimir resumen de atención |

## **3.5 RF-05: Módulo Pacientes / Historial**

**Descripción:** Consulta y gestión del registro histórico completo de pacientes.

**Prioridad:** Media

| Requerimiento | Descripción |
| ----- | ----- |
| RF-05.1 | Visualizar lista completa de todos los pacientes registrados |
| RF-05.2 | Filtros disponibles: Por fecha, Por estado (Atendido/No atendido), Por nombre |
| RF-05.3 | Búsqueda rápida por CI o nombre del paciente |
| RF-05.4 | Botón 'Ver más' para acceder al detalle completo |
| RF-05.5 | Vista detallada debe mostrar: Datos generales, Antecedentes, Triaje, Diagnóstico, Atención |
| RF-05.6 | Paginación de resultados (20 registros por página) |
| RF-05.7 | Exportar historial individual a formato PDF |

## **3.6 RF-06: Módulo de Reportes**

**Descripción:** Generación de reportes estadísticos y gerenciales para análisis y toma de decisiones.

**Prioridad:** Media

| Requerimiento | Descripción |
| ----- | ----- |
| RF-06.1 | Reporte de pacientes atendidos por período (día/semana/mes/año) |
| RF-06.2 | Reporte de distribución de pacientes por nivel de prioridad |
| RF-06.3 | Reporte de tiempo promedio de atención |
| RF-06.4 | Reporte de medicamentos dispensados con cantidades |
| RF-06.5 | Reporte de pacientes por especialidad médica |
| RF-06.6 | Filtros por rango de fechas personalizable |
| RF-06.7 | Visualización de datos mediante gráficos (barras, líneas, torta) |
| RF-06.8 | Opción de exportar reportes a PDF y Excel |
| RF-06.9 | Programación de reportes automáticos periódicos (opcional) |

# **4\. REQUERIMIENTOS NO FUNCIONALES**

## **4.1 RNF-01: Rendimiento**

| ID | Descripción |
| ----- | ----- |
| RNF-01.1 | Tiempo de respuesta máximo: 3 segundos para operaciones normales |
| RNF-01.2 | Capacidad de soportar al menos 50 usuarios simultáneos |
| RNF-01.3 | Base de datos capaz de almacenar mínimo 100,000 registros de pacientes |
| RNF-01.4 | Actualización de cola de triaje en tiempo real (máximo 2 segundos de latencia) |

## **4.2 RNF-02: Seguridad**

| ID | Descripción |
| ----- | ----- |
| RNF-02.1 | Todas las contraseñas deben encriptarse con algoritmo bcrypt o similar |
| RNF-02.2 | Implementar protocolo HTTPS para todas las comunicaciones |
| RNF-02.3 | Sistema de control de acceso basado en roles (RBAC) |
| RNF-02.4 | Registro de auditoría de todas las operaciones críticas (log de acciones) |
| RNF-02.5 | Sesiones con timeout automático después de 30 minutos de inactividad |
| RNF-02.6 | Protección contra inyección SQL mediante consultas parametrizadas |
| RNF-02.7 | Validación de entrada de datos en frontend y backend |

## **4.3 RNF-03: Usabilidad**

| ID | Descripción |
| ----- | ----- |
| RNF-03.1 | Interfaz intuitiva que requiera mínima capacitación (máximo 2 horas) |
| RNF-03.2 | Diseño responsivo compatible con tablets y pantallas de 10 pulgadas o más |
| RNF-03.3 | Mensajes de error claros y descriptivos en español |
| RNF-03.4 | Navegación consistente con máximo 3 clics para cualquier funcionalidad |
| RNF-03.5 | Confirmaciones para acciones críticas (eliminar, finalizar atención) |
| RNF-03.6 | Código de colores estándar para niveles de prioridad médica |

## **4.4 RNF-04: Disponibilidad**

| ID | Descripción |
| ----- | ----- |
| RNF-04.1 | Disponibilidad del sistema: 99% del tiempo (24/7) |
| RNF-04.2 | Mantenimientos programados fuera de horario clínico principal |
| RNF-04.3 | Sistema de respaldo automático de base de datos cada 24 horas |
| RNF-04.4 | Plan de recuperación ante desastres con RTO de 4 horas |

## **4.5 RNF-05: Mantenibilidad**

| ID | Descripción |
| ----- | ----- |
| RNF-05.1 | Código documentado siguiendo estándares de Python (PEP 8\) y JavaScript (ESLint) |
| RNF-05.2 | Arquitectura modular que facilite actualizaciones sin afectar otros componentes |
| RNF-05.3 | Sistema de versionado de código con Git |
| RNF-05.4 | Documentación técnica completa del sistema (manual de desarrollador) |

# **5\. ARQUITECTURA TÉCNICA**

## **5.1 Stack Tecnológico**

| Capa | Tecnología | Justificación |
| ----- | ----- | ----- |
| Frontend | HTML5, CSS3, JavaScript | Estándar web universal, compatible con todos los navegadores modernos |
| Backend | Django Framework (Python) | Framework robusto con sistema de autenticación integrado, ORM potente, alta seguridad |
| Base de Datos | PostgreSQL / MySQL | Base de datos relacional robusta, escalable, con soporte para Django ORM |
| Servidor Web | Gunicorn \+ Nginx | Servidor WSGI eficiente para Django \+ proxy reverso para optimización |

## **5.2 Arquitectura del Sistema**

El sistema seguirá una arquitectura MVC (Model-View-Controller) implementada a través de Django:

* **Model (Modelo):** Django ORM para gestión de base de datos y modelos de datos  
* **View (Vista):** Templates HTML con renderizado del lado del servidor  
* **Controller (Controlador):** Views de Django para lógica de negocio y procesamiento de solicitudes

## **5.3 Componentes Principales**

1. **Módulo de Autenticación:** Django Authentication System con roles personalizados  
2. **Módulo de Gestión de Pacientes:** CRUD completo para datos de pacientes  
3. **Módulo de Triaje:** Sistema de clasificación y cola dinámica  
4. **Módulo de Atención:** Gestión del proceso de atención médica  
5. **Módulo de Reportes:** Generación de estadísticas y exportación  
6. **Módulo de Historial:** Consulta y gestión de registros históricos

# **6\. MODELO DE DATOS**

## **6.1 Entidades Principales**

### **6.1.1 Usuario**

| Campo | Tipo | Restricción | Descripción |
| ----- | ----- | ----- | ----- |
| id | Integer | PK, Auto | Identificador único |
| username | String(50) | Unique, Not Null | Nombre de usuario |
| password | String(255) | Not Null | Contraseña encriptada |
| rol | String(20) | Not Null | Administrador/Clínico/Farmacia |
| nombre\_completo | String(100) | Not Null | Nombre completo del usuario |
| fecha\_creacion | DateTime | Not Null | Fecha de creación del usuario |
| activo | Boolean | Default True | Estado del usuario |

### **6.1.2 Paciente**

| Campo | Tipo | Restricción | Descripción |
| ----- | ----- | ----- | ----- |
| id | Integer | PK, Auto | Identificador único |
| nombre\_completo | String(100) | Not Null | Nombre completo del paciente |
| ci | String(20) | Unique, Not Null | Cédula de identidad |
| sexo | String(10) | Not Null | Masculino/Femenino/Otro |
| fecha\_nacimiento | Date | Not Null | Fecha de nacimiento |
| tipo\_paciente | String(10) | Not Null | Nuevo/Antiguo |
| fecha\_registro | DateTime | Not Null | Fecha de registro en sistema |

### **6.1.3 Triaje**

| Campo | Tipo | Restricción | Descripción |
| ----- | ----- | ----- | ----- |
| id | Integer | PK, Auto | Identificador único |
| paciente\_id | Integer | FK, Not Null | Referencia a Paciente |
| fecha\_hora\_consulta | DateTime | Not Null | Fecha y hora de consulta |
| especialidad | String(50) | Not Null | Especialidad médica |
| medico | String(100) | Not Null | Médico asignado |
| enfermeria | String(100) | Not Null | Enfermera responsable |
| talla | Decimal(5,2) | Not Null | Talla en cm |
| peso | Decimal(5,2) | Not Null | Peso en kg |
| temperatura | Decimal(4,2) | Not Null | Temperatura en °C |
| presion\_arterial | String(10) | Not Null | Formato: 120/80 |
| pulsacion | Integer | Not Null | Pulsaciones por minuto |
| nivel\_prioridad | String(10) | Not Null | Alta/Media/Baja |
| sintomatologia | Text | Nullable | Descripción de síntomas |
| tratamiento | Text | Nullable | Tratamiento indicado |
| estudios\_complementarios | Text | Nullable | Estudios solicitados |
| estado | String(20) | Not Null | EnEspera/EnAtencion/Atendido |

### **6.1.4 Atención**

| Campo | Tipo | Restricción | Descripción |
| ----- | ----- | ----- | ----- |
| id | Integer | PK, Auto | Identificador único |
| triaje\_id | Integer | FK, Unique, Not Null | Referencia a Triaje |
| usuario\_id | Integer | FK, Not Null | Usuario que atendió |
| fecha\_inicio | DateTime | Not Null | Inicio de atención |
| fecha\_fin | DateTime | Not Null | Fin de atención |
| observaciones | Text | Nullable | Observaciones adicionales |
| medicamentos\_dispensados | Text | Nullable | Lista de medicamentos |

## **6.2 Relaciones entre Entidades**

* Un Paciente puede tener múltiples registros de Triaje (1:N)  
* Un Triaje tiene una única Atención (1:1)  
* Un Usuario puede realizar múltiples Atenciones (1:N)  
* Un Triaje pertenece a un único Paciente (N:1)

# **7\. CASOS DE USO PRINCIPALES**

## **7.1 CU-01: Iniciar Sesión**

| Elemento | Descripción |
| ----- | ----- |
| Actor | Personal Clínico, Administrador, Farmacia |
| Precondición | Usuario registrado en el sistema |
| Flujo Principal | 1\. Usuario accede a pantalla de login2. Ingresa credenciales (usuario y contraseña)3. Sistema valida credenciales4. Sistema carga rol del usuario5. Redirige a pantalla Principal/Triaje |
| Flujo Alternativo | 3a. Credenciales inválidas    3a.1. Sistema muestra mensaje de error    3a.2. Regresa a paso 23b. Intentos máximos excedidos (3)    3b.1. Sistema bloquea temporalmente la cuenta |
| Postcondición | Usuario autenticado con sesión activa |

## **7.2 CU-02: Registrar Nuevo Paciente**

| Elemento | Descripción |
| ----- | ----- |
| Actor | Personal Clínico |
| Precondición | Usuario autenticado con rol Clínico |
| Flujo Principal | 1\. Usuario accede a módulo 'Registrar Paciente'2. Completa Datos Generales del paciente3. Sistema valida CI único4. Completa Antecedentes médicos5. Completa Triaje/Ficha Técnica6. Asigna nivel de prioridad7. Completa Diagnóstico e Indicaciones8. Sistema guarda registro completo9. Paciente ingresa a cola de triaje según prioridad |
| Flujo Alternativo | 3a. CI ya existe en sistema    3a.1. Sistema muestra mensaje de error    3a.2. Ofrece opción de ver registro existente6a. Validación de signos vitales fuera de rango    6a.1. Sistema muestra advertencia    6a.2. Usuario confirma o corrige valores |
| Postcondición | Paciente registrado y en cola de triaje |

## **7.3 CU-03: Atender Paciente**

| Elemento | Descripción |
| ----- | ----- |
| Actor | Personal Clínico, Farmacia |
| Precondición | Paciente en cola de triaje con estado 'En Espera' |
| Flujo Principal | 1\. Usuario selecciona paciente de cola2. Hace clic en botón 'Atender'3. Sistema muestra módulo de Atención con datos completos4. Sistema cambia estado a 'En Atención'5. Usuario revisa información del paciente6. Registra medicamentos dispensados (si aplica)7. Agrega observaciones adicionales8. Usuario hace clic en 'Finalizar Atención'9. Sistema confirma acción10. Sistema registra fecha/hora de finalización11. Cambia estado a 'Atendido'12. Paciente sale de cola activa |
| Flujo Alternativo | 9a. Usuario cancela finalización    9a.1. Regresa a módulo de atención    9a.2. Estado permanece 'En Atención' |
| Postcondición | Paciente atendido y removido de cola activa |

## **7.4 CU-04: Consultar Historial de Paciente**

| Elemento | Descripción |
| ----- | ----- |
| Actor | Personal Clínico, Administrador |
| Precondición | Usuario autenticado |
| Flujo Principal | 1\. Usuario accede a módulo 'Pacientes/Historial'2. Sistema muestra lista de pacientes3. Usuario puede aplicar filtros (fecha, estado, nombre)4. Usuario busca paciente específico5. Hace clic en botón 'Ver más'6. Sistema muestra detalle completo del paciente7. Usuario visualiza toda la información histórica |
| Flujo Alternativo | 4a. Paciente no encontrado    4a.1. Sistema muestra mensaje 'Sin resultados'6a. Usuario desea exportar a PDF    6a.1. Hace clic en botón 'Exportar'    6a.2. Sistema genera PDF del historial |
| Postcondición | Información del paciente consultada |

## **7.5 CU-05: Generar Reporte Estadístico**

| Elemento | Descripción |
| ----- | ----- |
| Actor | Administrador, Personal Clínico |
| Precondición | Usuario autenticado con permisos de reportes |
| Flujo Principal | 1\. Usuario accede a módulo 'Reportes'2. Selecciona tipo de reporte deseado3. Define rango de fechas4. Aplica filtros adicionales (opcional)5. Hace clic en 'Generar Reporte'6. Sistema procesa datos7. Sistema muestra reporte con gráficos y tablas8. Usuario puede exportar en formato deseado |
| Flujo Alternativo | 6a. Sin datos para el período seleccionado    6a.1. Sistema muestra mensaje informativo    6a.2. Regresa a paso 28a. Usuario selecciona exportar a PDF    8a.1. Sistema genera PDF del reporte8b. Usuario selecciona exportar a Excel    8b.1. Sistema genera archivo Excel |
| Postcondición | Reporte generado y disponible para consulta/exportación |

# **8\. DISEÑO DE INTERFAZ DE USUARIO**

## **8.1 Principios de Diseño**

* **Simplicidad:** Interfaz limpia y minimalista, enfocada en funcionalidad  
* **Consistencia:** Elementos visuales uniformes en todas las pantallas  
* **Accesibilidad:** Contraste adecuado, fuentes legibles (mínimo 14px)  
* **Retroalimentación:** Indicadores visuales claros de acciones y estados  
* **Eficiencia:** Minimizar clics y pasos para completar tareas

## **8.2 Paleta de Colores del Sistema**

| Elemento | Color | Uso |
| ----- | ----- | ----- |
| Prioridad Alta | Rojo (\#DC3545) | Pacientes de emergencia, alertas críticas |
| Prioridad Media | Amarillo (\#FFC107) | Pacientes con urgencia moderada |
| Prioridad Baja | Verde (\#28A745) | Pacientes sin urgencia |
| Primario | Azul (\#007BFF) | Botones principales, encabezados |
| Secundario | Gris (\#6C757D) | Botones secundarios, texto auxiliar |
| Éxito | Verde oscuro (\#198754) | Confirmaciones, operaciones exitosas |
| Advertencia | Naranja (\#FD7E14) | Advertencias, precauciones |

## **8.3 Componentes de Interfaz Estándar**

### **8.3.1 Navegación Principal**

* Barra de navegación superior fija con logo y nombre de usuario  
* Menú de pestañas: Principal | Registrar | Atención | Historial | Reportes  
* Botón de cerrar sesión visible en todo momento

### **8.3.2 Formularios**

* Campos de entrada con etiquetas claras y placeholders descriptivos  
* Validación en tiempo real con mensajes de error debajo del campo  
* Indicador visual de campos obligatorios (asterisco rojo \*)  
* Botones de acción alineados a la derecha: Cancelar | Guardar

### **8.3.3 Tablas de Datos**

* Encabezados con fondo oscuro y texto blanco  
* Filas alternadas con colores claros para mejor legibilidad  
* Hover effect en filas para indicar interactividad  
* Botones de acción en última columna

# **9\. SEGURIDAD Y CONTROL DE ACCESO**

## **9.1 Matriz de Permisos por Rol**

| Funcionalidad | Administrador | Personal Clínico | Farmacia |
| ----- | ----- | ----- | ----- |
| Gestión de Usuarios | ✓ Completo | ✗ Sin acceso | ✗ Sin acceso |
| Registrar Paciente | ✓ Completo | ✓ Completo | ✗ Solo lectura |
| Ver Cola de Triaje | ✓ Completo | ✓ Completo | ✓ Completo |
| Atender Paciente | ✓ Completo | ✓ Completo | ✓ Limitado\* |
| Consultar Historial | ✓ Completo | ✓ Completo | ✓ Completo |
| Generar Reportes | ✓ Completo | ✓ Completo | ✗ Sin acceso |
| Exportar Datos | ✓ Completo | ✓ Limitado | ✗ Sin acceso |
| Configuración Sistema | ✓ Completo | ✗ Sin acceso | ✗ Sin acceso |

***\* Farmacia:** Solo puede registrar medicamentos dispensados, no puede modificar diagnóstico ni tratamiento*

## **9.2 Políticas de Seguridad**

### **9.2.1 Contraseñas**

* Longitud mínima: 8 caracteres  
* Debe contener: mayúsculas, minúsculas, números  
* Encriptación: bcrypt con salt de 12 rondas  
* Cambio de contraseña cada 90 días (recomendado)

### **9.2.2 Sesiones**

* Timeout por inactividad: 30 minutos  
* Token de sesión renovado cada 15 minutos  
* Cierre de sesión automático al cerrar navegador  
* Registro de actividad por usuario (log de auditoría)

### **9.2.3 Protección de Datos**

* Conexiones HTTPS obligatorias  
* Certificado SSL/TLS válido  
* Respaldo automático diario de base de datos  
* Encriptación de datos sensibles en base de datos  
* Cumplimiento de normativas de privacidad de datos médicos

# **10\. PLAN DE IMPLEMENTACIÓN**

## **10.1 Fases del Proyecto**

| Fase | Actividades | Duración | Entregables |
| ----- | ----- | ----- | ----- |
| Fase 1: Análisis | Recopilación de requerimientos, análisis de necesidades, diseño de arquitectura | 2 semanas | Documento SRS, Diagrama de arquitectura |
| Fase 2: Diseño | Diseño de base de datos, diseño de interfaces, prototipado | 2 semanas | Modelo de datos, Wireframes, Prototipos |
| Fase 3: Desarrollo | Implementación de módulos, integración de componentes, pruebas unitarias | 6 semanas | Código fuente, Módulos funcionales |
| Fase 4: Pruebas | Pruebas de integración, pruebas de sistema, pruebas de usuario | 2 semanas | Reporte de pruebas, Correcciones |
| Fase 5: Despliegue | Instalación en servidor, configuración, capacitación de usuarios | 1 semana | Sistema en producción, Manual de usuario |
| Fase 6: Soporte | Mantenimiento, correcciones, mejoras | Continuo | Actualizaciones, Soporte técnico |

## **10.2 Recursos Necesarios**

### **10.2.1 Equipo de Desarrollo**

* 1 Líder de Proyecto / Analista  
* 2 Desarrolladores Full Stack (Django \+ Frontend)  
* 1 Diseñador UI/UX  
* 1 QA Tester

### **10.2.2 Infraestructura Técnica**

* Servidor web (cloud o dedicado) con mínimo 4GB RAM  
* Base de datos PostgreSQL o MySQL  
* Certificado SSL para HTTPS  
* Sistema de respaldo automatizado  
* Repositorio Git para control de versiones

# **11\. CRITERIOS DE ACEPTACIÓN**

El sistema será considerado aceptado cuando cumpla con los siguientes criterios:

7. **Funcionalidad Completa:** Todos los módulos definidos en RF-01 a RF-06 están operativos  
8. **Rendimiento:** Tiempo de respuesta menor a 3 segundos para el 95% de operaciones  
9. **Seguridad:** Sistema de autenticación funcional, contraseñas encriptadas, HTTPS implementado  
10. **Usabilidad:** Personal capacitado puede operar el sistema sin asistencia técnica  
11. **Estabilidad:** Sistema opera sin errores críticos durante 7 días consecutivos  
12. **Compatibilidad:** Funciona correctamente en Chrome, Firefox, Safari y Edge  
13. **Documentación:** Manual de usuario y documentación técnica entregados y aprobados  
14. **Capacitación:** Personal clínico capacitado y aprobado en uso del sistema

# **12\. ANEXOS**

## **12.1 Glosario de Términos Médicos**

| Término | Definición |
| ----- | ----- |
| Triaje | Método de clasificación de pacientes según gravedad y urgencia de atención |
| Signos Vitales | Indicadores básicos de funciones corporales: temperatura, presión, pulso |
| Sintomatología | Conjunto de síntomas que presenta un paciente |
| Estudios Complementarios | Exámenes médicos adicionales: análisis de sangre, rayos X, etc. |
| Prioridad Alta | Paciente en estado crítico que requiere atención inmediata |
| Prioridad Media | Paciente con condición estable pero requiere atención pronta |
| Prioridad Baja | Paciente con condición no urgente, puede esperar |

## **12.2 Referencias**

15. Django Documentation: https://docs.djangoproject.com/  
16. Python Best Practices (PEP 8): https://pep8.org/  
17. Web Content Accessibility Guidelines (WCAG): https://www.w3.org/WAI/  
18. OWASP Security Guidelines: https://owasp.org/  
19. IEEE Standard for Software Requirements Specifications

## **12.3 Historial de Cambios**

Este documento será actualizado conforme avance el proyecto. Todos los cambios significativos serán registrados en la tabla de Control de Versiones al inicio del documento.

**FIN DEL DOCUMENTO**

*Este documento es propiedad de la institución y contiene información confidencial sobre el Sistema de Triaje Clínico.*