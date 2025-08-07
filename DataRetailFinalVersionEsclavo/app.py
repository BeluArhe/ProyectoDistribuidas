from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cx_Oracle
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de Oracle
ORACLE_CONFIG = {
    'username': os.getenv('ORACLE_USERNAME', 'esclavo'),
    'password': os.getenv('ORACLE_PASSWORD', 'esclavo'),
    'host': os.getenv('ORACLE_HOST', 'DISMAL-HP'),
    'port': os.getenv('ORACLE_PORT', '1521'),
    'service_name': os.getenv('ORACLE_SERVICE_NAME', 'orcl')
}

def get_oracle_connection():
    """Obtiene una conexión fresca a Oracle"""
    dsn = cx_Oracle.makedsn(
        ORACLE_CONFIG['host'], 
        ORACLE_CONFIG['port'], 
        service_name=ORACLE_CONFIG['service_name']
    )
    return cx_Oracle.connect(
        ORACLE_CONFIG['username'], 
        ORACLE_CONFIG['password'], 
        dsn
    )

def execute_query(query, params=None):
    """Ejecuta una query y retorna resultados"""
    try:
        with get_oracle_connection() as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Error ejecutando query: {e}")
        return []

def execute_dml(query, params=None):
    """Ejecuta INSERT/UPDATE/DELETE"""
    try:
        with get_oracle_connection() as connection:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                connection.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error ejecutando DML: {e}")
        return 0

def initialize_database():
    """Inicializa la conexión a la base de datos"""
    try:
        # Test simple de conexión
        with get_oracle_connection() as conn:
            print("✅ Conexión a Oracle establecida correctamente")
            return True
    except Exception as e:
        print(f"❌ Error conectando a Oracle: {e}")
        return False

# ================ RUTAS PRINCIPALES ================

@app.route('/test')
def test():
    """Endpoint de prueba"""
    return jsonify({'status': 'OK', 'message': 'Servidor funcionando correctamente'})

@app.route('/')
def index():
    """Dashboard principal simple"""
    return render_template('simple_dashboard.html')

@app.route('/productos')
def productos():
    """Página de gestión de productos"""
    return render_template('productos_simple.html')

@app.route('/clientes') 
def clientes():
    """Página de gestión de clientes"""
    return render_template('clientes_simple.html')

@app.route('/sucursales')
def sucursales():
    """Página de gestión de sucursales"""
    return render_template('sucursales_simple.html')

@app.route('/empleados')
def empleados():
    """Página de gestión de empleados"""
    return render_template('empleados_simple.html')

@app.route('/tarjetas')
def tarjetas():
    """Página de gestión de tarjetas"""
    return render_template('tarjetas_simple.html')

@app.route('/fabricas')
def fabricas():
    """Página de gestión de fábricas"""  
    return render_template('fabricas_simple.html')



# Página de auditoría esclavo (única)
@app.route('/auditoria_esclavo')
def auditoria_esclavo():
    return render_template('auditoria_esclavo.html')

