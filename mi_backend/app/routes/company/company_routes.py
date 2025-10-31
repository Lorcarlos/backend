from flask import Blueprint, jsonify
from ...services.company.company_service import CompanyService
from ...services.log.log_service import LogService
from utils.decorators import role_required

company_bp = Blueprint("company", __name__, url_prefix="/companies")


@company_bp.route("/", methods=["GET"])
@role_required([1])
def get_companies():
    try:
        companies = CompanyService.get_all_companies()

        return jsonify({"ok": True, "companies": companies}), 200

    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_companies.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500


@company_bp.route("/<id_company>", methods=["GET"])
@role_required([1])
def get_company_by_id(id_company):

    try:
        id_company = int(id_company)
        if id_company <= 0:
            return (
                jsonify({"ok": False, "error": "El id ingresado debe ser positivo"}),
                400,
            )

        company = CompanyService.get_company_by_id(id_company)

        return jsonify({"ok": True, "company": company}), 200

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 404
    except Exception as e:
        LogService.create_log(
            {
                "module": f"{__name__}.{get_company_by_id.__name__}",
                "message": f"Exception error {str(e)}",
            }
        )
        return jsonify({"ok": False, "error": str(e)}), 500