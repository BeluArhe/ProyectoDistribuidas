#!/usr/bin/env python3
"""
Script para crear SOLO las secuencias necesarias (sin recrear tablas)
"""

import os
import cx_Oracle
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_missing_sequences():
    """Crea solo las secuencias que faltan"""
    try:
        # Configuración de conexión
        host = os.getenv('ORACLE_HOST', 'DESKTOP-IFVF9EL')
        port = os.getenv('ORACLE_PORT', '1521')
        service_name = os.getenv('ORACLE_SERVICE_NAME', 'orcl')
        username = os.getenv('ORACLE_USERNAME', 'master')
        password = os.getenv('ORACLE_PASSWORD', 'master')
        
        # DSN de conexión
        dsn = f"{host}:{port}/{service_name}"
        print(f"🔗 Conectando a Oracle: {username}@{dsn}")
        
        # Conectar a Oracle
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        cursor = connection.cursor()
        print("✅ Conexión exitosa a Oracle Database")
        
        # Secuencias a crear con valores iniciales basados en datos existentes
        sequences_data = [
            ('producto_seq', 'PRODUCTO', 'ID_PRODUCTO'),
            ('cliente_seq', 'CLIENTE_CHILLOGALLO', 'ID_CLIENTE'),  
            ('sucursal_seq', 'SUCURSAL_QS', 'ID_SUCURSAL'),
            ('empleado_seq', 'EMPLEADO_SUR', 'ID_EMPLEADO'),
            ('tarjeta_seq', 'TARJETA', 'ID_TARJETA'),
            ('fabrica_seq', 'FABRICA', 'ID_FABRICA')
        ]
        
        print("\n🔢 Creando secuencias necesarias:")
        print("-" * 60)
        
        for seq_name, table_name, id_column in sequences_data:
            try:
                # Verificar si la secuencia ya existe
                cursor.execute(f"SELECT COUNT(*) FROM USER_SEQUENCES WHERE SEQUENCE_NAME = UPPER('{seq_name}')")
                seq_exists = cursor.fetchone()[0] > 0
                
                if seq_exists:
                    print(f"⚠️  {seq_name:<20} - Ya existe, saltando...")
                    continue
                
                # Obtener el valor máximo actual de la tabla
                cursor.execute(f"SELECT NVL(MAX({id_column}), 0) + 1 FROM {table_name}")
                start_value = cursor.fetchone()[0]
                
                # Crear la secuencia
                create_seq_sql = f"""
                CREATE SEQUENCE {seq_name}
                START WITH {start_value}
                INCREMENT BY 1
                NOCACHE
                NOORDER
                NOCYCLE
                """
                
                cursor.execute(create_seq_sql)
                print(f"✅ {seq_name:<20} - Creada exitosamente (inicia en {start_value})")
                
            except cx_Oracle.Error as e:
                print(f"❌ {seq_name:<20} - ERROR: {e}")
        
        # Confirmar cambios
        connection.commit()
        
        print("\n🎯 Verificando secuencias creadas:")
        print("-" * 60)
        
        for seq_name, _, _ in sequences_data:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM USER_SEQUENCES WHERE SEQUENCE_NAME = UPPER('{seq_name}')")
                seq_exists = cursor.fetchone()[0] > 0
                
                if seq_exists:
                    cursor.execute(f"SELECT {seq_name}.NEXTVAL FROM DUAL")
                    next_val = cursor.fetchone()[0]
                    # Devolver el valor
                    cursor.execute(f"SELECT {seq_name}.CURRVAL FROM DUAL") 
                    curr_val = cursor.fetchone()[0]
                    print(f"✅ {seq_name:<20} - Funcionando (valor actual: {curr_val})")
                else:
                    print(f"❌ {seq_name:<20} - NO CREADA")
                    
            except cx_Oracle.Error as e:
                print(f"❌ {seq_name:<20} - ERROR AL VERIFICAR: {e}")
        
        cursor.close()
        connection.close()
        print("\n✅ Proceso completado - Las secuencias están listas")
        
    except cx_Oracle.Error as e:
        print(f"❌ Error de Oracle: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    create_missing_sequences()