# ================ API ENDPOINTS PARA PRODUCTOS ================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Obtiene todos los productos"""
    try:
        query = "SELECT * FROM VW_PRODUCTO ORDER BY id_producto"
        products = execute_query(query)
        print(f"DEBUG: Productos obtenidos: {len(products) if products else 0}")
        if products is None:
            return jsonify({'success': False, 'data': [], 'error': 'No se pudieron obtener productos'}), 200
        return jsonify({'success': True, 'data': products})
    except Exception as e:
        print(f"ERROR en get_products: {str(e)}")
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Obtiene un producto por ID"""
    try:
        query = "SELECT * FROM VW_PRODUCTO WHERE id_producto = :id"
        result = execute_query(query, {'id': product_id})
        if result:
            return jsonify(result[0])
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Crea un nuevo producto - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Los productos son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Los productos son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un producto - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Los productos son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

# ================ API ENDPOINTS PARA CLIENTES ================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Obtiene todos los clientes"""
    try:
        query = "SELECT * FROM CLIENTE_CARAPUNGO ORDER BY id_cliente"
        customers = execute_query(query)
        print(f"DEBUG: Clientes obtenidos: {len(customers) if customers else 0}")
        if customers is None:
            return jsonify({'success': False, 'data': [], 'error': 'No se pudieron obtener clientes'}), 200
        return jsonify({'success': True, 'data': customers})
    except Exception as e:
        print(f"ERROR en get_customers: {str(e)}")
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Obtiene un cliente por ID"""
    try:
        query = "SELECT * FROM CLIENTE_CARAPUNGO WHERE id_cliente = :id"
        result = execute_query(query, {'id': customer_id})
        if result:
            return jsonify(result[0])
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Crea un nuevo cliente"""
    try:
        data = request.json
        
        # Obtener el siguiente ID (max + 1)
        with get_oracle_connection() as connection:
            with connection.cursor() as cursor:
                # Obtener el ID máximo actual
                cursor.execute("SELECT NVL(MAX(id_cliente), 0) + 1 FROM CLIENTE_CARAPUNGO")
                next_id = cursor.fetchone()[0]
                
                # Insertar con el nuevo ID
                query = """
                INSERT INTO CLIENTE_CARAPUNGO (id_cliente, nombre, direccion, telefono) 
                VALUES (:id_cliente, :nombre, 'Carapungo', :telefono)
                """
                params = {
                    'id_cliente': next_id,
                    'nombre': data['nombre'],
                    'telefono': data['telefono']
                }
                
                cursor.execute(query, params)
                connection.commit()
                
                return jsonify({'success': True, 'message': f'Cliente creado exitosamente con ID {next_id}'})
                
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Actualiza un cliente"""
    try:
        data = request.json
        query = """
        UPDATE CLIENTE_CARAPUNGO 
        SET nombre = :nombre, telefono = :telefono
        WHERE id_cliente = :id
        """
        params = {
            'nombre': data['nombre'],
            'telefono': data['telefono'],
            'id': customer_id
        }
        result = execute_dml(query, params)
        if result > 0:
            return jsonify({'success': True, 'message': 'Cliente actualizado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al actualizar cliente'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Elimina un cliente"""
    try:
        query = "DELETE FROM CLIENTE_CARAPUNGO WHERE id_cliente = :id"
        result = execute_dml(query, {'id': customer_id})
        if result > 0:
            return jsonify({'success': True, 'message': 'Cliente eliminado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al eliminar cliente'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ================ API ENDPOINTS PARA SUCURSALES ================

@app.route('/api/sucursales/test', methods=['GET'])
def test_sucursales():
    """Test directo sin modelos"""
    return jsonify({'success': True, 'data': [{'id': 1, 'nombre': 'Test', 'ciudad': 'Quito-Norte', 'direccion': 'Test Dir'}]})

@app.route('/api/sucursales', methods=['GET'])
def get_sucursales():
    """Obtiene todas las sucursales"""
    try:
        query = "SELECT * FROM SUCURSAL_QN ORDER BY id_sucursal"
        sucursales = execute_query(query)
        print(f"DEBUG: Sucursales obtenidas: {len(sucursales) if sucursales else 0}")
        if sucursales is None:
            return jsonify({'success': False, 'data': [], 'error': 'No se pudieron obtener sucursales'}), 200
        return jsonify({'success': True, 'data': sucursales})
    except Exception as e:
        print(f"ERROR en get_sucursales: {str(e)}")
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.route('/api/sucursales/<int:sucursal_id>', methods=['GET'])
def get_sucursal(sucursal_id):
    """Obtiene una sucursal por ID"""
    try:
        query = "SELECT * FROM SUCURSAL_QN WHERE id_sucursal = :id"
        result = execute_query(query, {'id': sucursal_id})
        if result:
            return jsonify(result[0])
        else:
            return jsonify({'error': 'Sucursal no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sucursales', methods=['POST'])
def create_sucursal():
    """Crea una nueva sucursal"""
    try:
        data = request.json
        
        # Obtener el siguiente ID (max + 1)
        with get_oracle_connection() as connection:
            with connection.cursor() as cursor:
                # Obtener el ID máximo actual
                cursor.execute("SELECT NVL(MAX(id_sucursal), 0) + 1 FROM SUCURSAL_QN")
                next_id = cursor.fetchone()[0]
                
                # Insertar con el nuevo ID
                query = """
                INSERT INTO SUCURSAL_QN (id_sucursal, nombre, ciudad, direccion) 
                VALUES (:id_sucursal, :nombre, 'Quito-Norte', :direccion)
                """
                params = {
                    'id_sucursal': next_id,
                    'nombre': data['nombre'],
                    'direccion': data.get('direccion', '')
                }
                
                cursor.execute(query, params)
                connection.commit()
                
                return jsonify({'success': True, 'message': f'Sucursal creada exitosamente con ID {next_id}'})
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sucursales/<int:sucursal_id>', methods=['PUT'])
def update_sucursal(sucursal_id):
    """Actualiza una sucursal"""
    try:
        data = request.json
        query = """
        UPDATE SUCURSAL_QN 
        SET nombre = :nombre, direccion = :direccion
        WHERE id_sucursal = :id
        """
        params = {
            'nombre': data['nombre'],
            'direccion': data.get('direccion', ''),
            'id': sucursal_id
        }
        result = execute_dml(query, params)
        if result > 0:
            return jsonify({'success': True, 'message': 'Sucursal actualizada exitosamente'})
        else:
            return jsonify({'error': 'Error al actualizar sucursal'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sucursales/<int:sucursal_id>', methods=['DELETE'])
def delete_sucursal(sucursal_id):
    """Elimina una sucursal"""
    try:
        query = "DELETE FROM SUCURSAL_QN WHERE id_sucursal = :id"
        result = execute_dml(query, {'id': sucursal_id})
        if result > 0:
            return jsonify({'success': True, 'message': 'Sucursal eliminada exitosamente'})
        else:
            return jsonify({'error': 'Error al eliminar sucursal'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================ API ENDPOINTS PARA EMPLEADOS ================

@app.route('/api/empleados', methods=['GET'])
def get_empleados():
    """Obtiene todos los empleados"""
    try:
        query = "SELECT * FROM EMPLEADO_NORTE ORDER BY id_empleado"
        empleados = execute_query(query)
        print(f"DEBUG: Empleados obtenidos: {len(empleados) if empleados else 0}")
        if empleados is None:
            return jsonify({'success': False, 'data': [], 'error': 'No se pudieron obtener empleados'}), 200
        return jsonify({'success': True, 'data': empleados})
    except Exception as e:
        print(f"ERROR en get_empleados: {str(e)}")
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.route('/api/empleados/<int:empleado_id>', methods=['GET'])
def get_empleado(empleado_id):
    """Obtiene un empleado por ID"""
    try:
        query = "SELECT * FROM EMPLEADO_NORTE WHERE id_empleado = :id"
        result = execute_query(query, {'id': empleado_id})
        if result:
            return jsonify(result[0])
        else:
            return jsonify({'error': 'Empleado no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados', methods=['POST'])
def create_empleado():
    """Crea un nuevo empleado"""
    try:
        data = request.json
        
        # Obtener el siguiente ID (max + 1)
        with get_oracle_connection() as connection:
            with connection.cursor() as cursor:
                # Obtener el ID máximo actual
                cursor.execute("SELECT NVL(MAX(id_empleado), 0) + 1 FROM EMPLEADO_NORTE")
                next_id = cursor.fetchone()[0]
                
                # Insertar con el nuevo ID - solo los campos que existen
                query = """
                INSERT INTO EMPLEADO_NORTE (id_empleado, nombre, sucursal, cargo) 
                VALUES (:id_empleado, :nombre, 'Norte', :cargo)
                """
                params = {
                    'id_empleado': next_id,
                    'nombre': data['nombre'],
                    'cargo': data['cargo']
                }
                
                cursor.execute(query, params)
                connection.commit()
                
                return jsonify({'success': True, 'message': f'Empleado creado exitosamente con ID {next_id}'})
                
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/empleados/<int:empleado_id>', methods=['PUT'])
def update_empleado(empleado_id):
    """Actualiza un empleado"""
    try:
        data = request.json
        query = """
        UPDATE EMPLEADO_NORTE 
        SET nombre = :nombre, cargo = :cargo
        WHERE id_empleado = :id
        """
        params = {
            'nombre': data['nombre'],
            'cargo': data['cargo'],
            'id': empleado_id
        }
        result = execute_dml(query, params)
        if result > 0:
            return jsonify({'success': True, 'message': 'Empleado actualizado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al actualizar empleado'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/empleados/<int:empleado_id>', methods=['DELETE'])
def delete_empleado(empleado_id):
    """Elimina un empleado"""
    try:
        query = "DELETE FROM EMPLEADO_NORTE WHERE id_empleado = :id"
        result = execute_dml(query, {'id': empleado_id})
        if result > 0:
            return jsonify({'success': True, 'message': 'Empleado eliminado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al eliminar empleado'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ================ API ENDPOINTS PARA TARJETAS ================

def censor_card_number(card_number):
    """Censura el número de tarjeta mostrando solo los últimos 4 dígitos"""
    if not card_number:
        return "****-****-****-****"
    
    card_str = str(card_number)
    # Mantener solo los últimos 4 dígitos
    if len(card_str) >= 4:
        return "****-****-****-" + card_str[-4:]
    else:
        return "****-****-****-" + card_str

@app.route('/api/tarjetas', methods=['GET'])
def get_tarjetas():
    """Obtiene todas las tarjetas con números censurados por privacidad"""
    try:
        query = "SELECT * FROM VW_TARJETA ORDER BY id_tarjeta"
        tarjetas = execute_query(query)
        print(f"DEBUG: Tarjetas obtenidas: {len(tarjetas) if tarjetas else 0}")
        
        if tarjetas is None:
            return jsonify({'success': False, 'data': [], 'error': 'No se pudieron obtener tarjetas'}), 200
        
        # Censurar números de tarjetas por privacidad
        for tarjeta in tarjetas:
            if 'NUMERO' in tarjeta:
                tarjeta['NUMERO'] = censor_card_number(tarjeta['NUMERO'])
            elif 'numero' in tarjeta:
                tarjeta['numero'] = censor_card_number(tarjeta['numero'])
        
        return jsonify({'success': True, 'data': tarjetas})
    except Exception as e:
        print(f"ERROR en get_tarjetas: {str(e)}")
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.route('/api/tarjetas/<int:tarjeta_id>', methods=['GET'])
def get_tarjeta(tarjeta_id):
    """Obtiene una tarjeta por ID con número censurado por privacidad"""
    try:
        query = "SELECT * FROM VW_TARJETA WHERE id_tarjeta = :id"
        result = execute_query(query, {'id': tarjeta_id})
        if result:
            tarjeta = result[0]
            # Censurar número por privacidad
            if 'NUMERO' in tarjeta:
                tarjeta['NUMERO'] = censor_card_number(tarjeta['NUMERO'])
            elif 'numero' in tarjeta:
                tarjeta['numero'] = censor_card_number(tarjeta['numero'])
            return jsonify(tarjeta)
        else:
            return jsonify({'error': 'Tarjeta no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tarjetas', methods=['POST'])
def create_tarjeta():
    """Crea una nueva tarjeta - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Las tarjetas son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

@app.route('/api/tarjetas/<int:tarjeta_id>', methods=['PUT'])
def update_tarjeta(tarjeta_id):
    """Actualiza una tarjeta - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Las tarjetas son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

@app.route('/api/tarjetas/<int:tarjeta_id>', methods=['DELETE'])
def delete_tarjeta(tarjeta_id):
    """Elimina una tarjeta - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Las tarjetas son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

# ================ API ENDPOINTS PARA FÁBRICAS ================

@app.route('/api/fabricas', methods=['GET'])
def get_fabricas():
    """Obtiene todas las fábricas"""
    try:
        query = "SELECT * FROM VW_FABRICA ORDER BY id_fabrica"
        fabricas = execute_query(query)
        print(f"DEBUG: Fábricas obtenidas: {len(fabricas) if fabricas else 0}")
        if fabricas is None:
            return jsonify({'success': False, 'data': [], 'error': 'No se pudieron obtener fábricas'}), 200
        return jsonify({'success': True, 'data': fabricas})
    except Exception as e:
        print(f"ERROR en get_fabricas: {str(e)}")
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.route('/api/fabricas/<int:fabrica_id>', methods=['GET'])
def get_fabrica(fabrica_id):
    """Obtiene una fábrica por ID"""
    try:
        query = "SELECT * FROM VW_FABRICA WHERE id_fabrica = :id"
        result = execute_query(query, {'id': fabrica_id})
        if result:
            return jsonify(result[0])
        else:
            return jsonify({'error': 'Fábrica no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fabricas', methods=['POST'])
def create_fabrica():
    """Crea una nueva fábrica - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Las fábricas son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

@app.route('/api/fabricas/<int:fabrica_id>', methods=['PUT'])
def update_fabrica(fabrica_id):
    """Actualiza una fábrica - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Las fábricas son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403

@app.route('/api/fabricas/<int:fabrica_id>', methods=['DELETE'])
def delete_fabrica(fabrica_id):
    """Elimina una fábrica - DESHABILITADO (Solo Lectura)"""
    return jsonify({
        'success': False, 
        'error': 'Operación no permitida: Las fábricas son de solo lectura (vista materializada)',
        'message': 'Esta entidad se gestiona desde el servidor maestro'
    }), 403



# ================ API ENDPOINTS PARA AUDITORÍA ESCLAVO ÚNICA ================
@app.route('/api/auditoria_esclavo', methods=['GET'])
def get_auditoria_esclavo():
    """Obtiene todos los registros de la tabla AUDITORIA_ESCLAVO ordenados por ID descendente"""
    query = "SELECT * FROM AUDITORIA_ESCLAVO ORDER BY ID_AUDITORIA DESC"
    try:
        data = execute_query(query)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.teardown_appcontext
def close_db(error):
    """Cierra la conexión de base de datos al finalizar"""
    # Las conexiones se manejan automáticamente con context managers
    pass

if __name__ == '__main__':
    # Inicializar la base de datos antes de ejecutar la aplicación
    if initialize_database():
        print("✅ Conexión a Oracle establecida correctamente")
        print("🚀 Iniciando servidor en http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Error: No se pudo conectar a la base de datos Oracle")
        print("Verifica tu configuración en .env y que Oracle esté ejecutándose")
