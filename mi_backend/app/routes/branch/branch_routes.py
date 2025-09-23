from flask import Blueprint, jsonify, request
from ...services.branch.branch_service import BranchService

branch_bp = Blueprint("branch", __name__, url_prefix="/branches")


@branch_bp.route("/", methods=["GET"])
def get_branches():
    
    try:

        branches = BranchService.get_all_branches()

        return jsonify({"ok": True, "branches": branches}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@branch_bp.route("/<id_branch>", methods=["GET"])
def get_branch(id_branch):
    
    try:
        id_branch = int(id_branch)

        if id_branch <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        branch = BranchService.get_branch_by_id(id_branch)

        return jsonify({"ok": True, "branch": branch}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
