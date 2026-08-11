from flask import Blueprint, jsonify, request

from ..models import ServiceTicket, db

service_tickets_bp = Blueprint("service_tickets", __name__, url_prefix="/service-tickets")


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
    tickets = [
        {
            "id": ticket.id,
            "customer_id": ticket.customer_id,
            "mechanic_id": ticket.mechanic_id,
            "issue": ticket.issue,
            "status": ticket.status,
        }
        for ticket in db.service_tickets
    ]
    return jsonify(tickets), 200


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
    if not data.get("customer_id") or not data.get("mechanic_id") or not data.get("issue"):
        return jsonify({"message": "Validation failed", "errors": {"customer_id": ["Missing data for required field."], "mechanic_id": ["Missing data for required field."], "issue": ["Missing data for required field."]}}), 400

    ticket = ServiceTicket(
        id=len(db.service_tickets) + 1,
        customer_id=data["customer_id"],
        mechanic_id=data["mechanic_id"],
        issue=data["issue"],
        status=data.get("status", "open"),
    )
    db.service_tickets.append(ticket)
    return jsonify({"id": ticket.id, "customer_id": ticket.customer_id, "mechanic_id": ticket.mechanic_id, "issue": ticket.issue, "status": ticket.status}), 201
