from functools import wraps

from flask import current_app, jsonify, request


def validate_required_fields(data, required_fields):
    return {
        field: ["Missing data for required field."]
        for field in required_fields
        if data.get(field) in (None, "")
    }


def get_by_id(items, item_id):
    for item in items:
        if item.id == item_id:
            return item
    return None


def require_api_key(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        expected = current_app.config.get("API_KEY", "teacher-demo-key")
        provided = request.headers.get("X-API-Key")

        if provided != expected:
            return jsonify({"message": "Unauthorized"}), 401
        return view(*args, **kwargs)

    return wrapped
