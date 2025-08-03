// Variables globales
let editingCustomerId = null;

// Elementos del DOM
const customerForm = document.getElementById('customer-form');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const alertContainer = document.getElementById('alert-container');
const customersTableBody = document.getElementById('customers-tbody');

// Inicializar cuando la página carga
document.addEventListener('DOMContentLoaded', function() {
    loadCustomers();
    
    // Event listener para el formulario
    customerForm.addEventListener('submit', handleFormSubmit);
    
    // Event listener para el botón cancelar
    cancelBtn.addEventListener('click', cancelEdit);
});

// Cargar todos los clientes
async function loadCustomers() {
    try {
        const response = await fetch('/api/customers');
        const data = await response.json();
        
        if (data.success) {
            displayCustomers(data.data);
        } else {
            showAlert('Error al cargar clientes: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

// Mostrar clientes en la tabla
function displayCustomers(customers) {
    customersTableBody.innerHTML = '';
    
    if (customers.length === 0) {
        customersTableBody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No hay clientes registrados</td></tr>';
        return;
    }
    
    customers.forEach(customer => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${customer.ID_CLIENTE}</td>
            <td>${customer.NOMBRE}</td>
            <td>${customer.DIRECCION}</td>
            <td>${customer.TELEFONO}</td>
            <td>
                <button class="btn btn-warning" onclick="editCustomer(${customer.ID_CLIENTE})">Editar</button>
                <button class="btn btn-danger" onclick="deleteCustomer(${customer.ID_CLIENTE})">Eliminar</button>
            </td>
        `;
        customersTableBody.appendChild(row);
    });
}

// Manejar envío del formulario
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(customerForm);
    const customerData = {
        nombre: formData.get('nombre'),
        telefono: formData.get('telefono')
    };
    
    try {
        let response;
        if (editingCustomerId) {
            // Actualizar cliente existente
            response = await fetch(`/api/customers/${editingCustomerId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(customerData)
            });
        } else {
            // Crear nuevo cliente
            response = await fetch('/api/customers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(customerData)
            });
        }
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(data.message, 'success');
            resetForm();
            loadCustomers();
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

// Editar cliente
async function editCustomer(customerId) {
    try {
        const response = await fetch(`/api/customers/${customerId}`);
        const data = await response.json();
        
        if (data.success) {
            const customer = data.data;
            
            // Llenar el formulario con los datos del cliente
            document.getElementById('nombre').value = customer.NOMBRE;
            document.getElementById('telefono').value = customer.TELEFONO;
            
            // Cambiar el estado del formulario a modo edición
            editingCustomerId = customerId;
            formTitle.textContent = 'Editar Cliente';
            submitBtn.textContent = 'Actualizar Cliente';
            cancelBtn.style.display = 'inline-block';
            
            // Scroll al formulario
            document.querySelector('.form-container').scrollIntoView({ behavior: 'smooth' });
            
        } else {
            showAlert('Error al cargar cliente: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

// Eliminar cliente
async function deleteCustomer(customerId) {
    if (!confirm('¿Estás seguro de que quieres eliminar este cliente?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/customers/${customerId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert(data.message, 'success');
            loadCustomers();
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
    customerForm.reset();
    editingCustomerId = null;
    formTitle.textContent = 'Agregar Nuevo Cliente';
    submitBtn.textContent = 'Agregar Cliente';
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
