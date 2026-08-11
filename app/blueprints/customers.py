from flask import Blueprint, jsonify, request

from ..models import Customer, db

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("/", methods=["GET"])
def list_customers():
    """List all customers.
    ---
    tags:
      - Customers
    summary: List customers
    description: Returns all registered customers.
    responses:
      200:
        description: Customers retrieved successfully.
    """
    customers = [{"id": customer.id, "name": customer.name, "phone": customer.phone} for customer in db.customers]
    return jsonify(customers), 200


@customers_bp.route("/", methods=["POST"])
def create_customer():
    """Create a customer.
    ---
    tags:
      - Customers
    summary: Create customer
    description: Creates a customer with a name and phone.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - phone
          properties:
            name:
              type: string
            phone:
              type: string
    responses:
      201:
        description: Customer created successfully.
      400:
        description: Validation failed.
    """
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("phone"):
        return jsonify({"message": "Validation failed", "errors": {"name": ["Missing data for required field."], "phone": ["Missing data for required field."]}}), 400

    customer = Customer(id=len(db.customers) + 1, name=data["name"], phone=data["phone"])
    db.customers.append(customer)
    return jsonify({"id": customer.id, "name": customer.name, "phone": customer.phone}), 201
