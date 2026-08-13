from flask import Blueprint, jsonify, request

from .common import get_by_id, require_api_key, validate_required_fields
from ..models import Mechanic, db

mechanics_bp = Blueprint("mechanics", __name__, url_prefix="/mechanics")


def _serialize_mechanic(mechanic):
  return {"id": mechanic.id, "name": mechanic.name, "specialty": mechanic.specialty}


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
    mechanics = [_serialize_mechanic(mechanic) for mechanic in db.mechanics]
    return jsonify(mechanics), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    """Get a mechanic by id.
    ---
    tags:
      - Mechanics
    summary: Get mechanic by id
    parameters:
      - in: path
        name: mechanic_id
        required: true
        type: integer
    responses:
      200:
        description: Mechanic found.
      404:
        description: Mechanic not found.
    """
    mechanic = get_by_id(db.mechanics, mechanic_id)
    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    return jsonify(_serialize_mechanic(mechanic)), 200


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
    errors = validate_required_fields(data, ["name", "specialty"])
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    mechanic = Mechanic(id=len(db.mechanics) + 1, name=data["name"], specialty=data["specialty"])
    db.mechanics.append(mechanic)
    return jsonify(_serialize_mechanic(mechanic)), 201


@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
@require_api_key
def update_mechanic(mechanic_id):
    """Replace a mechanic.
    ---
    tags:
      - Mechanics
    summary: Replace mechanic
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: mechanic_id
        required: true
        type: integer
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
      200:
        description: Mechanic updated.
      400:
        description: Validation failed.
      401:
        description: Unauthorized.
      404:
        description: Mechanic not found.
    """
    mechanic = get_by_id(db.mechanics, mechanic_id)
    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    data = request.get_json(silent=True) or {}
    errors = validate_required_fields(data, ["name", "specialty"])
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    mechanic.name = data["name"]
    mechanic.specialty = data["specialty"]
    return jsonify(_serialize_mechanic(mechanic)), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["PATCH"])
@require_api_key
def patch_mechanic(mechanic_id):
    """Partially update a mechanic.
    ---
    tags:
      - Mechanics
    summary: Patch mechanic
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: mechanic_id
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
            specialty:
              type: string
    responses:
      200:
        description: Mechanic updated.
      400:
        description: No valid fields supplied.
      401:
        description: Unauthorized.
      404:
        description: Mechanic not found.
    """
    mechanic = get_by_id(db.mechanics, mechanic_id)
    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    data = request.get_json(silent=True) or {}
    allowed_fields = {"name", "specialty"}
    provided = [field for field in allowed_fields if field in data]
    if not provided:
        return jsonify({"message": "No valid fields supplied."}), 400

    for field in provided:
        if data.get(field) in (None, ""):
            return jsonify({"message": "Validation failed", "errors": {field: ["Missing data for required field."]}}), 400

    if "name" in data:
        mechanic.name = data["name"]
    if "specialty" in data:
        mechanic.specialty = data["specialty"]

    return jsonify(_serialize_mechanic(mechanic)), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
@require_api_key
def delete_mechanic(mechanic_id):
    """Delete a mechanic.
    ---
    tags:
      - Mechanics
    summary: Delete mechanic
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: mechanic_id
        required: true
        type: integer
    responses:
      200:
        description: Mechanic deleted.
      401:
        description: Unauthorized.
      404:
        description: Mechanic not found.
    """
    mechanic = get_by_id(db.mechanics, mechanic_id)
    if mechanic is None:
        return jsonify({"message": "Mechanic not found"}), 404

    db.mechanics.remove(mechanic)
    return jsonify({"message": "Mechanic deleted"}), 200
