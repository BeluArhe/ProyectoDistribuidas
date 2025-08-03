#!/usr/bin/env python3
"""
Script de prueba para verificar conexión y tablas de Oracle
"""

import os
import cx_Oracle
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_oracle_connection():
    """Prueba la conexión a Oracle y verifica las tablas"""
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
        
        # Lista de tablas que deberían existir
        tables_to_check = [
            'PRODUCTO',
            'CLIENTE_CHILLOGALLO', 
            'SUCURSAL_QS',
            'EMPLEADO_SUR',
            'TARJETA',
            'FABRICA'
        ]
        
        print("\n📋 Verificando tablas:")
        print("-" * 50)
        
        for table_name in tables_to_check:
            try:
                # Verificar si la tabla existe
                cursor.execute(f"SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = '{table_name}'")
                table_exists = cursor.fetchone()[0] > 0
                
                if table_exists:
                    # Contar registros
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"✅ {table_name:<20} - {count} registros")
                    
                    # Mostrar estructura de la tabla
                    cursor.execute(f"SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{table_name}' ORDER BY COLUMN_ID")
                    columns = [row[0] for row in cursor.fetchall()]
                    print(f"   Columnas: {', '.join(columns)}")
                    
                    # Mostrar algunos datos de ejemplo si hay registros
                    if count > 0:
                        cursor.execute(f"SELECT * FROM {table_name} WHERE ROWNUM <= 3")
                        rows = cursor.fetchall()
                        print(f"   Datos ejemplo: {rows}")
                    print()
                else:
                    print(f"❌ {table_name:<20} - NO EXISTE")
                    
            except cx_Oracle.Error as e:
                print(f"❌ {table_name:<20} - ERROR: {e}")
        
        # Verificar secuencias
        print("\n🔢 Verificando secuencias:")
        print("-" * 50)
        sequences_to_check = [
            'producto_seq',
            'cliente_seq',
            'sucursal_seq', 
            'empleado_seq',
            'tarjeta_seq',
            'fabrica_seq'
        ]
        
        for seq_name in sequences_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM USER_SEQUENCES WHERE SEQUENCE_NAME = UPPER('{seq_name}')")
                seq_exists = cursor.fetchone()[0] > 0
                
                if seq_exists:
                    cursor.execute(f"SELECT {seq_name}.NEXTVAL FROM DUAL")
                    next_val = cursor.fetchone()[0]
                    print(f"✅ {seq_name:<20} - Próximo valor: {next_val}")
                else:
                    print(f"❌ {seq_name:<20} - NO EXISTE")
                    
            except cx_Oracle.Error as e:
                print(f"❌ {seq_name:<20} - ERROR: {e}")
        
        cursor.close()
        connection.close()
        print("\n✅ Prueba completada")
        
    except cx_Oracle.Error as e:
        print(f"❌ Error de Oracle: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    test_oracle_connection()
