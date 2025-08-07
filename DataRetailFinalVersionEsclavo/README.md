# DataRetail - Nodo Esclavo (Sistema Distribuido)

Sistema de gestión distribuida especializado como **nodo esclavo** con vistas materializadas para datos replicados y gestión local de datos fragmentados. Implementado con Oracle Database, Python Flask e interfaces web modernas.

## 🚀 Características del Nodo Esclavo

- ✅ **Vistas Materializadas**: Datos sincronizados desde el servidor maestro
- ✅ **Gestión Local**: CRUD completo para datos fragmentados por ubicación
- ✅ **Solo Lectura**: Productos, tarjetas y fábricas desde vistas materializadas
- ✅ **Auditoría Esclavo**: Registro de operaciones locales independiente
- ✅ **API REST Híbrida**: Endpoints de lectura y escritura según tipo de dato
- ✅ **Interfaz Moderna**: UI responsive con estilos unificados
- ✅ **Privacidad**: Números de tarjetas censurados automáticamente

## 📊 Arquitectura de Datos del Nodo Esclavo

### Tablas Locales (CRUD Completo)
- **`CLIENTE_CARAPUNGO`**: Clientes específicos de Carapungo
- **`SUCURSAL_QN`**: Sucursales de Quito-Norte solamente  
- **`EMPLEADO_NORTE`**: Empleados asignados al Norte
- **`AUDITORIA_ESCLAVO`**: Registro de operaciones del nodo esclavo

### Vistas Materializadas (Solo Lectura)
- **`VW_PRODUCTO`**: Catálogo completo sincronizado desde maestro
- **`VW_TARJETA`**: Información de tarjetas (números censurados)
- **`VW_FABRICA`**: Datos de fabricantes replicados

### Sistema de Auditoría Local
- **`AUDITORIA_ESCLAVO`**: Registro independiente de operaciones del nodo

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
Crea o edita el archivo `.env` con tus credenciales de Oracle (nodo esclavo):
```env
ORACLE_HOST=DISMAL-HP
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=orcl
ORACLE_USERNAME=esclavo
ORACLE_PASSWORD=esclavo
```

### 3. Verificar conexión a Oracle
El nodo esclavo se conecta automáticamente a la base de datos configurada.
No requiere creación de esquemas adicionales ya que usa vistas materializadas del maestro.

### 4. Ejecutar la aplicación esclavo
```bash
python app.py
```

### 5. Acceder al sistema
Abre tu navegador en: `http://localhost:5000`

## 📁 Estructura Completa del Proyecto

```
DataRetailFinalVersionEsclavo/
├── app.py                    # Aplicación Flask con API híbrida
├── .env                      # Variables de entorno del nodo esclavo
├── requirements.txt          # Dependencias Python
├── README.md                 # Esta documentación
├── templates/                # Plantillas HTML modernas
│   ├── simple_dashboard.html # Dashboard principal del esclavo
│   ├── productos_simple.html # Vista de productos (solo lectura)
│   ├── clientes_simple.html  # CRUD de clientes locales
│   ├── sucursales_simple.html# CRUD de sucursales locales
│   ├── empleados_simple.html # CRUD de empleados locales
│   ├── tarjetas_simple.html  # Vista de tarjetas (solo lectura)
│   ├── fabricas_simple.html  # Vista de fábricas (solo lectura)
│   └── auditoria_esclavo.html# Auditoría del nodo esclavo
└── static/                   # Archivos estáticos
    └── css/
        └── modern.css        # Estilos modernos unificados
```

## 🎯 Módulos del Nodo Esclavo

### 1. **Productos** (Vista Materializada - Solo Lectura)
- Datos sincronizados desde el servidor maestro
- Campos: ID, descripción, precio, stock, categoría
- **Sin operaciones CRUD** - Vista de solo lectura

### 2. **Clientes** (Tabla Local - CRUD Completo)
- Gestión local de clientes de Carapungo
- Campos: ID, nombre, dirección (fija: 'Carapungo'), teléfono
- **CRUD completo** con IDs auto-incrementales

### 3. **Sucursales** (Tabla Local - CRUD Completo)
- Gestión local de sucursales de Quito-Norte
- Campos: ID, nombre, ciudad (fija: 'Quito-Norte'), dirección
- **CRUD completo** con IDs auto-incrementales

### 4. **Empleados** (Tabla Local - CRUD Completo)
- Gestión local de empleados del Norte
- Campos: ID, nombre, sucursal (fija: 'Norte'), cargo
- **CRUD completo** con IDs auto-incrementales

### 5. **Tarjetas** (Vista Materializada - Solo Lectura)
- Datos sincronizados con **números censurados** por privacidad
- Campos: ID, número (****-****-****-XXXX), tipo
- **Sin operaciones CRUD** - Vista de solo lectura con privacidad

### 6. **Fábricas** (Vista Materializada - Solo Lectura)
- Datos de fabricantes sincronizados desde maestro
- Campos: ID, nombre, país
- **Sin operaciones CRUD** - Vista de solo lectura

### 7. **Auditoría Esclavo**
- Registro independiente de operaciones del nodo esclavo
- Solo visualización de registros locales
- Información específica del nodo esclavo

## 🔧 API Endpoints del Nodo Esclavo

