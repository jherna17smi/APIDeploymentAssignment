import os
from importlib import import_module

from flask import Flask, jsonify, request
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from config import TestingConfig
from .blueprints.customers import customers_bp
from .blueprints.inventory import inventory_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .models import Member, db


SWAGGER_URL = "/apidocs"
SWAGGER_JSON_URL = "/swagger.json"


def create_app(config_name=None):
    app = Flask(__name__)

    if isinstance(config_name, str):
        config_obj = None
        if config_name == "TestingConfig":
            config_obj = TestingConfig
        else:
            try:
                config_module = import_module(config_name)
                config_obj = getattr(config_module, config_name)
            except (ImportError, AttributeError):
                config_obj = TestingConfig

        if config_obj is not None:
            app.config.from_object(config_obj)
    elif config_name is not None:
        app.config.from_object(config_name)

    app.config.setdefault("TESTING", True)
    app.config.setdefault("API_KEY", os.getenv("API_KEY", "teacher-demo-key"))
    app.config.setdefault("SECRET_KEY", os.getenv("SECRET_KEY", "dev-secret-key"))
    app.config.setdefault("APP_HOST", os.getenv("APP_HOST", "127.0.0.1:5000"))
    app.config.setdefault("SWAGGER_SCHEMES", ["http"])

    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        SWAGGER_JSON_URL,
        config={"app_name": "BasicofTTD API"},
    )
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(mechanics_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(inventory_bp)

    swagger_template = {
        "swagger": "2.0",
        "host": app.config["APP_HOST"],
        "info": {
            "title": "BasicofTTD API",
            "version": "1.0.0",
            "description": "API documentation for the BasicofTTD sample project.",
        },
        "schemes": app.config["SWAGGER_SCHEMES"],
        "securityDefinitions": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "name": "X-API-Key",
                "in": "header",
            }
        },
    }

    @app.route("/swagger.json")
    def swagger_spec():
        return jsonify(swagger(app, template=swagger_template))

    @app.route("/sum", methods=["POST"])
    def sum_route():
        """Calculate the sum of two numbers.

        Accepts a JSON payload with num1 and num2 and returns their sum.
        ---
        tags:
          - Math
        summary: Add two numbers
        description: Returns the addition of num1 and num2 from the request body.
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: SumPayload
              required:
                - num1
                - num2
              properties:
                num1:
                  type: integer
                  example: 2
                num2:
                  type: integer
                  example: 3
        responses:
          200:
            description: Sum calculated successfully.
            schema:
              id: SumResponse
              properties:
                result:
                  type: integer
                  example: 5
          400:
            description: Missing required number fields.
            schema:
              id: SumErrorResponse
              properties:
                message:
                  type: string
                  example: Missing properties num1 and/or num2
        """
        data = request.get_json(silent=True) or {}
        try:
            return jsonify({"result": data["num1"] + data["num2"]}), 200
        except KeyError:
            return jsonify({"message": "Missing properties num1 and/or num2"}), 400

    @app.route("/members/", methods=["POST"])
    def create_member():
        """Create a new member.

        Accepts member details and returns the created member name.
        ---
        tags:
          - Members
        summary: Create member
        description: Creates a member when the required payload fields are present.
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: MemberPayload
              required:
                - name
                - email
                - DOB
                - password
              properties:
                name:
                  type: string
                  example: John Doe
                email:
                  type: string
                  format: email
                  example: jd@email.com
                DOB:
                  type: string
                  format: date
                  example: "1900-01-01"
                password:
                  type: string
                  example: "123"
        responses:
          201:
            description: Member created successfully.
            schema:
              id: MemberResponse
              properties:
                name:
                  type: string
                  example: John Doe
          400:
            description: Validation failed.
            schema:
              id: MemberErrorResponse
              properties:
                message:
                  type: string
                  example: Validation failed
                errors:
                  type: object
                  additionalProperties:
                    type: array
                    items:
                      type: string
        """
        data = request.get_json(silent=True) or {}
        required_fields = ["name", "email", "DOB", "password"]

        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            errors = {field: ["Missing data for required field."] for field in missing}
            return jsonify({"message": "Validation failed", "errors": errors}), 400

        member = Member(
            name=data["name"],
            email=data["email"],
            DOB=data["DOB"],
            password=data["password"],
        )
        db.members.append(member)
        return jsonify({"name": member.name}), 201

    return app


app = create_app(TestingConfig)
