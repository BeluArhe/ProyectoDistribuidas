// Variables globales
let editingProductId = null;

// Elementos del DOM
const productForm = document.getElementById('product-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const alertContainer = document.getElementById('alert-container');
const productsTableBody = document.getElementById('products-tbody');

// Inicializar cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    
    // Event listener para el formulario
    productForm.addEventListener('submit', handleFormSubmit);
    
    // Event listener para el botón cancelar
    cancelBtn.addEventListener('click', cancelEdit);
});

// Cargar todos los productos
async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        const data = await response.json();
        
        if (data.success) {
            displayProducts(data.data);
        } else {
            showAlert('Error al cargar productos: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

// Mostrar productos en la tabla
function displayProducts(products) {
    productsTableBody.innerHTML = '';
    
    if (products.length === 0) {
        productsTableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">No hay productos registrados</td></tr>';
        return;
    }
    
    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.ID_PRODUCTO}</td>
            <td>${product.NOMBRE}</td>
            <td>$${parseFloat(product.PRECIO).toFixed(2)}</td>
            <td>
                <button class="btn btn-warning" onclick="editProduct(${product.ID_PRODUCTO})">Editar</button>
                <button class="btn btn-danger" onclick="deleteProduct(${product.ID_PRODUCTO})">Eliminar</button>
            </td>
        `;
        productsTableBody.appendChild(row);
    });
}

// Manejar envío del formulario
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(productForm);
    const productData = {
        nombre: formData.get('nombre'),
        precio: parseFloat(formData.get('precio'))
    };
    
    try {
        let response;
        if (editingProductId) {
            // Actualizar producto existente
            response = await fetch(`/api/products/${editingProductId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });
        } else {
            // Crear nuevo producto
            response = await fetch('/api/products', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });
        }
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(data.message, 'success');
            resetForm();
            loadProducts();
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

// Editar producto
async function editProduct(productId) {
    try {
        const response = await fetch(`/api/products/${productId}`);
        const data = await response.json();
        
        if (data.success) {
            const product = data.data;
            
            // Llenar el formulario con los datos del producto
            document.getElementById('nombre').value = product.NOMBRE;
            document.getElementById('precio').value = product.PRECIO;
            
            // Cambiar el estado del formulario a modo edición
            editingProductId = productId;
            formTitle.textContent = 'Editar Producto';
            submitBtn.textContent = 'Actualizar Producto';
            cancelBtn.style.display = 'inline-block';
            
            // Scroll al formulario
            document.querySelector('.form-container').scrollIntoView({ behavior: 'smooth' });
            
        } else {
            showAlert('Error al cargar producto: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

// Eliminar producto
async function deleteProduct(productId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este producto?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/products/${productId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(data.message, 'success');
            loadProducts();
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

// Cancelar edición
function cancelEdit() {
    resetForm();
}

// Resetear formulario
function resetForm() {
    productForm.reset();
    editingProductId = null;
    formTitle.textContent = 'Agregar Nuevo Producto';
    submitBtn.textContent = 'Agregar Producto';
    cancelBtn.style.display = 'none';
}

// Mostrar alerta
function showAlert(message, type) {
    const alertClass = type === 'success' ? 'alert-success' : 'alert-error';
    const alertHTML = `
        <div class="alert ${alertClass}">
            ${message}
        </div>
    `;
    
    alertContainer.innerHTML = alertHTML;
    
    // Auto-hide alert after 5 seconds
    setTimeout(() => {
        alertContainer.innerHTML = '';
    }, 5000);
}
