# DataRetail - Sistema de Gestión Distribuida con Oracle

Sistema completo de gestión distribuida con fragmentación de datos, replicación y auditoría automática usando Oracle Database, Python Flask y interfaces web HTML.

## 🚀 Características del Sistema Distribuido

- ✅ **Fragmentación Horizontal**: Datos divididos por ubicación geográfica
- ✅ **Replicación**: Tablas maestras disponibles en todos los nodos
- ✅ **Auditoría Automática**: Triggers que registran todas las operaciones
- ✅ **API REST Completa**: Endpoints para todas las tablas
- ✅ **Interfaz Web Responsive**: Gestión visual de todos los módulos
- ✅ **Conexión Oracle nativa**: Usando cx_Oracle

## 📊 Arquitectura de Datos

### Tablas Fragmentadas (Quito-Sur)
- **`sucursal_qs`**: Solo sucursales de Quito-Sur
- **`cliente_chillogallo`**: Solo clientes de Chillogallo
- **`empleado_sur`**: Solo empleados del Sur

### Tablas Replicadas (Disponibles en todos los nodos)
- **`producto`**: Catálogo completo de productos
- **`tarjeta`**: Información de tarjetas de pago
- **`fabrica`**: Datos de fabricantes

### Sistema de Auditoría
- **`auditoria_master`**: Registro automático de todas las operaciones (INSERT, UPDATE, DELETE)

## 📋 Requisitos Previos

