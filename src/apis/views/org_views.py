from services import OrganizationService
from flask import request, jsonify
from apis.forms import OrganizationForm
from apis.decorators import private


org_service = OrganizationService()


@private
def organization_list():
    if request.method == "GET":
        org_id = request.args.get("org_id")
        if not org_id:
            return jsonify({
                "detail": "org_id is a required query parameter"
            }), 400

        return jsonify(org_service.get_organization(org_id=org_id))

    if request.method == "POST":
        form = OrganizationForm(request.json)

        if not form.is_valid():
            return jsonify({"detail": form.errors}), 400

        try:
            output = form.save(form.validated_data)

            return jsonify(output)
        except Exception as exc:
            return jsonify({"detail": repr(exc)}), 400
