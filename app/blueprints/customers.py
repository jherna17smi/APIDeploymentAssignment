from flask import Blueprint, jsonify, request

from .common import get_by_id, require_api_key, validate_required_fields
from ..models import Customer, db

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


def _serialize_customer(customer):
  return {"id": customer.id, "name": customer.name, "phone": customer.phone}


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
    customers = [_serialize_customer(customer) for customer in db.customers]
    return jsonify(customers), 200


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Get a customer by id.
    ---
    tags:
      - Customers
    summary: Get customer by id
    parameters:
      - in: path
        name: customer_id
        required: true
        type: integer
    responses:
      200:
        description: Customer found.
      404:
        description: Customer not found.
    """
    customer = get_by_id(db.customers, customer_id)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    return jsonify(_serialize_customer(customer)), 200


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
    errors = validate_required_fields(data, ["name", "phone"])
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    customer = Customer(id=len(db.customers) + 1, name=data["name"], phone=data["phone"])
    db.customers.append(customer)
    return jsonify(_serialize_customer(customer)), 201


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
@require_api_key
def update_customer(customer_id):
    """Replace a customer.
    ---
    tags:
      - Customers
    summary: Replace customer
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: customer_id
        required: true
        type: integer
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
      200:
        description: Customer updated.
      400:
        description: Validation failed.
      401:
        description: Unauthorized.
      404:
        description: Customer not found.
    """
    customer = get_by_id(db.customers, customer_id)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    data = request.get_json(silent=True) or {}
    errors = validate_required_fields(data, ["name", "phone"])
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    customer.name = data["name"]
    customer.phone = data["phone"]
    return jsonify(_serialize_customer(customer)), 200


@customers_bp.route("/<int:customer_id>", methods=["PATCH"])
@require_api_key
def patch_customer(customer_id):
    """Partially update a customer.
    ---
    tags:
      - Customers
    summary: Patch customer
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: customer_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            phone:
              type: string
    responses:
      200:
        description: Customer updated.
      400:
        description: No valid fields supplied.
      401:
        description: Unauthorized.
      404:
        description: Customer not found.
    """
    customer = get_by_id(db.customers, customer_id)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    data = request.get_json(silent=True) or {}
    allowed_fields = {"name", "phone"}
    provided = [field for field in allowed_fields if field in data]
    if not provided:
        return jsonify({"message": "No valid fields supplied."}), 400

    for field in provided:
        if data.get(field) in (None, ""):
            return jsonify({"message": "Validation failed", "errors": {field: ["Missing data for required field."]}}), 400

    if "name" in data:
        customer.name = data["name"]
    if "phone" in data:
        customer.phone = data["phone"]

    return jsonify(_serialize_customer(customer)), 200


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
@require_api_key
def delete_customer(customer_id):
    """Delete a customer.
    ---
    tags:
      - Customers
    summary: Delete customer
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: customer_id
        required: true
        type: integer
    responses:
      200:
        description: Customer deleted.
      401:
        description: Unauthorized.
      404:
        description: Customer not found.
    """
    customer = get_by_id(db.customers, customer_id)
    if customer is None:
        return jsonify({"message": "Customer not found"}), 404

    db.customers.remove(customer)
    return jsonify({"message": "Customer deleted"}), 200
