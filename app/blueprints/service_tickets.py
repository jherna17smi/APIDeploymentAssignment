from flask import Blueprint, jsonify, request

from .common import get_by_id, require_api_key, validate_required_fields
from ..models import ServiceTicket, db

service_tickets_bp = Blueprint("service_tickets", __name__, url_prefix="/service-tickets")


def _serialize_service_ticket(ticket):
  return {
    "id": ticket.id,
    "customer_id": ticket.customer_id,
    "mechanic_id": ticket.mechanic_id,
    "issue": ticket.issue,
    "status": ticket.status,
  }


@service_tickets_bp.route("/", methods=["GET"])
def list_service_tickets():
    """List all service tickets.
    ---
    tags:
      - Service Tickets
    summary: List service tickets
    description: Returns all service tickets.
    responses:
      200:
        description: Service tickets retrieved successfully.
    """
    tickets = [_serialize_service_ticket(ticket) for ticket in db.service_tickets]
    return jsonify(tickets), 200


@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
def get_service_ticket(ticket_id):
    """Get a service ticket by id.
    ---
    tags:
      - Service Tickets
    summary: Get service ticket by id
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
    responses:
      200:
        description: Service ticket found.
      404:
        description: Service ticket not found.
    """
    ticket = get_by_id(db.service_tickets, ticket_id)
    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    return jsonify(_serialize_service_ticket(ticket)), 200


@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    """Create a service ticket.
    ---
    tags:
      - Service Tickets
    summary: Create service ticket
    description: Creates a service ticket for a customer and mechanic.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - customer_id
            - mechanic_id
            - issue
          properties:
            customer_id:
              type: integer
            mechanic_id:
              type: integer
            issue:
              type: string
    responses:
      201:
        description: Service ticket created successfully.
      400:
        description: Validation failed.
    """
    data = request.get_json(silent=True) or {}
    errors = validate_required_fields(data, ["customer_id", "mechanic_id", "issue"])
    if errors:
      return jsonify({"message": "Validation failed", "errors": errors}), 400

    if get_by_id(db.customers, data["customer_id"]) is None:
      return jsonify({"message": "Validation failed", "errors": {"customer_id": ["Unknown customer id."]}}), 400

    if get_by_id(db.mechanics, data["mechanic_id"]) is None:
      return jsonify({"message": "Validation failed", "errors": {"mechanic_id": ["Unknown mechanic id."]}}), 400

    ticket = ServiceTicket(
        id=len(db.service_tickets) + 1,
        customer_id=data["customer_id"],
        mechanic_id=data["mechanic_id"],
        issue=data["issue"],
        status=data.get("status", "open"),
    )
    db.service_tickets.append(ticket)
    return jsonify(_serialize_service_ticket(ticket)), 201


@service_tickets_bp.route("/<int:ticket_id>", methods=["PUT"])
@require_api_key
def update_service_ticket(ticket_id):
    """Replace a service ticket.
    ---
    tags:
      - Service Tickets
    summary: Replace service ticket
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - customer_id
            - mechanic_id
            - issue
          properties:
            customer_id:
              type: integer
            mechanic_id:
              type: integer
            issue:
              type: string
            status:
              type: string
    responses:
      200:
        description: Service ticket updated.
      400:
        description: Validation failed.
      401:
        description: Unauthorized.
      404:
        description: Service ticket not found.
    """
    ticket = get_by_id(db.service_tickets, ticket_id)
    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    data = request.get_json(silent=True) or {}
    errors = validate_required_fields(data, ["customer_id", "mechanic_id", "issue"])
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    if get_by_id(db.customers, data["customer_id"]) is None:
        return jsonify({"message": "Validation failed", "errors": {"customer_id": ["Unknown customer id."]}}), 400

    if get_by_id(db.mechanics, data["mechanic_id"]) is None:
        return jsonify({"message": "Validation failed", "errors": {"mechanic_id": ["Unknown mechanic id."]}}), 400

    ticket.customer_id = data["customer_id"]
    ticket.mechanic_id = data["mechanic_id"]
    ticket.issue = data["issue"]
    ticket.status = data.get("status", ticket.status)
    return jsonify(_serialize_service_ticket(ticket)), 200


@service_tickets_bp.route("/<int:ticket_id>", methods=["PATCH"])
@require_api_key
def patch_service_ticket(ticket_id):
    """Partially update a service ticket.
    ---
    tags:
      - Service Tickets
    summary: Patch service ticket
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            customer_id:
              type: integer
            mechanic_id:
              type: integer
            issue:
              type: string
            status:
              type: string
    responses:
      200:
        description: Service ticket updated.
      400:
        description: Validation failed or no valid fields.
      401:
        description: Unauthorized.
      404:
        description: Service ticket not found.
    """
    ticket = get_by_id(db.service_tickets, ticket_id)
    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    data = request.get_json(silent=True) or {}
    allowed_fields = {"customer_id", "mechanic_id", "issue", "status"}
    provided = [field for field in allowed_fields if field in data]
    if not provided:
        return jsonify({"message": "No valid fields supplied."}), 400

    for field in provided:
        if data.get(field) in (None, ""):
            return jsonify({"message": "Validation failed", "errors": {field: ["Missing data for required field."]}}), 400

    if "customer_id" in data and get_by_id(db.customers, data["customer_id"]) is None:
        return jsonify({"message": "Validation failed", "errors": {"customer_id": ["Unknown customer id."]}}), 400

    if "mechanic_id" in data and get_by_id(db.mechanics, data["mechanic_id"]) is None:
        return jsonify({"message": "Validation failed", "errors": {"mechanic_id": ["Unknown mechanic id."]}}), 400

    if "customer_id" in data:
        ticket.customer_id = data["customer_id"]
    if "mechanic_id" in data:
        ticket.mechanic_id = data["mechanic_id"]
    if "issue" in data:
        ticket.issue = data["issue"]
    if "status" in data:
        ticket.status = data["status"]

    return jsonify(_serialize_service_ticket(ticket)), 200


@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@require_api_key
def delete_service_ticket(ticket_id):
    """Delete a service ticket.
    ---
    tags:
      - Service Tickets
    summary: Delete service ticket
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: ticket_id
        required: true
        type: integer
    responses:
      200:
        description: Service ticket deleted.
      401:
        description: Unauthorized.
      404:
        description: Service ticket not found.
    """
    ticket = get_by_id(db.service_tickets, ticket_id)
    if ticket is None:
        return jsonify({"message": "Service ticket not found"}), 404

    db.service_tickets.remove(ticket)
    return jsonify({"message": "Service ticket deleted"}), 200
