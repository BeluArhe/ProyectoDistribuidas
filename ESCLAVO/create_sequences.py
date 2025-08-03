#!/usr/bin/env python3
"""
Script para crear las secuencias necesarias en Oracle
"""

import os
import cx_Oracle
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_sequences():
    """Crea las secuencias necesarias para las tablas"""
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
        
        # Lista de secuencias a crear con sus valores iniciales
        sequences_to_create = [
            ('PRODUCTO_SEQ', 'PRODUCTO', 'ID_PRODUCTO'),
            ('CLIENTE_SEQ', 'CLIENTE_CHILLOGALLO', 'ID_CLIENTE'),
            ('SUCURSAL_SEQ', 'SUCURSAL_QS', 'ID_SUCURSAL'),
            ('EMPLEADO_SEQ', 'EMPLEADO_SUR', 'ID_EMPLEADO'),
            ('TARJETA_SEQ', 'TARJETA', 'ID_TARJETA'),
            ('FABRICA_SEQ', 'FABRICA', 'ID_FABRICA')
        ]
        
        print("\n🔢 Creando secuencias:")
        print("-" * 50)
        
        for seq_name, table_name, id_column in sequences_to_create:
            try:
                # Obtener el valor máximo actual de la tabla
                cursor.execute(f"SELECT NVL(MAX({id_column}), 0) + 1 FROM {table_name}")
                start_value = cursor.fetchone()[0]
                
                # Verificar si la secuencia ya existe
                cursor.execute(f"SELECT COUNT(*) FROM USER_SEQUENCES WHERE SEQUENCE_NAME = '{seq_name}'")
                seq_exists = cursor.fetchone()[0] > 0
                
                if seq_exists:
                    print(f"⚠️  {seq_name:<20} - Ya existe")
                    continue
                
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
                print(f"✅ {seq_name:<20} - Creada (inicia en {start_value})")
                
            except cx_Oracle.Error as e:
                print(f"❌ {seq_name:<20} - ERROR: {e}")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("\n✅ Secuencias creadas exitosamente")
        
    except cx_Oracle.Error as e:
        print(f"❌ Error de Oracle: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    create_sequences()
