from flask import Blueprint, jsonify, request
from ...services.company.company_service import CompanyService

company_bp = Blueprint("company", __name__, url_prefix="/companies")


@company_bp.route("/", methods=["GET"])
def get_companies():
    try:
        companies = CompanyService.get_all_companies()

        return jsonify({"ok": True, "companies": companies}), 200

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@company_bp.route("/<id_company>", methods=["GET"])
def get_company_by_id(id_company):

    try:
        id_company = int(id_company)
        if id_company <= 0:
            return jsonify({"ok": False, "error": "El id ingresado debe ser positivo"})

        company = CompanyService.get_company_by_id(id_company)

        return jsonify({"ok": True, "company": company}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
