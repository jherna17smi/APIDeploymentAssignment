from flask import Blueprint, jsonify, request

from .common import get_by_id, require_api_key, validate_required_fields
from ..models import InventoryItem, db

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


def _serialize_inventory_item(item):
  return {"id": item.id, "name": item.name, "quantity": item.quantity, "price": item.price}


@inventory_bp.route("/", methods=["GET"])
def list_inventory():
    """List all inventory items.
    ---
    tags:
      - Inventory
    summary: List inventory items
    description: Returns all inventory items.
    responses:
      200:
        description: Inventory items retrieved successfully.
    """
    inventory = [_serialize_inventory_item(item) for item in db.inventory]
    return jsonify(inventory), 200


@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    """Get an inventory item by id.
    ---
    tags:
      - Inventory
    summary: Get inventory item by id
    parameters:
      - in: path
        name: item_id
        required: true
        type: integer
    responses:
      200:
        description: Inventory item found.
      404:
        description: Inventory item not found.
    """
    item = get_by_id(db.inventory, item_id)
    if item is None:
        return jsonify({"message": "Inventory item not found"}), 404

    return jsonify(_serialize_inventory_item(item)), 200


@inventory_bp.route("/", methods=["POST"])
def create_inventory_item():
    """Create an inventory item.
    ---
    tags:
      - Inventory
    summary: Create inventory item
    description: Creates an inventory item with a name, quantity, and price.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - quantity
            - price
          properties:
            name:
              type: string
            quantity:
              type: integer
            price:
              type: number
    responses:
      201:
        description: Inventory item created successfully.
      400:
        description: Validation failed.
    """
    data = request.get_json(silent=True) or {}
    errors = validate_required_fields(data, ["name", "quantity", "price"])
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    item = InventoryItem(id=len(db.inventory) + 1, name=data["name"], quantity=data["quantity"], price=data["price"])
    db.inventory.append(item)
    return jsonify(_serialize_inventory_item(item)), 201


@inventory_bp.route("/<int:item_id>", methods=["PUT"])
@require_api_key
def update_inventory_item(item_id):
    """Replace an inventory item.
    ---
    tags:
      - Inventory
    summary: Replace inventory item
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: item_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - quantity
            - price
          properties:
            name:
              type: string
            quantity:
              type: integer
            price:
              type: number
    responses:
      200:
        description: Inventory item updated.
      400:
        description: Validation failed.
      401:
        description: Unauthorized.
      404:
        description: Inventory item not found.
    """
    item = get_by_id(db.inventory, item_id)
    if item is None:
        return jsonify({"message": "Inventory item not found"}), 404

    data = request.get_json(silent=True) or {}
    errors = validate_required_fields(data, ["name", "quantity", "price"])
    if errors:
        return jsonify({"message": "Validation failed", "errors": errors}), 400

    item.name = data["name"]
    item.quantity = data["quantity"]
    item.price = data["price"]
    return jsonify(_serialize_inventory_item(item)), 200


@inventory_bp.route("/<int:item_id>", methods=["PATCH"])
@require_api_key
def patch_inventory_item(item_id):
    """Partially update an inventory item.
    ---
    tags:
      - Inventory
    summary: Patch inventory item
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: item_id
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
            quantity:
              type: integer
            price:
              type: number
    responses:
      200:
        description: Inventory item updated.
      400:
        description: No valid fields supplied.
      401:
        description: Unauthorized.
      404:
        description: Inventory item not found.
    """
    item = get_by_id(db.inventory, item_id)
    if item is None:
        return jsonify({"message": "Inventory item not found"}), 404

    data = request.get_json(silent=True) or {}
    allowed_fields = {"name", "quantity", "price"}
    provided = [field for field in allowed_fields if field in data]
    if not provided:
        return jsonify({"message": "No valid fields supplied."}), 400

    for field in provided:
        if data.get(field) in (None, ""):
            return jsonify({"message": "Validation failed", "errors": {field: ["Missing data for required field."]}}), 400

    if "name" in data:
        item.name = data["name"]
    if "quantity" in data:
        item.quantity = data["quantity"]
    if "price" in data:
        item.price = data["price"]

    return jsonify(_serialize_inventory_item(item)), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
@require_api_key
def delete_inventory_item(item_id):
    """Delete an inventory item.
    ---
    tags:
      - Inventory
    summary: Delete inventory item
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: item_id
        required: true
        type: integer
    responses:
      200:
        description: Inventory item deleted.
      401:
        description: Unauthorized.
      404:
        description: Inventory item not found.
    """
    item = get_by_id(db.inventory, item_id)
    if item is None:
        return jsonify({"message": "Inventory item not found"}), 404

    db.inventory.remove(item)
    return jsonify({"message": "Inventory item deleted"}), 200
