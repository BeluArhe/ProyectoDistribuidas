from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import db
from models import (ProductModel, ClienteChillogattoModel, SucursalQSModel, 
                   EmpleadoSurModel, TarjetaModel, FabricaModel, AuditoriaModel)
import os

app = Flask(__name__)
CORS(app)

def initialize_database():
    """Inicializa la conexión a la base de datos"""
    if not db.connect():
        print("Error: No se pudo conectar a la base de datos")
        return False
    return True

# ================ RUTAS PRINCIPALES ================

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

@app.route('/auditoria')
def auditoria():
    """Página de auditoría"""
    return render_template('auditoria_simple.html')

# ================ API ENDPOINTS PARA PRODUCTOS ================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Obtiene todos los productos"""
    try:
        products = ProductModel.get_all()
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
        product = ProductModel.get_by_id(product_id)
        if product:
            return jsonify(product)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Crea un nuevo producto"""
    try:
        data = request.json
        result = ProductModel.create(
            nombre=data['nombre'],
            precio=data['precio']
        )
        if result:
            return jsonify({'success': True, 'message': 'Producto creado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al crear producto'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto"""
    try:
        data = request.json
        result = ProductModel.update(
            product_id=product_id,
            nombre=data['nombre'],
            precio=data['precio']
        )
        if result:
            return jsonify({'success': True, 'message': 'Producto actualizado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al actualizar producto'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un producto"""
    try:
        result = ProductModel.delete(product_id)
        if result:
            return jsonify({'success': True, 'message': 'Producto eliminado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al eliminar producto'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ================ API ENDPOINTS PARA CLIENTES ================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Obtiene todos los clientes"""
    try:
        customers = ClienteChillogattoModel.get_all()
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
        customer = ClienteChillogattoModel.get_by_id(customer_id)
        if customer:
            return jsonify(customer)
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Crea un nuevo cliente"""
    try:
        data = request.json
        result = ClienteChillogattoModel.create(
            nombre=data['nombre'],
            telefono=data['telefono']
        )
        if result:
            return jsonify({'success': True, 'message': 'Cliente creado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al crear cliente'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Actualiza un cliente"""
    try:
        data = request.json
        result = ClienteChillogattoModel.update(
            cliente_id=customer_id,
            nombre=data['nombre'],
            telefono=data['telefono']
        )
        if result:
            return jsonify({'success': True, 'message': 'Cliente actualizado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al actualizar cliente'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Elimina un cliente"""
    try:
        result = ClienteChillogattoModel.delete(customer_id)
        if result:
            return jsonify({'success': True, 'message': 'Cliente eliminado exitosamente'})
        else:
            return jsonify({'success': False, 'error': 'Error al eliminar cliente'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ================ API ENDPOINTS PARA SUCURSALES ================

@app.route('/api/sucursales', methods=['GET'])
def get_sucursales():
    """Obtiene todas las sucursales"""
    try:
        sucursales = SucursalQSModel.get_all()
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
        sucursal = SucursalQSModel.get_by_id(sucursal_id)
        if sucursal:
            return jsonify(sucursal)
        else:
            return jsonify({'error': 'Sucursal no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sucursales', methods=['POST'])
def create_sucursal():
    """Crea una nueva sucursal"""
    try:
        data = request.json
        result = SucursalQSModel.create(
            nombre=data['nombre'],
            direccion=data.get('direccion')
        )
        if result:
            return jsonify({'success': True, 'message': 'Sucursal creada exitosamente'})
        else:
            return jsonify({'error': 'Error al crear sucursal'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sucursales/<int:sucursal_id>', methods=['PUT'])
def update_sucursal(sucursal_id):
    """Actualiza una sucursal"""
    try:
        data = request.json
        result = SucursalQSModel.update(
            sucursal_id=sucursal_id,
            nombre=data['nombre'],
            direccion=data.get('direccion')
        )
        if result:
            return jsonify({'success': True, 'message': 'Sucursal actualizada exitosamente'})
        else:
            return jsonify({'error': 'Error al actualizar sucursal'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sucursales/<int:sucursal_id>', methods=['DELETE'])
def delete_sucursal(sucursal_id):
    """Elimina una sucursal"""
    try:
        result = SucursalQSModel.delete(sucursal_id)
        if result:
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
        empleados = EmpleadoSurModel.get_all()
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
        empleado = EmpleadoSurModel.get_by_id(empleado_id)
        if empleado:
            return jsonify(empleado)
        else:
            return jsonify({'error': 'Empleado no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados', methods=['POST'])
def create_empleado():
    """Crea un nuevo empleado"""
    try:
        data = request.json
        result = EmpleadoSurModel.create(
            nombre=data['nombre'],
            cargo=data['cargo']
        )
        if result:
            return jsonify({'success': True, 'message': 'Empleado creado exitosamente'})
        else:
            return jsonify({'error': 'Error al crear empleado'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados/<int:empleado_id>', methods=['PUT'])
def update_empleado(empleado_id):
    """Actualiza un empleado"""
    try:
        data = request.json
        result = EmpleadoSurModel.update(
            empleado_id=empleado_id,
            nombre=data['nombre'],
            cargo=data['cargo']
        )
        if result:
            return jsonify({'success': True, 'message': 'Empleado actualizado exitosamente'})
        else:
            return jsonify({'error': 'Error al actualizar empleado'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados/<int:empleado_id>', methods=['DELETE'])
def delete_empleado(empleado_id):
    """Elimina un empleado"""
    try:
        result = EmpleadoSurModel.delete(empleado_id)
        if result:
            return jsonify({'success': True, 'message': 'Empleado eliminado exitosamente'})
        else:
            return jsonify({'error': 'Error al eliminar empleado'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================ API ENDPOINTS PARA TARJETAS ================

@app.route('/api/tarjetas', methods=['GET'])
def get_tarjetas():
    """Obtiene todas las tarjetas"""
    try:
        tarjetas = TarjetaModel.get_all()
        print(f"DEBUG: Tarjetas obtenidas: {len(tarjetas) if tarjetas else 0}")
        if tarjetas is None:
            return jsonify({'success': False, 'data': [], 'error': 'No se pudieron obtener tarjetas'}), 200
        return jsonify({'success': True, 'data': tarjetas})
    except Exception as e:
        print(f"ERROR en get_tarjetas: {str(e)}")
        return jsonify({'success': False, 'data': [], 'error': str(e)}), 500

@app.route('/api/tarjetas/<int:tarjeta_id>', methods=['GET'])
def get_tarjeta(tarjeta_id):
    """Obtiene una tarjeta por ID"""
    try:
        tarjeta = TarjetaModel.get_by_id(tarjeta_id)
        if tarjeta:
            return jsonify(tarjeta)
        else:
            return jsonify({'error': 'Tarjeta no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tarjetas', methods=['POST'])
def create_tarjeta():
    """Crea una nueva tarjeta"""
    try:
        data = request.json
        result = TarjetaModel.create(
            tipo=data['tipo'],
            numero=data['numero']
        )
        if result:
            return jsonify({'success': True, 'message': 'Tarjeta creada exitosamente'})
        else:
            return jsonify({'error': 'Error al crear tarjeta'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tarjetas/<int:tarjeta_id>', methods=['PUT'])
def update_tarjeta(tarjeta_id):
    """Actualiza una tarjeta"""
    try:
        data = request.json
        result = TarjetaModel.update(
            tarjeta_id=tarjeta_id,
            tipo=data['tipo'],
            numero=data['numero']
        )
        if result:
            return jsonify({'success': True, 'message': 'Tarjeta actualizada exitosamente'})
        else:
            return jsonify({'error': 'Error al actualizar tarjeta'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tarjetas/<int:tarjeta_id>', methods=['DELETE'])
def delete_tarjeta(tarjeta_id):
    """Elimina una tarjeta"""
    try:
        result = TarjetaModel.delete(tarjeta_id)
        if result:
            return jsonify({'success': True, 'message': 'Tarjeta eliminada exitosamente'})
        else:
            return jsonify({'error': 'Error al eliminar tarjeta'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================ API ENDPOINTS PARA FÁBRICAS ================

@app.route('/api/fabricas', methods=['GET'])
def get_fabricas():
    """Obtiene todas las fábricas"""
    try:
        fabricas = FabricaModel.get_all()
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
        fabrica = FabricaModel.get_by_id(fabrica_id)
        if fabrica:
            return jsonify(fabrica)
        else:
            return jsonify({'error': 'Fábrica no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fabricas', methods=['POST'])
def create_fabrica():
    """Crea una nueva fábrica"""
    try:
        data = request.json
        result = FabricaModel.create(
            nombre=data['nombre'],
            pais=data['pais']
        )
        if result:
            return jsonify({'success': True, 'message': 'Fábrica creada exitosamente'})
        else:
            return jsonify({'error': 'Error al crear fábrica'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fabricas/<int:fabrica_id>', methods=['PUT'])
def update_fabrica(fabrica_id):
    """Actualiza una fábrica"""
    try:
        data = request.json
        result = FabricaModel.update(
            fabrica_id=fabrica_id,
            nombre=data['nombre'],
            pais=data['pais']
        )
        if result:
            return jsonify({'success': True, 'message': 'Fábrica actualizada exitosamente'})
        else:
            return jsonify({'error': 'Error al actualizar fábrica'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fabricas/<int:fabrica_id>', methods=['DELETE'])
def delete_fabrica(fabrica_id):
    """Elimina una fábrica"""
    try:
        result = FabricaModel.delete(fabrica_id)
        if result:
            return jsonify({'success': True, 'message': 'Fábrica eliminada exitosamente'})
        else:
            return jsonify({'error': 'Error al eliminar fábrica'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================ API ENDPOINTS PARA AUDITORÍA ================

@app.route('/api/auditoria', methods=['GET'])
def get_auditoria():
    """Obtiene todos los registros de auditoría"""
    try:
        table_name = request.args.get('table', None)
        if table_name:
            auditoria = AuditoriaModel.get_by_table(table_name)
        else:
            auditoria = AuditoriaModel.get_recent(100)
        return jsonify(auditoria)
    except Exception as e:
        return jsonify([]), 500

@app.route('/api/auditoria/<int:auditoria_id>', methods=['GET'])
def get_auditoria_by_id(auditoria_id):
    """Obtiene un registro de auditoría por ID"""
    try:
        auditoria = AuditoriaModel.get_by_id(auditoria_id)
        if auditoria:
            return jsonify(auditoria)
        else:
            return jsonify({'error': 'Registro no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auditoria', methods=['POST'])
def create_auditoria():
    """Crea un nuevo registro de auditoría"""
    try:
        data = request.json
        result = AuditoriaModel.create(
            tabla_afectada=data['tabla_afectada'],
            accion=data['accion'],
            usuario=data['usuario'],
            descripcion=data.get('descripcion')
        )
        if result:
            return jsonify({'success': True, 'message': 'Registro creado exitosamente'})
        else:
            return jsonify({'error': 'Error al crear registro'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auditoria/<int:auditoria_id>', methods=['PUT'])
def update_auditoria(auditoria_id):
    """Actualiza un registro de auditoría"""
    try:
        data = request.json
        result = AuditoriaModel.update(
            auditoria_id=auditoria_id,
            tabla_afectada=data['tabla_afectada'],
            accion=data['accion'],
            usuario=data['usuario'],
            descripcion=data.get('descripcion')
        )
        if result:
            return jsonify({'success': True, 'message': 'Registro actualizado exitosamente'})
        else:
            return jsonify({'error': 'Error al actualizar registro'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auditoria/<int:auditoria_id>', methods=['DELETE'])
def delete_auditoria(auditoria_id):
    """Elimina un registro de auditoría"""
    try:
        result = AuditoriaModel.delete(auditoria_id)
        if result:
            return jsonify({'success': True, 'message': 'Registro eliminado exitosamente'})
        else:
            return jsonify({'error': 'Error al eliminar registro'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.teardown_appcontext
def close_db(error):
    """Cierra la conexión de base de datos al finalizar"""
    # Comentado temporalmente - mantener conexión activa
    # db.disconnect()
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
