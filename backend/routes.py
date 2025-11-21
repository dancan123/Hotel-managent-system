from flask import Blueprint, request, jsonify
from db import db
from models import Room, Customer, Reservation, Employee, Invoice
from datetime import datetime
from sqlalchemy import and_, or_

api = Blueprint('api', __name__, url_prefix='/api/v1')

# Helper function for validation
def validate_room_data(data):
    required = ['room_number', 'type', 'capacity', 'price_per_night', 'status']
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, None

def validate_customer_data(data):
    required = ['first_name', 'last_name', 'email', 'phone']
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, None

def validate_reservation_data(data):
    required = ['customer_id', 'room_id', 'check_in_date', 'check_out_date', 'total_cost']
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, None

def validate_employee_data(data):
    required = ['first_name', 'last_name', 'email', 'phone', 'role', 'department', 'salary', 'hire_date']
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, None

def validate_invoice_data(data):
    required = ['reservation_id', 'amount', 'payment_status']
    for field in required:
        if field not in data:
            return False, f"Missing field: {field}"
    return True, None

# Rooms CRUD
@api.route('/rooms', methods=['GET', 'POST'])
def rooms():
    if request.method == 'GET':
        status = request.args.get('status')
        type_filter = request.args.get('type')
        query = Room.query
        if status:
            query = query.filter_by(status=status)
        if type_filter:
            query = query.filter_by(type=type_filter)
        rooms = query.all()
        return jsonify([{
            'id': r.id,
            'room_number': r.room_number,
            'type': r.type,
            'capacity': r.capacity,
            'price_per_night': float(r.price_per_night),
            'status': r.status,
            'amenities': r.amenities,
            'created_at': r.created_at.isoformat(),
            'updated_at': r.updated_at.isoformat()
        } for r in rooms])
    else:
        data = request.get_json()
        valid, error = validate_room_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            print(f"Creating room: {data}")
            room = Room(
                room_number=data['room_number'],
                type=data['type'],
                capacity=data['capacity'],
                price_per_night=data['price_per_night'],
                status=data['status'],
                amenities=data.get('amenities')
            )
            db.session.add(room)
            db.session.commit()
            print(f"Room created with id: {room.id}")
            return jsonify({'message': 'Room created', 'id': room.id}), 201
        except Exception as e:
            print(f"Error creating room: {e}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@api.route('/rooms/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def room(id):
    room = Room.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': room.id,
            'room_number': room.room_number,
            'type': room.type,
            'capacity': room.capacity,
            'price_per_night': float(room.price_per_night),
            'status': room.status,
            'amenities': room.amenities,
            'created_at': room.created_at.isoformat(),
            'updated_at': room.updated_at.isoformat()
        })
    elif request.method == 'PUT':
        data = request.get_json()
        valid, error = validate_room_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            room.room_number = data['room_number']
            room.type = data['type']
            room.capacity = data['capacity']
            room.price_per_night = data['price_per_night']
            room.status = data['status']
            room.amenities = data.get('amenities')
            db.session.commit()
            return jsonify({'message': 'Room updated'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        try:
            db.session.delete(room)
            db.session.commit()
            return jsonify({'message': 'Room deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

# Customers CRUD
@api.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        customers = Customer.query.all()
        return jsonify([{
            'id': c.id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email': c.email,
            'phone': c.phone,
            'address': c.address,
            'created_at': c.created_at.isoformat(),
            'updated_at': c.updated_at.isoformat()
        } for c in customers])
    else:
        data = request.get_json()
        valid, error = validate_customer_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            customer = Customer(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                address=data.get('address')
            )
            db.session.add(customer)
            db.session.commit()
            return jsonify({'message': 'Customer created', 'id': customer.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@api.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': customer.id,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'created_at': customer.created_at.isoformat(),
            'updated_at': customer.updated_at.isoformat()
        })
    elif request.method == 'PUT':
        data = request.get_json()
        valid, error = validate_customer_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            customer.first_name = data['first_name']
            customer.last_name = data['last_name']
            customer.email = data['email']
            customer.phone = data['phone']
            customer.address = data.get('address')
            db.session.commit()
            return jsonify({'message': 'Customer updated'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        try:
            db.session.delete(customer)
            db.session.commit()
            return jsonify({'message': 'Customer deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

# Reservations CRUD
@api.route('/reservations', methods=['GET', 'POST'])
def reservations():
    if request.method == 'GET':
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        query = Reservation.query
        if start_date and end_date:
            query = query.filter(and_(Reservation.check_in_date >= start_date, Reservation.check_out_date <= end_date))
        if status:
            query = query.filter_by(status=status)
        reservations = query.all()
        return jsonify([{
            'id': r.id,
            'customer_id': r.customer_id,
            'room_id': r.room_id,
            'check_in_date': r.check_in_date.isoformat(),
            'check_out_date': r.check_out_date.isoformat(),
            'status': r.status,
            'total_cost': float(r.total_cost),
            'special_requests': r.special_requests,
            'created_at': r.created_at.isoformat(),
            'updated_at': r.updated_at.isoformat()
        } for r in reservations])
    else:
        data = request.get_json()
        valid, error = validate_reservation_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        # Check room availability
        room = Room.query.get(data['room_id'])
        if not room or room.status != 'available':
            return jsonify({'error': 'Room not available'}), 400
        # Check for overlapping reservations
        overlapping = Reservation.query.filter(
            and_(
                Reservation.room_id == data['room_id'],
                Reservation.status.in_(['confirmed', 'checked_in']),
                or_(
                    and_(Reservation.check_in_date <= data['check_out_date'], Reservation.check_out_date >= data['check_in_date'])
                )
            )
        ).first()
        if overlapping:
            return jsonify({'error': 'Room not available for these dates'}), 400
        try:
            reservation = Reservation(
                customer_id=data['customer_id'],
                room_id=data['room_id'],
                check_in_date=datetime.fromisoformat(data['check_in_date']),
                check_out_date=datetime.fromisoformat(data['check_out_date']),
                status=data.get('status', 'pending'),
                total_cost=data['total_cost'],
                special_requests=data.get('special_requests')
            )
            db.session.add(reservation)
            db.session.commit()
            return jsonify({'message': 'Reservation created', 'id': reservation.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@api.route('/reservations/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def reservation(id):
    reservation = Reservation.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': reservation.id,
            'customer_id': reservation.customer_id,
            'room_id': reservation.room_id,
            'check_in_date': reservation.check_in_date.isoformat(),
            'check_out_date': reservation.check_out_date.isoformat(),
            'status': reservation.status,
            'total_cost': float(reservation.total_cost),
            'special_requests': reservation.special_requests,
            'created_at': reservation.created_at.isoformat(),
            'updated_at': reservation.updated_at.isoformat()
        })
    elif request.method == 'PUT':
        data = request.get_json()
        valid, error = validate_reservation_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        # Similar checks for update
        try:
            reservation.customer_id = data['customer_id']
            reservation.room_id = data['room_id']
            reservation.check_in_date = datetime.fromisoformat(data['check_in_date'])
            reservation.check_out_date = datetime.fromisoformat(data['check_out_date'])
            reservation.status = data.get('status', reservation.status)
            reservation.total_cost = data['total_cost']
            reservation.special_requests = data.get('special_requests')
            db.session.commit()
            return jsonify({'message': 'Reservation updated'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        try:
            db.session.delete(reservation)
            db.session.commit()
            return jsonify({'message': 'Reservation cancelled'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

# Employees CRUD
@api.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        employees = Employee.query.all()
        return jsonify([{
            'id': e.id,
            'first_name': e.first_name,
            'last_name': e.last_name,
            'email': e.email,
            'phone': e.phone,
            'role': e.role,
            'department': e.department,
            'salary': float(e.salary),
            'hire_date': e.hire_date.isoformat(),
            'created_at': e.created_at.isoformat(),
            'updated_at': e.updated_at.isoformat()
        } for e in employees])
    else:
        data = request.get_json()
        valid, error = validate_employee_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            employee = Employee(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                phone=data['phone'],
                role=data['role'],
                department=data['department'],
                salary=data['salary'],
                hire_date=datetime.fromisoformat(data['hire_date'])
            )
            db.session.add(employee)
            db.session.commit()
            return jsonify({'message': 'Employee created', 'id': employee.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@api.route('/employees/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'phone': employee.phone,
            'role': employee.role,
            'department': employee.department,
            'salary': float(employee.salary),
            'hire_date': employee.hire_date.isoformat(),
            'created_at': employee.created_at.isoformat(),
            'updated_at': employee.updated_at.isoformat()
        })
    elif request.method == 'PUT':
        data = request.get_json()
        valid, error = validate_employee_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            employee.first_name = data['first_name']
            employee.last_name = data['last_name']
            employee.email = data['email']
            employee.phone = data['phone']
            employee.role = data['role']
            employee.department = data['department']
            employee.salary = data['salary']
            employee.hire_date = datetime.fromisoformat(data['hire_date'])
            db.session.commit()
            return jsonify({'message': 'Employee updated'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        try:
            db.session.delete(employee)
            db.session.commit()
            return jsonify({'message': 'Employee deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

# Invoices CRUD
@api.route('/invoices', methods=['GET', 'POST'])
def invoices():
    if request.method == 'GET':
        invoices = Invoice.query.all()
        return jsonify([{
            'id': i.id,
            'reservation_id': i.reservation_id,
            'amount': float(i.amount),
            'payment_status': i.payment_status,
            'payment_date': i.payment_date.isoformat() if i.payment_date else None,
            'payment_method': i.payment_method,
            'created_at': i.created_at.isoformat(),
            'updated_at': i.updated_at.isoformat()
        } for i in invoices])
    else:
        data = request.get_json()
        valid, error = validate_invoice_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            invoice = Invoice(
                reservation_id=data['reservation_id'],
                amount=data['amount'],
                payment_status=data['payment_status'],
                payment_date=datetime.fromisoformat(data['payment_date']) if data.get('payment_date') else None,
                payment_method=data.get('payment_method')
            )
            db.session.add(invoice)
            db.session.commit()
            return jsonify({'message': 'Invoice created', 'id': invoice.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

@api.route('/invoices/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def invoice(id):
    invoice = Invoice.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({
            'id': invoice.id,
            'reservation_id': invoice.reservation_id,
            'amount': float(invoice.amount),
            'payment_status': invoice.payment_status,
            'payment_date': invoice.payment_date.isoformat() if invoice.payment_date else None,
            'payment_method': invoice.payment_method,
            'created_at': invoice.created_at.isoformat(),
            'updated_at': invoice.updated_at.isoformat()
        })
    elif request.method == 'PUT':
        data = request.get_json()
        valid, error = validate_invoice_data(data)
        if not valid:
            return jsonify({'error': error}), 400
        try:
            invoice.reservation_id = data['reservation_id']
            invoice.amount = data['amount']
            invoice.payment_status = data['payment_status']
            invoice.payment_date = datetime.fromisoformat(data['payment_date']) if data.get('payment_date') else None
            invoice.payment_method = data.get('payment_method')
            db.session.commit()
            return jsonify({'message': 'Invoice updated'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        try:
            db.session.delete(invoice)
            db.session.commit()
            return jsonify({'message': 'Invoice deleted'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

# Reporting
@api.route('/reports/occupancy', methods=['GET'])
def occupancy_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date or not end_date:
        return jsonify({'error': 'start_date and end_date required'}), 400
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except:
        return jsonify({'error': 'Invalid date format'}), 400
    total_rooms = Room.query.count()
    occupied_reservations = Reservation.query.filter(
        and_(
            Reservation.status.in_(['confirmed', 'checked_in']),
            or_(
                and_(Reservation.check_in_date <= end.date(), Reservation.check_out_date >= start.date())
            )
        )
    ).count()
    occupancy_rate = (occupied_reservations / total_rooms) * 100 if total_rooms > 0 else 0
    return jsonify({'occupancy_rate': occupancy_rate, 'total_rooms': total_rooms, 'occupied': occupied_reservations})

@api.route('/reports/revenue', methods=['GET'])
def revenue_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date or not end_date:
        return jsonify({'error': 'start_date and end_date required'}), 400
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except:
        return jsonify({'error': 'Invalid date format'}), 400
    from sqlalchemy import func
    result = db.session.query(func.sum(Reservation.total_cost)).filter(
        and_(
            Reservation.status.in_(['confirmed', 'checked_in', 'checked_out']),
            Reservation.check_in_date >= start.date(),
            Reservation.check_out_date <= end.date()
        )
    ).scalar()
    total_revenue = float(result) if result else 0.0
    return jsonify({'total_revenue': total_revenue})

@api.route('/reports/customer-stats', methods=['GET'])
def customer_stats():
    from sqlalchemy import func
    stats = db.session.query(
        Customer.id,
        Customer.first_name,
        Customer.last_name,
        func.count(Reservation.id).label('reservation_count')
    ).join(Reservation, Customer.id == Reservation.customer_id).group_by(Customer.id).all()
    return jsonify([{
        'customer_id': s.id,
        'name': f"{s.first_name} {s.last_name}",
        'reservation_count': s.reservation_count
    } for s in stats])