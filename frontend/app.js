// Hotel Management System - Frontend JavaScript

const API_BASE = 'https://hotel-managent-system-1.onrender.com/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    console.log('Hotel Management System frontend loaded.');

    // Navigation handling
    const navLinks = document.querySelectorAll('nav a');
    const sections = document.querySelectorAll('main section');

    function showSection(sectionId) {
        sections.forEach(section => {
            section.style.display = section.id === sectionId ? 'block' : 'none';
        });
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.target.getAttribute('href').substring(1);
            showSection(target);
            // Load data for the section
            loadSectionData(target);
        });
    });

    // Default to dashboard
    showSection('dashboard');
    loadSectionData('dashboard');

    // Initialize data loading for all sections
    loadAllData();

    // Start real-time polling
    setInterval(() => {
        loadRooms();
        loadReservations();
    }, 5000); // Poll every 5 seconds
});

// Generic fetch function with error handling
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        alert('An error occurred while communicating with the server.');
        return null;
    }
}

// Load data for a specific section
function loadSectionData(sectionId) {
    switch (sectionId) {
        case 'rooms':
            loadRooms();
            break;
        case 'customers':
            loadCustomers();
            break;
        case 'reservations':
            loadReservations();
            break;
        case 'employees':
            loadEmployees();
            break;
        case 'billing':
            loadInvoices();
            break;
        case 'reports':
            // Reports can be loaded on demand
            break;
    }
}

// Load all data initially
function loadAllData() {
    loadRooms();
    loadCustomers();
    loadReservations();
    loadEmployees();
    loadInvoices();
}

