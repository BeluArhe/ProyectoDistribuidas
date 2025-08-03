# Configuración de Base de Datos - DataRetail Esclavo

## Archivos de Configuración Creados

### 1. `.env` - Archivo de configuración principal
Contiene todas las variables de entorno necesarias para la conexión a Oracle Database.

### 2. `.env.example` - Plantilla de configuración
Archivo de ejemplo que puedes copiar para crear tu propio `.env`.

## Variables de Configuración Principales

### Conexión a Oracle (Esclavo)
```
ORACLE_HOST=localhost          # Host del servidor Oracle
ORACLE_PORT=1521              # Puerto de Oracle (por defecto 1521)
ORACLE_SERVICE_NAME=xe        # Nombre del servicio Oracle
ORACLE_USERNAME=hr            # Usuario de la base de datos
ORACLE_PASSWORD=hr            # Contraseña del usuario
```

### Conexión al Master (para vistas materializadas)
```
MASTER_HOST=localhost         # Host del servidor master
MASTER_PORT=1521             # Puerto del master
MASTER_SERVICE_NAME=xe       # Servicio del master
MASTER_USERNAME=hr           # Usuario del master
MASTER_PASSWORD=hr           # Contraseña del master
```

## Instrucciones de Configuración

### 1. Configurar Oracle Database

#### Para Oracle Express Edition (XE):
```sql
-- Conectar como SYSTEM o SYS
sqlplus system/password@xe

-- Crear usuario (si no existe)
CREATE USER hr IDENTIFIED BY hr;

-- Otorgar permisos necesarios
GRANT CONNECT, RESOURCE TO hr;
GRANT CREATE VIEW TO hr;
GRANT CREATE MATERIALIZED VIEW TO hr;
GRANT CREATE DATABASE LINK TO hr;
GRANT SELECT ANY TABLE TO hr;
GRANT CREATE TRIGGER TO hr;
GRANT CREATE SEQUENCE TO hr;

-- Otorgar cuota ilimitada en tablespace
ALTER USER hr QUOTA UNLIMITED ON USERS;
```

### 2. Crear Database Link al Master

```sql
-- Conectar como el usuario hr
sqlplus hr/hr@xe

-- Crear database link al master
CREATE DATABASE LINK dbl_master
CONNECT TO hr IDENTIFIED BY hr
USING '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=xe)))';

-- Probar el database link
SELECT COUNT(*) FROM dual@dbl_master;
```

### 3. Ejecutar Scripts de Base de Datos

```bash
# 1. Ejecutar el script master (en el servidor master)
sqlplus hr/hr@xe @database_setup.sql

# 2. Ejecutar el script esclavo (en el servidor esclavo)
sqlplus hr/hr@xe @database_setup_esclavo.sql
```

### 4. Verificar Configuración

```sql
-- Verificar tablas creadas
SELECT table_name FROM user_tables;

-- Verificar vistas materializadas
SELECT mview_name, refresh_mode, refresh_method FROM user_mviews;

-- Verificar database links
SELECT db_link FROM user_db_links;

-- Probar vistas materializadas
SELECT COUNT(*) FROM vw_producto;
SELECT COUNT(*) FROM vw_tarjeta;
SELECT COUNT(*) FROM vw_fabrica;
```

### 5. Actualizar Vistas Materializadas Manualmente

```sql
-- Actualizar todas las vistas
BEGIN
  DBMS_MVIEW.REFRESH('VW_PRODUCTO', 'C');
  DBMS_MVIEW.REFRESH('VW_TARJETA', 'C');
  DBMS_MVIEW.REFRESH('VW_FABRICA', 'C');
  COMMIT;
END;
/
```

## Ejecutar la Aplicación

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python app.py
```

## Solución de Problemas Comunes

### Error ORA-12514: TNS:listener does not currently know of service
- Verificar que el servicio Oracle esté ejecutándose
- Verificar el ORACLE_SERVICE_NAME en el archivo .env
- Verificar la configuración del listener

### Error ORA-01017: invalid username/password
- Verificar las credenciales en el archivo .env
- Verificar que el usuario existe en Oracle
- Verificar que el usuario tiene los permisos necesarios

### Error ORA-02019: connection description for remote database not found
- Verificar que el database link esté creado correctamente
- Verificar la conectividad con el servidor master
- Verificar la configuración del TNS

### Vistas materializadas no se crean
- Verificar que el database link funcione: `SELECT * FROM dual@dbl_master`
- Verificar que las tablas existan en el master
- Verificar permisos de SELECT en las tablas del master

## Seguridad

- **NUNCA** subir el archivo `.env` al repositorio
- Cambiar las credenciales por defecto en producción
- Usar contraseñas seguras
- Limitar los permisos del usuario a los mínimos necesarios
- Configurar firewall para limitar acceso a los puertos de Oracle
