import cx_Oracle
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class OracleDatabase:
    def __init__(self):
        self.host = os.getenv('ORACLE_HOST')
        self.port = os.getenv('ORACLE_PORT')
        self.service_name = os.getenv('ORACLE_SERVICE_NAME')
        self.username = os.getenv('ORACLE_USERNAME')
        self.password = os.getenv('ORACLE_PASSWORD')
        self.connection = None
    
    def connect(self):
        """Establece conexión con Oracle Database"""
        try:
            # Crear DSN (Data Source Name)
            dsn = cx_Oracle.makedsn(
                host=self.host,
                port=self.port,
                service_name=self.service_name
            )
            
            # Establecer conexión
            self.connection = cx_Oracle.connect(
                user=self.username,
                password=self.password,
                dsn=dsn
            )
            print("Conexión exitosa a Oracle Database")
            return True
            
        except cx_Oracle.Error as error:
            print(f"Error al conectar con Oracle: {error}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con Oracle Database"""
        try:
            if self.connection and self.connection.ping():
                self.connection.close()
                print("Conexión cerrada")
        except:
            # La conexión ya está cerrada o no es válida
            pass
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        try:
            # Verificar si la conexión está activa
            if not self.connection or not self.connection.ping():
                print("Reconectando a Oracle...")
                self.connect()
            
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Obtener nombres de columnas
            columns = [desc[0] for desc in cursor.description]
            
            # Obtener datos
            rows = cursor.fetchall()
            
            # Convertir a lista de diccionarios
            result = []
            for row in rows:
                result.append(dict(zip(columns, row)))
            
            cursor.close()
            return result
            
        except cx_Oracle.Error as error:
            print(f"Error ejecutando consulta: {error}")
            return []
    
    def execute_dml(self, query, params=None):
        """Ejecuta operaciones INSERT, UPDATE, DELETE"""
        try:
            # Verificar si la conexión está activa
            if not self.connection or not self.connection.ping():
                print("Reconectando a Oracle...")
                self.connect()
                
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            
            return affected_rows
            
        except cx_Oracle.Error as error:
            print(f"Error ejecutando DML: {error}")
            if self.connection:
                self.connection.rollback()
            return None

# Instancia global de la base de datos
db = OracleDatabase()