// Rooms functions
async function loadRooms() {
    const rooms = await apiRequest(`${API_BASE}/rooms`);
    if (rooms) {
        const tbody = document.querySelector('#rooms tbody');
        tbody.innerHTML = '';
        rooms.forEach(room => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${room.room_number}</td>
                <td>${room.type}</td>
                <td>${room.status}</td>
                <td>
                    <button class="edit-btn" data-id="${room.id}" data-entity="room">Edit</button>
                    <button class="delete-btn" data-id="${room.id}" data-entity="room">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
        attachCrudListeners();
    }
}

async function createRoom(data) {
    const result = await apiRequest(`${API_BASE}/rooms`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    if (result) {
        loadRooms();
        return true;
    }
    return false;
}

async function updateRoom(id, data) {
    const result = await apiRequest(`${API_BASE}/rooms/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
    if (result) {
        loadRooms();
        return true;
    }
    return false;
}

async function deleteRoom(id) {
    const result = await apiRequest(`${API_BASE}/rooms/${id}`, {
        method: 'DELETE'
    });
    if (result) {
        loadRooms();
        return true;
    }
    return false;
}

// Customers functions
async function loadCustomers() {
    const customers = await apiRequest(`${API_BASE}/customers`);
    if (customers) {
        const tbody = document.querySelector('#customers tbody');
        tbody.innerHTML = '';
        customers.forEach(customer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${customer.first_name} ${customer.last_name}</td>
                <td>${customer.email}</td>
                <td>${customer.phone}</td>
                <td>
                    <button class="edit-btn" data-id="${customer.id}" data-entity="customer">Edit</button>
                    <button class="delete-btn" data-id="${customer.id}" data-entity="customer">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
        attachCrudListeners();
    }
}

async function createCustomer(data) {
    const result = await apiRequest(`${API_BASE}/customers`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    if (result) {
        loadCustomers();
        return true;
    }
    return false;
}

async function updateCustomer(id, data) {
    const result = await apiRequest(`${API_BASE}/customers/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
    if (result) {
        loadCustomers();
        return true;
    }
    return false;
}

async function deleteCustomer(id) {
    const result = await apiRequest(`${API_BASE}/customers/${id}`, {
        method: 'DELETE'
    });
    if (result) {
        loadCustomers();
        return true;
    }
    return false;
}

// Reservations functions
async function loadReservations() {
    const reservations = await apiRequest(`${API_BASE}/reservations`);
    if (reservations) {
        const tbody = document.querySelector('#reservations tbody');
        tbody.innerHTML = '';
        reservations.forEach(reservation => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${reservation.id}</td>
                <td>${reservation.customer_id}</td>
                <td>${reservation.room_id}</td>
                <td>${reservation.check_in_date}</td>
                <td>${reservation.check_out_date}</td>
                <td>
                    <button class="edit-btn" data-id="${reservation.id}" data-entity="reservation">Edit</button>
                    <button class="delete-btn" data-id="${reservation.id}" data-entity="reservation">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
        attachCrudListeners();
    }
}

async function createReservation(data) {
    const result = await apiRequest(`${API_BASE}/reservations`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    if (result) {
        loadReservations();
        return true;
    }
    return false;
}

async function updateReservation(id, data) {
    const result = await apiRequest(`${API_BASE}/reservations/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
    if (result) {
        loadReservations();
        return true;
    }
    return false;
}

async function deleteReservation(id) {
    const result = await apiRequest(`${API_BASE}/reservations/${id}`, {
        method: 'DELETE'
    });
    if (result) {
        loadReservations();
        return true;
    }
    return false;
}

// Employees functions
async function loadEmployees() {
    const employees = await apiRequest(`${API_BASE}/employees`);
    if (employees) {
        const tbody = document.querySelector('#employees tbody');
        tbody.innerHTML = '';
        employees.forEach(employee => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${employee.first_name} ${employee.last_name}</td>
                <td>${employee.role}</td>
                <td>${employee.department}</td>
                <td>
                    <button class="edit-btn" data-id="${employee.id}" data-entity="employee">Edit</button>
                    <button class="delete-btn" data-id="${employee.id}" data-entity="employee">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
        attachCrudListeners();
    }
}

async function createEmployee(data) {
    const result = await apiRequest(`${API_BASE}/employees`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    if (result) {
        loadEmployees();
        return true;
    }
    return false;
}

async function updateEmployee(id, data) {
    const result = await apiRequest(`${API_BASE}/employees/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
    if (result) {
        loadEmployees();
        return true;
    }
    return false;
}

async function deleteEmployee(id) {
    const result = await apiRequest(`${API_BASE}/employees/${id}`, {
        method: 'DELETE'
    });
    if (result) {
        loadEmployees();
        return true;
    }
    return false;
}

// Invoices functions
async function loadInvoices() {
    const invoices = await apiRequest(`${API_BASE}/invoices`);
    if (invoices) {
        const tbody = document.querySelector('#billing tbody');
        tbody.innerHTML = '';
        invoices.forEach(invoice => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${invoice.id}</td>
                <td>${invoice.reservation_id}</td>
                <td>$${invoice.amount}</td>
                <td>${invoice.payment_status}</td>
                <td>
                    <button class="edit-btn" data-id="${invoice.id}" data-entity="invoice">Edit</button>
                    <button class="delete-btn" data-id="${invoice.id}" data-entity="invoice">Delete</button>
                </td>
            `;
            tbody.appendChild(row);
        });
        attachCrudListeners();
    }
}

async function createInvoice(data) {
    const result = await apiRequest(`${API_BASE}/invoices`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    if (result) {
        loadInvoices();
        return true;
    }
    return false;
}

async function updateInvoice(id, data) {
    const result = await apiRequest(`${API_BASE}/invoices/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
    if (result) {
        loadInvoices();
        return true;
    }
    return false;
}

async function deleteInvoice(id) {
    const result = await apiRequest(`${API_BASE}/invoices/${id}`, {
        method: 'DELETE'
    });
    if (result) {
        loadInvoices();
        return true;
    }
    return false;
}

// Form submission handlers
document.querySelector('#rooms form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputs = e.target.querySelectorAll('input');
    const data = {
        room_number: inputs[0].value,
        type: inputs[1].value,
        capacity: 1,
        price_per_night: 100,
        status: inputs[2].value || 'available'
    };
    if (await createRoom(data)) {
        e.target.reset();
    }
});

document.querySelector('#customers form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputs = e.target.querySelectorAll('input');
    const name = inputs[0].value.split(' ');
    const data = {
        first_name: name[0] || '',
        last_name: name.slice(1).join(' ') || '',
        email: inputs[1].value,
        phone: inputs[2].value
    };
    if (await createCustomer(data)) {
        e.target.reset();
    }
});

document.querySelector('#reservations form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputs = e.target.querySelectorAll('input');
    const data = {
        customer_id: parseInt(inputs[0].value) || 1, // Assume id entered
        room_id: parseInt(inputs[1].value) || 1,
        check_in_date: inputs[2].value,
        check_out_date: inputs[3].value,
        total_cost: 0
    };
    if (await createReservation(data)) {
        e.target.reset();
    }
});

document.querySelector('#employees form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputs = e.target.querySelectorAll('input');
    const name = inputs[0].value.split(' ');
    const data = {
        first_name: name[0] || '',
        last_name: name.slice(1).join(' ') || '',
        email: '',
        phone: '',
        role: inputs[1].value,
        department: inputs[2].value,
        salary: 0,
        hire_date: new Date().toISOString().split('T')[0]
    };
    if (await createEmployee(data)) {
        e.target.reset();
    }
});

document.querySelector('#billing form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputs = e.target.querySelectorAll('input');
    const data = {
        reservation_id: parseInt(inputs[0].value) || 1,
        amount: parseFloat(inputs[1].value) || 0,
        payment_status: inputs[2].value || 'pending'
    };
    if (await createInvoice(data)) {
        e.target.reset();
    }
});

// CRUD event listeners
function attachCrudListeners() {
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.target.dataset.id;
            const entity = e.target.dataset.entity;
            // For simplicity, prompt for new data. In a real app, use modals.
            const newData = prompt('Enter new data as JSON:');
            if (newData) {
                try {
                    const data = JSON.parse(newData);
                    updateEntity(entity, id, data);
                } catch (err) {
                    alert('Invalid JSON');
                }
            }
        });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = e.target.dataset.id;
            const entity = e.target.dataset.entity;
            if (confirm('Are you sure you want to delete this item?')) {
                deleteEntity(entity, id);
            }
        });
    });
}

async function updateEntity(entity, id, data) {
    switch (entity) {
        case 'room':
            await updateRoom(id, data);
            break;
        case 'customer':
            await updateCustomer(id, data);
            break;
        case 'reservation':
            await updateReservation(id, data);
            break;
        case 'employee':
            await updateEmployee(id, data);
            break;
        case 'invoice':
            await updateInvoice(id, data);
            break;
    }
}

async function deleteEntity(entity, id) {
    switch (entity) {
        case 'room':
            await deleteRoom(id);
            break;
        case 'customer':
            await deleteCustomer(id);
            break;
        case 'reservation':
            await deleteReservation(id);
            break;
        case 'employee':
            await deleteEmployee(id);
            break;
        case 'invoice':
            await deleteInvoice(id);
            break;
    }
}