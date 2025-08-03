from database import db

class ProductModel:
    """Modelo para gestionar productos en Oracle Database"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los productos"""
        query = "SELECT * FROM PRODUCTO ORDER BY id_producto"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(product_id):
        """Obtiene un producto por ID"""
        query = "SELECT * FROM PRODUCTO WHERE id_producto = :id"
        result = db.execute_query(query, {'id': product_id})
        return result[0] if result else None
    
    @staticmethod
    def create(nombre, precio):
        """Crea un nuevo producto"""
        query = """
        INSERT INTO PRODUCTO (id_producto, nombre, precio) 
        VALUES (producto_seq.NEXTVAL, :nombre, :precio)
        """
        params = {
            'nombre': nombre,
            'precio': precio
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def update(product_id, nombre, precio):
        """Actualiza un producto existente"""
        query = """
        UPDATE PRODUCTO 
        SET nombre = :nombre, precio = :precio
        WHERE id_producto = :id
        """
        params = {
            'id': product_id,
            'nombre': nombre,
            'precio': precio
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def delete(product_id):
        """Elimina un producto"""
        query = "DELETE FROM PRODUCTO WHERE id_producto = :id"
        return db.execute_dml(query, {'id': product_id})

class ClienteChillogattoModel:
    """Modelo para gestionar clientes de Chillogallo en Oracle Database"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los clientes"""
        query = "SELECT * FROM CLIENTE_CHILLOGALLO ORDER BY id_cliente"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(cliente_id):
        """Obtiene un cliente por ID"""
        query = "SELECT * FROM CLIENTE_CHILLOGALLO WHERE id_cliente = :id"
        result = db.execute_query(query, {'id': cliente_id})
        return result[0] if result else None
    
    @staticmethod
    def create(nombre, telefono):
        """Crea un nuevo cliente"""
        query = """
        INSERT INTO CLIENTE_CHILLOGALLO (id_cliente, nombre, direccion, telefono) 
        VALUES (cliente_seq.NEXTVAL, :nombre, 'Chillogallo', :telefono)
        """
        params = {
            'nombre': nombre,
            'telefono': telefono
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def update(cliente_id, nombre, telefono):
        """Actualiza un cliente existente"""
        query = """
        UPDATE CLIENTE_CHILLOGALLO 
        SET nombre = :nombre, telefono = :telefono
        WHERE id_cliente = :id
        """
        params = {
            'id': cliente_id,
            'nombre': nombre,
            'telefono': telefono
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def delete(cliente_id):
        """Elimina un cliente"""
        query = "DELETE FROM CLIENTE_CHILLOGALLO WHERE id_cliente = :id"
        return db.execute_dml(query, {'id': cliente_id})

class SucursalQSModel:
    """Modelo para gestionar sucursales de Quito-Sur"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las sucursales"""
        query = "SELECT * FROM SUCURSAL_QS ORDER BY id_sucursal"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(sucursal_id):
        """Obtiene una sucursal por ID"""
        query = "SELECT * FROM SUCURSAL_QS WHERE id_sucursal = :id"
        result = db.execute_query(query, {'id': sucursal_id})
        return result[0] if result else None
    
    @staticmethod
    def create(nombre, direccion=None):
        """Crea una nueva sucursal"""
        query = """
        INSERT INTO SUCURSAL_QS (id_sucursal, nombre, ciudad, direccion) 
        VALUES (sucursal_seq.NEXTVAL, :nombre, 'Quito-Sur', :direccion)
        """
        params = {
            'nombre': nombre,
            'direccion': direccion
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def update(sucursal_id, nombre, direccion=None):
        """Actualiza una sucursal existente"""
        query = """
        UPDATE SUCURSAL_QS 
        SET nombre = :nombre, direccion = :direccion
        WHERE id_sucursal = :id
        """
        params = {
            'id': sucursal_id,
            'nombre': nombre,
            'direccion': direccion
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def delete(sucursal_id):
        """Elimina una sucursal"""
        query = "DELETE FROM SUCURSAL_QS WHERE id_sucursal = :id"
        return db.execute_dml(query, {'id': sucursal_id})

class EmpleadoSurModel:
    """Modelo para gestionar empleados del Sur"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los empleados"""
        query = "SELECT * FROM EMPLEADO_SUR ORDER BY id_empleado"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(empleado_id):
        """Obtiene un empleado por ID"""
        query = "SELECT * FROM EMPLEADO_SUR WHERE id_empleado = :id"
        result = db.execute_query(query, {'id': empleado_id})
        return result[0] if result else None
    
    @staticmethod
    def create(nombre, cargo):
        """Crea un nuevo empleado"""
        query = """
        INSERT INTO EMPLEADO_SUR (id_empleado, nombre, sucursal, cargo) 
        VALUES (empleado_seq.NEXTVAL, :nombre, 'Sur', :cargo)
        """
        params = {
            'nombre': nombre,
            'cargo': cargo
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def update(empleado_id, nombre, cargo):
        """Actualiza un empleado existente"""
        query = """
        UPDATE EMPLEADO_SUR 
        SET nombre = :nombre, cargo = :cargo
        WHERE id_empleado = :id
        """
        params = {
            'id': empleado_id,
            'nombre': nombre,
            'cargo': cargo
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def delete(empleado_id):
        """Elimina un empleado"""
        query = "DELETE FROM EMPLEADO_SUR WHERE id_empleado = :id"
        return db.execute_dml(query, {'id': empleado_id})

class TarjetaModel:
    """Modelo para gestionar tarjetas"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las tarjetas"""
        query = "SELECT * FROM TARJETA ORDER BY id_tarjeta"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(tarjeta_id):
        """Obtiene una tarjeta por ID"""
        query = "SELECT * FROM TARJETA WHERE id_tarjeta = :id"
        result = db.execute_query(query, {'id': tarjeta_id})
        return result[0] if result else None
    
    @staticmethod
    def create(tipo, numero):
        """Crea una nueva tarjeta"""
        query = """
        INSERT INTO TARJETA (id_tarjeta, tipo, numero) 
        VALUES (tarjeta_seq.NEXTVAL, :tipo, :numero)
        """
        params = {
            'tipo': tipo,
            'numero': numero
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def update(tarjeta_id, tipo, numero):
        """Actualiza una tarjeta existente"""
        query = """
        UPDATE TARJETA 
        SET tipo = :tipo, numero = :numero
        WHERE id_tarjeta = :id
        """
        params = {
            'id': tarjeta_id,
            'tipo': tipo,
            'numero': numero
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def delete(tarjeta_id):
        """Elimina una tarjeta"""
        query = "DELETE FROM TARJETA WHERE id_tarjeta = :id"
        return db.execute_dml(query, {'id': tarjeta_id})

class FabricaModel:
    """Modelo para gestionar fábricas"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las fábricas"""
        query = "SELECT * FROM FABRICA ORDER BY id_fabrica"
        return db.execute_query(query)
    
    @staticmethod
    def get_by_id(fabrica_id):
        """Obtiene una fábrica por ID"""
        query = "SELECT * FROM FABRICA WHERE id_fabrica = :id"
        result = db.execute_query(query, {'id': fabrica_id})
        return result[0] if result else None
    
    @staticmethod
    def create(nombre, pais):
        """Crea una nueva fábrica"""
        query = """
        INSERT INTO FABRICA (id_fabrica, nombre, pais) 
        VALUES (fabrica_seq.NEXTVAL, :nombre, :pais)
        """
        params = {
            'nombre': nombre,
            'pais': pais
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def update(fabrica_id, nombre, pais):
        """Actualiza una fábrica existente"""
        query = """
        UPDATE FABRICA 
        SET nombre = :nombre, pais = :pais
        WHERE id_fabrica = :id
        """
        params = {
            'id': fabrica_id,
            'nombre': nombre,
            'pais': pais
        }
        return db.execute_dml(query, params)
    
    @staticmethod
    def delete(fabrica_id):
        """Elimina una fábrica"""
        query = "DELETE FROM FABRICA WHERE id_fabrica = :id"
        return db.execute_dml(query, {'id': fabrica_id})

class AuditoriaModel:
    """Modelo para consultar auditoría"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los registros de auditoría"""
        query = """
        SELECT id_auditoria, user_name, fecha, tipo_operacion, nombre_table, anterior, nuevo
        FROM auditoria_master 
        ORDER BY fecha DESC
        """
        return db.execute_query(query)
    
    @staticmethod
    def get_by_table(table_name):
        """Obtiene auditoría por tabla"""
        query = """
        SELECT id_auditoria, user_name, fecha, tipo_operacion, nombre_table, anterior, nuevo
        FROM auditoria_master 
        WHERE nombre_table = :table_name
        ORDER BY fecha DESC
        """
        return db.execute_query(query, {'table_name': table_name})
    
    @staticmethod
    def get_recent(limit=50):
        """Obtiene los registros más recientes de auditoría"""
        query = """
        SELECT * FROM (
            SELECT id_auditoria, user_name, fecha, tipo_operacion, nombre_table, anterior, nuevo
            FROM auditoria_master 
            ORDER BY fecha DESC
        ) WHERE ROWNUM <= :limit
        """
        return db.execute_query(query, {'limit': limit})