### Productos (Vista Materializada - Solo Lectura)
- `GET /api/products` - Listar productos desde vista materializada
- `GET /api/products/{id}` - Obtener producto específico
- ❌ `POST/PUT/DELETE` - **Operaciones CRUD deshabilitadas**

### Clientes (Tabla Local - CRUD Completo)
- `GET /api/customers` - Listar clientes de Carapungo
- `POST /api/customers` - Crear cliente local
- `PUT /api/customers/{id}` - Actualizar cliente local
- `DELETE /api/customers/{id}` - Eliminar cliente local

### Sucursales (Tabla Local - CRUD Completo)
- `GET /api/sucursales` - Listar sucursales de Quito-Norte
- `POST /api/sucursales` - Crear sucursal local
- `PUT /api/sucursales/{id}` - Actualizar sucursal local
- `DELETE /api/sucursales/{id}` - Eliminar sucursal local

### Empleados (Tabla Local - CRUD Completo)
- `GET /api/empleados` - Listar empleados del Norte
- `POST /api/empleados` - Crear empleado local
- `PUT /api/empleados/{id}` - Actualizar empleado local
- `DELETE /api/empleados/{id}` - Eliminar empleado local

### Tarjetas (Vista Materializada - Solo Lectura con Privacidad)
- `GET /api/tarjetas` - Listar tarjetas (números censurados)
- `GET /api/tarjetas/{id}` - Obtener tarjeta específica (número censurado)
- ❌ `POST/PUT/DELETE` - **Operaciones CRUD deshabilitadas**

### Fábricas (Vista Materializada - Solo Lectura)
- `GET /api/fabricas` - Listar fábricas desde vista materializada
- `GET /api/fabricas/{id}` - Obtener fábrica específica
- ❌ `POST/PUT/DELETE` - **Operaciones CRUD deshabilitadas**

### Auditoría Esclavo
- `GET /api/auditoria_esclavo` - Obtener registros de auditoría del nodo esclavo

## � Características de Seguridad

### Privacidad de Datos Sensibles
- **Números de Tarjeta**: Se censuran automáticamente mostrando solo los últimos 4 dígitos
- **Acceso Controlado**: Las vistas materializadas son estrictamente de solo lectura

### Separación de Responsabilidades
- **Vistas Materializadas**: Solo consultas desde el nodo maestro
- **Tablas Locales**: CRUD completo con operaciones seguras
- **IDs Autogenerados**: Utiliza `MAX(ID) + 1` para evitar conflictos

## 📊 Auditoría del Nodo Esclavo

### Auditoría Específica del Nodo
- Registro independiente de operaciones del nodo esclavo
- Solo visualización de datos locales de `AUDITORIA_ESCLAVO`
- Información específica del comportamiento del nodo esclavo

## 🚨 Solución de Problemas

### Error de conexión Oracle:
```bash
# Verificar que Oracle esté ejecutándose
lsnrctl status

# Verificar credenciales del nodo esclavo
echo $ORACLE_USERNAME  # Linux/Mac
echo %ORACLE_USERNAME% # Windows
```

### Error DPI-1047 (Oracle Client):
```bash
# Windows: Agregar ruta al PATH
set PATH=%PATH%;C:\oracle\instantclient_19_x

# Linux: Configurar LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/lib/oracle/19.x/client64/lib
```

### Verificar vistas materializadas:
```sql
-- Verificar que las vistas estén disponibles
SELECT view_name FROM user_views WHERE view_name LIKE 'VW_%';

-- Verificar tabla de auditoría esclavo
SELECT COUNT(*) FROM AUDITORIA_ESCLAVO;
```

## 🔍 Monitoreo del Nodo Esclavo

### Consultas útiles para administración:
```sql
-- Ver registros de auditoría del esclavo
SELECT * FROM AUDITORIA_ESCLAVO ORDER BY fecha_hora DESC;

-- Verificar tablas locales
SELECT table_name FROM user_tables 
WHERE table_name IN ('CLIENTE_CARAPUNGO', 'EMPLEADO_NORTE', 'SUCURSAL_QN');
```

## 💡 Características Técnicas del Nodo Esclavo

- **Backend**: Python 3.8+, Flask 2.3+, cx_Oracle, flask-cors
- **Base de Datos**: Oracle Database con vistas materializadas y tablas locales
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla) con diseño moderno unificado
- **Auditoría**: Registro específico del nodo esclavo en `AUDITORIA_ESCLAVO`
- **Seguridad**: Variables de entorno, censura de datos sensibles, separación de accesos
- **Arquitectura**: Nodo esclavo especializado con responsabilidades específicas

## 🎯 Funcionalidades Destacadas

- ✅ **Híbrido**: Vistas materializadas (solo lectura) + Tablas locales (CRUD)
- ✅ **Privacidad**: Números de tarjeta censurados automáticamente
- ✅ **IDs Seguros**: Generación automática con `MAX(ID) + 1`
- ✅ **Interfaz Moderna**: Diseño unificado y responsivo
- ✅ **Auditoría Específica**: Registro independiente del nodo esclavo

---

## 🏁 Estado del Proyecto

**✨ Producción Lista** - El nodo esclavo está completamente funcional con todas las características implementadas y documentadas.
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para problemas específicos de Oracle o fragmentación:
1. Consulta la documentación de Oracle Database
2. Revisa los logs de auditoría en la tabla `auditoria_master`
3. Verifica las restricciones de fragmentación con las consultas proporcionadas
