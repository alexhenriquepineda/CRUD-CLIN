from flask import Blueprint, request, jsonify
from crud import (get_all_users,
                  get_user_by_id,
                  create_user,
                  update_user,
                  delete_user)
from schema import user_to_dict

router = Blueprint("router", __name__)


@router.route("/users", methods=["GET"])
def read_users():
    users = get_all_users()

    return jsonify([user_to_dict(user) for user in users])


@router.route("/users/<int:user_id>", methods=["GET"])
def read_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user_to_dict(user))


@router.route("/users", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    user = create_user(name)
    return jsonify(user_to_dict(user)), 201


@router.route("/users/<int:user_id>", methods=["PUT"])
def update(user_id):
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    user = update_user(user_id, name)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user_to_dict(user))


@router.route("/users/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    success = delete_user(user_id)
    if not success:
        return jsonify({"error": "user not found"}), 404
    return jsonify({"result": True})
