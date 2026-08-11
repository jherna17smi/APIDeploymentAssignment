from flask import Blueprint, jsonify, request

from ..models import InventoryItem, db

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")


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
    inventory = [
        {"id": item.id, "name": item.name, "quantity": item.quantity, "price": item.price}
        for item in db.inventory
    ]
    return jsonify(inventory), 200


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
    if not data.get("name") or not data.get("quantity") or not data.get("price"):
        return jsonify({"message": "Validation failed", "errors": {"name": ["Missing data for required field."], "quantity": ["Missing data for required field."], "price": ["Missing data for required field."]}}), 400

    item = InventoryItem(id=len(db.inventory) + 1, name=data["name"], quantity=data["quantity"], price=data["price"])
    db.inventory.append(item)
    return jsonify({"id": item.id, "name": item.name, "quantity": item.quantity, "price": item.price}), 201