### Software Necesario:
1. **Python 3.8+** - [Descargar Python](https://www.python.org/downloads/)
2. **Oracle Database** - Cualquiera de estas opciones:
   - Oracle Database XE (Express Edition) - Gratuita
   - Oracle Database en Docker
   - Oracle Cloud Always Free
3. **Oracle Instant Client** - [Descargar aquí](https://www.oracle.com/database/technologies/instant-client.html)

### Configuración Oracle Instant Client:
1. Descarga Oracle Instant Client para tu sistema operativo
2. Extrae los archivos
3. Agrega la ruta al PATH del sistema

## 🛠️ Instalación

### 1. Preparar el entorno
```bash
cd DataRetail
python -m venv venv
venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
Edita el archivo `.env` con tus credenciales de Oracle:
```env
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=ORCL
ORACLE_USERNAME=tu_usuario
ORACLE_PASSWORD=tu_password
```

### 3. Crear la base de datos
Ejecuta el script SQL en tu base de datos Oracle:
```bash
sqlplus tu_usuario/tu_password@localhost:1521/ORCL @database_setup.sql
```

### 4. Ejecutar la aplicación
```bash
python app.py
```

### 5. Acceder al sistema
Abre tu navegador en: `http://localhost:5000`

## 📁 Estructura Completa del Proyecto

```
DataRetail/
├── app.py                  # Aplicación Flask con todos los endpoints
├── database.py            # Clase de conexión Oracle
├── models.py              # Modelos para todas las tablas
├── requirements.txt       # Dependencias Python
├── .env                   # Variables de entorno
├── database_setup.sql     # Script completo de BD
├── README.md              # Esta documentación
├── templates/             # Plantillas HTML
│   ├── index.html         # Dashboard principal
│   ├── products.html      # Gestión de productos
│   ├── customers.html     # Gestión de clientes
│   ├── sucursales.html    # Gestión de sucursales
│   ├── empleados.html     # Gestión de empleados
│   ├── tarjetas.html      # Gestión de tarjetas
│   ├── fabricas.html      # Gestión de fábricas
│   └── auditoria.html     # Visualización de auditoría
└── static/               # Archivos estáticos
    ├── css/
    │   └── style.css      # Estilos responsivos
    └── js/
        ├── products.js    # Lógica de productos
        └── customers.js   # Lógica de clientes
```

## 🎯 Módulos del Sistema

### 1. **Productos** (Tabla Replicada)
- Gestión completa de productos
- Campos: ID, nombre, precio
- Disponible en todos los nodos

### 2. **Clientes** (Tabla Fragmentada)
- Solo clientes de Chillogallo
- Campos: ID, nombre, dirección (fija), teléfono
- Restricción: `direccion = 'Chillogallo'`

### 3. **Sucursales** (Tabla Fragmentada)
- Solo sucursales de Quito-Sur
- Campos: ID, nombre, ciudad (fija), dirección
- Restricción: `ciudad = 'Quito-Sur'`

### 4. **Empleados** (Tabla Fragmentada)
- Solo empleados del Sur
- Campos: ID, nombre, sucursal (fija), cargo
- Restricción: `sucursal = 'Sur'`

### 5. **Tarjetas** (Tabla Replicada)
- Información de tarjetas de pago
- Campos: ID, tipo, número
- Disponible en todos los nodos

### 6. **Fábricas** (Tabla Replicada)
- Datos de fabricantes
- Campos: ID, nombre, país
- Disponible en todos los nodos

### 7. **Auditoría**
- Visualización de todas las operaciones
- Filtros por tabla
- Información: usuario, fecha, operación, datos anteriores/nuevos

## 🔧 API Endpoints

### Productos (Replicada)
- `GET /api/products` - Listar productos
- `POST /api/products` - Crear producto
- `PUT /api/products/{id}` - Actualizar producto
- `DELETE /api/products/{id}` - Eliminar producto

### Clientes (Fragmentada - Chillogallo)
- `GET /api/customers` - Listar clientes
- `POST /api/customers` - Crear cliente
- `PUT /api/customers/{id}` - Actualizar cliente
- `DELETE /api/customers/{id}` - Eliminar cliente

### Sucursales (Fragmentada - Quito-Sur)
- `GET /api/sucursales` - Listar sucursales
- `POST /api/sucursales` - Crear sucursal
- `PUT /api/sucursales/{id}` - Actualizar sucursal
- `DELETE /api/sucursales/{id}` - Eliminar sucursal

### Empleados (Fragmentada - Sur)
- `GET /api/empleados` - Listar empleados
- `POST /api/empleados` - Crear empleado
- `PUT /api/empleados/{id}` - Actualizar empleado
- `DELETE /api/empleados/{id}` - Eliminar empleado

### Tarjetas (Replicada)
- `GET /api/tarjetas` - Listar tarjetas
- `POST /api/tarjetas` - Crear tarjeta
- `PUT /api/tarjetas/{id}` - Actualizar tarjeta
- `DELETE /api/tarjetas/{id}` - Eliminar tarjeta

### Fábricas (Replicada)
- `GET /api/fabricas` - Listar fábricas
- `POST /api/fabricas` - Crear fábrica
- `PUT /api/fabricas/{id}` - Actualizar fábrica
- `DELETE /api/fabricas/{id}` - Eliminar fábrica

### Auditoría
- `GET /api/auditoria` - Obtener registros de auditoría
- `GET /api/auditoria?table={nombre}` - Filtrar por tabla

## 🔒 Seguridad y Auditoría

### Triggers Automáticos
Cada tabla tiene triggers que registran automáticamente:
- **INSERT**: Nuevos registros
- **UPDATE**: Modificaciones
- **DELETE**: Eliminaciones

### Información de Auditoría
- Usuario que realizó la operación
- Fecha y hora exacta
- Tipo de operación (I/U/D)
- Valores anteriores y nuevos
- Tabla afectada

## 🚨 Solución de Problemas

### Error de conexión Oracle:
```bash
# Verificar que Oracle esté ejecutándose
lsnrctl status

# Verificar Oracle Instant Client
echo $ORACLE_HOME  # Linux/Mac
echo %ORACLE_HOME% # Windows
```

### Error DPI-1047 (Oracle Client):
```bash
# Windows: Agregar ruta al PATH
set PATH=%PATH%;C:\oracle\instantclient_19_x

# Linux: Configurar LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/lib/oracle/19.x/client64/lib
```

### Verificar restricciones de fragmentación:
```sql
-- Verificar que las restricciones estén activas
SELECT constraint_name, status FROM user_constraints 
WHERE constraint_type = 'C' AND constraint_name LIKE 'CHK_%';
```

## � Monitoreo del Sistema

### Consultas útiles para administración:
```sql
-- Ver registros por tabla
SELECT nombre_table, COUNT(*) as registros 
FROM auditoria_master 
GROUP BY nombre_table;

-- Operaciones recientes
SELECT * FROM auditoria_master 
WHERE fecha >= SYSDATE - 1 
ORDER BY fecha DESC;

-- Verificar fragmentación
SELECT 'Clientes Chillogallo', COUNT(*) FROM cliente_chillogallo
UNION ALL
SELECT 'Sucursales Quito-Sur', COUNT(*) FROM sucursal_qs
UNION ALL
SELECT 'Empleados Sur', COUNT(*) FROM empleado_sur;
```

## � Características Técnicas

- **Backend**: Python 3.8+, Flask 2.3+, cx_Oracle
- **Base de Datos**: Oracle Database con fragmentación y replicación
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Auditoría**: Triggers automáticos PL/SQL
- **Seguridad**: Variables de entorno, parámetros preparados
- **Arquitectura**: Sistema distribuido con fragmentación horizontal

## 🤝 Contribución

1. Fork del proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para problemas específicos de Oracle o fragmentación:
1. Consulta la documentación de Oracle Database
2. Revisa los logs de auditoría en la tabla `auditoria_master`
3. Verifica las restricciones de fragmentación con las consultas proporcionadas
