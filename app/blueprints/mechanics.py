from flask import Blueprint, jsonify, request

from ..models import Mechanic, db

mechanics_bp = Blueprint("mechanics", __name__, url_prefix="/mechanics")


@mechanics_bp.route("/", methods=["GET"])
def list_mechanics():
    """List all mechanics.
    ---
    tags:
      - Mechanics
    summary: List mechanics
    description: Returns all registered mechanics.
    responses:
      200:
        description: Mechanics retrieved successfully.
    """
    mechanics = [
        {"id": mechanic.id, "name": mechanic.name, "specialty": mechanic.specialty}
        for mechanic in db.mechanics
    ]
    return jsonify(mechanics), 200


@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    """Create a mechanic.
    ---
    tags:
      - Mechanics
    summary: Create mechanic
    description: Creates a mechanic with a name and specialty.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - specialty
          properties:
            name:
              type: string
            specialty:
              type: string
    responses:
      201:
        description: Mechanic created successfully.
      400:
        description: Validation failed.
    """
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("specialty"):
        return jsonify({"message": "Validation failed", "errors": {"name": ["Missing data for required field."], "specialty": ["Missing data for required field."]}}), 400

    mechanic = Mechanic(id=len(db.mechanics) + 1, name=data["name"], specialty=data["specialty"])
    db.mechanics.append(mechanic)
    return jsonify({"id": mechanic.id, "name": mechanic.name, "specialty": mechanic.specialty}), 201
